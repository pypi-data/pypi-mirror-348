from ..core import decoder
import re

@decoder
def rot_family(s:str):
    res=[]
    
    # First try with original string
    for i in range(1,26):
        rot=''.join(
            chr((ord(c)-65-i)%26+65) if c.isupper()
            else chr((ord(c)-97-i)%26+97) if c.islower()
            else c for c in s
        )
        if rot!=s and rot.isprintable() and len(rot)>=4:
            res.append((f"ROT{i}",rot))
    
    # Then try with a cleaned string (letters, braces, common special chars only)
    # This helps with ROT-encoded flags surrounded by noise
    cleaned = re.sub(r"[^A-Za-z0-9{}_\-]", "", s)
    if cleaned != s and len(cleaned) >= 4:
        for i in range(1,26):
            rot=''.join(
                chr((ord(c)-65-i)%26+65) if c.isupper()
                else chr((ord(c)-97-i)%26+97) if c.islower()
                else c for c in cleaned
            )
            if rot!=cleaned and rot.isprintable():
                # Check if it looks like a flag
                if re.search(r"(?i)f\w*a\w*g", rot) or re.search(r"[{([].*[})\]]", rot):
                    res.append((f"ROT{i}-clean",rot))
    
    return res 