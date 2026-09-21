#!/usr/bin/env python3
"""F0 cold inventory for BYD V4. Reads INPUT only and refuses overwrite."""

from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mkroot import ROOT
from psd_tools import PSDImage
import psd_tools


REFUSE_OVERWRITE = True
JOB = ROOT / "Projects" / "BYD" / "Jobs" / "V4"
INPUT = JOB / "INPUT"
MATRIX = JOB / "WORK" / "00_MATRIZ"
LOGS = JOB / "WORK" / "06_LOGS"
OUTPUTS = {
    "input": MATRIX / "input_baseline_observado_sha256_v2.json",
    "psd": MATRIX / "inventario_psd_estrutural_v2.json",
    "summary": MATRIX / "inventario_psd_v2.md",
    "log": LOGS / "intake_psd_tools_v2.log",
}


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def rel(path: Path) -> str:
    return path.relative_to(JOB).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def bbox(value: Any) -> dict[str, int] | None:
    if value is None:
        return None
    try:
        return {"left": value.x1, "top": value.y1, "right": value.x2, "bottom": value.y2,
                "width": value.width, "height": value.height}
    except (AttributeError, TypeError):
        return None


def scalar(value: Any) -> str | int | float | bool | None:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def descriptor_items(value: Any) -> list[tuple[Any, Any]]:
    """psd-tools EngineData dictionaries do not subclass collections.abc.Mapping."""
    try:
        return list(value.items())
    except (AttributeError, TypeError):
        return []


def descriptor_values_for_key(value: Any, key_wanted: str, *, depth: int = 0) -> list[Any]:
    if depth > 16:
        return []
    values: list[Any] = []
    items = descriptor_items(value)
    if items:
        for key, child in items:
            if str(scalar(key)) == key_wanted:
                values.append(child)
            values.extend(descriptor_values_for_key(child, key_wanted, depth=depth + 1))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for child in value:
            values.extend(descriptor_values_for_key(child, key_wanted, depth=depth + 1))
    return values


def fonts_for_type_layer(layer: Any) -> list[str]:
    """Resolve StyleRun Font indexes against the layer's ResourceDict FontSet."""
    try:
        font_set = getattr(layer, "resource_dict")["FontSet"]
        font_names = [str(scalar(entry["Name"])) for entry in font_set]
        indexes = descriptor_values_for_key(getattr(layer, "engine_dict"), "Font")
        return sorted({font_names[int(index)] for index in indexes if isinstance(index, int) and 0 <= index < len(font_names)})
    except (AttributeError, KeyError, TypeError, ValueError, IndexError):
        return []


def node_record(layer: Any, path: list[str], depth: int, counts: dict[str, int]) -> dict[str, Any]:
    layer_kind = str(getattr(layer, "kind", type(layer).__name__))
    counts[layer_kind] = counts.get(layer_kind, 0) + 1
    layer_name = str(getattr(layer, "name", ""))
    record: dict[str, Any] = {
        "path": " / ".join(path + [layer_name]),
        "depth": depth,
        "layer_id": getattr(layer, "layer_id", None),
        "name": layer_name,
        "kind": layer_kind,
        "class": type(layer).__name__,
        "visible": bool(getattr(layer, "visible", False)),
        "opacity": getattr(layer, "opacity", None),
        "blend_mode": str(getattr(layer, "blend_mode", "")),
        "clipping_layer": bool(getattr(layer, "clipping_layer", False)),
        "bbox_structural": bbox(getattr(layer, "bbox", None)),
    }
    if layer_kind == "type":
        record["text"] = str(getattr(layer, "text", ""))
        record["font_descriptor_values"] = fonts_for_type_layer(layer)
    return record


def walk_layers(layers: Any, path: list[str], depth: int, nodes: list[dict[str, Any]], counts: dict[str, int]) -> None:
    for layer in layers:
        record = node_record(layer, path, depth, counts)
        nodes.append(record)
        try:
            children = list(layer)
        except TypeError:
            children = []
        if children:
            walk_layers(children, path + [record["name"]], depth + 1, nodes, counts)


