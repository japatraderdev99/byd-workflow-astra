"""Reconcile copied source hashes with R18 final-image/template manifests; no render."""
from pathlib import Path
from collections import Counter
import json
P=Path(__file__).resolve().parents[1];base='workspace/Projects/BYD/Jobs/V4/';v=P/base
copied={r['path']:r for r in json.loads((P/'manifests/source-copy.json').read_text())['files']}
manifest=json.loads((v/'WORK/04_QA/manifest.json').read_text());templates=json.loads((v/'WORK/04_QA/production-r18/templates_manifest_r18.json').read_text());spec=json.loads((v/'WORK/00_MATRIZ/production_spec_r18.json').read_text())
errors=[]
for kind,rows in [('png',manifest['files']),('psd',templates['files'])]:
 for r in rows:
  ref=copied.get(base+r['file'])
  if not ref or ref['sha256']!=r['sha256'] or ref['bytes']!=r['bytes']:errors.append({'kind':kind,'file':r['file'],'reason':'Historical manifest differs from verified copy'})
pairs={(r['offer_id'],r['format']) for r in manifest['files']};expected={(o['id'],f['id']) for o in spec['offers'] for f in spec['formats']}
if pairs!=expected or len(manifest['files'])!=140:errors.append({'reason':'Offer x format coverage differs'})
if len(templates['files'])!=7:errors.append({'reason':'Template count differs'})
master=copied.get(base+spec['source']);expected_master='8abc513ff9aa7bedea76e03bc9cdea78fc4cb263044c855be23ac5d0c66917f6'
if not master or master['sha256']!=expected_master:errors.append({'reason':'Original master hash differs'})
result={'status':'FAIL' if errors else 'PASS','pngs':len(manifest['files']),'templates':len(templates['files']),'unique_offer_format_pairs':len(pairs),'by_format':dict(Counter(r['format'] for r in manifest['files'])),'master_matches_recorded_input':master is not None and master['sha256']==expected_master,'errors':errors,'method':'Compare already byte-verified source-copy hashes to historical R18 manifests. No new Photoshop run or visual approval.'}
(P/'data/final_artifact_reconciliation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False));raise SystemExit(bool(errors))
