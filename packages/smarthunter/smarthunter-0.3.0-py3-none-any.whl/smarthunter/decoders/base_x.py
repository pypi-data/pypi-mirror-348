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
    
    # Extract potential base64 fragments
    b64_fragments = re.findall(r"[A-Za-z0-9+/]{8,}={0,2}", s)
    for fragment in b64_fragments:
        if len(fragment) % 4 == 0 or len(fragment) >= 8:
            try:
                decoded = base64.b64decode(fragment).decode('utf-8','ignore')
                if len(decoded) >= 4 and decoded.isprintable():
                    res.append(("Base64", decoded))
            except: pass
    
    # Extract potential base32 fragments
    b32_fragments = re.findall(r"[A-Z2-7]{8,}={0,6}", s)
    for fragment in b32_fragments:
        try:
            decoded = base64.b32decode(fragment).decode('utf-8','ignore')
            if len(decoded) >= 4 and decoded.isprintable():
                res.append(("Base32", decoded))
        except: pass
    
    # Extract potential base85 fragments
    b85_fragments = re.findall(r"[A-Za-z0-9!#$%&()*+\-;<=>?@^_`{|}~]{8,}", s)
    for fragment in b85_fragments:
        try:
            decoded = base64.b85decode(fragment).decode('utf-8','ignore')
            if len(decoded) >= 4 and decoded.isprintable():
                res.append(("Base85", decoded))
        except: pass
    
    # Base58 check - take longest contiguous base58 characters
    b58_fragment = re.search(r"[123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{8,}", s)
    if b58_fragment:
        fragment = b58_fragment.group()
        out = _base_n(fragment.encode(), BASE58)
        if out: 
            decoded = out.decode('utf-8','ignore')
            if len(decoded) >= 4 and decoded.isprintable():
                res.append(("Base58", decoded))
    
    # Base62 check
    b62_fragment = re.search(r"[0-9A-Za-z]{8,}", s)
    if b62_fragment:
        fragment = b62_fragment.group()
        out = _base_n(fragment.encode(), BASE62)
        if out: 
            decoded = out.decode('utf-8','ignore')
            if len(decoded) >= 4 and decoded.isprintable():
                res.append(("Base62", decoded))
    
    return res 