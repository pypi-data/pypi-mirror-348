from ..core import decoder

@decoder
def rot_family(s:str):
    res=[]
    for i in range(1,26):
        rot=''.join(
            chr((ord(c)-65-i)%26+65) if c.isupper()
            else chr((ord(c)-97-i)%26+97) if c.islower()
            else c for c in s
        )
        if rot!=s and rot.isprintable() and len(rot)>=4:
            res.append((f"ROT{i}",rot))
    return res 