"""Find actual SKILL.md reads and retain only byte-matching historical snapshots."""
from pathlib import Path
import json,re,hashlib,os
P=Path(__file__).resolve().parents[1];D=json.loads((P/'data/expanded_audit.json').read_text());b=Path(os.environ.get('CODEX_SESSIONS_DIR',str(Path.home()/'.codex/sessions')))/'2026/09/19';reads=[];snapshots={}
def strings(x,depth=0):
 if depth>8:return []
 if isinstance(x,str):
  vals=[x]
  if x.lstrip().startswith(('{','[')):
   try:vals+=strings(json.loads(x),depth+1)
   except (ValueError,TypeError):pass
  return vals
 if isinstance(x,dict):return [s for v in x.values() for s in strings(v,depth+1)]
 if isinstance(x,list):return [s for v in x for s in strings(v,depth+1)]
 return []
for t in D['threads']:
 calls={};outputs={}
 for ln,line in enumerate((b/t['source_file']).open(),1):
  d=json.loads(line);a=d.get('payload',{})
  if d['timestamp']>'2026-09-20T05:22:56.047Z' or d['type']!='response_item':continue
  if a.get('type') in ('custom_tool_call','function_call'):
   s=str(a.get('input',a.get('arguments','')))
   if 'SKILL.md' in s:
    paths=re.findall(r'[^\s\"\'`\\<>]+/SKILL\.md',s)
    calls[a.get('call_id')]={'thread':t['role'],'source_file':t['source_file'],'line':ln,'timestamp':d['timestamp'],'paths':paths}
  elif a.get('type') in ('custom_tool_call_output','function_call_output'):outputs[a.get('call_id')]=a.get('output')
 for cid,c in calls.items():
  texts=strings(outputs.get(cid));items=[]
  for path in c.pop('paths'):
   f=Path(path);name=f.parent.name;full=False
   if f.is_file():
    raw=f.read_bytes();text=raw.decode();full=any(text.strip() in s for s in texts)
    if full:
     dest=P/'evidence/skills'/name/'SKILL.md';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw);snapshots[name]={'path':str(dest.relative_to(P)),'sha256':hashlib.sha256(raw).hexdigest(),'verified_as_full_substring_of_historical_tool_output':True}
   items.append({'skill':name,'historical_path':path,'matching_output_found':cid in outputs,'full_snapshot_verified':full})
  reads.append({**c,'skills':items})
(P/'data/skill_reads.json').write_text(json.dumps({'reads':reads,'snapshots':snapshots,'scope':'Historical skill read calls and exact content verification; invocation does not prove every rule was followed'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'reads':len(reads),'snapshots':snapshots,'skills':sorted({x['skill'] for r in reads for x in r['skills']})},ensure_ascii=False,indent=2))
