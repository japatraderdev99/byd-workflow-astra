"""Read-only SHA256 check of the transfer package, without Photoshop."""
from pathlib import Path
import json,hashlib,argparse,concurrent.futures
P=Path(__file__).resolve().parents[1]
def check(r):
 p=P/r['path']
 if not p.is_file():return {'path':r['path'],'error':'MISSING'}
 if p.stat().st_size!=r['bytes']:return {'path':r['path'],'error':'SIZE'}
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 if h.hexdigest()!=r['sha256']:return {'path':r['path'],'error':'HASH'}
 return None
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--mode',choices=['text','full'],default='text');x=a.parse_args()
 records=json.loads((P/'manifests/package.json').read_text())['files'];records=[r for r in records if x.mode=='full' or r['in_git']]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:errors=[r for r in pool.map(check,records) if r]
 print(json.dumps({'mode':x.mode,'checked':len(records),'errors':errors,'status':'FAIL' if errors else 'PASS'},ensure_ascii=False))
 raise SystemExit(bool(errors))
