import re
_regex = re.compile(rb'(?:%[0-9A-Fa-f]{2}){2,}')

def find_url_sequences(buf: bytes):
    return [m.start() for m in _regex.finditer(buf)] 