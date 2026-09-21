#!/usr/bin/env python3
"""Build an F0 candidate matrix from the saved psd-tools tree and Photoshop geometry TSV.

This script does not open INPUT or Photoshop. It preserves raw PSD visibility and
derives effective visibility from ancestors for the builder to make an explicit choice.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

from mkroot import ROOT

REFUSE_OVERWRITE = True
JOB = ROOT / "Projects" / "BYD" / "Jobs" / "V4"
MATRIX = JOB / "WORK" / "00_MATRIZ"
LOGS = JOB / "WORK" / "06_LOGS"
TREE = MATRIX / "inventario_psd_estrutural_v2.json"
GEOMETRY = MATRIX / "geometria_photoshop.tsv"
OUT = MATRIX / "matriz_candidatos_estrutural.json"
LOG = LOGS / "mapear_ofertas_estrutural.log"

OFFER_GROUPS = {
    "atto-2": ["ATTO 2"], "atto-8": ["ATTO 8"], "dolphin-gs": ["DOLPHIN GS"],
    "dolphin-mini-5l-gs": ["DOLPHIN MINI 5L GS"], "dolphin-se": ["DOLPHIN SE"],
    "king-gs": ["KING GS 2627"], "seal-26-27": ["SEAL"], "sealion-26-27": ["SEALION"],
    "song-plus": ["SONG PLUS 1.5"], "song-premium": ["SONG PREMIUM"],
    "song-pro-flex": ["SONG PRO GS FLEX 2627"], "song-pro": ["SONG PRO GS 2627"],
    "vd-atto-2": ["VD - ATTO 2"], "vd-dolphin-mini": ["VD - DOLPHIN"],
    "vd-king-gl": ["VD - KING"], "vd-shark": ["PR - SHARK", "SHARK"],
    "vd-song-pro-flex": ["VD - SONG PRO FLEX"], "vd-song-pro": ["VD - SONG PRO"],
    "yuan-plus-awd-26-27": ["YUAN PLUS AWD"], "yuan-pro": ["YUAN PRO"],
}


def timestamp() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def norm(value: str) -> str:
    return " ".join(value.upper().split())


def parse_geometry() -> dict[int, dict]:
    records: dict[int, dict] = {}
    for line in GEOMETRY.read_text(encoding="utf-8", errors="replace").splitlines():
        fields = line.split("\t")
        if len(fields) < 8 or not fields[1].isdigit():
            continue
        record = {"photoshop_path": fields[0], "layer_id": int(fields[1]), "photoshop_kind": fields[2],
                  "photoshop_visible_raw": fields[3].lower() == "true",
                  "bbox_photoshop": {"left": int(fields[4]), "top": int(fields[5]),
                                     "right": int(fields[6]), "bottom": int(fields[7])}}
        if len(fields) > 8:
            record["font_live"] = fields[8]
        if len(fields) > 9:
            record["text_live"] = "\t".join(fields[9:])
        records[record["layer_id"]] = record
    return records


def merge(node: dict, geom: dict[int, dict], effective: bool) -> dict:
    result = {key: node.get(key) for key in ("layer_id", "name", "kind", "path", "text", "bbox_structural") if key in node}
    result["visible_raw_psd"] = node["visible"]
    result["visible_effective_from_raw_ancestors"] = effective
    if node["layer_id"] in geom:
        result["photoshop"] = geom[node["layer_id"]]
    return result


def descendants(nodes: list[dict], root: dict) -> list[dict]:
    prefix = root["path"] + " / "
    return [node for node in nodes if node["path"].startswith(prefix)]


def named_groups(items: list[dict], name: str) -> list[dict]:
    target = norm(name)
    return [node for node in items if node["kind"] in {"group", "artboard"} and norm(node["name"]) == target]


def parent_path(node: dict) -> str:
    return " / ".join(node["path"].split(" / ")[:-1])


def main() -> int:
    started = timestamp()
    tick = time.monotonic()
    if REFUSE_OVERWRITE and (OUT.exists() or LOG.exists()):
        print("ERRO|REFUSE_OVERWRITE|matriz_candidatos_estrutural.json or mapear_ofertas_estrutural.log")
        return 2
    tree = json.loads(TREE.read_text(encoding="utf-8"))
    nodes = tree["layers"]
    geom = parse_geometry()
    by_path = {node["path"]: node for node in nodes}

    def effective(node: dict) -> bool:
        parts = node["path"].split(" / ")
        return all(by_path.get(" / ".join(parts[:length]), {"visible": False})["visible"] for length in range(1, len(parts) + 1))

    roots = [node for node in nodes if node["depth"] == 1]
    roots_by_name: dict[str, list[dict]] = {}
    for root in roots:
        roots_by_name.setdefault(norm(root["name"]), []).append(root)

    offers = []
    unresolved = []
    for offer_id, candidates in OFFER_GROUPS.items():
        candidate_roots = [root for group_name in candidates for root in roots_by_name.get(norm(group_name), [])]
        candidate_records = []
        for root in candidate_roots:
            inside = descendants(nodes, root)
            offer_group = named_groups(inside, "OFERTA")
            price_groups = [node for node in inside if node["kind"] == "group" and "PREÇO" in norm(node["name"])]
            legal_groups = named_groups(inside, "TEXTO LEGAL")
            car_groups = [node for node in inside if node["kind"] == "group" and norm(node["name"]) in {"CARRO", "DOLPHIN MINI"}]
            title_nodes = [node for node in inside if node["kind"] == "type" and parent_path(node) in {entry["path"] for entry in offer_group}]
            price_nodes = [node for node in inside if node["kind"] == "type" and any(node["path"].startswith(group["path"] + " / ") for group in price_groups)]
            legal_nodes = [node for node in inside if node["kind"] == "type" and any(node["path"].startswith(group["path"] + " / ") for group in legal_groups)]
            car_candidates = [node for node in inside if node["kind"] in {"pixel", "smartobject"} and any(node["path"].startswith(group["path"] + " / ") for group in car_groups)]
            core_paths = {node["path"] for node in title_nodes + price_nodes + legal_nodes}
            other_text = [node for node in inside if node["kind"] == "type" and node["path"] not in core_paths]
            conditional = [node for node in other_text if any(token in norm((node["name"] + " " + node.get("text", ""))) for token in ("EXCLUSIVO", "CARREGADOR", "SELO", "NEW", "ÚLTIMAS"))]
            benefit_or_headline = [node for node in other_text if node not in conditional]
            candidate_records.append({
                "source_group": merge(root, geom, effective(root)),
                "roles": {
                    "offer_group_candidates": [merge(node, geom, effective(node)) for node in offer_group],
                    "title_text_candidates": [merge(node, geom, effective(node)) for node in title_nodes],
                    "price_group_candidates": [merge(node, geom, effective(node)) for node in price_groups],
                    "price_text_candidates": [merge(node, geom, effective(node)) for node in price_nodes],
                    "legal_group_candidates": [merge(node, geom, effective(node)) for node in legal_groups],
                    "legal_text_candidates": [merge(node, geom, effective(node)) for node in legal_nodes],
                    "car_group_candidates": [merge(node, geom, effective(node)) for node in car_groups],
                    "car_cutout_candidates": [merge(node, geom, effective(node)) for node in car_candidates],
                    "benefit_or_headline_candidates": [merge(node, geom, effective(node)) for node in benefit_or_headline],
                    "conditional_badge_candidates": [merge(node, geom, effective(node)) for node in conditional],
                },
            })
        state = "CANDIDATE_REQUIRES_REFERENCE_VALIDATION"
        if offer_id == "vd-shark":
            state = "AMBIGUOUS_TWO_PSD_GROUPS_REQUIRES_REFERENCE_VALIDATION"
            unresolved.append({"offer_id": offer_id, "reason": "Brief calls it vd-shark, but PSD candidates are PR - SHARK (Producer Rural, R$299.990) and SHARK (R$344.990); choose only against approved reference."})
        if not candidate_records:
            state = "MISSING_PSD_GROUP"
            unresolved.append({"offer_id": offer_id, "reason": "No top-level PSD group matched the candidate mapping."})
        offers.append({"offer_id": offer_id, "status": state, "source_group_candidates": candidate_records})
    payload = {
        "schema": "byd-v4-offer-candidate-matrix/v1",
        "created_at": timestamp(),
        "model_requested": "gpt-5.6-terra/high",
        "model_observed_runtime": "gpt-6-astra / inherited-default (not a measurement of requested Terra)",
        "sources": {"structural_tree": "inventario_psd_estrutural_v2.json", "geometry": "geometria_photoshop.tsv"},
        "visibility_rule": "visible_raw_psd is the stored flag. visible_effective_from_raw_ancestors is the AND of that flag and every ancestor flag; child=true under a hidden offer root is therefore effectively false.",
        "status_rule": "Every association is a candidate until cross-checked against the approved feed reference; no source group is activated by this file.",
        "excluded_psd_group": {"layer_id": 209, "name": "YUAN PLUS (desconsiderar)", "reason": "PSD layer name explicitly says desconsiderar and it is outside the 20-offer scope."},
        "pilot_offers_requested": ["yuan-plus-awd-26-27", "dolphin-mini-5l-gs", "vd-atto-2"],
        "offers": offers,
        "unresolved": unresolved,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    LOG.write_text("\n".join([
        f"{started} | INICIO|mapear_ofertas_estrutural|modelo_solicitado=gpt-5.6-terra|esforco_solicitado=high|modelo_observado=gpt-6-astra|esforco_observado=herdado-padrao",
        f"{timestamp()} | OK|mapear_ofertas_estrutural|duracao_s={time.monotonic() - tick:.3f}|offers={len(offers)}|unresolved={len(unresolved)}|input_opened=false|photoshop_opened=false",
        "",
    ]), encoding="utf-8")
    print(f"OK|mapear_ofertas_estrutural|offers={len(offers)}|unresolved={len(unresolved)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
