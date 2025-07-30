"""Flag hidden inside ordinary text by spacing every Nth char."""
from .._base import Decoder

class BaseXX(Decoder):
    name = "basexx"
    pattern = lambda buf: []  # no fast pattern – tested last

    def try_decode(self, raw: bytes):
        # naive heuristic: every 2nd byte alnum?
        step = 2
        cand = raw[::step].decode(errors="ignore")
        if cand.startswith("flag") or "dam{" in cand:
            return cand, 0.4
        return (None, 0.0) 