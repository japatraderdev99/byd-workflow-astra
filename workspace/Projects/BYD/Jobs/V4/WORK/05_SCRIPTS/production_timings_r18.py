#!/usr/bin/env python3
"""Prepare a non-overlapping native timing report for the R18 final package.

Do not run until production, corrections and reexport validation have finished. The report writes
one new JSON file and refuses to overwrite it. Nested offer/format events are
reported as detail only; aggregation uses terminal completed elapsed_ms once per
run, never their children.
"""
from __future__ import annotations

import datetime as dt
import json
import re
from email.utils import parsedate_to_datetime
from pathlib import Path


def workspace_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".mkroot").exists():
            return candidate
    raise RuntimeError("MISSING_MKROOT")


ROOT = workspace_root(Path(__file__).resolve())
V4 = ROOT / "Projects/BYD/Jobs/V4"
LOG_DIR = V4 / "WORK/06_LOGS"
OUT = V4 / "WORK/04_QA/production_timings_r18.json"
RUN_LOGS = [
    ("r01", "build_production_r01.log"),
    ("probe_r02", "probe_r02.log"),
    ("probe_r03", "probe_r03.log"),
    ("r03", "build_production_r03.log"),
    ("probe_r05", "probe_r05.log"),
    ("r07", "build_production_r07.log"),
    ("r10", "build_production_r10.log"),
    ("r12_failed", "patch_controle_r12.log"),
    ("r14", "patch_controle_r14.log"),
    ("r16", "patch_controle_r16.log"),
    ("reuse_r13_failed_visual", "render_reuse_r13.log"),
    ("r17_partial_strip", "recapture_templates_r17.log"),
    ("r19_failed", "recapture_templates_r19.log"),
    ("r20", "recapture_templates_r20.log"),
    ("reuse_r18", "render_reuse_r18.log"),
]
RUN_LOGS = [("pilot_p%02d" % i, "build_p%02d.log" % i) for i in range(1, 13)] + [("pilot_patch_p%02d" % i, "patch_p%02d.log" % i) for i in range(13, 19)] + RUN_LOGS
ELAPSED = re.compile(r"(?:^|\|)elapsed_ms=(\d+)(?:\||$)")


def parse_log(label: str, path: Path) -> dict:
    record = {"run": label, "log": str(path.relative_to(V4)), "status": "MISSING", "terminal": None, "nested_events": [], "errors": []}
    if not path.exists():
        return record
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    terminals = []
    dated = []
    for line in lines:
        try: dated.append(parsedate_to_datetime(line.split("|")[0]))
        except (TypeError, ValueError): pass
    record["observed_wall_span_seconds"] = (dated[-1]-dated[0]).total_seconds() if len(dated)>1 else None
    for line in lines:
        fields = line.split("|")
        elapsed = ELAPSED.search(line)
        elapsed_ms = int(elapsed.group(1)) if elapsed else None
        event = fields[1:3] if len(fields) >= 3 else fields[1:]
        if "|ERRO|" in line:
            record["errors"].append(line)
        if "|OK|completed|" in line:
            terminals.append({"line": line, "elapsed_ms": elapsed_ms})
        elif elapsed_ms is not None:
            record["nested_events"].append({"event": event, "elapsed_ms": elapsed_ms, "line": line})
    if terminals:
        # A retry can append a second terminal event. It is kept explicit rather
        # than summed, since individual event timings may overlap or nest.
        record["status"] = "COMPLETED" if len(terminals) == 1 else "MULTIPLE_TERMINALS"
        record["terminal"] = terminals[-1]
        record["terminal_candidates"] = terminals
    else:
        record["status"] = "ERROR_NO_TERMINAL" if record["errors"] else "INCOMPLETE_NO_TERMINAL"
    return record


def main() -> None:
    if OUT.exists():
        raise RuntimeError("REFUSE_OVERWRITE|" + str(OUT.relative_to(V4)))
    runs = [parse_log(label, LOG_DIR / filename) for label, filename in RUN_LOGS]
    completed = [run["terminal"]["elapsed_ms"] for run in runs if run["status"] == "COMPLETED" and run["terminal"] and run["terminal"]["elapsed_ms"] is not None]
    report = {
        "schema": "byd-v4-production-timings-r18/v1",
        "write_guard": "REFUSE_OVERWRITE",
        "generated_at": dt.datetime.now().astimezone().isoformat(),
        "runs": runs,
        "aggregate": {
            "completed_terminal_elapsed_ms_total": sum(completed),
            "completed_terminal_run_count": len(completed),
            "method": "Only exactly one terminal OK|completed elapsed_ms per log is aggregated. Nested trial, offer, format and export elapsed_ms values are retained as detail and are never summed.",
        },
        "limits": "No token, billing, human active time, wall-clock gaps, Astra-agent visual review, human/client approval, or delivery status is measured here.",
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK|production_timings_r18|runs=" + str(len(runs)))


if __name__ == "__main__":
    main()
