from ..core import decoder, re

@decoder
def numeric_ascii(s:str):
    out=[]
    if re.fullmatch(r"(\\?[0-7]{3}){4,}", s):
        try: out.append(("Octal", bytes(int(o,8) for o in re.findall(r"[0-7]{3}",s)).decode()))
        except: pass
    if re.fullmatch(r"(?:\d{2,3}\s*){4,}", s):
        try: out.append(("Decimal", ''.join(chr(int(n)) for n in s.split())))
        except: pass
    if re.fullmatch(r"(?:[01]{7,8}\s*){4,}", s):
        try: out.append(("Binary", ''.join(chr(int(b,2)) for b in s.split())))
        except: pass
    return out 