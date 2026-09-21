#!/usr/bin/env python3
"""QA técnico de pilotos. Não aprova composição nem conteúdo."""
import argparse,hashlib,io,json,re,struct,time
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image,ImageCms
from psd_tools import PSDImage
REFUSE_OVERWRITE=True
p=argparse.ArgumentParser();p.add_argument('--revision',required=True);p.add_argument('--png-dir',required=True);p.add_argument('--psd-dir',required=True);p.add_argument('--output',required=True);a=p.parse_args()
root=Path(__file__).resolve().parent
while not(root/'.mkroot').exists():
 if root==root.parent:raise RuntimeError('MKROOT_NOT_FOUND')
 root=root.parent
base=root/'Projects/BYD/Jobs/V4';out=base/a.output
if out.exists():raise RuntimeError('REFUSE_OVERWRITE')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for buf in iter(lambda:f.read(1024*1024),b''):h.update(buf)
 return h.hexdigest()
start=time.monotonic();rows=[];psds=[]
for f in sorted((base/a.png_dir).glob(a.revision+'_byd_*.png')):
 m=re.fullmatch(a.revision+r'_byd_(.+)_(\d+)x(\d+)\.png',f.name)
 with Image.open(f) as im:
  profile=im.info.get('icc_profile');name=ImageCms.getProfileName(ImageCms.ImageCmsProfile(io.BytesIO(profile))).strip() if profile else None
  with f.open('rb') as raw: header=raw.read(26)
  bits=header[24];opaque=im.mode=='RGB' or (im.mode=='RGBA' and im.getextrema()[3]==(255,255))
  checks=dict(dimensions=bool(m and im.size==(int(m[2]),int(m[3]))),rgb=im.mode=='RGB',eight_bit=bits==8,opaque=opaque,srgb=bool(name and 'srgb' in name.lower()))
  rows.append(dict(file=str(f.relative_to(base)),offer_id=m[1] if m else None,size=list(im.size),mode=im.mode,bits=bits,icc=name,bytes=f.stat().st_size,sha256=sha(f),checks=checks,technical_pass=all(checks.values()),visual_status='NOT_APPROVED_BY_THIS_SCRIPT'))
for f in sorted((base/a.psd_dir).glob(a.revision.upper()+'_TRIAL_*.psd')):
 psd=PSDImage.open(f);layers=list(psd.descendants());top=[l.name for l in psd]
 needed=['#GUIAS','FIXO','OFERTA','CONDICIONAIS','LEGAL','VEICULO','BG']
 psds.append(dict(file=str(f.relative_to(base)),size=list(psd.size),sha256=sha(f),bytes=f.stat().st_size,top_groups=top,required_groups_present=all(n in top for n in needed),text_layers=sum(l.kind=='type' for l in layers),smart_objects=sum(l.kind=='smartobject' for l in layers),status='DRAFT_3_STATES_NOT_CANONICAL'))
report=dict(at=datetime.now(timezone.utc).isoformat(),elapsed_seconds=round(time.monotonic()-start,3),revision=a.revision,png_count=len(rows),png_pass=sum(x['technical_pass'] for x in rows),psd_count=len(psds),pngs=rows,psds=psds,approval=False)
with out.open('x') as f:json.dump(report,f,ensure_ascii=False,indent=2)
print('OK|technical_qa|png='+str(len(rows))+'|pass='+str(report['png_pass'])+'|psd='+str(len(psds))+'|seconds='+str(report['elapsed_seconds']))
if not rows or report['png_pass']!=len(rows):raise SystemExit(1)
