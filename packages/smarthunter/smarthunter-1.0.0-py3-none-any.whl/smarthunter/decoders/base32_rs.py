import re, base64
from .._base import Decoder

try:
    import smarthunter_fast as _fast
    rust = _fast.decode_base32
except ImportError:
    rust = None

class Base32Rust(Decoder):
    name = "base32"
    pattern = rb'(?:[A-Z2-7]{8}\s*){2,}=?=?=?=?'

    def try_decode(self, raw: bytes):
        raw = b"".join(raw.split())
        if rust:
            txt = rust(raw)
            if txt:
                return txt.decode(), 0.9
        try:
            decoded = base64.b32decode(raw)
            return self._ok(decoded.decode(errors="ignore"), 0.5)
        except Exception:
            return (None, 0.0) 