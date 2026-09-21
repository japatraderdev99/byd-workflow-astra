#!/usr/bin/env python3
"""Assemble the R11 local set from R03 strip, R10, and the complete R14 set.

Prepared cold.  This script never reads R12.  It writes only with
``--execute`` and refuses an existing R11 destination, spec, or manifest.
Before it creates a destination, R14 must have exactly one clean terminal
``OK|completed`` and exactly the five PSDs plus thirteen PNGs defined below.
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
OUT_TEMPLATES = V4 / "WORK/01_TEMPLATES" / (DATE + "-r11")
OUT_STAGING = V4 / "WORK/03_STAGING" / (DATE + "-r11")
OUT_SPEC = V4 / "WORK/00_MATRIZ/production_spec_r11.json"
OUT_MANIFEST = V4 / "WORK/04_QA/assembly_r11_v3.json"

PATCH_FORMATS = ("1920x276", "1920x1080", "1920x1125", "1080x1920", "1109x1973")
MULTI_PATCH_FORMATS = ("1920x1080", "1920x1125", "1080x1920", "1109x1973")
PATCH_OFFERS = ("dolphin-mini-5l-gs", "vd-song-pro-flex", "yuan-pro")
EXPECTED_R14_PSDS = frozenset("BYD_TPL_" + fmt + ".psd" for fmt in PATCH_FORMATS)
EXPECTED_R14_PNGS = frozenset(
    {"byd_dolphin-mini-5l-gs_1920x276.png"}
    | {"byd_" + offer + "_" + fmt + ".png" for fmt in MULTI_PATCH_FORMATS for offer in PATCH_OFFERS}
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(V4))


def expected_r14() -> dict:
    if not R14_LOG.is_file():
        raise RuntimeError("R14_LOG_MISSING")
    lines = R14_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    terminals = [line for line in lines if "|OK|completed|" in line]
    errors = [line for line in lines if "|ERRO|" in line]
    if len(terminals) != 1 or errors:
        raise RuntimeError("R14_NOT_CLEANLY_COMPLETED")
    if not R14_TEMPLATES.is_dir() or not R14_STAGING.is_dir():
        raise RuntimeError("R14_OUTPUT_DIRECTORIES_MISSING")
    psds = sorted(path for path in R14_TEMPLATES.rglob("*") if path.is_file())
    pngs = sorted(path for path in R14_STAGING.rglob("*") if path.is_file())
    actual_psds = {path.name for path in psds}
    actual_pngs = {path.name for path in pngs}
    if len(psds) != 5 or actual_psds != EXPECTED_R14_PSDS:
        raise RuntimeError("R14_PSD_SCOPE_MISMATCH|expected=5|actual=" + str(len(psds)))
    if len(pngs) != 13 or actual_pngs != EXPECTED_R14_PNGS:
        raise RuntimeError("R14_PNG_SCOPE_MISMATCH|expected=13|actual=" + str(len(pngs)))
    return {
        "status": "OK_COMPLETED",
        "log": rel(R14_LOG),
        "terminal": terminals[0],
        "expected_psd_count": 5,
        "expected_png_count": 13,
        "psds": [rel(path) for path in psds],
        "pngs": [rel(path) for path in pngs],
    }


def require_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise RuntimeError("MISSING_SOURCE|" + label + "|" + rel(path))


def plan_copy(source: Path, destination: Path, kind: str, r14_override: bool, plan: list[dict]) -> None:
    require_file(source, kind)
    if destination.exists():
        raise RuntimeError("REFUSE_OVERWRITE|" + rel(destination))
    plan.append({"source": source, "destination": destination, "kind": kind, "r14_override": r14_override})


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
    if len(formats) != 7 or len(set(format_ids)) != 7 or "1920x276" not in format_ids:
        raise RuntimeError("INVALID_R03_FORMAT_SCOPE")
    if len(r10.get("formats", [])) != 6 or "1920x276" in [item.get("id") for item in r10["formats"]]:
        raise RuntimeError("INVALID_R10_FORMAT_SCOPE")
    offer_ids = [item.get("id") for item in offers]
    if len(offers) != 20 or len(set(offer_ids)) != 20 or any(not value for value in offer_ids):
        raise RuntimeError("INVALID_R10_OFFER_SCOPE")

    r14 = expected_r14()
    plan: list[dict] = []
    for fmt in formats:
        fmt_id = fmt["id"]
        is_strip = fmt_id == "1920x276"
        base_templates = V4 / (r03["output_templates"] if is_strip else r10["output_templates"])
        base_staging = V4 / (r03["output_staging"] if is_strip else r10["output_staging"])

        template_name = "BYD_TPL_" + fmt_id + ".psd"
        r14_template = R14_TEMPLATES / template_name
        template_source = r14_template if template_name in EXPECTED_R14_PSDS else base_templates / template_name
        plan_copy(template_source, OUT_TEMPLATES / template_name, "template:" + fmt_id, template_source == r14_template, plan)

        # R14 makes no preview. Preserve the known original R03/R10 preview.
        preview_name = "BYD_TPL_" + fmt_id + "_preview.png"
        plan_copy(base_templates / preview_name, OUT_TEMPLATES / preview_name, "preview:" + fmt_id, False, plan)

        for offer_id in offer_ids:
            png_name = "byd_" + offer_id + "_" + fmt_id + ".png"
            r14_png = R14_STAGING / png_name
            png_source = r14_png if png_name in EXPECTED_R14_PNGS else base_staging / png_name
            plan_copy(png_source, OUT_STAGING / png_name, "png:" + offer_id + ":" + fmt_id, png_source == r14_png, plan)

    # Every source, including the complete R14 scope, is checked before writes.
    OUT_TEMPLATES.mkdir(parents=False)
    OUT_STAGING.mkdir(parents=False)
    copied = []
    for item in plan:
        shutil.copy2(item["source"], item["destination"])
        copied.append({
            "source": rel(item["source"]),
            "destination": rel(item["destination"]),
            "kind": item["kind"],
            "r14_override": item["r14_override"],
            "bytes": item["destination"].stat().st_size,
            "sha256": digest(item["destination"]),
        })

    spec = dict(r03)
    spec["offers"] = offers
    spec["revision"] = REVISION
    spec["assembly_revision"] = "r11_v3"
    spec["output_templates"] = "WORK/01_TEMPLATES/" + DATE + "-r11/"
    spec["output_staging"] = "WORK/03_STAGING/" + DATE + "-r11/"
    spec["assembly_sources"] = {
        "strip_default": r03["output_templates"] + " and " + r03["output_staging"],
        "other_formats_default": r10["output_templates"] + " and " + r10["output_staging"],
        "r14": r14,
        "policy": "R14 is mandatory and exact: five patch PSDs and thirteen changed PNGs. All previews remain R03/R10 originals. R12 is not an assembly source.",
    }
    OUT_SPEC.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MANIFEST.write_text(json.dumps({
        "schema": "byd-v4-assembly-r11-v3/v1",
        "created_at": dt.datetime.now().astimezone().isoformat(),
        "revision": REVISION,
        "assembly_revision": "r11_v3",
        "write_guard": "REFUSE_OVERWRITE",
        "method": "byte copies only; no image recompression, PSD mutation, promotion, visual approval, or external delivery",
        "r14": r14,
        "count": len(copied),
        "r14_override_count": sum(1 for item in copied if item["r14_override"]),
        "files": copied,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK|ASSEMBLED_R11_V3|files=" + str(len(copied)) + "|r14_overrides=" + str(sum(1 for item in copied if item["r14_override"])))


if __name__ == "__main__":
    main()
