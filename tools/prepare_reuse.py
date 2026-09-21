"""Prepare a new immutable request/JSX pair. Does not open Photoshop."""
from pathlib import Path
import argparse,json,re
P=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('--revision',required=True);a.add_argument('--offers',nargs='+',required=True);a.add_argument('--formats',nargs='+',required=True);x=a.parse_args()
if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{2,60}',x.revision):a.error('Invalid revision')
v=P/'workspace/Projects/BYD/Jobs/V4';s=json.loads((v/'WORK/00_MATRIZ/production_spec_r18.json').read_text())
for vals,allowed in [(x.offers,{o['id'] for o in s['offers']}),(x.formats,{f['id'] for f in s['formats']})]:
 if len(vals)!=len(set(vals)) or not set(vals)<=allowed:a.error('Unknown or duplicate ID')
req_rel=f'WORK/00_MATRIZ/render_request_{x.revision}.json';jsx_rel=f'WORK/05_SCRIPTS/render_{x.revision}.jsx'
req={'revision':'r18','output_folder':f'WORK/03_STAGING/reuse-{x.revision}','log_file':f'WORK/06_LOGS/reuse-{x.revision}.log','validation_output':f'WORK/04_QA/reuse-{x.revision}.json','templates':[{'format':f,'path':s['output_templates']+'BYD_TPL_'+f+'.psd'} for f in x.formats],'offer_ids':x.offers}
for rel in [req_rel,jsx_rel,req['output_folder'],req['log_file'],req['validation_output']]:
 if (v/rel).exists():raise SystemExit('REFUSE_OVERWRITE '+rel)
for t in req['templates']:
 if not (v/t['path']).is_file():raise SystemExit('MISSING_BINARY '+t['path'])
source=(v/'WORK/05_SCRIPTS/render_canonical_v2.jsx').read_text();needle="var REQUEST_REL = 'WORK/00_MATRIZ/render_request_r18.json';"
if source.count(needle)!=1:raise SystemExit('UNEXPECTED_RENDERER')
(v/req_rel).write_text(json.dumps(req,ensure_ascii=False,indent=2)+'\n');(v/jsx_rel).write_text(source.replace(needle,f"var REQUEST_REL = '{req_rel}';"))
print('PREPARED_NOT_EXECUTED',req_rel,jsx_rel,'expected_pngs',len(x.offers)*len(x.formats))
print('Next: review, check_jsx, one operator lock, native execution, log + independent QA. validation_output is not written by renderer.')
