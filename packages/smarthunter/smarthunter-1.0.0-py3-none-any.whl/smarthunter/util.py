import string, math

PRINTABLE = set(string.printable.encode())

def printable_ratio(bs: bytes) -> float:
    if not bs:
        return 0.0
    return sum(b in PRINTABLE for b in bs) / len(bs)

def entropy(bs: bytes) -> float:
    if not bs:
        return 0.0
    freq = [bs.count(b) / len(bs) for b in set(bs)]
    return -sum(p * math.log2(p) for p in freq)

def sanity_ascii(txt: str | bytes) -> bool:
    if isinstance(txt, bytes):
        try:
            txt = txt.decode()
        except UnicodeDecodeError:
            return False
    return 0.8 < printable_ratio(txt.encode()) and 2 < len(txt) < 500 