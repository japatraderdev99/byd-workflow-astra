"""Export tool dispatch metadata and referenced case paths, without raw arguments/results."""
from pathlib import Path
import json,re,collections,csv,os
P=Path(__file__).resolve().parents[1];D=json.loads((P/'data/expanded_audit.json').read_text());base=Path(os.environ.get('CODEX_SESSIONS_DIR',str(Path.home()/'.codex/sessions')))/'2026/09/19';rows=[]
for t in D['threads']:
 for ln,line in enumerate((base/t['source_file']).open(),1):
  d=json.loads(line);a=d.get('payload',{})
  if d['timestamp']>'2026-09-20T05:22:56.047Z' or d['type']!='response_item' or a.get('type') not in ('function_call','custom_tool_call'):continue
  s=str(a.get('input',a.get('arguments','')));paths=sorted(set(re.findall(r'(?:Projects/BYD/Jobs/V4/|operacao/lib/)[^\s\"\'`\\<>;]+',s)))
  rows.append({'timestamp':d['timestamp'],'thread_role':t['role'],'tool':a.get('name'),'call_id':a.get('call_id'),'nested_tool_names_observed':sorted(set(re.findall(r'tools\.([a-zA-Z_0-9]+)\s*\(',s))),'case_paths_referenced':paths,'source_file':t['source_file'],'source_line':ln})
rows.sort(key=lambda r:r['timestamp']);counts=collections.Counter(r['tool'] for r in rows)
(P/'data/tool_dispatch_ledger.json').write_text(json.dumps({'scope':'Six BYD tasks until final handoff; outer dispatches, not native billable calls; nested names are references, not proof of execution count','count':len(rows),'counts':dict(counts),'rows':rows},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'count':len(rows),'counts':dict(counts)}))
