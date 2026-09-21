#!/usr/bin/env python3
"""Assemble R11 from the verified R14 strip, R16 large formats, R03, and R10.

Prepared cold.  It writes only with ``--execute`` and refuses every existing
R11 destination artifact.  R14 is deliberately an exception limited to the
completed 1920x276 strip before its later error.  R16 is mandatory, cleanly
completed, and exact for the four large formats.  R12 is never read.
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
DATE = "2026-09-20"
REVISION = "r11"
R03_SPEC = V4 / "WORK/00_MATRIZ/production_spec_r03.json"
R10_SPEC = V4 / "WORK/00_MATRIZ/production_spec_r10.json"
R14_LOG = V4 / "WORK/06_LOGS/patch_controle_r14.log"
R14_TEMPLATES = V4 / "WORK/01_TEMPLATES" / (DATE + "-r14")
R14_STAGING = V4 / "WORK/03_STAGING" / (DATE + "-r14")
R16_LOG = V4 / "WORK/06_LOGS/patch_controle_r16.log"
R16_TEMPLATES = V4 / "WORK/01_TEMPLATES" / (DATE + "-r16")
R16_STAGING = V4 / "WORK/03_STAGING" / (DATE + "-r16")
OUT_TEMPLATES = V4 / "WORK/01_TEMPLATES" / (DATE + "-r11")
OUT_STAGING = V4 / "WORK/03_STAGING" / (DATE + "-r11")
OUT_SPEC = V4 / "WORK/00_MATRIZ/production_spec_r11.json"
OUT_MANIFEST = V4 / "WORK/04_QA/assembly_r11_v4.json"

STRIP_FORMAT = "1920x276"
LARGE_FORMATS = ("1920x1080", "1920x1125", "1080x1920", "1109x1973")
PATCH_OFFERS = ("dolphin-mini-5l-gs", "vd-song-pro-flex", "yuan-pro")
R14_STRIP_PSD = "BYD_TPL_1920x276.psd"
R14_STRIP_PNG = "byd_dolphin-mini-5l-gs_1920x276.png"
EXPECTED_R16_PSDS = frozenset("BYD_TPL_" + fmt + ".psd" for fmt in LARGE_FORMATS)
EXPECTED_R16_PNGS = frozenset(
    "byd_" + offer + "_" + fmt + ".png" for fmt in LARGE_FORMATS for offer in PATCH_OFFERS
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(V4))


def only_files(directory: Path) -> list[Path]:
    return sorted(path for path in directory.rglob("*") if path.is_file())


def verified_r14_strip() -> dict:
    if not R14_LOG.is_file() or not R14_TEMPLATES.is_dir() or not R14_STAGING.is_dir():
        raise RuntimeError("R14_STRIP_EVIDENCE_MISSING")
    lines = R14_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    format_indexes = [index for index, line in enumerate(lines) if "|FORMAT_OK|1920x276|" in line]
    error_indexes = [index for index, line in enumerate(lines) if "|ERRO|" in line]
    if len(format_indexes) != 1 or not error_indexes or format_indexes[0] >= error_indexes[0]:
        raise RuntimeError("R14_STRIP_NOT_FORMAT_OK_BEFORE_ERROR")
    psds, pngs = only_files(R14_TEMPLATES), only_files(R14_STAGING)
    if len(psds) != 1 or {path.name for path in psds} != {R14_STRIP_PSD}:
        raise RuntimeError("R14_STRIP_PSD_SCOPE_MISMATCH")
    if len(pngs) != 1 or {path.name for path in pngs} != {R14_STRIP_PNG}:
        raise RuntimeError("R14_STRIP_PNG_SCOPE_MISMATCH")
    return {
        "status": "EXCEPTION_FORMAT_OK_BEFORE_LATER_ERROR",
        "log": rel(R14_LOG),
        "format_ok": lines[format_indexes[0]],
        "first_later_error": lines[error_indexes[0]],
        "psd": rel(psds[0]),
        "png": rel(pngs[0]),
        "scope": "only 1920x276 template and Dolphin Mini PNG; no other R14 output is eligible",
        "human_review": "external prerequisite; not asserted by this script",
    }


def complete_r16() -> dict:
    if not R16_LOG.is_file() or not R16_TEMPLATES.is_dir() or not R16_STAGING.is_dir():
        raise RuntimeError("R16_EVIDENCE_MISSING")
    lines = R16_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    terminals = [line for line in lines if "|OK|completed|" in line]
    errors = [line for line in lines if "|ERRO|" in line]
    if len(terminals) != 1 or errors:
        raise RuntimeError("R16_NOT_CLEANLY_COMPLETED")
    psds, pngs = only_files(R16_TEMPLATES), only_files(R16_STAGING)
    if len(psds) != 4 or {path.name for path in psds} != EXPECTED_R16_PSDS:
        raise RuntimeError("R16_PSD_SCOPE_MISMATCH|expected=4|actual=" + str(len(psds)))
    if len(pngs) != 12 or {path.name for path in pngs} != EXPECTED_R16_PNGS:
        raise RuntimeError("R16_PNG_SCOPE_MISMATCH|expected=12|actual=" + str(len(pngs)))
    return {
        "status": "OK_COMPLETED",
        "log": rel(R16_LOG),
        "terminal": terminals[0],
        "expected_psd_count": 4,
        "expected_png_count": 12,
        "psds": [rel(path) for path in psds],
        "pngs": [rel(path) for path in pngs],
    }


def require_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise RuntimeError("MISSING_SOURCE|" + label + "|" + rel(path))


def plan_copy(source: Path, destination: Path, kind: str, source_revision: str, plan: list[dict]) -> None:
    require_file(source, kind)
    if destination.exists():
        raise RuntimeError("REFUSE_OVERWRITE|" + rel(destination))
    plan.append({"source": source, "destination": destination, "kind": kind, "source_revision": source_revision})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Required to write the new local R11 assembly.")
    args = parser.parse_args()
    if not args.execute:
        raise RuntimeError("REFUSE_ASSEMBLY_WITHOUT_--execute")
    for target in (OUT_TEMPLATES, OUT_STAGING, OUT_SPEC, OUT_MANIFEST):
        if target.exists():
            raise RuntimeError("REFUSE_OVERWRITE|" + rel(target))

    r03 = json.loads(R03_SPEC.read_text(encoding="utf-8"))
    r10 = json.loads(R10_SPEC.read_text(encoding="utf-8"))
    formats = r03.get("formats", [])
    offers = r10.get("offers", [])
    format_ids = [item.get("id") for item in formats]
    if len(formats) != 7 or len(set(format_ids)) != 7 or set(LARGE_FORMATS).difference(format_ids) or STRIP_FORMAT not in format_ids:
        raise RuntimeError("INVALID_R03_FORMAT_SCOPE")
    if len(r10.get("formats", [])) != 6 or STRIP_FORMAT in [item.get("id") for item in r10["formats"]]:
        raise RuntimeError("INVALID_R10_FORMAT_SCOPE")
    offer_ids = [item.get("id") for item in offers]
    if len(offers) != 20 or len(set(offer_ids)) != 20 or any(not value for value in offer_ids) or set(PATCH_OFFERS).difference(offer_ids):
        raise RuntimeError("INVALID_R10_OFFER_SCOPE")

    r14 = verified_r14_strip()
    r16 = complete_r16()
    plan: list[dict] = []
    for fmt in formats:
        fmt_id = fmt["id"]
        is_strip = fmt_id == STRIP_FORMAT
        is_large = fmt_id in LARGE_FORMATS
        base_templates = V4 / (r03["output_templates"] if is_strip else r10["output_templates"])
        base_staging = V4 / (r03["output_staging"] if is_strip else r10["output_staging"])

        template_name = "BYD_TPL_" + fmt_id + ".psd"
        if is_strip:
            template_source, template_revision = R14_TEMPLATES / template_name, "r14_exception_strip"
        elif is_large:
            template_source, template_revision = R16_TEMPLATES / template_name, "r16"
        else:
            template_source, template_revision = base_templates / template_name, "r10"
        plan_copy(template_source, OUT_TEMPLATES / template_name, "template:" + fmt_id, template_revision, plan)

        # No patch preview is used: established R03/R10 previews are retained.
        preview_name = "BYD_TPL_" + fmt_id + "_preview.png"
        plan_copy(base_templates / preview_name, OUT_TEMPLATES / preview_name, "preview:" + fmt_id, "r03" if is_strip else "r10", plan)

        for offer_id in offer_ids:
            png_name = "byd_" + offer_id + "_" + fmt_id + ".png"
            if is_strip and offer_id == "dolphin-mini-5l-gs":
                png_source, png_revision = R14_STAGING / png_name, "r14_exception_strip"
            elif is_large and offer_id in PATCH_OFFERS:
                png_source, png_revision = R16_STAGING / png_name, "r16"
            else:
                png_source, png_revision = base_staging / png_name, "r03" if is_strip else "r10"
            plan_copy(png_source, OUT_STAGING / png_name, "png:" + offer_id + ":" + fmt_id, png_revision, plan)

    # All source files and both exception/terminal scopes are checked before writes.
    OUT_TEMPLATES.mkdir(parents=False)
    OUT_STAGING.mkdir(parents=False)
    copied = []
    for item in plan:
        shutil.copy2(item["source"], item["destination"])
        copied.append({
            "source": rel(item["source"]),
            "destination": rel(item["destination"]),
            "kind": item["kind"],
            "source_revision": item["source_revision"],
            "bytes": item["destination"].stat().st_size,
            "sha256": digest(item["destination"]),
        })

    spec = dict(r03)
    spec["offers"] = offers
    spec["revision"] = REVISION
    spec["assembly_revision"] = "r11_v4"
    spec["output_templates"] = "WORK/01_TEMPLATES/" + DATE + "-r11/"
    spec["output_staging"] = "WORK/03_STAGING/" + DATE + "-r11/"
    spec["assembly_sources"] = {
        "strip_default": r03["output_templates"] + " and " + r03["output_staging"],
        "other_formats_default": r10["output_templates"] + " and " + r10["output_staging"],
        "r14_exception": r14,
        "r16": r16,
        "policy": "R14 contributes only its completed strip PSD and Dolphin Mini PNG before a later error. R16 is mandatory for the four large PSDs and twelve changed PNGs. Previews remain R03/R10 originals; R12 is not read.",
    }
    OUT_SPEC.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MANIFEST.write_text(json.dumps({
        "schema": "byd-v4-assembly-r11-v4/v1",
        "created_at": dt.datetime.now().astimezone().isoformat(),
        "revision": REVISION,
        "assembly_revision": "r11_v4",
        "write_guard": "REFUSE_OVERWRITE",
        "method": "byte copies only; no image recompression, PSD mutation, promotion, visual approval, or external delivery",
        "r14_exception": r14,
        "r16": r16,
        "count": len(copied),
        "source_revision_counts": {name: sum(1 for item in copied if item["source_revision"] == name) for name in ("r03", "r10", "r14_exception_strip", "r16")},
        "files": copied,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK|ASSEMBLED_R11_V4|files=" + str(len(copied)))


if __name__ == "__main__":
    main()
