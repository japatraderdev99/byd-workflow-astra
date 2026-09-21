#!/usr/bin/env python3
"""Local R11 promotion, guarded by technical and Astra-agent visual evidence.

This is a local promotion gate.  An Astra visual pass is not a human/client
approval and must never be written as one in the resulting manifest.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
from pathlib import Path


def workspace_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".mkroot").exists():
            return candidate
    raise RuntimeError("MISSING_MKROOT")


ROOT = workspace_root(Path(__file__).resolve())
V4 = ROOT / "Projects/BYD/Jobs/V4"
REVISION = "r11"
DATE = "2026-09-20"
SPEC = V4 / "WORK/00_MATRIZ/production_spec_r11.json"
QA_DIR = V4 / "WORK/04_QA/production-r11"
TECH = QA_DIR / "technical_all.json"
ASTRA_VISUAL = QA_DIR / "head_visual_review.json"
MANIFEST = QA_DIR / "manifest_r11.json"
STAGING = V4 / "WORK/03_STAGING" / (DATE + "-r11")
OUTPUT = V4 / "OUTPUT" / (DATE + "-r11")
DESTINATION = {"1920x276": "BANNER DESK", "1920x1125": "BANNER DESK", "360x80": "BANNER MOBILE", "1109x1973": "BANNER MOBILE", "1080x1080": "ESTATICOS", "1080x1920": "ESTATICOS", "1920x1080": "ESTATICOS"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Required for local copy after all preflight checks pass.")
    args = parser.parse_args()
    if not args.execute:
        raise RuntimeError("REFUSE_PROMOTION_WITHOUT_--execute")
    if MANIFEST.exists():
        raise RuntimeError("REFUSE_OVERWRITE_MANIFEST")
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    tech = json.loads(TECH.read_text(encoding="utf-8"))
    visual = json.loads(ASTRA_VISUAL.read_text(encoding="utf-8"))
    if spec.get("revision") != REVISION or len(spec["offers"]) != 20 or len(spec["formats"]) != 7:
        raise RuntimeError("INVALID_R11_SCOPE")
    rows = tech.get("rows", [])
    if len(rows) != 140 or tech.get("pass") != 140:
        raise RuntimeError("TECHNICAL_QA_NOT_140_PASS")
    if visual.get("review_type") != "ASTRA_AGENT_VISUAL_REVIEW":
        raise RuntimeError("INVALID_REVIEW_TYPE_EXPECTED_ASTRA_AGENT")
    approved = {row["file"]: row for row in visual.get("files", []) if row.get("status") == "PASS"}
    if len(approved) != 140:
        raise RuntimeError("ASTRA_VISUAL_REVIEW_NOT_140_PASS")
    plan = []
    for row in rows:
        source = V4 / row["file"]
        review = approved.get(row["file"])
        if review is None or not source.is_file():
            raise RuntimeError("MISSING_ASTRA_REVIEW_OR_SOURCE|" + row["file"])
        actual = digest(source)
        if actual != row.get("sha256") or actual != review.get("sha256"):
            raise RuntimeError("HASH_MISMATCH|" + row["file"])
        fmt = row["format"]
        if fmt not in DESTINATION:
            raise RuntimeError("UNKNOWN_FORMAT|" + fmt)
        destination = OUTPUT / DESTINATION[fmt] / fmt / source.name
        if destination.exists():
            raise RuntimeError("REFUSE_OVERWRITE|" + str(destination.relative_to(V4)))
        plan.append((source, destination, row))
    promoted = []
    for source, destination, row in plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        if digest(destination) != row["sha256"]:
            raise RuntimeError("POSTCOPY_HASH_MISMATCH|" + str(destination.relative_to(V4)))
        promoted.append({**row, "output_file": str(destination.relative_to(V4)), "visual_status": "ASTRA_AGENT_VISUAL_REVIEW_PASS", "visual_review_is_human_approval": False, "delivery_status": "LOCAL_OUTPUT_NOT_EXTERNALLY_SENT"})
    MANIFEST.write_text(json.dumps({"revision": REVISION, "created_at": dt.datetime.now().astimezone().isoformat(), "count": len(promoted), "files": promoted, "visual_review_type": "ASTRA_AGENT_VISUAL_REVIEW", "visual_review_is_human_approval": False, "delivery_status": "LOCAL_ONLY"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK|PROMOTED_R11|" + str(len(promoted)))


if __name__ == "__main__":
    main()
