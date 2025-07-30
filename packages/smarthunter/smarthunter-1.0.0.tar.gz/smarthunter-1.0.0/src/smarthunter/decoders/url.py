import urllib.parse
from .._base import Decoder
from ..util import sanity_ascii
from .. import _finder

class URL(Decoder):
    name = "url"
    # we reuse SIMD finder directly for pattern
    pattern = _finder.find_url_sequences

    def try_decode(self, raw: bytes):
        try:
            txt = urllib.parse.unquote_to_bytes(raw).decode(errors="ignore")
            return self._ok(txt, 0.8)
        except Exception:
            return (None, 0.0) 