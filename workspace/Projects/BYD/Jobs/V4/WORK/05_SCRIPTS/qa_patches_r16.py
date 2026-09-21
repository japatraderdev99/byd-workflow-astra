from pathlib import Path
import json,hashlib,io
from PIL import Image,ImageCms,ImageChops
ROOT=Path(__file__).resolve()
while not(ROOT/'.mkroot').exists():ROOT=ROOT.parent
b=ROOT/'Projects/BYD/Jobs/V4';folder=b/'WORK/03_STAGING/2026-09-20-r16';out=b/'WORK/04_QA/production-r16';out.mkdir(exist_ok=True)
rows=[]
for p in sorted(folder.glob('*.png')):
 fmt=p.stem.rsplit('_',1)[1];w,h=map(int,fmt.split('x'));offer=p.stem[4:-(len(fmt)+1)]
 old=b/('WORK/03_STAGING/2026-09-19-r03' if h==276 else 'WORK/03_STAGING/2026-09-20-r10')/p.name
 with Image.open(p) as im, Image.open(old) as before:
  profile=ImageCms.getProfileName(ImageCms.ImageCmsProfile(io.BytesIO(im.info['icc_profile']))).strip()
  checks={'dimensions':im.size==(w,h),'RGB8':im.mode=='RGB' and p.read_bytes()[24]==8,'sRGB':'srgb' in profile.lower()}
  diff=ImageChops.difference(im,before);bbox=diff.getbbox()
 rows.append({'file':str(p.relative_to(b)),'offer_id':offer,'format':fmt,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'profile':profile,'checks':checks,'technical_pass':all(checks.values()),'changed_bbox':bbox,'before':str(old.relative_to(b)),'visual_status':'PENDING_HEAD_REVIEW'})
f=out/('technical_'+str(len(rows))+'.json')
if f.exists():raise RuntimeError('REFUSE_OVERWRITE')
f.write_text(json.dumps({'rows':rows,'count':len(rows)},indent=2));print(json.dumps({'count':len(rows),'checks':all(r['technical_pass'] for r in rows),'differences':[{'offer':r['offer_id'],'format':r['format'],'bbox':r['changed_bbox']} for r in rows]},indent=2))
