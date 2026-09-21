#!/usr/bin/env python3
"""Assemble the R11 local set from R03 strip, R10, and a completed R12 only.

Prepared cold.  It writes only with ``--execute`` and will refuse any existing
R11 destination, spec, or manifest.  R12 is an optional replacement source:
its files are eligible only after the one-shot R12 log has an ``OK|completed``
terminal and no ``ERRO`` event.  An R12 file left by a failed/interrupted run
therefore stops assembly instead of producing a mixed partial set.
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
R12_LOG = V4 / "WORK/06_LOGS/patch_controle_r12.log"
R12_TEMPLATES = V4 / "WORK/01_TEMPLATES" / (DATE + "-r12")
R12_STAGING = V4 / "WORK/03_STAGING" / (DATE + "-r12")
OUT_TEMPLATES = V4 / "WORK/01_TEMPLATES" / (DATE + "-r11")
OUT_STAGING = V4 / "WORK/03_STAGING" / (DATE + "-r11")
OUT_SPEC = V4 / "WORK/00_MATRIZ/production_spec_r11.json"
OUT_MANIFEST = V4 / "WORK/04_QA/assembly_r11_v2.json"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(V4))


def r12_status() -> tuple[bool, dict]:
    produced = []
    for directory in (R12_TEMPLATES, R12_STAGING):
        if directory.exists():
            produced.extend(sorted(item for item in directory.rglob("*") if item.is_file()))
    if not R12_LOG.exists():
        if produced:
            raise RuntimeError("R12_OUTPUT_WITHOUT_LOG")
        return False, {"status": "NO_LOG_NO_OUTPUTS", "log": rel(R12_LOG), "files": []}
    lines = R12_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    terminals = [line for line in lines if "|OK|completed|" in line]
    errors = [line for line in lines if "|ERRO|" in line]
    completed = len(terminals) == 1 and not errors
    if produced and not completed:
        raise RuntimeError("R12_PARTIAL_OR_FAILED_OUTPUTS_NOT_ALLOWED")
    return completed, {
        "status": "OK_COMPLETED" if completed else "INCOMPLETE_NO_OUTPUTS",
        "log": rel(R12_LOG),
        "terminal": terminals[0] if completed else None,
        "error_count": len(errors),
        "files": [rel(path) for path in produced],
    }


def require_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise RuntimeError("MISSING_SOURCE|" + label + "|" + rel(path))


def plan_copy(source: Path, destination: Path, kind: str, r12_override: bool, plan: list[dict]) -> None:
    require_file(source, kind)
    if destination.exists():
        raise RuntimeError("REFUSE_OVERWRITE|" + rel(destination))
    plan.append({"source": source, "destination": destination, "kind": kind, "r12_override": r12_override})


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

    use_r12, r12 = r12_status()
    plan: list[dict] = []
    for fmt in formats:
        fmt_id = fmt["id"]
        is_strip = fmt_id == "1920x276"
        base_templates = V4 / (r03["output_templates"] if is_strip else r10["output_templates"])
        base_staging = V4 / (r03["output_staging"] if is_strip else r10["output_staging"])

        template_name = "BYD_TPL_" + fmt_id + ".psd"
        r12_template = R12_TEMPLATES / template_name
        template_source = r12_template if use_r12 and r12_template.is_file() else base_templates / template_name
        plan_copy(template_source, OUT_TEMPLATES / template_name, "template:" + fmt_id, template_source == r12_template, plan)

        # Previews remain the original R03/R10 preview assets; no R12 preview
        # is considered.  This preserves the established Atto 2 preview anchor.
        preview_name = "BYD_TPL_" + fmt_id + "_preview.png"
        plan_copy(base_templates / preview_name, OUT_TEMPLATES / preview_name, "preview:" + fmt_id, False, plan)

        for offer_id in offer_ids:
            png_name = "byd_" + offer_id + "_" + fmt_id + ".png"
            r12_png = R12_STAGING / png_name
            png_source = r12_png if use_r12 and r12_png.is_file() else base_staging / png_name
            plan_copy(png_source, OUT_STAGING / png_name, "png:" + offer_id + ":" + fmt_id, png_source == r12_png, plan)

    # Every source is checked before creating either destination directory.
    OUT_TEMPLATES.mkdir(parents=False)
    OUT_STAGING.mkdir(parents=False)
    copied = []
    for item in plan:
        shutil.copy2(item["source"], item["destination"])
        copied.append({
            "source": rel(item["source"]),
            "destination": rel(item["destination"]),
            "kind": item["kind"],
            "r12_override": item["r12_override"],
            "bytes": item["destination"].stat().st_size,
            "sha256": digest(item["destination"]),
        })

    spec = dict(r03)
    spec["offers"] = offers
    spec["revision"] = REVISION
    spec["assembly_revision"] = "r11_v2"
    spec["output_templates"] = "WORK/01_TEMPLATES/" + DATE + "-r11/"
    spec["output_staging"] = "WORK/03_STAGING/" + DATE + "-r11/"
    spec["assembly_sources"] = {
        "strip_default": r03["output_templates"] + " and " + r03["output_staging"],
        "other_formats_default": r10["output_templates"] + " and " + r10["output_staging"],
        "r12": r12,
        "policy": "R12 files replace only matching existing template/PNG names after one clean OK|completed terminal. Previews always remain R03/R10 originals.",
    }
    OUT_SPEC.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MANIFEST.write_text(json.dumps({
        "schema": "byd-v4-assembly-r11-v2/v1",
        "created_at": dt.datetime.now().astimezone().isoformat(),
        "revision": REVISION,
        "assembly_revision": "r11_v2",
        "write_guard": "REFUSE_OVERWRITE",
        "method": "byte copies only; no image recompression, PSD mutation, promotion, visual approval, or external delivery",
        "r12": r12,
        "count": len(copied),
        "r12_override_count": sum(1 for item in copied if item["r12_override"]),
        "files": copied,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK|ASSEMBLED_R11_V2|files=" + str(len(copied)) + "|r12_overrides=" + str(sum(1 for item in copied if item["r12_override"])))


if __name__ == "__main__":
    main()
