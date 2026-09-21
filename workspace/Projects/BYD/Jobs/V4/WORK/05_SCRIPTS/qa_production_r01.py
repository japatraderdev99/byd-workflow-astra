"""Read-only technical inventory and review sheets; no approval inferred."""
from pathlib import Path
import json,hashlib,io,time,argparse
from PIL import Image,ImageCms,ImageDraw
ROOT=Path(__file__).resolve()
while not (ROOT/'.mkroot').exists():ROOT=ROOT.parent
BASE=ROOT/'Projects/BYD/Jobs/V4'
p=argparse.ArgumentParser();p.add_argument('--revision',default='r01');p.add_argument('--format');a=p.parse_args()
spec=json.loads((BASE/f'WORK/00_MATRIZ/production_spec_{a.revision}.json').read_text());folder=BASE/spec['output_staging'];out=BASE/f'WORK/04_QA/production-{a.revision}';out.mkdir(exist_ok=True)
rows=[];start=time.monotonic()
for fmt in spec['formats']:
 if a.format and fmt['id']!=a.format:continue
 files=[folder/f"byd_{o['id']}_{fmt['id']}.png" for o in spec['offers']]
 if not all(f.exists() for f in files):print('WAIT|'+fmt['id']);continue
 for f in files:
  with Image.open(f) as im:
   icc=im.info.get('icc_profile');profile=ImageCms.getProfileName(ImageCms.ImageCmsProfile(io.BytesIO(icc))).strip() if icc else ''
   checks={'dimensions':im.size==(fmt['w'],fmt['h']),'rgb':im.mode=='RGB','srgb':'srgb' in profile.lower(),'8bit':f.read_bytes()[24]==8}
   rows.append({'file':str(f.relative_to(BASE)),'offer_id':f.name[4:-(len(fmt['id'])+5)],'format':fmt['id'],'width':im.width,'height':im.height,'mode':im.mode,'profile':profile,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'checks':checks,'technical_pass':all(checks.values()),'visual_status':'PENDING_HEAD_REVIEW','template':spec["output_templates"]+f"BYD_TPL_{fmt['id']}.psd"})
 # Review 4 images per sheet, preserve original micro/strip pixels.
 per_page=2 if fmt['family']=='portrait' else 4
 for page in range((len(files)+per_page-1)//per_page):
  subset=files[page*per_page:page*per_page+per_page];tw=fmt['w'] if fmt['h']<=276 else min(900,fmt['w']);th=round(fmt['h']*tw/fmt['w']);cols=1 if fmt['h']<=276 else 2;nr=4 if cols==1 else (1 if per_page==2 else 2)
  board=Image.new('RGB',(cols*tw,nr*(th+32)), '#13212d');draw=ImageDraw.Draw(board)
  for j,f in enumerate(subset):
   im=Image.open(f);im.thumbnail((tw,th));x=(j%cols)*tw;y=(j//cols)*(th+32);draw.text((x+8,y+8),f.stem,fill='white');board.paste(im,(x,y+32))
  sheet=out/f"review_{fmt['id']}_{page+1:02}.jpg"
  if not sheet.exists():board.save(sheet,quality=97)
report=out/('technical_'+(a.format or 'all')+'.json')
if report.exists():raise RuntimeError('REFUSE_OVERWRITE')
report.write_text(json.dumps({'rows':rows,'png_count':len(rows),'pass':sum(r['technical_pass'] for r in rows),'seconds':time.monotonic()-start},indent=2))
print('OK|PNG='+str(len(rows))+'|pass='+str(sum(r['technical_pass'] for r in rows)))
