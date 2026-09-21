"""Copy the exact R18-delivered bytes into a separate folder; never alter the V4 snapshot."""
from pathlib import Path
import json,hashlib,subprocess,shutil,datetime as dt
P=Path(__file__).resolve().parents[1];base='workspace/Projects/BYD/Jobs/V4/';v=P/base;dest=P/'resultado_historico_R18'
if dest.exists():raise SystemExit('REFUSE_OVERWRITE historical delivery')
copies=json.loads((P/'manifests/source-copy.json').read_text())['files'];by_path={r['path']:r for r in copies};by_hash={}
for r in copies:by_hash.setdefault(r['sha256'],[]).append(r)
manifest=json.loads((v/'WORK/04_QA/manifest.json').read_text());plan=[];differences=[]
for row in manifest['files']:
 current=by_path[base+row['file']];matches=by_hash.get(row['sha256'],[])
 if not matches:raise SystemExit('NO_HISTORICAL_BYTES '+row['file'])
 preferred=next((r for r in matches if r['path']==base+row['file']),None) or next((r for r in matches if r['path']==base+row.get('staging_file','')),None) or matches[0]
 relative=Path(row['file']).relative_to('OUTPUT/2026-09-20-r18');target=dest/relative
 plan.append((preferred,target,row))
 if current['sha256']!=row['sha256']:
  original=P.parents[1]/'Projects/BYD/Jobs/V4'/row['file']
  differences.append({'file':row['file'],'offer_id':row['offer_id'],'format':row['format'],'historical_sha256':row['sha256'],'current_snapshot_sha256':current['sha256'],'historical_bytes':row['bytes'],'current_bytes':current['bytes'],'source_file_mtime_observed_at_handoff':dt.datetime.fromtimestamp(original.stat().st_mtime,dt.timezone.utc).isoformat(),'recovered_from':preferred['path'],'historical_result_path':str(target.relative_to(P)),'cause_or_actor':None})
result=[]
for src,target,row in plan:
 target.parent.mkdir(parents=True,exist_ok=True);r=subprocess.run(['cp','-c',str(P/src['path']),str(target)],capture_output=True)
 if r.returncode:shutil.copy2(P/src['path'],target)
 actual=hashlib.sha256(target.read_bytes()).hexdigest()
 if actual!=row['sha256']:raise RuntimeError('HASH_MISMATCH '+str(target))
 result.append({'file':str(target.relative_to(P)),'offer_id':row['offer_id'],'format':row['format'],'bytes':target.stat().st_size,'sha256':actual,'copied_from':src['path']})
report={'schema':'byd-r18-historical-recovery/v1','status':'PASS_HISTORICAL_DELIVERY_RECONSTRUCTED_BY_EXACT_HASH','historical_manifest':'workspace/Projects/BYD/Jobs/V4/WORK/04_QA/manifest.json','historical_files':len(result),'current_snapshot_matches_historical':len(result)-len(differences),'current_snapshot_differences':len(differences),'canonical_psds_match':7,'differences':differences,'files':result,'scope':'Exact archived bytes copied from already verified files; no image editing, no Photoshop, no overwrite of V4, no attribution of later modifications to the original run.'}
(P/'data/historical_delivery_recovery.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':report['status'],'files':len(result),'differences':len(differences)}))
