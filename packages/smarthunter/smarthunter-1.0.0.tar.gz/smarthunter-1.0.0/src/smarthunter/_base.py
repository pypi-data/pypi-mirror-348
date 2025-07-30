import re
from abc import ABC, abstractmethod
from .util import sanity_ascii

class Decoder(ABC):
    """Subclass, set .name and .pattern (bytes regex or callable).
       Register by inheriting; registry picks it up automatically."""
    _is_decoder = True
    name: str
    pattern: bytes | str | re.Pattern

    @abstractmethod
    def try_decode(self, raw: bytes) -> tuple[str | None, float]:
        ...

    # helper for subclasses
    def _ok(self, txt: str, score: float = 0.5):
        return (txt, score) if sanity_ascii(txt) else (None, 0.0) 