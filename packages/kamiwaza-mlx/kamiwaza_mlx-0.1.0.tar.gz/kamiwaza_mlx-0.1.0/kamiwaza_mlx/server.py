#!/usr/bin/env python3
"""
**Internal copy of `server.py`** packaged under `kamiwaza_mlx` so end-users can
simply run:

    python -m kamiwaza_mlx.server -m <model> [--port 1234]

The body of the file is identical to the original standalone script (save for
this prologue) to avoid any behavioural changes during the move.
"""

from __future__ import annotations

import argparse, base64, io, json, logging, math, re, time, uuid, asyncio
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import requests, uvicorn, mlx.core as mx
from PIL import Image
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, model_validator

# ────────────────────────── CLI & logging ──────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", default="mlx-community/Qwen2-VL-2B-Instruct-4bit")
parser.add_argument("--host", default="0.0.0.0")
parser.add_argument("--port", type=int, default=18_000)
parser.add_argument("-V", "--vision", action="store_true", help="Force vision pipeline; otherwise auto-detect.")
parser.add_argument("--strip-thinking", action="store_true")
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

# ───────────────────────── timers / tiny helpers ─────────────────────────

class _Timer:  # noqa: D101 – internal util
    __slots__ = ("start", "in_tok")

    def __init__(self, in_tok: int):
        self.start = time.perf_counter()
        self.in_tok = in_tok
        logging.info("Starting generation with %d input tokens", in_tok)

    def done(self, out_tok: int):
        dt = time.perf_counter() - self.start
        tps = 0.0 if dt == 0 else (self.in_tok + out_tok) / dt
        logging.info(
            "Generation completed: %d tokens in %.2fs (%.2f tokens/sec)", out_tok, dt, tps
        )


# ───────────────────────── constants / regex ───────────────────────
MAX_TOKENS = -1
PATCH_LIMIT = 1536
PATCH_SIZE = 32
THINK_RE = re.compile(r"<think>(.*?)</think>", re.S | re.I)  # capture group!

# ──────────────────────────── helpers ──────────────────────────────

def _tok_len(text: str) -> int:
    if hasattr(PROCESSOR, "encode"):
        return len(PROCESSOR.encode(text))
    if hasattr(PROCESSOR, "tokenizer"):
        return len(PROCESSOR.tokenizer.encode(text))
    return len(text.split())  # hopeless fallback


def _model_cfg(model) -> Dict[str, Any]:
    cfg = getattr(model, "config", {})
    return cfg if isinstance(cfg, dict) else cfg.__dict__


def strip_thoughts(text: str, flag: bool) -> str:
    return THINK_RE.sub("", text) if flag else text


def _cap_image(img: Image.Image) -> Image.Image:
    w, h = img.size
    patches = math.ceil(w / PATCH_SIZE) * math.ceil(h / PATCH_SIZE)
    if patches <= PATCH_LIMIT:
        return img
    scale = math.sqrt(PATCH_LIMIT / patches)
    return img.resize((int(w * scale), int(h * scale)), Image.BICUBIC)


def load_image(ref: str) -> Image.Image:
    if ref.startswith("data:image/"):
        img = Image.open(io.BytesIO(base64.b64decode(ref.split(",", 1)[1])))
    elif ref.startswith("http"):
        img = Image.open(io.BytesIO(requests.get(ref, timeout=15).content))
    else:
        img = Image.open(ref)
    return _cap_image(img.convert("RGB"))


# ────────────────────────── usage helper ───────────────────────────

def _usage_dict(in_tok: int, out_tok: int, dur: float, reasoning_tok: int) -> Dict[str, Any]:
    """Return an OpenAI-style `usage` dict including optional reasoning tokens."""

    return {
        "input_tokens": in_tok,
        "input_tokens_details": {"cached_tokens": 0},
        "output_tokens": out_tok,
        "output_tokens_details": {"reasoning_tokens": reasoning_tok},
        "total_tokens": in_tok + out_tok,
        "tokens_per_second": (in_tok + out_tok) / max(dur, 1e-6),  # never ÷0
    }


# ────────────────────────── model loader ───────────────────────────

