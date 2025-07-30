import re
from .._base import Decoder

class Octal(Decoder):
    name = "oct"
    pattern = re.compile(rb'(?:[0-7]{3}\s*){4,}')

    def try_decode(self, raw: bytes):
        try:
            nums = [int(raw[i:i+3], 8) for i in range(0, len(raw), 3)]
            txt = bytes(nums).decode(errors="ignore")
            return self._ok(txt, 0.4)
        except Exception:
            return (None, 0.0) 