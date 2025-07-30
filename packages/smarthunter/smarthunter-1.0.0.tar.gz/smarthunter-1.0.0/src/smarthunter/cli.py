import typer, json, rich
from pathlib import Path
from .core import scan

app = typer.Typer(no_args_is_help=True, add_completion=False)

@app.command()
def hunt(
    binary: Path,
    out: Path = typer.Option(None, help="Save hits as JSON"),
    min: int = 4,
    max: int = 120,
    workers: int = typer.Option(0, help="0=auto"),
):
    """Smart-hunt strings & flags inside any file."""
    hits = list(scan(binary, minlen=min, maxlen=max, workers=(workers or None)))
    hits.sort(key=lambda h: (-h.score, h.offset))
    for h in hits:
        rich.print(f"[green]{h.offset:08x}[/] [{h.codec}] {h.text!r}")
    if out:
        out.write_text(json.dumps([h._asdict() for h in hits], indent=2))
        rich.print(f"[bold cyan]Saved → {out}") 