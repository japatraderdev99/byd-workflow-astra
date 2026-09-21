"""Build distribution manifest after the verified source copy. No production execution."""
from pathlib import Path
import json,hashlib,subprocess,re,unicodedata
P=Path(__file__).resolve().parents[1]
ALLOWED={'.md','.json','.jsonl','.tsv','.csv','.py','.jsx','.jsxinc','.sh','.txt','.log','.html','.js','.ts','.css','.toml','.yaml','.yml','.sql','.mmd'}
SPECIAL={'.mkroot','.gitignore'}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 prior=json.loads((P/'manifests/source-copy.json').read_text());checked={r['path']:r for r in prior['files']};rows=[];gitpaths=[]
 for f in sorted(P.rglob('*')):
  if not f.is_file() or '.git' in f.relative_to(P).parts or '__pycache__' in f.parts or f.name=='.DS_Store':continue
  rel=str(f.relative_to(P))
  if rel in ('manifests/package.json','manifests/publication.json'):continue
  if f.is_symlink():raise RuntimeError('SYMLINK '+rel)
  in_git=f.suffix.lower() in ALLOWED or f.name in SPECIAL
  if f.name.startswith('.env') or f.name.endswith('private.json'):raise RuntimeError('PRIVATE_FILE '+rel)
  old=checked.get(rel)
  if old and f.stat().st_size!=old['bytes']:raise RuntimeError('SOURCE_COPY_SIZE_CHANGED '+rel)
  digest=old['sha256'] if old else sha(f)
  if in_git:
   if f.stat().st_size>40*1024*1024:raise RuntimeError('LARGE_TEXT '+rel)
   raw=f.read_bytes()
   try:s=raw.decode('utf-8')
   except UnicodeDecodeError:
    if f.suffix.lower()!='.log':raise
    s=raw.decode('latin-1') # Preserve original legacy log bytes; scan without transcoding.
   if '\0' in s:raise RuntimeError('BINARY_DISGUISED_AS_TEXT '+rel)
   if re.search(r'gh[pousr]_[A-Za-z0-9]{30,}|sk-(?:proj-)?[A-Za-z0-9_-]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',s):raise RuntimeError('POTENTIAL_SECRET '+rel)
   gitpaths.append(unicodedata.normalize('NFC',rel))
  rows.append({'path':unicodedata.normalize('NFC',rel),'bytes':f.stat().st_size,'sha256':digest,'in_git':in_git})
 out={'schema':'byd-handoff-package/v1','scope':'Complete local package; binary assets intentionally absent from Git','source_copy_verified_files':len(checked),'source_copy_verified_bytes':prior['verified_bytes'],'files':rows,'files_count':len(rows),'bytes':sum(r['bytes'] for r in rows),'git_text_files':len(gitpaths),'excluded_from_self_manifest':['manifests/package.json','manifests/publication.json','.git/'],'validation':'Original source files copied and hashed at both ends; new files hashed here; UTF-8 (legacy logs inspected as Latin-1 without transcoding) and credential-pattern checks before Git staging'}
 (P/'manifests/package.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 gitpaths.append('manifests/package.json')
 result=subprocess.run(['git','add','--pathspec-from-file=-','--pathspec-file-nul'],cwd=P,input=('\0'.join(gitpaths)+'\0').encode(),capture_output=True)
 if result.returncode:raise RuntimeError(result.stderr.decode())
 print(json.dumps({k:v for k,v in out.items() if k!='files'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
