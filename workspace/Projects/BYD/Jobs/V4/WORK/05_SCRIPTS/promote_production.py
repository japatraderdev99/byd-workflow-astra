"""Copies only explicitly reviewed files; never overwrites output."""
from pathlib import Path
import json,hashlib,shutil,datetime
ROOT=Path(__file__).resolve()
while not(ROOT/'.mkroot').exists():ROOT=ROOT.parent
b=ROOT/'Projects/BYD/Jobs/V4';qa=b/'WORK/04_QA/production-r01';tech=json.loads((qa/'technical_all.json').read_text());visual=json.loads((qa/'head_visual_review.json').read_text());approved={x['file']:x for x in visual['files'] if x['status']=='PASS'}
assert len(tech['rows'])==140 and tech['pass']==140
assert len(approved)==140
mapping={'1920x276':'BANNER DESK','1920x1125':'BANNER DESK','360x80':'BANNER MOBILE','1109x1973':'BANNER MOBILE','1080x1080':'ESTATICOS','1080x1920':'ESTATICOS','1920x1080':'ESTATICOS'}
manifest=b/'WORK/04_QA/manifest.json'
if manifest.exists():raise RuntimeError('REFUSE_OVERWRITE_MANIFEST')
plan=[]
for r in tech['rows']:
 src=b/r['file'];v=approved[r['file']];assert v['sha256']==r['sha256']==hashlib.sha256(src.read_bytes()).hexdigest();dst=b/'OUTPUT'/mapping[r['format']]/r['format']/src.name
 if dst.exists():raise RuntimeError('REFUSE_OVERWRITE|'+str(dst))
 plan.append((src,dst,r))
rows=[]
for src,dst,r in plan:
 dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);assert hashlib.sha256(dst.read_bytes()).hexdigest()==r['sha256'];r=dict(r);r.update(output_file=str(dst.relative_to(b)),visual_status='HEAD_VISUAL_REVIEW_PASS',delivery_status='LOCAL_OUTPUT_NOT_EXTERNALLY_SENT');rows.append(r)
manifest.write_text(json.dumps({'created_at':datetime.datetime.now().astimezone().isoformat(),'count':len(rows),'files':rows,'delivery_status':'LOCAL_ONLY'},ensure_ascii=False,indent=2))
print('OK|PROMOTED|'+str(len(rows)))
