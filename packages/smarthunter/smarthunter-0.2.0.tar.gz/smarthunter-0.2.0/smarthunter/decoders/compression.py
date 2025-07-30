from ..core import decoder
import base64, binascii, zlib, gzip, bz2, lzma, io

MAGICS={
    b"\x1f\x8b":("gzip", gzip.decompress),
    b"\x78\x9c":("zlib", zlib.decompress),
    b"\x42\x5a\x68":("bz2", bz2.decompress),
    b"\xfd7zXZ":("xz", lzma.decompress)
}

@decoder
def compression_dec(s:str):
    outs=[]
    try:
        raw=base64.b64decode(s,validate=True)
    except Exception: raw=None
    for label,decomp in MAGICS.values():
        src=raw if raw and raw.startswith(label.encode() if isinstance(label,str) else label) else None
        if not src and s.encode().startswith(label): src=s.encode()
        if src:
            try: outs.append((f"{label.decode() if isinstance(label,bytes) else label}", decomp(src).decode('utf-8','ignore')))
            except: pass
    return outs 