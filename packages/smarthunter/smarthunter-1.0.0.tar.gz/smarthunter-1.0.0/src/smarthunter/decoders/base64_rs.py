import base64, re
from .._base import Decoder
from ..util import sanity_ascii

try:
    import smarthunter_fast as _fast
    rust = _fast.decode_base64
except ImportError:
    rust = None

class Base64Rust(Decoder):
    name = "base64"
    pattern = rb'(?:[A-Za-z0-9+/]{4}\s*){3,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?'

    def try_decode(self, raw: bytes):
        raw = b"".join(raw.split())  # strip whitespace
        if rust:
            txt = rust(raw)
            if txt:
                return txt.decode(), 0.9
        try:
            txt = base64.b64decode(raw, validate=True).decode(errors="ignore")
            return self._ok(txt, 0.6)
        except Exception:
            return (None, 0.0) 