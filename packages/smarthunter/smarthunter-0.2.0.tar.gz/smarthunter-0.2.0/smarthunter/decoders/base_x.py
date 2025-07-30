from ..core import decoder
import base64, re, string, math

BASE58 = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
BASE62 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def _base_n(data:bytes, alphabet:bytes):
    n=len(alphabet); v=0
    for c in data:
        i=alphabet.find(bytes([c]));  # -1 if not found
        if i<0: return None
        v=v*n+i
    out=bytearray()
    while v:
        v,mod=divmod(v,256); out.append(mod)
    return bytes(reversed(out))

@decoder
def base_family(s:str):
    res=[]
    try:
        if len(s)%4==0 and re.fullmatch(r"[A-Za-z0-9+/=]{8,}",s):
            res.append(("Base64",base64.b64decode(s).decode('utf-8','ignore')))
    except: pass
    try:
        res.append(("Base32",base64.b32decode(s).decode('utf-8','ignore')))
    except: pass
    try:
        res.append(("Base85",base64.b85decode(s).decode('utf-8','ignore')))
    except: pass
    if set(s.encode())<=set(BASE58):
        out=_base_n(s.encode(),BASE58)
        if out: res.append(("Base58",out.decode('utf-8','ignore')))
    if set(s.encode())<=set(BASE62):
        out=_base_n(s.encode(),BASE62)
        if out: res.append(("Base62",out.decode('utf-8','ignore')))
    return res 