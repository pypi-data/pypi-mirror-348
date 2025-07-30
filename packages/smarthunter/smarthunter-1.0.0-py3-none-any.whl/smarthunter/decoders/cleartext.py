import re
from .._base import Decoder
from ..util import printable_ratio

class ClearText(Decoder):
    name = "ascii"
    pattern = re.compile(rb'[ -~]{6,}')   # ≥6 printable ASCII bytes

    def try_decode(self, raw: bytes):
        txt = raw.decode(errors="ignore")
        if printable_ratio(raw) > 0.95:
            return txt, 0.2
        return (None, 0.0) 