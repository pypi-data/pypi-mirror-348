from __future__ import annotations
import mmap, os, time, concurrent.futures as cf
from pathlib import Path
from .registry import decoders

try:
    from . import _finder
    url_seq_finder = _finder.find_url_sequences
except ImportError:
    from . import _finder_fallback as _finder
    url_seq_finder = _finder.find_url_sequences

CHUNK = 1 << 20       # 1 MiB
CPU   = max((os.cpu_count() or 2) - 1, 1)

class Hit(tuple):
    __slots__ = ()
    offset: int; length: int; codec: str; text: str; score: float

def _scan_chunk(args):
    buf, start = args
    hits = []
    for dec in decoders():
        # fast pre-filter
        if isinstance(dec.pattern, (bytes, str)):
            import re
            patt = dec._compiled if hasattr(dec, "_compiled") else \
                   setattr(dec, "_compiled", re.compile(dec.pattern))
            for m in patt.finditer(buf):
                txt, sc = dec.try_decode(m.group(0))
                if txt:
                    hits.append(Hit((start+m.start(), len(m.group(0)), dec.name, txt, sc)))
        else:   # callable pattern (e.g. URL SIMD finder)
            for pos in dec.pattern(buf):
                raw = buf[pos:pos+120]      # safety cap
                txt, sc = dec.try_decode(raw)
                if txt:
                    hits.append(Hit((start+pos, len(raw), dec.name, txt, sc)))
    return hits

def scan(path: Path | str, *, minlen=4, maxlen=120, workers=CPU):
    t0 = time.perf_counter()
    p = Path(path)
    with p.open("rb") as fh, mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        args = ((mm[i:i+CHUNK], i) for i in range(0, len(mm), CHUNK))
        with cf.ProcessPoolExecutor(max_workers=workers) as pool:
            for sub in pool.map(_scan_chunk, args, chunksize=2):
                for hit in sub:
                    if minlen <= hit.length <= maxlen:
                        yield hit
    print(f"[smarthunter] done in {time.perf_counter()-t0:.2f}s")

def hunt_bytes(bs: bytes, **kw):
    from tempfile import TemporaryDirectory, NamedTemporaryFile
    with NamedTemporaryFile() as tmp:
        tmp.write(bs); tmp.flush()
        yield from scan(tmp.name, **kw) 