def load_model(repo: str) -> Tuple[Any, Any, bool]:
    want_vl = args.vision or "vl" in Path(repo).name.lower()
    if want_vl:
        try:
            from mlx_vlm import load as vlm_load

            cfg_path = Path(repo) / "config.json"
            cfg = json.load(open(cfg_path)) if cfg_path.exists() else {}
            model, proc = vlm_load(repo, **cfg)
            log.info("🖼️  vision model loaded via mlx-vlm")
            return model, proc, True
        except Exception as e:  # noqa: BLE001 – blanket log here is fine
            log.warning("vision load failed (%s) – falling back to LM", e)

    from mlx_lm import load as lm_load

    model, tok = lm_load(repo)
    log.info("💬  language model loaded via mlx-lm")
    return model, tok, False


MODEL, PROCESSOR, IS_VISION = load_model(args.model)
MODEL_NAME = Path(args.model).name

# ─────────────────── Pydantic request / schema ────────────────────

class MsgPart(BaseModel):
    type: str
    text: str | None = None
    image_url: Dict[str, str] | None = None


class ChatMsg(BaseModel):
    role: str
    content: Union[str, List[MsgPart]]


class ChatReq(BaseModel):
    model: str = MODEL_NAME
    messages: List[ChatMsg]
    images: List[str] | None = None
    max_tokens: int = MAX_TOKENS
    temperature: float = 1.0
    top_p: float = 1.0
    stream: bool = False
    strip_thinking: bool | None = None

    @model_validator(mode="after")
    def _flatten(cls, v):  # noqa: D401
        imgs, flat = list(v.images or []), []
        for m in v.messages:
            if isinstance(m.content, list):
                buf = []
                for p in m.content:
                    if p.type == "text" and p.text:
                        buf.append(p.text)
                    elif p.type == "image_url" and p.image_url:
                        imgs.append(p.image_url["url"])
                m.content = "\n".join(buf)
            flat.append({"role": m.role, "content": m.content})
        v.__dict__["flat"] = flat
        v.__dict__["all_images"] = imgs
        return v


class _ThinkFilter:  # noqa: D401 – simple state machine
    def __init__(self):
        self.state, self.buf = "NORMAL", ""

    def feed(self, s: str) -> str | None:  # noqa: C901 – tiny FSM, keep inline
        self.buf += s
        out = ""
        while True:
            if self.state == "NORMAL":
                i = self.buf.find("<think>")
                if i == -1:
                    out, self.buf = self.buf, ""
                    return out
                out += self.buf[:i]
                self.buf = self.buf[i + 7 :]
                self.state = "IN"
            elif self.state == "IN":
                j = self.buf.find("</think>")
                if j == -1:
                    return None
                self.buf = self.buf[j + 8 :]
                self.state = "STRIP_NL"
            elif self.state == "STRIP_NL":
                self.buf = self.buf.lstrip("\n")
                self.state = "NORMAL"


def build_prompt(req: ChatReq, n_imgs: int) -> str:
    if IS_VISION:
        from mlx_vlm import apply_chat_template

        return apply_chat_template(PROCESSOR, config=_model_cfg(MODEL), prompt=req.flat, num_images=n_imgs)
    if getattr(PROCESSOR, "chat_template", None):
        return PROCESSOR.apply_chat_template(req.flat, tokenize=False, add_generation_prompt=True)
    chunks = [f"<|{m['role']}|>\n{m['content']}</s>" for m in req.flat]
    chunks.append("<|assistant|>\n")
    return "\n".join(chunks)


# ─────────────────── generation (vision / language) ───────────────

