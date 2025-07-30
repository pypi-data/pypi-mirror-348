from .._base import Decoder
BRAILLE_OFFSET = 0x2800

class Braille(Decoder):
    name = "braille"
    pattern = b'\xe2\xa0'  # UTF-8 lead bytes for Braille block

    _map = {i: chr(0x30 + i) for i in range(64)}  # dummy → '0'-'9','A'… etc.

    def try_decode(self, raw: bytes):
        try:
            txt = "".join(self._map[(ord(c) - BRAILLE_OFFSET) & 0x3F]
                          for c in raw.decode("utf-8") if ord(c) >= BRAILLE_OFFSET)
            return self._ok(txt, 0.3)
        except Exception:
            return (None, 0.0) 