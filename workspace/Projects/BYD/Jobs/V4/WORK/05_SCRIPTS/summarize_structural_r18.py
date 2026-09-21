#!/usr/bin/env python3
"""Summarize the complete R18 read-only PSD QA into a strict seven-row gate.

This script does not inspect PSD structure itself. Run qa_templates_r01.py
first, after Photoshop has finished. It independently re-hashes the seven
templates, checks every structural result in qa_templates_r18.json, and binds
Layer Comp acceptance to the 280 native R17/R20 apply tests.

Usage:
  python3 WORK/05_SCRIPTS/summarize_structural_r18.py --revision r18
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REFUSE_OVERWRITE = True
EXPECTED_ROOTS = {"BG", "VEICULO", "LEGAL", "CONDICIONAIS", "OFERTA", "FIXO", "#GUIAS"}
STATE_ROOTS = {"BG", "VEICULO", "LEGAL", "CONDICIONAIS", "OFERTA"}
TEXT_FIELDS = {"title", "price", "legal", "benefit", "headline"}
STRIP_FORMAT = "1920x276"
REST_FORMATS = {"1920x1080", "1920x1125", "1080x1080", "1080x1920", "1109x1973", "360x80"}


def find_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".mkroot").exists():
            return candidate
    raise RuntimeError("MISSING_MKROOT")


ROOT = find_root(Path(__file__).resolve())
V4 = ROOT / "Projects/BYD/Jobs/V4"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"MISSING_INPUT|{path.relative_to(ROOT)}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"INVALID_JSON_ROOT|{path.relative_to(ROOT)}")
    return value


def log_lines(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"MISSING_NATIVE_LOG|{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def event_lines(lines: list[str], event: str, phase: str, fmt: str) -> list[str]:
    marker = f"|{event}|{phase}|{fmt}|"
    return [line for line in lines if marker in line]


def offer_ids_from_events(lines: list[str], phase: str, fmt: str) -> list[str]:
    marker = f"|COMP_APPLY_OK|{phase}|{fmt}|"
    values = []
    for line in lines:
        if marker not in line:
            continue
        tail = line.split(marker, 1)[1]
        values.append(tail.split("|", 1)[0])
    return values


def native_format_evidence(lines: list[str], fmt: str, expected_offers: set[str]) -> dict[str, Any]:
    before_ids = offer_ids_from_events(lines, "before_save", fmt)
    after_ids = offer_ids_from_events(lines, "after_reopen", fmt)
    expected_counter = Counter({offer_id: 1 for offer_id in expected_offers})
    checks = {
        "before_save_20_exact_offers": Counter(before_ids) == expected_counter,
        "after_reopen_20_exact_offers": Counter(after_ids) == expected_counter,
        "output_saved_once": len([line for line in lines if f"|OUTPUT_SAVED|{fmt}|" in line]) == 1,
        "format_ok_once": len([line for line in lines if f"|FORMAT_OK|{fmt}|" in line]) == 1,
    }
    return {
        "format": fmt,
        "before_save_count": len(before_ids),
        "after_reopen_count": len(after_ids),
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }


def native_layer_comp_evidence(spec: dict[str, Any], r17_log: Path, r20_log: Path) -> dict[str, Any]:
    expected_offers = {offer["id"] for offer in spec["offers"]}
    r17 = log_lines(r17_log)
    r20 = log_lines(r20_log)
    by_format: dict[str, Any] = {}
    by_format[STRIP_FORMAT] = native_format_evidence(r17, STRIP_FORMAT, expected_offers)
    for fmt in sorted(REST_FORMATS):
        by_format[fmt] = native_format_evidence(r20, fmt, expected_offers)

    strip_ok_indexes = [i for i, line in enumerate(r17) if f"|FORMAT_OK|{STRIP_FORMAT}|" in line]
    r17_error_indexes = [i for i, line in enumerate(r17) if "|ERRO|" in line]
    r20_terminals = [line for line in r20 if "|OK|completed|templates=6|" in line]
    run_checks = {
        "r17_strip_completed_before_later_interruption": (
            len(strip_ok_indexes) == 1
            and bool(r17_error_indexes)
            and strip_ok_indexes[0] < r17_error_indexes[0]
        ),
        "r20_clean_terminal": len(r20_terminals) == 1 and not any("|ERRO|" in line for line in r20),
        "exact_format_scope": set(by_format) == ({STRIP_FORMAT} | REST_FORMATS),
        "all_formats_native_pass": all(item["status"] == "PASS" for item in by_format.values()),
    }
    total = sum(item["before_save_count"] + item["after_reopen_count"] for item in by_format.values())
    run_checks["native_apply_tests_280"] = total == 280
    return {
        "status": "PASS" if all(run_checks.values()) else "FAIL",
        "tests": total,
        "checks": run_checks,
        "formats": by_format,
        "logs": [str(r17_log.relative_to(V4)), str(r20_log.relative_to(V4))],
    }


def format_from_template_path(path_value: str) -> str | None:
    match = re.fullmatch(r"BYD_TPL_(.+)\.psd", Path(path_value).name)
    return match.group(1) if match else None


def canon_text(value: str) -> str:
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii").lower().strip()


def manifest_index(manifest: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, bool]]:
    rows = manifest.get("files", [])
    result: dict[str, dict[str, Any]] = {}
    duplicates = False
    for row in rows if isinstance(rows, list) else []:
        fmt = format_from_template_path(str(row.get("file", "")))
        if not fmt or fmt in result:
            duplicates = True
            continue
        result[fmt] = row
    checks = {
        "revision_r18": manifest.get("revision") == "r18",
        "declared_count_7": manifest.get("count") == 7,
        "rows_7": isinstance(rows, list) and len(rows) == 7,
        "unique_format_rows": not duplicates and len(result) == 7,
    }
    return result, checks


def check_roots(report: dict[str, Any]) -> bool:
    roots = report.get("root_groups", {})
    return (
        isinstance(roots, dict)
        and set(roots) == EXPECTED_ROOTS
        and all(item.get("status") == "PASS" and item.get("count") == 1 for item in roots.values())
    )


def check_states(report: dict[str, Any]) -> bool:
    states = report.get("state_groups", {})
    return (
        isinstance(states, dict)
        and set(states) == STATE_ROOTS
        and all(
            item.get("status") == "PASS"
            and item.get("count") == 20
            and item.get("missing") == []
            and item.get("duplicates") == []
            for item in states.values()
        )
    )


def check_texts(report: dict[str, Any], offers_by_id: dict[str, dict[str, Any]]) -> tuple[bool, dict[str, Any]]:
    editable = report.get("text_editable_counts", {})
    comparisons = report.get("main_text_comparison", [])
    by_offer: dict[str, dict[str, Any]] = {}
    duplicate = False
    for row in comparisons if isinstance(comparisons, list) else []:
        offer_id = row.get("offer_id")
        if not offer_id or offer_id in by_offer:
            duplicate = True
        else:
            by_offer[offer_id] = row
    failures = []
    for offer_id, offer in offers_by_id.items():
        row = by_offer.get(offer_id, {})
        fields = row.get("fields", {})
        if not isinstance(fields, dict) or set(fields) != TEXT_FIELDS:
            failures.append(f"{offer_id}:field_scope")
            continue
        for field in sorted(TEXT_FIELDS):
            item = fields[field]
            if field == "headline" and offer.get("headline") is None:
                passed = item.get("status") == "NOT_APPLICABLE" and item.get("source") == []
            else:
                source = item.get("source", [])
                template = item.get("template", [])
                passed = (
                    item.get("status") == "PASS"
                    and isinstance(source, list)
                    and bool(source)
                    and isinstance(template, list)
                    and all(value in template for value in source)
                    and item.get("missing_normalized_source_text", []) == []
                )
            if not passed:
                failures.append(f"{offer_id}:{field}")
    checks = {
        "editable_type_layers_present": isinstance(editable.get("type_layers"), int) and editable["type_layers"] > 0,
        "layer_count_covers_text": isinstance(editable.get("all_layers"), int) and editable.get("all_layers", 0) >= editable.get("type_layers", 1),
        "comparison_offer_scope": not duplicate and set(by_offer) == set(offers_by_id),
        "all_required_texts_match": not failures,
    }
    return all(checks.values()), {"checks": checks, "failures": failures}


def check_anchors(report: dict[str, Any], offers_by_id: dict[str, dict[str, Any]]) -> tuple[bool, list[str]]:
    rows = report.get("anchors_and_visibility", [])
    by_offer: dict[str, dict[str, Any]] = {}
    duplicate = False
    for row in rows if isinstance(rows, list) else []:
        offer_id = row.get("offer_id")
        if not offer_id or offer_id in by_offer:
            duplicate = True
        else:
            by_offer[offer_id] = row
    failures = []
    for offer_id, offer in offers_by_id.items():
        row = by_offer.get(offer_id, {})
        if not (
            row.get("state_group_count") == 1
            and row.get("anchor_name") == offer.get("anchor_name")
            and row.get("anchor_name_found") is True
            and row.get("source_anchor_id") == offer.get("anchor_id")
            and row.get("car_components_source_ids", []) == offer.get("car_components", [])
        ):
            failures.append(offer_id)
    passed = not duplicate and set(by_offer) == set(offers_by_id) and not failures
    return passed, failures


def check_tags(report: dict[str, Any], offers_by_id: dict[str, dict[str, Any]]) -> tuple[bool, dict[str, Any]]:
    tags = report.get("embedded_car_tags", {})
    expected_tag_states = {offer_id for offer_id, offer in offers_by_id.items() if offer.get("car_tag_names")}
    expected_new_states = {
        offer_id
        for offer_id, offer in offers_by_id.items()
        if "New" in (offer.get("car_tag_names") or [])
    }
    new_rows = tags.get("new_found", [])
    song_rows = tags.get("song_pro_found", [])
    found_new_states = {row.get("state") for row in new_rows if row.get("root") == "CONDICIONAIS" and row.get("visible") is True}
    song_words = {
        " ".join(canon_text(str(row.get("text", ""))).split())
        for row in song_rows
        if row.get("state") == "song-pro" and row.get("root") == "CONDICIONAIS" and row.get("visible") is True
    }
    checks = {
        "source_tag_scope": set(tags.get("expected_tag_states", [])) == expected_tag_states,
        "source_new_scope": set(tags.get("new_expected_states", [])) == expected_new_states,
        "new_tags_in_conditionals": found_new_states == expected_new_states and len(new_rows) == len(expected_new_states),
        "song_pro_words_in_conditionals": song_words == {"ultimas", "unidades"} and len(song_rows) == 2,
        "no_vehicle_tag_leaks": tags.get("car_tag_leaks") == [],
        "qa_status_pass": tags.get("status") == "PASS",
    }
    return all(checks.values()), checks


def check_bg_uuids(report: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    item = report.get("bg_smart_object_uuids", {})
    records = item.get("records", [])
    uuids = [record.get("uuid") for record in records if record.get("uuid")]
    checks = {
        "qa_status_pass": item.get("status") == "PASS",
        "one_unique_uuid": item.get("unique_uuid_count") == 1 and len(item.get("unique_uuids", [])) == 1,
        "twenty_bg_smart_objects": isinstance(records, list) and len(records) == 20,
        "all_records_decoded": len(uuids) == 20 and not any(record.get("error") for record in records),
        "records_share_uuid": len(set(uuids)) == 1,
    }
    return all(checks.values()), checks


def check_layer_comp_decoder(report: dict[str, Any], native_pass: bool) -> tuple[bool, dict[str, Any]]:
    item = report.get("layer_comps", {})
    status = item.get("status")
    decoded_pass = status == "PASS" and item.get("count") == 20
    unavailable_with_native = status == "UNAVAILABLE" and native_pass
    checks = {
        "native_40_tests_for_format": native_pass,
        "decoder_pass_20_or_unavailable": decoded_pass or unavailable_with_native,
        "decoder_not_fail": status != "FAIL",
    }
    return all(checks.values()), {"decoder_status": status, "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    if args.revision != "r18":
        parser.error("This frozen summarizer accepts only --revision r18")

    qa_path = V4 / "WORK/04_QA/qa_templates_r18_v2.json"
    spec_path = V4 / "WORK/00_MATRIZ/production_spec_r18.json"
    manifest_path = V4 / "WORK/04_QA/production-r18/templates_manifest_r18.json"
    output_path = V4 / "WORK/04_QA/production-r18/structural7.json"
    r17_log = V4 / "WORK/06_LOGS/recapture_templates_r17.log"
    r20_log = V4 / "WORK/06_LOGS/recapture_templates_r20.log"
    if output_path.exists() and REFUSE_OVERWRITE:
        raise FileExistsError(f"REFUSE_OVERWRITE|{output_path.relative_to(ROOT)}")

    qa = read_json(qa_path)
    spec = read_json(spec_path)
    manifest = read_json(manifest_path)
    offers_by_id = {offer["id"]: offer for offer in spec.get("offers", [])}
    formats_by_id = {fmt["id"]: fmt for fmt in spec.get("formats", [])}
    expected_formats = set(formats_by_id)
    expected_offer_ids = set(offers_by_id)
    if len(offers_by_id) != 20 or len(formats_by_id) != 7:
        raise RuntimeError("INVALID_R18_SPEC_SCOPE")

    native = native_layer_comp_evidence(spec, r17_log, r20_log)
    manifest_by_format, manifest_checks = manifest_index(manifest)
    qa_rows = qa.get("templates", [])
    qa_by_format: dict[str, dict[str, Any]] = {}
    qa_duplicates = False
    for report in qa_rows if isinstance(qa_rows, list) else []:
        fmt = format_from_template_path(str(report.get("path", "")))
        if not fmt or fmt in qa_by_format:
            qa_duplicates = True
            continue
        qa_by_format[fmt] = report

    global_checks = {
        "spec_revision_r18": spec.get("revision") == "r18",
        "spec_native_checks_closed": spec.get("native_template_status") == "NATIVE_CHECKS_CLOSED",
        "spec_template_directory_r17": spec.get("output_templates") == "WORK/01_TEMPLATES/2026-09-20-r17/",
        "qa_schema": qa.get("schema") == "byd-v4-template-structural-qa/v1",
        "qa_revision_r18": qa.get("revision") == "r18",
        "qa_expected_templates_7": qa.get("expected_templates") == 7,
        "qa_rows_7_unique": isinstance(qa_rows, list) and len(qa_rows) == 7 and not qa_duplicates and len(qa_by_format) == 7,
        "qa_format_scope": set(qa_by_format) == expected_formats,
        "qa_expected_dimensions": qa.get("expected_dimensions") == {
            fmt_id: [fmt["w"], fmt["h"]] for fmt_id, fmt in formats_by_id.items()
        },
        "qa_observed_dimensions_once_each": qa.get("observed_dimensions") == {
            fmt_id: 1 for fmt_id in expected_formats
        },
        "qa_source_spec_r18": qa.get("source_spec") == str(spec_path.relative_to(ROOT)),
        "qa_source_inventory": qa.get("source_inventory") == "Projects/BYD/Jobs/V4/WORK/00_MATRIZ/inventario_psd_estrutural_v2.json",
        "manifest_scope": all(manifest_checks.values()) and set(manifest_by_format) == expected_formats,
        "native_layer_comp_tests_280": native.get("status") == "PASS" and native.get("tests") == 280,
    }

    rows = []
    for fmt_id in [fmt["id"] for fmt in spec["formats"]]:
        report = qa_by_format.get(fmt_id, {})
        manifest_row = manifest_by_format.get(fmt_id, {})
        fmt = formats_by_id[fmt_id]
        qa_file = ROOT / str(report.get("path", "__missing__"))
        manifest_file = V4 / str(manifest_row.get("file", "__missing__"))
        same_path = qa_file.resolve() == manifest_file.resolve()
        actual_exists = qa_file.is_file() and manifest_file.is_file() and same_path
        actual_hash = sha256(qa_file) if actual_exists else None
        expected_canvas = [fmt["w"], fmt["h"]]
        text_pass, text_detail = check_texts(report, offers_by_id)
        anchors_pass, anchor_failures = check_anchors(report, offers_by_id)
        tags_pass, tag_checks = check_tags(report, offers_by_id)
        bg_pass, bg_checks = check_bg_uuids(report)
        native_format = native.get("formats", {}).get(fmt_id, {})
        comps_pass, comps_detail = check_layer_comp_decoder(report, native_format.get("status") == "PASS")
        checks = {
            "global_scope": all(global_checks.values()),
            "roots_7": check_roots(report),
            "five_state_roots_20_each": check_states(report),
            "dimensions": report.get("canvas") == expected_canvas,
            "editable_texts_and_source_comparison": text_pass,
            "anchors_20": anchors_pass,
            "embedded_tags": tags_pass,
            "bg_uuid_reuse_20": bg_pass,
            "layer_comps_native_and_decoder": comps_pass,
            "manifest_path_match": same_path,
            "manifest_hash_match": bool(actual_hash) and actual_hash == report.get("sha256") == manifest_row.get("sha256"),
            "manifest_bytes_match": actual_exists and qa_file.stat().st_size == report.get("bytes") == manifest_row.get("bytes"),
        }
        passed = all(checks.values())
        rows.append({
            "format": fmt_id,
            "file": manifest_row.get("file"),
            "sha256": actual_hash,
            "checks": checks,
            "details": {
                "text": text_detail,
                "anchor_failures": anchor_failures,
                "tags": tag_checks,
                "bg_uuids": bg_checks,
                "layer_comps": comps_detail,
                "native_layer_comp_evidence": native_format,
            },
            "structural_pass": passed,
        })

    pass_count = sum(1 for row in rows if row["structural_pass"])
    overall_pass = pass_count == 7 and len(rows) == 7 and all(global_checks.values())
    result = {
        "schema": "byd-v4-structural-summary-r18/v1",
        "revision": "r18",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "write_guard": "REFUSE_OVERWRITE",
        "method": "Strict summary of psd-tools structural QA, current template SHA-256, template manifest, and 280 native Photoshop Layer Comp apply tests.",
        "source_structural_qa": str(qa_path.relative_to(V4)),
        "status": "PASS" if overall_pass else "FAIL",
        "pass": pass_count if overall_pass else min(pass_count, 6),
        "fail": 0 if overall_pass else 7 - min(pass_count, 6),
        "rows": rows,
        "global_checks": global_checks,
        "manifest_checks": manifest_checks,
        "native_layer_comps": native,
        "layer_comp_decoder_policy": "PASS with count 20, or UNAVAILABLE only when the format has 40 successful native apply tests. FAIL is never accepted.",
        "human_approval": "NOT_ASSERTED",
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not overall_pass:
        print(f"ERRO|STRUCTURAL_R18|pass={result['pass']}|rows=7|report={output_path.relative_to(ROOT)}", file=sys.stderr)
        return 2
    print(f"OK|STRUCTURAL_R18|pass=7|native_apply_tests=280|report={output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERRO|summarize_structural_r18|{type(exc).__name__}|{exc}", file=sys.stderr)
        raise