if IS_VISION:  # ──────────── VISION PATH ────────────
    from mlx_vlm.utils import generate as vlm_gen, stream_generate as vlm_stream

    def sync_gen(prompt: str, imgs, req: ChatReq) -> str:  # noqa: D401
        timer = _Timer(len(prompt))
        txt = vlm_gen(
            MODEL,
            PROCESSOR,
            prompt,
            image=imgs,
            max_tokens=req.max_tokens,
            temp=req.temperature,
            top_p=req.top_p,
            verbose=False,
        )
        timer.done(_tok_len(txt))
        return txt

    def stream_chunks(prompt: str, imgs, req: ChatReq):  # noqa: C901 – ported as-is
        rid, created, first = f"chatcmpl-{uuid.uuid4()}", int(time.time()), False
        should_strip = args.strip_thinking if req.strip_thinking is None else req.strip_thinking
        timer = _Timer(len(prompt))
        out_tok = 0

        def _emit(chunk: str):
            nonlocal first, out_tok
            if not chunk:
                return
            out_tok += _tok_len(chunk)
            delta = {"content": chunk}
            if not first:
                delta["role"] = "assistant"  # ← add the value!
                first = True
            return _sse_chunk(rid, created, delta)

        if not should_strip:
            for r in vlm_stream(
                MODEL,
                PROCESSOR,
                prompt,
                image=imgs,
                max_tokens=req.max_tokens,
                temp=req.temperature,
                top_p=req.top_p,
            ):
                if r.text:
                    yield _emit(r.text)
            yield "data: [DONE]\n\n"
            final = {
                "id": rid,
                "object": "chat.completion.chunk",
                "created": created,
                "model": MODEL_NAME,
                "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            }
            yield f"data: {json.dumps(final)}\n\n"
            timer.done(out_tok)
            yield "data: [DONE]\n\n"
            return

        state, buf = "NORMAL", ""
        for r in vlm_stream(
            MODEL,
            PROCESSOR,
            prompt,
            image=imgs,
            max_tokens=req.max_tokens,
            temp=req.temperature,
            top_p=req.top_p,
        ):
            if not r.text:
                continue
            buf += r.text
            while True:
                if state == "NORMAL":
                    k = buf.find("<think>")
                    if k == -1:
                        chunk, buf = buf, ""
                    else:
                        chunk, buf, state = buf[:k], buf[k + 7 :], "IN_THINK"
                    if chunk:
                        yield _emit(chunk)
                    if k == -1:
                        break
                elif state == "IN_THINK":
                    k = buf.find("</think>")
                    if k == -1:
                        buf = ""
                        break
                    buf, state = buf[k + 8 :], "STRIP"
                elif state == "STRIP":
                    buf = buf.lstrip("\n")
                    state = "NORMAL"
        if buf:
            yield _emit(buf)
        final = {
            "id": rid,
            "object": "chat.completion.chunk",
            "created": created,
            "model": MODEL_NAME,
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
        }
        yield f"data: {json.dumps(final)}\n\n"
        timer.done(out_tok)
        yield "data: [DONE]\n\n"

else:  # ──────────── TEXT-ONLY PATH ────────────
    from mlx_lm.generate import stream_generate as lm_stream
    from mlx_lm.sample_utils import make_sampler

    def _sampler(req: ChatReq):
        return make_sampler(temp=req.temperature, top_p=req.top_p, min_p=0.0, min_tokens_to_keep=1)

    def _encode(txt: str):
        return mx.array(PROCESSOR.encode(txt))

    def sync_gen(prompt: str, _imgs, req: ChatReq) -> str:  # noqa: C901, D401
        prompt_ids = _encode(prompt)
        sampler = _sampler(req)
        timer = _Timer(len(prompt_ids))
        out, comp_tok, think_tok = [], 0, 0
        t0 = time.perf_counter()
        for r in lm_stream(
            model=MODEL,
            tokenizer=PROCESSOR,
            prompt=prompt_ids,
            max_tokens=req.max_tokens,
            sampler=sampler,
        ):
            if r.token == PROCESSOR.eos_token_id:
                break
            out.append(r.text)
            comp_tok += 1
            if "<think>" in r.text:
                think_tok += len(PROCESSOR.encode("".join(THINK_RE.findall(r.text))))
        dt = time.perf_counter() - t0

        full = "".join(out)
        inner = THINK_RE.findall(full)
        think_tok = sum(len(PROCESSOR.encode(seg)) for seg in inner)
        reasoning_tok = 0 if (req.strip_thinking or args.strip_thinking) else think_tok
        req.__dict__["_usage"] = _usage_dict(len(prompt_ids), comp_tok, dt, reasoning_tok)

        timer.done(comp_tok)

        return full if not (req.strip_thinking or args.strip_thinking) else strip_thoughts(full, True)

    def stream_chunks(prompt: str, _imgs, req: ChatReq):  # noqa: C901
        rid, created, sent_role = f"chatcmpl-{uuid.uuid4()}", int(time.time()), False
        prompt_ids = _encode(prompt)
        sampler = _sampler(req)
        think = _ThinkFilter()
        strip_it = args.strip_thinking if req.strip_thinking is None else req.strip_thinking
        SYNC_EVERY, tok_ctr, out_tok = 16, 0, 0
        timer = _Timer(len(prompt_ids))
        reasoning_tok = 0

        for r in lm_stream(
            model=MODEL,
            tokenizer=PROCESSOR,
            prompt=prompt_ids,
            max_tokens=req.max_tokens,
            sampler=sampler,
        ):
            if r.token == PROCESSOR.eos_token_id:
                break
            piece = r.text
            if strip_it:
                piece = think.feed(piece)
                if piece is None:
                    reasoning_tok += 1
                    tok_ctr += 1
                    if tok_ctr % SYNC_EVERY == 0:
                        mx.synchronize()
                    continue
            if piece == "":
                piece = "\n"
            delta = {"content": piece}
            if not sent_role:
                delta["role"] = "assistant"
                sent_role = True
            out_tok += 1
            yield _sse_chunk(rid, created, delta)
            tok_ctr += 1
            if tok_ctr % SYNC_EVERY == 0:
                mx.synchronize()

        timer.done(out_tok)
        final = {
            "id": rid,
            "object": "chat.completion.chunk",
            "created": created,
            "model": MODEL_NAME,
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
        }
        yield f"data: {json.dumps(final)}\n\n"
        timer.done(out_tok)
        yield "data: [DONE]\n\n"


# ───────────────────────── SSE helper ─────────────────────────────

def _sse_chunk(rid: str, created: int, delta: Dict[str, str]) -> str:
    payload = {
        "id": rid,
        "object": "chat.completion.chunk",
        "created": created,
        "model": MODEL_NAME,
        "choices": [{"index": 0, "delta": delta, "finish_reason": None}],
    }
    return f"data: {json.dumps(payload)}\n\n"


# ─────────────────────────── FastAPI app ─────────────────────────
app = FastAPI()


@app.post("/v1/chat/completions")
async def completions(req: ChatReq):  # noqa: C901 – same as original
    if req.model != MODEL_NAME:
        log.warning("Requested model '%s' ≠ loaded '%s'", req.model, MODEL_NAME)

    imgs = [load_image(u) for u in req.all_images] if IS_VISION else []
    prompt = build_prompt(req, len(imgs))

    if not req.stream:
        txt = strip_thoughts(sync_gen(prompt, imgs, req), req.strip_thinking or args.strip_thinking)
        if IS_VISION:
            usage = _usage_dict(len(prompt), _tok_len(txt), 0.0, 0)
        else:
            usage = req.__dict__.get("_usage")
            if not isinstance(usage, dict):
                p_tok, c_tok, dur = (len(prompt), len(txt), 0.0)
                usage = _usage_dict(p_tok, c_tok, dur, 0)
        return {
            "id": f"chatcmpl-{uuid.uuid4()}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": MODEL_NAME,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": txt},
                    "finish_reason": "stop",
                }
            ],
            "usage": usage,
        }

    async def event_stream():
        for chunk in stream_chunks(prompt, imgs, req):
            yield chunk
            await asyncio.sleep(0)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ─────────────────────────── main wrapper ─────────────────────────

def main() -> None:
    """Entry-point for `python -m kamiwaza_mlx.server` or console_scripts."""
    import runpy, sys as _sys

    # Re-execute the current module under the `__main__` name so that the
    # original `if __name__ == "__main__"` block below runs unchanged.
    _sys.argv[0] = "kamiwaza_mlx.server"
    runpy.run_module(__name__, run_name="__main__")


# ─────────────────────────── main ────────────────────────────────
if __name__ == "__main__":
    log.info(
        "Serving %s on %s:%d  (vision=%s)", MODEL_NAME, args.host, args.port, IS_VISION
    )
    uvicorn.run(app, host=args.host, port=args.port) 