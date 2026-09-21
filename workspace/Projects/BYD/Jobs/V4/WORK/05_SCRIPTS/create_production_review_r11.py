#!/usr/bin/env python3
"""Create the local R11 Astra-review board only when explicitly executed.

Card status is read at generation time from the available R11 status manifests.
It remains a snapshot and never represents human/client approval.
"""
from __future__ import annotations

import argparse
import html
import json
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
OUT = V4 / "WORK/04_QA/REVISAO_PRODUCAO_R11.html"
STAGING_REL = "../03_STAGING/" + DATE + "-" + REVISION
STAGING_FILE_REL = "WORK/03_STAGING/" + DATE + "-" + REVISION
QA_DIR = V4 / "WORK/04_QA/production-r11"
ASTRA_REVIEW = QA_DIR / "head_visual_review.json"
PROMOTION_MANIFEST = QA_DIR / "manifest_r11.json"


def status_snapshot() -> tuple[dict[str, str], str]:
    """Merge only existing manifests, giving local-promotion state precedence."""
    statuses: dict[str, str] = {}
    sources = []
    if ASTRA_REVIEW.is_file():
        review = json.loads(ASTRA_REVIEW.read_text(encoding="utf-8"))
        if review.get("review_type") == "ASTRA_AGENT_VISUAL_REVIEW":
            for row in review.get("files", []):
                if isinstance(row.get("file"), str):
                    statuses[row["file"]] = "ASTRA_AGENT_" + str(row.get("status", "STATUS_UNKNOWN"))
            sources.append("head_visual_review.json")
        else:
            sources.append("head_visual_review.json:invalid_review_type")
    if PROMOTION_MANIFEST.is_file():
        manifest = json.loads(PROMOTION_MANIFEST.read_text(encoding="utf-8"))
        for row in manifest.get("files", []):
            if isinstance(row.get("file"), str):
                statuses[row["file"]] = str(row.get("delivery_status", row.get("visual_status", "MANIFEST_STATUS_UNKNOWN")))
        sources.append("manifest_r11.json")
    return statuses, ", ".join(sources) if sources else "no status manifest available"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Required to create the review HTML.")
    args = parser.parse_args()
    if not args.execute:
        raise RuntimeError("REFUSE_WRITE_WITHOUT_--execute")
    if OUT.exists():
        raise RuntimeError("REFUSE_OVERWRITE")
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    if spec.get("revision") != REVISION or len(spec["offers"]) != 20 or len(spec["formats"]) != 7:
        raise RuntimeError("INVALID_R11_SCOPE")
    statuses, status_source = status_snapshot()
    status_values = sorted(set(statuses.values()) | {"PENDING_ASTRA_AGENT_REVIEW"})
    parts = ["<!doctype html><html lang=\"pt-BR\"><meta charset=\"utf-8\"><title>BYD R11 Astra review</title><style>body{background:#0e1922;color:#e7eef4;font:15px system-ui;margin:24px}nav{position:sticky;top:0;background:#0e1922;padding:12px 0;display:flex;gap:10px;flex-wrap:wrap}a{color:#c4ecf5}select{padding:8px;background:#1d3444;color:white}.status{display:inline-block;margin:5px 0 8px;padding:3px 6px;border-radius:4px;background:#25485a;font-size:12px}section{margin:28px 0}article{display:inline-block;vertical-align:top;background:#142631;padding:12px;margin:0 12px 18px 0;width:min(43vw,900px)}img{display:block;width:100%;height:auto}.micro article{width:360px}.strip article{display:block;width:min(95vw,1920px)}.hidden{display:none}</style><h1>BYD R11 - Astra agent visual review</h1><p>Status snapshot: " + html.escape(status_source) + ". This is Astra-agent visual QA only; it is not human/client approval, promotion, delivery, or client send.</p><nav><label>Offer <select id=\"of\"><option value=\"\">All</option>"]
    for offer in spec["offers"]:
        parts.append("<option>" + html.escape(offer["id"]) + "</option>")
    parts.append("</select></label><label>Status <select id=\"st\"><option value=\"\">All</option>")
    for status in status_values:
        parts.append("<option>" + html.escape(status) + "</option>")
    parts.append("</select></label>")
    for fmt in spec["formats"]:
        parts.append("<a href=\"#" + fmt["id"] + "\">" + fmt["id"] + "</a>")
    parts.append("</nav>")
    for fmt in spec["formats"]:
        fmt_id = fmt["id"]
        parts.append("<section id=\"" + fmt_id + "\" class=\"" + fmt["family"] + "\"><h2>" + fmt_id + "</h2>")
        for offer in spec["offers"]:
            offer_id = offer["id"]
            png_name = "byd_" + offer_id + "_" + fmt_id + ".png"
            png = STAGING_REL + "/" + png_name
            file_key = STAGING_FILE_REL + "/" + png_name
            status = statuses.get(file_key, "PENDING_ASTRA_AGENT_REVIEW")
            parts.append("<article data-offer=\"" + offer_id + "\" data-status=\"" + html.escape(status, quote=True) + "\"><figcaption>" + offer_id + " - " + fmt_id + "</figcaption><span class=\"status\">" + html.escape(status) + "</span><a href=\"" + png + "\"><img loading=\"lazy\" src=\"" + png + "\" alt=\"" + offer_id + " " + fmt_id + "\"></a></article>")
        parts.append("</section>")
    parts.append("<script>const f=()=>{const o=document.querySelector('#of').value,s=document.querySelector('#st').value;document.querySelectorAll('article').forEach(a=>a.classList.toggle('hidden',(!!o&&a.dataset.offer!==o)||(!!s&&a.dataset.status!==s)))};document.querySelector('#of').onchange=f;document.querySelector('#st').onchange=f;</script></html>")
    OUT.write_text("".join(parts), encoding="utf-8")
    print("OK|review_html_r11")


if __name__ == "__main__":
    main()
