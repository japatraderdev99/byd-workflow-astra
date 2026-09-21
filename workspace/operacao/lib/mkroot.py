"""mkroot.py — resolução de raiz para Python.

    from mkroot import ROOT       # se lib/ estiver no sys.path
    # ou
    ROOT = mk_root(__file__)

Sobe a partir do arquivo até achar o marcador .mkroot.
"""
from pathlib import Path


def mk_root(start: str | Path) -> Path:
    here = Path(start).resolve()
    for parent in (here, *here.parents):
        if (parent / ".mkroot").is_file():
            return parent
    raise RuntimeError(f"MKROOT_NOT_FOUND a partir de {here}")


ROOT = mk_root(__file__)
