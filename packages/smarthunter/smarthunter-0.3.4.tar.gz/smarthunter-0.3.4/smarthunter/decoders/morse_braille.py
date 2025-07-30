from ..core import decoder, re
MORSE = {'.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F','--.':'G','....':'H','..':'I',
         '.---':'J','-.-':'K','.-..':'L','--':'M','-.':'N','---':'O','.--.':'P','--.-':'Q','.-.':'R',
         '...':'S','-':'T','..-':'U','...-':'V','.--':'W','-..-':'X','-.--':'Y','--..':'Z','/':' '}
BRAILLE = {0b100000:'A',0b101000:'B',0b110000:'C',0b110100:'D',0b100100:'E',0b111000:'F',
           0b111100:'G',0b101100:'H',0b011000:'I',0b011100:'J',0b100010:'K',0b101010:'L',
           0b110010:'M',0b110110:'N',0b100110:'O',0b111010:'P',0b111110:'Q',0b101110:'R',
           0b011010:'S',0b011110:'T',0b100011:'U',0b101011:'V',0b011101:'W',0b110011:'X',
           0b110111:'Y',0b100111:'Z'}

@decoder
def morse_braille(s:str):
    out=[]
    
    # Standard Morse pattern with strict match
    if re.fullmatch(r"[.\- /]{6,}",s):
        try: out.append(("Morse",''.join(MORSE.get(tok,'?') for tok in s.split())))
        except: pass
    
    # More tolerant Morse pattern - extracts the morse portion from noise
    morse_part = re.search(r"[.\- /]{6,}", s)
    if morse_part and morse_part.group() != s:
        morse_str = morse_part.group()
        # Clean up extra spaces
        cleaned_morse = re.sub(r"\s+", " ", morse_str.strip())
        try: 
            decoded = ''.join(MORSE.get(tok,'?') for tok in cleaned_morse.split())
            # Only add if not mostly question marks
            if decoded.count('?') < len(decoded) * 0.3:
                out.append(("Morse-clean", decoded))
        except: pass
    
    # Braille detection
    if all(0x2800<=ord(c)<=0x28FF for c in s):
        try:
            decoded=''.join(BRAILLE.get(ord(c)-0x2800,'?') for c in s)
            out.append(("Braille",decoded))
        except: pass
    
    return out 