def main() -> int:
    started = now()
    timer = time.monotonic()
    existing = [path for path in OUTPUTS.values() if path.exists()]
    if REFUSE_OVERWRITE and existing:
        print("ERRO|REFUSE_OVERWRITE|" + ", ".join(rel(path) for path in existing))
        return 2
    MATRIX.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    files = sorted(path for path in INPUT.rglob("*") if path.is_file())
    input_records = [
        {"path": rel(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
        for path in files
    ]
    psd_paths = [path for path in files if path.suffix.lower() == ".psd"]
    if len(psd_paths) != 1:
        raise RuntimeError(f"Expected exactly one PSD in INPUT; found {len(psd_paths)}")

    psd_path = psd_paths[0]
    psd = PSDImage.open(psd_path)
    nodes: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    walk_layers(psd, [], 0, nodes, counts)
    text_nodes = [node for node in nodes if node["kind"] == "type"]
    top_level = [node for node in nodes if node["depth"] == 0]

    baseline = {
        "schema": "byd-v4-input-baseline-observado/v2",
        "observed_at": now(),
        "authority": "cold SHA-256 observation generated in WORK; INPUT/_INPUT_SHA256.json was absent at observation",
        "file_count": len(input_records),
        "files": input_records,
    }
    structure = {
        "schema": "byd-v4-psd-structural-inventory/v2",
        "observed_at": now(),
        "tool": {"name": "psd-tools", "version": getattr(psd_tools, "__version__", "unknown")},
        "method_limit": "Structural metadata only. No render was generated and this inventory is not visual authority.",
        "source": {"path": rel(psd_path), "sha256": sha256(psd_path), "bytes": psd_path.stat().st_size},
        "document": {
            "width": psd.width,
            "height": psd.height,
            "color_mode": str(getattr(psd, "color_mode", "")),
            "depth": getattr(psd, "depth", None),
            "bbox_structural": bbox(getattr(psd, "bbox", None)),
        },
        "counts": {"nodes_total": len(nodes), "text_layers": len(text_nodes), "by_kind": counts},
        "top_level_layers": top_level,
        "layers": nodes,
    }
    fonts = sorted({font for node in text_nodes for font in node.get("font_descriptor_values", [])})
    summary = "\n".join([
        "# Inventário estrutural do PSD — BYD V4",
        "",
        f"- Observado em: `{structure['observed_at']}`",
        f"- Fonte: `{structure['source']['path']}`",
        f"- SHA-256 PSD: `{structure['source']['sha256']}`",
        f"- Documento estrutural: `{psd.width}×{psd.height}`, modo `{structure['document']['color_mode']}`, profundidade `{structure['document']['depth']}`.",
        f"- Camadas/nós: `{len(nodes)}`; texto: `{len(text_nodes)}`; tipos: `{json.dumps(counts, ensure_ascii=False, sort_keys=True)}`.",
        f"- Arquivos inventariados no INPUT: `{len(input_records)}`. `INPUT/_INPUT_SHA256.json` não estava presente; `input_baseline_observado_sha256.json` é o baseline observado, não uma comparação com baseline do cliente.",
        "- Limite: psd-tools foi usado somente para estrutura; não houve renderização e a leitura não prova geometria ou aparência final.",
        "",
        "## Topo da árvore",
        "",
        *[f"- `{node['layer_id']}` · `{node['kind']}` · visível=`{node['visible']}` · {node['name']}" for node in top_level],
        "",
        "## Fontes indicadas em descritores de camadas de texto",
        "",
        *([f"- `{font}`" for font in fonts] if fonts else ["- Nenhuma cadeia de fonte foi exposta pelos descritores lidos; ver JSON por camada."]),
        "",
        "O detalhe por caminho, ID, tipo, visibilidade, bbox estrutural, texto e descritores de fonte está em `inventario_psd_estrutural_v2.json`.",
        "",
    ])
    log = "\n".join([
        f"{started} | INICIO|intake_psd_tools|modelo=gpt-6-astra|esforco=herdado-padrao",
        f"{now()} | OK|intake_psd_tools|duracao_s={time.monotonic() - timer:.3f}|input_files={len(input_records)}|psd_nodes={len(nodes)}|text_layers={len(text_nodes)}|psd_tools={getattr(psd_tools, '__version__', 'unknown')}",
        "",
    ])
    OUTPUTS["input"].write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUTS["psd"].write_text(json.dumps(structure, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    OUTPUTS["summary"].write_text(summary, encoding="utf-8")
    OUTPUTS["log"].write_text(log, encoding="utf-8")
    print(f"OK|intake_psd_tools|duration_s={time.monotonic() - timer:.3f}|input_files={len(input_records)}|psd_nodes={len(nodes)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERRO|intake_psd_tools|{error!r}")
        raise
