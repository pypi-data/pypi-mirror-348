import re
from .._base import Decoder

class Decimal(Decoder):
    name = "dec"
    pattern = re.compile(rb'(?:\d{1,3}\s*){4,}')

    def try_decode(self, raw: bytes):
        nums = [int(x) for x in raw.split()]
        try:
            txt = bytes(nums).decode(errors="ignore")
            return self._ok(txt, 0.4)
        except Exception:
            return (None, 0.0) 