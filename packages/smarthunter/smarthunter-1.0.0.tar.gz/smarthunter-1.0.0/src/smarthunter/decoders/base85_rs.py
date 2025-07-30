import base64
from .._base import Decoder

try:
    import smarthunter_fast as _fast
    rust = _fast.decode_base85
except ImportError:
    rust = None

class Base85Rust(Decoder):
    name = "base85"
    pattern = rb'(?:[!-u]{5}){4,}'

    def try_decode(self, raw: bytes):
        if rust:
            txt = rust(raw)
            if txt:
                return txt.decode(), 0.9
        try:
            txt = base64.a85decode(raw).decode(errors="ignore")
            return self._ok(txt, 0.5)
        except Exception:
            return (None, 0.0) 