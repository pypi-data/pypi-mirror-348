import re, math, subprocess, functools, importlib, pkgutil, sys, webbrowser, json
from pathlib import Path
from collections import Counter
from datetime import datetime
from typing import List, Dict, Callable, Tuple
from rich import print
from Levenshtein import distance as ldist
from .html_template import HTML_TEMPLATE

# Registries ------------------------------------------------------------------
DECODER_REGISTRY: list[Callable[[str], list[tuple[str,str]]]] = []
PATTERN_REGISTRY: list[tuple[str,float,re.Pattern]] = []

def decoder(fn: Callable[[str], list[tuple[str,str]]]):
    DECODER_REGISTRY.append(fn); return fn

def pattern(name:str, score:float):
    def wrap(regex:str|re.Pattern):
        PATTERN_REGISTRY.append(
            (name, score, re.compile(regex, re.I) if isinstance(regex,str) else regex)
        ); return regex
    return wrap

# --------------------------------------------------------------------------------
ASCII_RE  = re.compile(rb"[\x20-\x7e]{4,}")
UTF16_RE  = re.compile(rb"(?:[\x20-\x7e]\x00){4,}")

def _clean_string(s: str) -> List[str]:
    """Split a string on non-printable characters and remove junk."""
    # Split the string on non-printable characters
    parts = re.split(r'[^\x20-\x7e]', s)
    # Filter out empty parts and parts that are too short
    return [part for part in parts if part and len(part) >= 4]

def _extract(buf: bytes) -> list[str]:
    result = []
    
    # Extract ASCII strings
    for m in ASCII_RE.finditer(buf):
        raw_str = m.group().decode('ascii','ignore')
        # Add the original string
        result.append(raw_str)
        # Also add cleaned sub-strings to catch embedded flags
        result.extend(_clean_string(raw_str))
    
    # Extract UTF-16 strings
    for m in UTF16_RE.finditer(buf):
        raw_str = m.group().decode('utf-16le','ignore')
        # Add the original string
        result.append(raw_str)
        # Also add cleaned sub-strings
        result.extend(_clean_string(raw_str))
    
    return result

def pull_strings(path: Path, decode_depth:int, budget:int) -> list[str]:
    data = path.read_bytes(); raw=_extract(data)
    try: raw += _extract(subprocess.check_output(["objdump","-s",path],stderr=subprocess.DEVNULL))
    except Exception: pass
    all_seen=set(raw); frontier=list(raw)
    for _ in range(decode_depth):
        new=[]
        for s in frontier:
            for fn in DECODER_REGISTRY:
                for tag,out in fn(s):
                    if out not in all_seen:
                        msg=f"[{tag}] {out}"
                        new.append(msg); all_seen.add(msg)
                        if len(all_seen) >= budget: break
            if len(all_seen) >= budget: break
        frontier=new
        if not frontier or len(all_seen) >= budget: break
    return list(all_seen)

# BK-tree clustering -----------------------------------------------------------
class BKTree:
    def __init__(self,w=None): self.w=w; self.k={}
    def add(self,word:str):
        if self.w is None: self.w=word; return
        d=ldist(word,self.w); self.k.setdefault(d,BKTree()).add(word)
    def near(self,word,stride:int,bag:set[str]|None=None):
        bag=bag or set(); d=ldist(word,self.w)
        if d<=stride: bag.add(self.w)
        for dist,node in self.k.items():
            if d-stride<=dist<=d+stride: node.near(word,stride,bag)
        return bag
def cluster(strings:list[str], stride:int)->list[list[str]]:
    tree=BKTree(); [tree.add(s) for s in strings]
    seen,setseen=set(),set()
    cl=[]
    for s in strings:
        if s in seen: continue
        grp=tree.near(s,stride)
        seen|=grp; cl.append(sorted(grp))
    return cl

# Scoring ----------------------------------------------------------------------
def entropy(s:str)->float:
    f=Counter(s); return -sum(c/len(s)*math.log2(c/len(s)) for c in f.values())

def detect_patterns(s:str)->dict[str,bool]:
    return {name:bool(rgx.search(s)) for name,_,rgx in PATTERN_REGISTRY}

def score(s:str, freq:Counter, total:int)->tuple[float,dict]:
    pat=detect_patterns(s)
    base=sum(sc for (name,sc,_) in PATTERN_REGISTRY if pat.get(name))
    ent=max(0,entropy(s)-3.5)
    length=min(len(s)/15,2)
    rarity=min(3,1/(freq[s]/total))
    return round(base+ent+length+rarity,2),{
        "patterns":[n for n,f in pat.items() if f],
        "entropy":round(ent,2),"length":round(length,2),"rarity":round(rarity,2)
    }

# HTML output ------------------------------------------------------------------
def write_html(name:str, clusters:list[dict], total:int, out:Path):
    html=HTML_TEMPLATE.render(name=name,total=total,clusters=clusters,
                              ts=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    out.write_text(html,encoding='utf-8')
    print(f"[green]✔ HTML:[/green] {out}")
    try:webbrowser.open(out.as_uri())
    except:pass

# Plugin loader ----------------------------------------------------------------
def _load_submodules(pkg):
    for mod in pkgutil.iter_modules(pkg.__path__):
        importlib.import_module(f"{pkg.__name__}.{mod.name}")

def load_plugins():
    from . import decoders, patterns
    _load_submodules(decoders); _load_submodules(patterns)

# High-level runner ------------------------------------------------------------
def run(target:Path, depth:int=2, stride:int=3, out_dir:Path|None=None,
        no_open=False, json_flag=False, budget:int=100_000):
    load_plugins()
    raw=pull_strings(target, depth, budget)
    freq=Counter(raw); uniq=list(freq)
    print(f"[blue]∙ Extracted {len(raw)} raw / {len(uniq)} unique strings.[/blue]")
    clusters_raw=cluster(uniq,stride)
    print(f"[blue]∙ {len(clusters_raw)} clusters (d≤{stride}).[/blue]")

    enriched=[]
    for grp in clusters_raw:
        rep=grp[0]; val,det=score(rep,freq,len(raw))
        pats=detect_patterns(rep)
        enriched.append({
            "rep":rep,"score":val,"details":det,"dup":grp[1:],
            "flag":pats.get("Flag",False),
            "url":pats.get("URL",False),
            "email":pats.get("Email",False),
            "ip":pats.get("IP",False),
            "hash":pats.get("Hash",False),
            "secret":pats.get("Secret",False),
        })
    enriched.sort(key=lambda x:x["score"],reverse=True)

    out_html=(out_dir or target.parent)/f"{target.name}_strings.html"
    write_html(target.name,enriched,len(raw),out_html)
    if json_flag:
        j=out_html.with_suffix(".json"); j.write_text(json.dumps(enriched,indent=2))
        print(f"[green]✔ JSON:[/green] {j}")
    if no_open: pass 