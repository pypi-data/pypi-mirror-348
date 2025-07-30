import importlib
import pkgutil
from types import ModuleType

_decoders: list["Decoder"] = []

def _discover() -> None:
    from . import decoders as _pkg
    for mod in pkgutil.iter_modules(_pkg.__path__, _pkg.__name__ + "."):
        module = importlib.import_module(mod.name)
        for attr in dir(module):
            obj = getattr(module, attr)
            if getattr(obj, "_is_decoder", False):
                _decoders.append(obj())

_discovered = False

def decoders() -> list["Decoder"]:
    global _discovered
    if not _discovered:
        _discover()
        _discovered = True
    return _decoders 