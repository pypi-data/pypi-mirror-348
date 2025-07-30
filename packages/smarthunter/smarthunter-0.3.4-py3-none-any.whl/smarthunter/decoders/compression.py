from ..core import decoder
import base64, binascii, zlib, gzip, bz2, lzma, io, re

MAGICS={
    b"\x1f\x8b":("gzip", gzip.decompress),
    b"\x78\x9c":("zlib", zlib.decompress),
    b"\x42\x5a\x68":("bz2", bz2.decompress),
    b"\xfd7zXZ":("xz", lzma.decompress)
}

@decoder
def compression_dec(s:str):
    outs=[]
    
    # Find the longest pure base64 fragment inside the string
    b64match = re.search(r"[A-Za-z0-9+/]{16,}={0,2}", s)
    raw = None
    if b64match:
        try: raw = base64.b64decode(b64match.group(), validate=True)
        except Exception: pass
    
    for magic_header, (label, decomp) in MAGICS.items():
        src = None
        if raw and raw.startswith(magic_header):
            src = raw
        elif s.encode().startswith(magic_header):
            src = s.encode()
        
        if src:
            try: outs.append((label, decomp(src).decode('utf-8','ignore')))
            except: pass
    return outs 