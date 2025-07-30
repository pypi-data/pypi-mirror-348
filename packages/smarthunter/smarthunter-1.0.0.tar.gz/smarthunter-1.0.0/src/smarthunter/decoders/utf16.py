from .._base import Decoder
from ..util import sanity_ascii

class UTF16(Decoder):
    name = "utf16"
    pattern = b'\x00'

    def try_decode(self, raw: bytes):
        for enc in ("utf-16le", "utf-16be"):
            try:
                txt = raw.decode(enc)
                if sanity_ascii(txt):
                    return txt, 0.7
            except UnicodeDecodeError:
                continue
        return (None, 0.0) 