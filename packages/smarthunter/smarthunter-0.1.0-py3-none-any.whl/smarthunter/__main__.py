#!/usr/bin/env python3
"""
Smart-Strings Hunter – CTF edition
==================================
Author : EllE (MIT licence)
Usage  : smarthunter <binary> [-o DIR] [--json] [--no-open] [--depth N]
"""

import argparse, math, re, os, json, subprocess, webbrowser, sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing    import List
from rich      import print, progress
from tqdm      import tqdm
from jinja2    import Template

# --------------------------------------------------------------------
# 1. Config & regexes
# --------------------------------------------------------------------
FLAG_PAT  = r"(?:flag|ctf|dam)\{[^}]{4,120}\}|key=.*|passw?or?d=.*"
FLAG_RE   = re.compile(FLAG_PAT, re.I)
ASCII_RE  = re.compile(rb"[\x20-\x7e]{4,}")
UTF16_RE  = re.compile(rb"(?:[\x20-\x7e]\x00){4,}")

try:
    from Levenshtein import distance as ldist
except ImportError:                              # fallback (slow)
    print("[yellow]python-Levenshtein missing – using pure Python.[/yellow]")
    from difflib import SequenceMatcher
    ldist = lambda a,b: int(round((1-SequenceMatcher(None,a,b).ratio())*max(len(a),len(b))))

# --------------------------------------------------------------------
# 2. Extraction helpers
# --------------------------------------------------------------------
def _extract(buf: bytes) -> List[str]:
    out = [m.group().decode("ascii","ignore") for m in ASCII_RE.finditer(buf)]
    out += [m.group().decode("utf-16le","ignore") for m in UTF16_RE.finditer(buf)]
    return out

def pull_strings(path: Path) -> List[str]:
    data = path.read_bytes()
    raw  = _extract(data)
    # also walk raw section dump via objdump -s (catches packed .data)
    try:
        dump = subprocess.check_output(["objdump","-s",path],stderr=subprocess.DEVNULL)
        raw += _extract(dump)
    except Exception:
        pass
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
def score(s,freq,total):
    sc  = 5 if FLAG_RE.search(s) else 0
    sc += max(0, entropy(s)-3.5)
    sc += min(len(s)/15,2)
    sc += min(3, 1/(freq[s]/total))
    return round(sc,2)

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
.score{color:#8f8}
details{margin-left:1.2em}
.gray{color:#666}
</style>
<h1>{{ name }} – Smart-Strings report</h1>
<p>{{ total }} raw strings → {{ clusters|length }} clusters. Generated {{ ts }} UTC.</p>
{% for c in clusters %}
<div><span class=score>[{{ c.score }}]</span>
<span class="{{ 'flag' if c.flag else '' }}">{{ c.rep|e }}</span>
{% if c.dup|length %}
<details class=gray><summary>{{ c.dup|length }} more dupes</summary>
{% for d in c.dup %}<div class=gray>{{ d|e }}</div>{% endfor %}</details>
{% endif %}</div>
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

    total   = len(raw)
    enriched=[]
    for grp in clusters:
        rep=grp[0]
        enriched.append({
            "rep":rep,
            "flag":bool(FLAG_RE.search(rep)),
            "score":score(rep,freq,total),
            "dup":grp[1:]
        })
    enriched.sort(key=lambda x:x["score"], reverse=True)

    html = HTML.render(name=path.name, total=total, clusters=enriched,
                       ts=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

    out_html = (Path(args.out) if args.out else path.parent) / f"{path.name}_strings.html"
    out_html.write_text(html,encoding="utf-8")
    print(f"[green]✔ HTML:[/green] {out_html}")

    if args.json:
        out_json = out_html.with_suffix(".json")
        out_json.write_text(json.dumps(enriched,indent=2))
        print(f"[green]✔ JSON:[/green] {out_json}")

    if not args.no_open:
        try: webbrowser.open(out_html.as_uri())
        except: pass

# --------------------------------------------------------------------
def parse():
    ap = argparse.ArgumentParser(prog="smarthunter",
         description="CTF-grade string miner → HTML.")
    ap.add_argument("binary", help="target binary / file")
    ap.add_argument("-o","--out", help="output dir")
    ap.add_argument("--json", action="store_true", help="also write JSON")
    ap.add_argument("--no-open", action="store_true", help="don't open browser")
    ap.add_argument("--depth", type=int, default=3, help="Levenshtein threshold (default 3)")
    return ap.parse_args()

def main():
    args = parse()
    try:
        hunt(Path(args.binary), args)
    except KeyboardInterrupt:
        print("\n[red]Aborted.[/red]"); sys.exit(130)

if __name__ == "__main__":
    main() 