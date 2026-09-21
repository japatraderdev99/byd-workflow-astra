#!/usr/bin/env python3
"""Medição append-only de tarefas. Sem dependência de Photoshop ou LLM."""
import argparse, datetime, json, os, subprocess, time
from pathlib import Path
REFUSE_OVERWRITE = True
root = Path(__file__).resolve().parent
while not (root / '.mkroot').exists():
    if root.parent == root: raise RuntimeError('MKROOT_NOT_FOUND')
    root = root.parent
p = argparse.ArgumentParser()
p.add_argument('--task', required=True)
p.add_argument('--phase', required=True)
p.add_argument('--format', default=None)
p.add_argument('--model-requested', default=None)
p.add_argument('--model-observed', default=None)
p.add_argument('command', nargs=argparse.REMAINDER)
a = p.parse_args()
cmd = a.command[1:] if a.command[:1] == ['--'] else a.command
if not cmd: p.error('Informe comando após --')
base = root / 'Projects/BYD/Jobs/V4/WORK/06_LOGS'
stamp = datetime.datetime.now(datetime.timezone.utc)
run_id = stamp.strftime('%Y%m%dT%H%M%S%fZ')
log_path = base / ('timed_' + run_id + '.log')
event_path = base / 'tempos_medidos_20260919.jsonl'
start = time.monotonic()
with log_path.open('x') as log:
    result = subprocess.run(cmd, cwd=root, stdout=log, stderr=subprocess.STDOUT)
elapsed = time.monotonic() - start
row = dict(run_id=run_id, task_id=a.task, phase=a.phase, format=a.format,
           model_requested=a.model_requested, model_observed=a.model_observed,
           start=stamp.isoformat(), end=datetime.datetime.now(datetime.timezone.utc).isoformat(),
           wall_seconds=round(elapsed, 3), ui_seconds=None, tokens=None, cost=None,
           returncode=result.returncode, result='OK' if result.returncode == 0 else 'ERRO',
           log=str(log_path.relative_to(root)))
fd = os.open(event_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
try: os.write(fd, (json.dumps(row, ensure_ascii=False) + '\n').encode())
finally: os.close(fd)
print(json.dumps(row, ensure_ascii=False))
raise SystemExit(result.returncode)
