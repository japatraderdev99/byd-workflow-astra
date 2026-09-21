from pathlib import Path
import hashlib,json,subprocess,shutil,time,concurrent.futures
PACKAGE=Path(__file__).resolve().parents[1]
ROOT=PACKAGE.parents[1]
TARGET=PACKAGE/'workspace'
SOURCES=['Projects/BYD/Jobs/V4','operacao/lib','AGENTS.md','.mkroot','psd-editor/01 Sistema Operacional','psd-editor/02 Padrões de Design','psd-editor/03 QA e Entrega','psd-editor/06 Automação e Scripts']
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def copy_one(p):
 rel=p.relative_to(ROOT);dst=TARGET/rel;dst.parent.mkdir(parents=True,exist_ok=True)
 if dst.exists():raise RuntimeError('REFUSE_OVERWRITE '+str(rel))
 stat=p.stat()
 r=subprocess.run(['cp','-c',str(p),str(dst)],capture_output=True)
 if r.returncode:shutil.copy2(p,dst)
 a=digest(p);b=digest(dst)
 if a!=b or p.stat().st_mtime_ns!=stat.st_mtime_ns:raise RuntimeError('SOURCE_CHANGED_OR_COPY_MISMATCH '+str(rel))
 return {'path':str(Path('workspace')/rel),'bytes':stat.st_size,'sha256':a,'copy_verified':True}
if __name__=='__main__':
 if not (ROOT/'.mkroot').is_file() or not (ROOT/'Projects/BYD/Jobs/V4').is_dir():raise RuntimeError('ORIGINAL_WORKSPACE_REQUIRED; Git clone does not contain source binaries')
 started=time.time();files=[];excluded=[]
 for rel in SOURCES:
  p=ROOT/rel
  for f in ([p] if p.is_file() else sorted(p.rglob('*'))):
   if not f.is_file():continue
   if f.name=='.DS_Store' or '__pycache__' in f.parts or f.suffix=='.pyc':excluded.append(str(f.relative_to(ROOT)));continue
   if f.is_symlink():raise RuntimeError('UNREVIEWED_SYMLINK '+str(f))
   files.append(f)
 print('COPY_START',len(files),sum(f.stat().st_size for f in files),flush=True)
 result=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for i,r in enumerate(pool.map(copy_one,files),1):
   result.append(r)
   if i%100==0:print('VERIFIED',i,'/',len(files),flush=True)
 (PACKAGE/'manifests').mkdir(exist_ok=True)
 (PACKAGE/'manifests/source-copy.json').write_text(json.dumps({'files':result,'excluded_regenerable':excluded,'elapsed_seconds':time.time()-started,'verified_bytes':sum(r['bytes'] for r in result)},ensure_ascii=False,indent=2)+'\n')
 print('COPY_VERIFIED',len(result),'elapsed',time.time()-started,flush=True)
