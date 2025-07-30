#!/usr/bin/env python3
"""
Smart-Strings Hunter – CTF edition
==================================
Author : EllE (MIT licence)
Usage  : smarthunter <binary> [-o DIR] [--json] [--no-open] [--depth N]
"""

import argparse, math, re, os, json, subprocess, webbrowser, sys
import base64, binascii, codecs
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing    import List, Dict, Any, Tuple
from rich      import print, progress
from tqdm      import tqdm
from jinja2    import Template
from .core import run

# --------------------------------------------------------------------
# 1. Config & regexes
# --------------------------------------------------------------------
# Flag patterns
FLAG_PAT  = r"(?:flag|ctf|dam)\{[^}]{4,120}\}|key=.*|passw?or?d=.*"
FLAG_RE   = re.compile(FLAG_PAT, re.I)

# String extraction regexes
ASCII_RE  = re.compile(rb"[\x20-\x7e]{4,}")
UTF16_RE  = re.compile(rb"(?:[\x20-\x7e]\x00){4,}")

# Information gathering patterns
IP_RE     = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
EMAIL_RE  = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
URL_RE    = re.compile(r"\b(?:https?://|www\.)[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+(?:/[^\s]*)?")
DOMAIN_RE = re.compile(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b")
HASH_MD5  = re.compile(r"\b[a-fA-F0-9]{32}\b")
HASH_SHA1 = re.compile(r"\b[a-fA-F0-9]{40}\b")
HASH_SHA256 = re.compile(r"\b[a-fA-F0-9]{64}\b")
USERNAME_RE = re.compile(r"\busername\s*[:=]\s*\S+", re.I)
PASSWORD_RE = re.compile(r"\bpassw(?:or)?d\s*[:=]\s*\S+", re.I)

# Pattern categories for scoring
PATTERN_INFO = {
    "flag": {"pattern": FLAG_RE, "score": 5.0, "name": "Flag pattern"},
    "ip": {"pattern": IP_RE, "score": 3.0, "name": "IP Address"},
    "email": {"pattern": EMAIL_RE, "score": 3.0, "name": "Email Address"},
    "url": {"pattern": URL_RE, "score": 2.5, "name": "URL"},
    "domain": {"pattern": DOMAIN_RE, "score": 2.0, "name": "Domain Name"},
    "hash_md5": {"pattern": HASH_MD5, "score": 2.0, "name": "MD5 Hash"},
    "hash_sha1": {"pattern": HASH_SHA1, "score": 2.0, "name": "SHA1 Hash"},
    "hash_sha256": {"pattern": HASH_SHA256, "score": 2.0, "name": "SHA256 Hash"},
    "username": {"pattern": USERNAME_RE, "score": 3.0, "name": "Username"},
    "password": {"pattern": PASSWORD_RE, "score": 4.0, "name": "Password"}
}

try:
    from Levenshtein import distance as ldist
except ImportError:                              # fallback (slow)
    print("[yellow]python-Levenshtein missing – using pure Python.[/yellow]")
    from difflib import SequenceMatcher
    ldist = lambda a,b: int(round((1-SequenceMatcher(None,a,b).ratio())*max(len(a),len(b))))

# --------------------------------------------------------------------
# 2. Extraction and decoder helpers
# --------------------------------------------------------------------
def _extract(buf: bytes) -> List[str]:
    """Extract ASCII and UTF-16 strings directly from bytes."""
    out = [m.group().decode("ascii","ignore") for m in ASCII_RE.finditer(buf)]
    out += [m.group().decode("utf-16le","ignore") for m in UTF16_RE.finditer(buf)]
    return out

def _try_decodings(s: str) -> List[Tuple[str, str]]:
    """Try to decode a string with various encodings, return successful results."""
    results = []
    
    # Don't try to decode if string is too short
    if len(s) < 8:
        return results
    
    # Helper to add if decode is successful and result is printable
    def try_decode(func, name):
        try:
            result = func(s)
            # Only keep if result is printable and different from input
            if (result != s and all(c.isprintable() or c.isspace() for c in result) 
                and len(result) >= 4):
                results.append((name, result))
        except Exception:
            pass
    
    # Base64 decode
    try_decode(lambda x: base64.b64decode(x.encode()).decode('utf-8'), "Base64")
    
    # Base64 URL-safe decode
    try_decode(lambda x: base64.urlsafe_b64decode(x.encode()).decode('utf-8'), "Base64-URL")
    
    # Base32 decode
    try_decode(lambda x: base64.b32decode(x.encode()).decode('utf-8'), "Base32")
    
    # Base85 decode
    try_decode(lambda x: base64.b85decode(x.encode()).decode('utf-8'), "Base85")
    
    # Hex decode
    if all(c in '0123456789abcdefABCDEF' for c in s):
        try_decode(lambda x: bytes.fromhex(x).decode('utf-8'), "Hex")
    
    # ROT13
    try_decode(lambda x: codecs.decode(x, 'rot_13'), "ROT13")
    
    # URL decode
    if '%' in s:
        try_decode(lambda x: codecs.decode(x.replace('%', '=').encode(), 'quopri').decode(), "URL-encoded")
    
    # Try other ROT variants
    for i in range(1, 26):
        if i != 13:  # Skip ROT13 as we've already done it
            try_decode(
                lambda x, rot=i: ''.join(
                    chr((ord(c) - ord('a') + rot) % 26 + ord('a')) if 'a' <= c <= 'z' else
                    chr((ord(c) - ord('A') + rot) % 26 + ord('A')) if 'A' <= c <= 'Z' else c
                    for c in x
                ), 
                f"ROT{i}"
            )
    
    # Try XOR with common keys (0-50)
    for key in range(1, 51):
        if all(c.isascii() for c in s):
            try:
                xored = ''.join(chr(ord(c) ^ key) for c in s)
                if all(c.isprintable() or c.isspace() for c in xored) and len(xored) >= 4:
                    results.append((f"XOR-{key}", xored))
            except Exception:
                pass
    
    return results

def pull_strings(path: Path) -> List[str]:
    """Extract strings from binary file and try to decode encoded content."""
    data = path.read_bytes()
    raw  = _extract(data)
    
    # also walk raw section dump via objdump -s (catches packed .data)
    try:
        dump = subprocess.check_output(["objdump","-s",path],stderr=subprocess.DEVNULL)
        raw += _extract(dump)
    except Exception:
        pass
    
    # Try to decode strings that might be encoded
    decoded = []
    for s in raw:
        decoded_results = _try_decodings(s)
        for decode_type, decoded_str in decoded_results:
            decoded.append(f"[{decode_type}] {decoded_str}")
    
    # Add decoded strings to raw extraction
    raw.extend(decoded)
    
    return raw

# --------------------------------------------------------------------
# 3. Fast BK-tree for clustering
# --------------------------------------------------------------------
class BKTree:
    def __init__(self, word=None): self.w, self.k = word, {}
    def add(self, word):
        if self.w is None: self.w = word; return
        d = ldist(word, self.w)
        self.k.setdefault(d,BKTree()).add(word)
    def near(self, word, maxd, bag=None):
        if bag is None: bag=set()
        d = ldist(word, self.w)
        if d<=maxd: bag.add(self.w)
        for dist,node in self.k.items():
            if d-maxd<=dist<=d+maxd: node.near(word,maxd,bag)
        return bag

def cluster(strings, maxd):
    tree = BKTree()
    for s in strings: tree.add(s)
    seen=set(); clusters=[]
    for s in strings:
        if s in seen: continue
        grp = tree.near(s,maxd)
        seen |= grp
        clusters.append(sorted(grp))
    return clusters

# --------------------------------------------------------------------
# 4. Scoring
# --------------------------------------------------------------------
def entropy(s): 
    f=Counter(s); return -sum(c/len(s)*math.log2(c/len(s)) for c in f.values())

def detect_patterns(s: str) -> Dict[str, bool]:
    """Detect various patterns in a string."""
    results = {}
    for name, info in PATTERN_INFO.items():
        pattern = info["pattern"]
        results[name] = bool(pattern.search(s))
    return results

def score(s: str, freq: Counter, total: int) -> Tuple[float, Dict[str, Any]]:
    """Score a string based on patterns, entropy, length, and rarity."""
    pattern_matches = detect_patterns(s)
    
    # Start with base score from patterns
    sc = sum(PATTERN_INFO[name]["score"] for name, matched in pattern_matches.items() if matched)
    
    # Add entropy score
    entropy_score = max(0, entropy(s) - 3.5)
    sc += entropy_score
    
    # Add length factor
    length_score = min(len(s) / 15, 2)
    sc += length_score
    
    # Add rarity factor
    rarity_score = min(3, 1 / (freq[s] / total))
    sc += rarity_score
    
    # Store score components for detailed reporting
    details = {
        "patterns": {name: matched for name, matched in pattern_matches.items() if matched},
        "entropy": round(entropy_score, 2),
        "length": round(length_score, 2),
        "rarity": round(rarity_score, 2)
    }
    
    return round(sc, 2), details

# --------------------------------------------------------------------
# 5. HTML template (tiny, no JS)
# --------------------------------------------------------------------
HTML = Template("""
<!DOCTYPE html><html lang=en><meta charset=utf-8>
<title>{{ name }} strings</title>
<style>
body{font-family:ui-monospace,monospace;background:#111;color:#ddd;padding:1rem;font-size:15px}
h1{color:#69f;margin:0 0 .5em}
a{color:#9df}
.flag{color:#ffa}
.email{color:#9f9}
.url{color:#99f}
.password{color:#f99}
.hash{color:#fc9}
.encoded{color:#c9f}
.ip{color:#9ff}
.score{color:#8f8}
details{margin-left:1.2em}
.gray{color:#666}
.tooltip{position:relative;display:inline-block;border-bottom:1px dotted #ccc;cursor:help}
.tooltip .tooltiptext{visibility:hidden;width:200px;background-color:#333;color:#fff;text-align:center;border-radius:6px;padding:5px;position:absolute;z-index:1;bottom:125%;left:50%;margin-left:-100px;opacity:0;transition:opacity 0.3s}
.tooltip:hover .tooltiptext{visibility:visible;opacity:1}
</style>
<h1>{{ name }} – Smart-Strings report</h1>
<p>{{ total }} raw strings → {{ clusters|length }} clusters. Generated {{ ts }} UTC.</p>
{% for c in clusters %}
<div>
  <span class=score>[{{ c.score }}]</span>
  <span class="tooltip {{ 'flag' if c.flag else '' }} {{ 'email' if c.email else '' }} {{ 'url' if c.url else '' }} {{ 'ip' if c.ip else '' }} {{ 'password' if c.password else '' }} {{ 'hash' if c.hash_md5 or c.hash_sha1 or c.hash_sha256 else '' }} {{ 'encoded' if c.rep.startswith('[') else '' }}">
    {{ c.rep|e }}
    <span class="tooltiptext">
      {% if c.details.patterns %}
        Matches: {{ c.details.patterns|join(', ') }}<br>
      {% endif %}
      Entropy: {{ c.details.entropy }} | Length: {{ c.details.length }} | Rarity: {{ c.details.rarity }}
    </span>
  </span>
  {% if c.dup|length %}
  <details class=gray><summary>{{ c.dup|length }} more dupes</summary>
  {% for d in c.dup %}<div class=gray>{{ d|e }}</div>{% endfor %}</details>
  {% endif %}
</div>
{% endfor %}
""")

# --------------------------------------------------------------------
# 6. Main driver
# --------------------------------------------------------------------
def hunt(path: Path, args):
    raw   = pull_strings(path)
    freq  = Counter(raw)
    uniq  = list(freq)
    print(f"[blue]∙ Extracted {len(raw)} raw / {len(uniq)} unique strings.[/blue]")

    clusters = cluster(uniq, args.depth)
    print(f"[blue]∙ {len(clusters)} clusters via BK-tree (d≤{args.depth}).[/blue]")

    total = len(raw)
    enriched = []
    for grp in clusters:
        rep = grp[0]
        score_value, score_details = score(rep, freq, total)
        patterns = detect_patterns(rep)
        
        enriched.append({
            "rep": rep,
            "flag": patterns["flag"],
            "email": patterns["email"],
            "url": patterns["url"],
            "ip": patterns["ip"],
            "password": patterns["password"],
            "hash_md5": patterns["hash_md5"],
            "hash_sha1": patterns["hash_sha1"],
            "hash_sha256": patterns["hash_sha256"],
            "score": score_value,
            "details": score_details,
            "dup": grp[1:]
        })
    enriched.sort(key=lambda x: x["score"], reverse=True)

    html = HTML.render(name=path.name, total=total, clusters=enriched,
                       ts=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

    out_html = (Path(args.out) if args.out else path.parent) / f"{path.name}_strings.html"
    out_html.write_text(html, encoding="utf-8")
    print(f"[green]✔ HTML:[/green] {out_html}")

    if args.json:
        out_json = out_html.with_suffix(".json")
        out_json.write_text(json.dumps(enriched, indent=2))
        print(f"[green]✔ JSON:[/green] {out_json}")

    if not args.no_open:
        try: webbrowser.open(out_html.as_uri())
        except: pass

# --------------------------------------------------------------------
def parse():
    ap=argparse.ArgumentParser(prog="smarthunter",description="Smart-Strings hunter")
    ap.add_argument("binary", help="target binary / file")
    ap.add_argument("-o","--out", help="output dir")
    ap.add_argument("--depth",type=int,default=2, help="nested decode depth (default 2)")
    ap.add_argument("--stride","--lev",type=int,default=3, help="Levenshtein cluster distance")
    ap.add_argument("--budget",type=int,default=100_000, help="max strings to keep")
    ap.add_argument("--json",action="store_true",help="also write JSON")
    ap.add_argument("--no-open",action="store_true",help="don't open browser")
    return ap.parse_args()

def main():
    a=parse()
    try:
        run(Path(a.binary), depth=a.depth, stride=a.stride,
            out_dir=Path(a.out) if a.out else None,
            no_open=a.no_open, json_flag=a.json, budget=a.budget)
    except KeyboardInterrupt:
        print("\n[red]Aborted.[/red]"); sys.exit(130)

if __name__ == "__main__":
    main() 