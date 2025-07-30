from .._base import Decoder
MORSE = {'.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F','--.':'G',
         '....':'H','..':'I','.---':'J','-.-':'K','.-..':'L','--':'M','-.':'N',
         '---':'O','.--.':'P','--.-':'Q','.-.':'R','...':'S','-':'T','..-':'U',
         '...-':'V','.--':'W','-..-':'X','-.--':'Y','--..':'Z','/':' '}

class Morse(Decoder):
    name = "morse"
    pattern = b'.-'

    def try_decode(self, raw: bytes):
        try:
            txt = "".join(MORSE.get(code, '') for code in raw.decode().split())
            return self._ok(txt, 0.3)
        except Exception:
            return (None, 0.0) 