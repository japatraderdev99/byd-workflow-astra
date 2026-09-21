#!/usr/bin/env python3
"""Read-only structural QA for the seven r01 template PSDs.

Do not run while Photoshop is producing files. The explicit acknowledgement
flag is intentional: psd-tools opens very large PSDs and can compete for RAM.
The script never changes a PSD. Its sole write is a new JSON report guarded by
REFUSE_OVERWRITE.

Usage after the operator has closed every Photoshop document and released lock:
  python3 WORK/05_SCRIPTS/qa_templates_r01.py --revision r11 --after-photoshop-finish
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from psd_tools import PSDImage


REFUSE_OVERWRITE = True
EXPECTED_ROOTS = ("BG", "VEICULO", "LEGAL", "CONDICIONAIS", "OFERTA", "FIXO", "#GUIAS")
TEXT_CONTAINERS = {
    "title": "OFERTA",
    "price": "OFERTA",
    "legal": "LEGAL",
    "benefit": "CONDICIONAIS",
    "headline": "CONDICIONAIS",
}
EXPECTED_NEW_OFFERS = {"atto-2", "sealion-26-27", "song-pro-flex"}
EXPECTED_EMBEDDED_TAG_OFFERS = EXPECTED_NEW_OFFERS | {"song-pro"}


def find_root(start: Path) -> Path:
    """Resolve workspace root from .mkroot without embedding an absolute path."""
    for candidate in (start, *start.parents):
        if (candidate / ".mkroot").exists():
            return candidate
    raise RuntimeError("Could not resolve workspace root (.mkroot not found).")


ROOT = find_root(Path(__file__).resolve())
V4 = ROOT / "Projects/BYD/Jobs/V4"
SOURCE_INVENTORY_PATH = V4 / "WORK/00_MATRIZ/inventario_psd_estrutural_v2.json"


def canon(value: str | None) -> str:
    # Structural names may contain Portuguese accents. Keep text comparison
    # separate in norm_text() so this does not change source-content evidence.
    ascii_value = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()).strip("-")


def norm_text(value: str | None) -> str:
    return " ".join((value or "").replace("\r", " ").replace("\n", " ").split())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_group(layer: Any) -> bool:
    try:
        return bool(layer.is_group())
    except (AttributeError, TypeError):
        return False


def walk(layers: Iterable[Any]) -> Iterable[Any]:
    for layer in layers:
        yield layer
        if is_group(layer):
            yield from walk(layer)


def parent_chain(layer: Any) -> list[Any]:
    chain: list[Any] = []
    current = getattr(layer, "parent", None)
    while current is not None and getattr(current, "name", None) is not None:
        chain.append(current)
        current = getattr(current, "parent", None)
    return chain


def effectively_visible(layer: Any) -> bool:
    if not bool(getattr(layer, "visible", False)):
        return False
    return all(bool(getattr(parent, "visible", True)) for parent in parent_chain(layer))


def direct_child_groups(group: Any) -> list[Any]:
    return [child for child in group if is_group(child)]


def top_groups(psd: PSDImage) -> dict[str, list[Any]]:
    found: dict[str, list[Any]] = defaultdict(list)
    expected_by_canon = {canon(name): name for name in EXPECTED_ROOTS}
    for layer in psd:
        if is_group(layer) and canon(layer.name) in expected_by_canon:
            found[expected_by_canon[canon(layer.name)]].append(layer)
    return found


def state_groups(container: Any, offer_ids: set[str]) -> dict[str, list[Any]]:
    found: dict[str, list[Any]] = defaultdict(list)
    for child in direct_child_groups(container):
        key = canon(child.name)
        if key in offer_ids:
            found[key].append(child)
    return found


def texts_under(layer: Any) -> list[str]:
    values = []
    for node in walk([layer]):
        if getattr(node, "kind", None) == "type":
            value = norm_text(getattr(node, "text", ""))
            if value:
                values.append(value)
    return values


def source_texts(inventory: dict[str, Any], offer: dict[str, Any]) -> dict[str, list[str]]:
    """Return canonical source content by source layer IDs in the production spec."""
    layers = inventory["layers"]
    by_id = {layer["layer_id"]: layer for layer in layers}

    def one(layer_id: int | None) -> list[str]:
        layer = by_id.get(layer_id)
        text = norm_text(layer.get("text", "")) if layer else ""
        return [text] if text else []

    result = {field: one(offer.get(field)) for field in ("title", "legal", "benefit", "headline")}
    price = by_id.get(offer["price"])
    if price:
        prefix = price["path"] + " / "
        result["price"] = [
            norm_text(layer.get("text", ""))
            for layer in layers
            if layer.get("kind") == "type" and layer.get("path", "").startswith(prefix) and norm_text(layer.get("text", ""))
        ]
    else:
        result["price"] = []
    return result


def find_state_texts(root_groups: dict[str, list[Any]], offer_id: str) -> dict[str, list[str]]:
    answer: dict[str, list[str]] = {}
    for field, root_name in TEXT_CONTAINERS.items():
        roots = root_groups.get(root_name, [])
        candidates = state_groups(roots[0], {offer_id}).get(offer_id, []) if len(roots) == 1 else []
        answer[field] = texts_under(candidates[0]) if len(candidates) == 1 else []
    return answer


def compare_main_text(spec: dict[str, Any], inventory: dict[str, Any], roots: dict[str, list[Any]]) -> list[dict[str, Any]]:
    results = []
    for offer in spec["offers"]:
        expected = source_texts(inventory, offer)
        actual = find_state_texts(roots, offer["id"])
        fields: dict[str, Any] = {}
        for field, source_values in expected.items():
            if field == "headline" and offer.get("headline") is None:
                fields[field] = {"status": "NOT_APPLICABLE", "source": [], "template": actual[field]}
                continue
            missing = [value for value in source_values if value not in actual[field]]
            fields[field] = {
                "status": "PASS" if source_values and not missing else "FAIL",
                "source": source_values,
                "template": actual[field],
                "missing_normalized_source_text": missing,
            }
        results.append({"offer_id": offer["id"], "fields": fields})
    return results


def nearest_offer(layer: Any, offer_ids: set[str]) -> str | None:
    for parent in [layer, *parent_chain(layer)]:
        candidate = canon(getattr(parent, "name", ""))
        if candidate in offer_ids:
            return candidate
        # State groups have precisely these prefixes. Do not use suffix
        # matching: retail and VD offer IDs could otherwise be conflated.
        for prefix in ("cond-", "car-"):
            if candidate.startswith(prefix):
                state_id = candidate[len(prefix):]
                if state_id in offer_ids:
                    return state_id
    return None


def nearest_root(layer: Any) -> str | None:
    names = {canon(name): name for name in EXPECTED_ROOTS}
    for parent in [layer, *parent_chain(layer)]:
        candidate = canon(getattr(parent, "name", ""))
        if candidate in names:
            return names[candidate]
    return None


def smart_object_uuid_report(psd: PSDImage, roots: dict[str, list[Any]]) -> dict[str, Any]:
    bg_roots = roots.get("BG", [])
    if len(bg_roots) != 1:
        return {"status": "FAIL", "reason": "Expected one BG root group.", "unique_uuids": []}
    records = []
    for node in walk([bg_roots[0]]):
        if getattr(node, "kind", None) != "smartobject":
            continue
        try:
            smart = node.smart_object
            records.append({"layer_id": node.layer_id, "name": node.name, "uuid": smart.unique_id, "filesize": smart.filesize})
        except Exception as exc:  # psd-tools can leave a malformed SO unreadable.
            records.append({"layer_id": getattr(node, "layer_id", None), "name": node.name, "error": type(exc).__name__})
    unique = sorted({record["uuid"] for record in records if record.get("uuid")})
    return {
        "status": "PASS" if len(unique) == 1 else "FAIL",
        "expected_unique_uuids": 1,
        "unique_uuid_count": len(unique),
        "unique_uuids": unique,
        "records": records,
    }


def layer_comp_report(psd: PSDImage) -> dict[str, Any]:
    """Report Layer Comp availability without claiming decoder support psd-tools lacks."""
    try:
        blocks = psd.tagged_blocks
    except Exception as exc:
        return {"status": "UNAVAILABLE", "reason": f"tagged_blocks unavailable: {type(exc).__name__}"}
    candidates = [(str(key), block) for key, block in blocks.items() if "comp" in str(key).lower()]
    if not candidates:
        return {"status": "UNAVAILABLE", "reason": "No Layer Comp tagged block exposed by psd-tools."}
    decoded_counts = []
    for key, block in candidates:
        count = None
        for attribute in ("layer_comps", "comps"):
            value = getattr(block, attribute, None)
            if isinstance(value, (list, tuple)):
                count = len(value)
                break
        if isinstance(block, (list, tuple)):
            count = len(block)
        decoded_counts.append({"key": key, "count": count})
    counts = [entry["count"] for entry in decoded_counts if isinstance(entry["count"], int)]
    if len(counts) == 1:
        return {"status": "PASS" if counts[0] == 20 else "FAIL", "expected": 20, "count": counts[0], "blocks": decoded_counts}
    return {"status": "UNAVAILABLE", "reason": "Layer Comp block is raw/undecoded in psd-tools.", "blocks": decoded_counts}


def embedded_tag_report(psd: PSDImage, spec: dict[str, Any]) -> dict[str, Any]:
    offer_ids = {offer["id"] for offer in spec["offers"]}
    visible_new = []
    visible_song_pro_words = []
    car_leaks = []
    for node in walk(psd):
        if getattr(node, "kind", None) != "type":
            continue
        text = canon(norm_text(getattr(node, "text", "")))
        state = nearest_offer(node, offer_ids)
        root = nearest_root(node)
        record = {"layer_id": node.layer_id, "text": norm_text(getattr(node, "text", "")), "state": state, "root": root, "visible": bool(getattr(node, "visible", False)), "effectively_visible": effectively_visible(node)}
        if text == "new":
            if root == "VEICULO" and bool(getattr(node, "visible", False)):
                car_leaks.append(record)
            if root == "CONDICIONAIS" and bool(getattr(node, "visible", False)):
                visible_new.append(record)
        if state == "song-pro" and text in {"ultimas", "unidades"}:
            if root == "VEICULO" and bool(getattr(node, "visible", False)):
                car_leaks.append(record)
            if root == "CONDICIONAIS" and bool(getattr(node, "visible", False)):
                visible_song_pro_words.append(record)
    new_states = {record["state"] for record in visible_new}
    song_pro_words = {canon(record["text"]) for record in visible_song_pro_words}
    return {
        "expected_tag_states": sorted(EXPECTED_EMBEDDED_TAG_OFFERS),
        "new_expected_states": sorted(EXPECTED_NEW_OFFERS),
        "new_found": visible_new,
        "song_pro_found": visible_song_pro_words,
        "car_tag_leaks": car_leaks,
        "status": "PASS" if new_states == EXPECTED_NEW_OFFERS and song_pro_words == {"ultimas", "unidades"} and not car_leaks else "FAIL",
    }


def anchor_report(psd: PSDImage, roots: dict[str, list[Any]], spec: dict[str, Any]) -> list[dict[str, Any]]:
    vehicle_roots = roots.get("VEICULO", [])
    report = []
    for offer in spec["offers"]:
        groups = state_groups(vehicle_roots[0], {offer["id"]}).get(offer["id"], []) if len(vehicle_roots) == 1 else []
        names = [node.name for node in walk(groups)] if len(groups) == 1 else []
        expected_names = [offer["anchor_name"]]
        for component in offer.get("car_components", []):
            # The native r01 finding proves IDs but template IDs can be regenerated;
            # component IDs are retained as evidence in this report, not compared to new IDs.
            expected_names.append(str(component))
        report.append({
            "offer_id": offer["id"],
            "state_group_count": len(groups),
            "anchor_name": offer["anchor_name"],
            "anchor_name_found": offer["anchor_name"] in names,
            "source_anchor_id": offer["anchor_id"],
            "car_components_source_ids": offer.get("car_components", []),
            "state_group_visible": bool(getattr(groups[0], "visible", False)) if len(groups) == 1 else None,
        })
    return report


def inspect_template(path: Path, spec: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    psd = PSDImage.open(path)
    roots = top_groups(psd)
    offer_ids = {offer["id"] for offer in spec["offers"]}
    root_check = {name: {"count": len(roots.get(name, [])), "status": "PASS" if len(roots.get(name, [])) == 1 else "FAIL"} for name in EXPECTED_ROOTS}
    states = {}
    for root_name in ("BG", "VEICULO", "LEGAL", "CONDICIONAIS", "OFERTA"):
        groups = state_groups(roots[root_name][0], offer_ids) if len(roots.get(root_name, [])) == 1 else {}
        missing = sorted(offer_ids - set(groups))
        duplicates = sorted(key for key, value in groups.items() if len(value) != 1)
        states[root_name] = {"count": sum(len(value) for value in groups.values()), "missing": missing, "duplicates": duplicates, "status": "PASS" if not missing and not duplicates else "FAIL"}
    all_nodes = list(walk(psd))
    type_layers = [node for node in all_nodes if getattr(node, "kind", None) == "type"]
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "canvas": [psd.width, psd.height],
        "root_groups": root_check,
        "state_groups": states,
        "text_editable_counts": {"type_layers": len(type_layers), "all_layers": len(all_nodes)},
        "main_text_comparison": compare_main_text(spec, inventory, roots),
        "bg_smart_object_uuids": smart_object_uuid_report(psd, roots),
        "layer_comps": layer_comp_report(psd),
        "embedded_car_tags": embedded_tag_report(psd, spec),
        "anchors_and_visibility": anchor_report(psd, roots, spec),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default="r11", help="Production revision whose production_spec_<revision>.json must be read (default: r11).")
    parser.add_argument("--after-photoshop-finish", action="store_true", help="Required acknowledgement that Photoshop production is finished.")
    parser.add_argument("--templates-dir", type=Path, help="Optional override for the seven PSD templates; default comes from the selected spec.")
    parser.add_argument("--output", type=Path, help="Optional new JSON report path; default is WORK/04_QA/qa_templates_<revision>.json.")
    args = parser.parse_args()
    if not args.after_photoshop_finish:
        parser.error("Refusing to inspect PSDs during production. Re-run only after Photoshop finishes with --after-photoshop-finish.")
    if not re.fullmatch(r"[a-z0-9]+", args.revision):
        parser.error("revision must contain only lowercase letters and digits")
    spec_path = V4 / f"WORK/00_MATRIZ/production_spec_{args.revision}.json"
    if not spec_path.is_file():
        raise FileNotFoundError(f"Missing selected production spec: {spec_path.relative_to(ROOT)}")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    default_templates_dir = V4 / spec["output_templates"]
    default_output = V4 / f"WORK/04_QA/qa_templates_{args.revision}.json"
    templates_dir = args.templates_dir or default_templates_dir
    templates_dir = templates_dir if templates_dir.is_absolute() else V4 / templates_dir
    output = args.output or default_output
    output = output if output.is_absolute() else V4 / output
    if output.exists() and REFUSE_OVERWRITE:
        raise FileExistsError(f"REFUSE_OVERWRITE: {output.relative_to(ROOT)} already exists")
    inventory = json.loads(SOURCE_INVENTORY_PATH.read_text(encoding="utf-8"))
    expected_dimensions = {(item["w"], item["h"]): item["id"] for item in spec["formats"]}
    psds = sorted(templates_dir.glob("*.psd"))
    if len(psds) != 7:
        raise RuntimeError(f"Expected exactly 7 PSDs in {templates_dir.relative_to(ROOT)}, found {len(psds)}")
    reports = []
    for path in psds:
        reports.append(inspect_template(path, spec, inventory))
        # psd-tools can retain object cycles for large PSDs; release between
        # templates so the final seven-file QA does not accumulate memory.
        gc.collect()
    observed_dimensions = Counter(tuple(report["canvas"]) for report in reports)
    report = {
        "schema": "byd-v4-template-structural-qa/v1",
        "write_guard": "REFUSE_OVERWRITE",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "method": "psd-tools read-only structural inspection; no render and no human visual approval.",
        "revision": args.revision,
        "source_spec": str(spec_path.relative_to(ROOT)),
        "source_inventory": str(SOURCE_INVENTORY_PATH.relative_to(ROOT)),
        "expected_templates": 7,
        "expected_dimensions": {name: list(dim) for dim, name in expected_dimensions.items()},
        "observed_dimensions": {f"{w}x{h}": count for (w, h), count in observed_dimensions.items()},
        "templates": reports,
        "human_approval": "NOT_ASSERTED",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK|qa_templates_r01|templates={len(reports)}|report={output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERRO|qa_templates_r01|{type(exc).__name__}|{exc}", file=sys.stderr)
        raise
