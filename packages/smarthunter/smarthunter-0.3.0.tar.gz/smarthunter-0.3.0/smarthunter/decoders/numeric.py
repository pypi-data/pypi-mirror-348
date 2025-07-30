from ..core import decoder, re

@decoder
def numeric_ascii(s:str):
    out=[]
    
    # Octal sequences - strict match
    if re.fullmatch(r"(\\?[0-7]{3}){4,}", s):
        try: out.append(("Octal", bytes(int(o,8) for o in re.findall(r"[0-7]{3}",s)).decode()))
        except: pass
    
    # Octal sequences - extract valid parts
    octal_parts = re.findall(r"(\\?[0-7]{3}){4,}", s)
    if octal_parts:
        for octal_part in octal_parts:
            try:
                octals = re.findall(r"[0-7]{3}", octal_part)
                if octals:
                    decoded = bytes(int(o,8) for o in octals).decode()
                    if decoded.isprintable() and len(decoded) >= 3:
                        out.append(("Octal-extract", decoded))
            except: pass
    
    # Decimal values - strict match
    if re.fullmatch(r"(?:\d{2,3}\s*){4,}", s):
        try: out.append(("Decimal", ''.join(chr(int(n)) for n in s.split())))
        except: pass
    
    # Decimal values - extract valid parts
    decimal_parts = re.findall(r"(?:\d{2,3}\s+){3,}\d{2,3}", s)
    if decimal_parts:
        for decimal_part in decimal_parts:
            try:
                nums = re.findall(r"\d{2,3}", decimal_part)
                if nums:
                    decoded = ''.join(chr(int(n)) for n in nums)
                    if decoded.isprintable() and len(decoded) >= 3:
                        out.append(("Decimal-extract", decoded))
            except: pass
    
    # Binary values - strict match
    if re.fullmatch(r"(?:[01]{7,8}\s*){4,}", s):
        try: out.append(("Binary", ''.join(chr(int(b,2)) for b in s.split())))
        except: pass
    
    # Binary values - extract valid parts
    binary_parts = re.findall(r"(?:[01]{7,8}\s+){3,}[01]{7,8}", s)
    if binary_parts:
        for binary_part in binary_parts:
            try:
                bins = re.findall(r"[01]{7,8}", binary_part)
                if bins:
                    decoded = ''.join(chr(int(b,2)) for b in bins)
                    if decoded.isprintable() and len(decoded) >= 3:
                        out.append(("Binary-extract", decoded))
            except: pass
    
    # Hex values - strict match for sequences like 464c4147 (FLAG)
    hex_parts = re.findall(r"(?:[0-9a-fA-F]{2}){4,}", s)
    if hex_parts:
        for hex_part in hex_parts:
            try:
                decoded = bytes.fromhex(hex_part).decode('utf-8', 'ignore')
                if decoded.isprintable() and len(decoded) >= 3:
                    out.append(("Hex-extract", decoded))
            except: pass
    
    return out 