import re, binascii
from .._base import Decoder

class Hex(Decoder):
    name = "hex"
    pattern = re.compile(rb'(?:[0-9A-Fa-f]{2}\s*){4,}')

    def try_decode(self, raw: bytes):
        try:
            data = binascii.unhexlify(b"".join(raw.split()))
            return self._ok(data.decode(errors="ignore"), 0.4)
        except Exception:
            return (None, 0.0) 