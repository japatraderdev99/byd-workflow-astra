#!/usr/bin/env python3
"""Read only text-engine descriptors from the source PSD; no render, no Photoshop."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

from mkroot import ROOT
from psd_tools import PSDImage
import psd_tools

REFUSE_OVERWRITE = True
JOB = ROOT / "Projects" / "BYD" / "Jobs" / "V4"
PSD_PATH = JOB / "INPUT" / "02_PSD_oficial todas as artes em feed" / "26.08.07 VAREJO BYD FEED 1080x1350.psd"
OUT = JOB / "WORK" / "00_MATRIZ" / "tipografia_psd_origem.json"
LOG = JOB / "WORK" / "06_LOGS" / "extrair_tipografia_psd.log"


def timestamp() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def key_name(value: object) -> str:
    return str(value).strip("'")


def items(value: object) -> list[tuple[object, object]]:
    try:
        return list(value.items())  # EngineData Dict
    except (AttributeError, TypeError):
        return []


def values_for_key(value: object, target: str, depth: int = 0) -> list[object]:
    if depth > 16:
        return []
    pairs = items(value)
    found: list[object] = []
    if pairs:
        for key, child in pairs:
            if key_name(key) == target:
                found.append(child)
            found.extend(values_for_key(child, target, depth + 1))
    elif not isinstance(value, (str, bytes)):
        try:
            for child in list(value):  # EngineData List
                found.extend(values_for_key(child, target, depth + 1))
        except TypeError:
            pass
    return found


def text_style(layer: object) -> dict:
    resource = layer.resource_dict
    font_names = [str(entry["Name"]) for entry in resource["FontSet"]]
    engine = layer.engine_dict
    indexes = [int(value) for value in values_for_key(engine, "Font")]
    fields = {name: [str(value) for value in values_for_key(engine, name)] for name in
              ("FontSize", "FauxBold", "FauxItalic", "HorizontalScale", "VerticalScale", "Tracking", "Leading")}
    return {"resource_dict_font_set": font_names,
            "style_run_font_indexes": indexes,
            "style_run_fonts_resolved": [font_names[index] for index in indexes if 0 <= index < len(font_names)],
            "style_fields": fields}


def visit(layers: object, path: list[str], rows: list[dict]) -> None:
    for layer in layers:
        name = str(layer.name)
        if str(getattr(layer, "kind", "")) == "type":
            rows.append({"layer_id": layer.layer_id, "path": " / ".join(path + [name]), "visible_raw_psd": bool(layer.visible),
                         "text": str(layer.text), **text_style(layer)})
        try:
            visit(list(layer), path + [name], rows)
        except TypeError:
            pass


def main() -> int:
    started = timestamp()
    tick = time.monotonic()
    if REFUSE_OVERWRITE and (OUT.exists() or LOG.exists()):
        print("ERRO|REFUSE_OVERWRITE|tipografia_psd_origem.json or extrair_tipografia_psd.log")
        return 2
    psd = PSDImage.open(PSD_PATH)
    rows: list[dict] = []
    visit(psd, [], rows)
    fonts = sorted({font for row in rows for font in row["style_run_fonts_resolved"]})
    payload = {"schema": "byd-v4-psd-text-engine/v1", "created_at": timestamp(),
               "method_limit": "psd-tools structural text-engine descriptors only; no render; ResourceDict FontSet can list unused fallback fonts.",
               "psd_tools_version": getattr(psd_tools, "__version__", "unknown"),
               "text_layer_count": len(rows), "fonts_referenced_by_style_runs": fonts, "layers": rows}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    LOG.write_text("\n".join([
        f"{started} | INICIO|extrair_tipografia_psd|modelo_solicitado=gpt-5.6-terra|esforco_solicitado=high|modelo_observado=gpt-6-astra|esforco_observado=herdado-padrao",
        f"{timestamp()} | OK|extrair_tipografia_psd|duracao_s={time.monotonic()-tick:.3f}|text_layers={len(rows)}|fonts={','.join(fonts)}|input_opened_read_only=true|render=false",
        "",
    ]), encoding="utf-8")
    print(f"OK|extrair_tipografia_psd|text_layers={len(rows)}|fonts={','.join(fonts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
