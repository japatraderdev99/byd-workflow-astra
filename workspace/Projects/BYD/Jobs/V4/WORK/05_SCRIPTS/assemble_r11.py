from pathlib import Path
import json,shutil,hashlib,datetime
ROOT=Path(__file__).resolve()
while not(ROOT/'.mkroot').exists():ROOT=ROOT.parent
b=ROOT/'Projects/BYD/Jobs/V4';spec=json.loads((b/'WORK/00_MATRIZ/production_spec_r03.json').read_text());r7=json.loads((b/'WORK/00_MATRIZ/production_spec_r10.json').read_text());spec['offers']=r7['offers'];spec.update(revision='r11',output_templates='WORK/01_TEMPLATES/2026-09-20-r11/',output_staging='WORK/03_STAGING/2026-09-20-r11/')
plan=[]
for f in spec['formats']:
 fmt=f['id'];tpl=b/(('WORK/01_TEMPLATES/2026-09-20-r08/' if fmt=='1920x276' else r7['output_templates'])+f'BYD_TPL_{fmt}.psd');plan.append((tpl,b/spec['output_templates']/tpl.name))
 preview=b/(('WORK/01_TEMPLATES/2026-09-19-r03/' if fmt=='1920x276' else r7['output_templates'])+f'BYD_TPL_{fmt}_preview.png');plan.append((preview,b/spec['output_templates']/preview.name))
 for o in spec['offers']:
  name=f"byd_{o['id']}_{fmt}.png";source=r7['output_staging']
  if fmt=='1920x276':source='WORK/03_STAGING/2026-09-20-r08/' if o['id']=='dolphin-mini-5l-gs' else 'WORK/03_STAGING/2026-09-19-r03/'
  plan.append((b/source/name,b/spec['output_staging']/name))
for src,dst in plan:
 if not src.exists():raise RuntimeError('MISSING|'+str(src.relative_to(b)))
 if dst.exists():raise RuntimeError('REFUSE_OVERWRITE|'+str(dst.relative_to(b)))
for key in ['output_templates','output_staging']:(b/spec[key]).mkdir(exist_ok=False)
rows=[]
for src,dst in plan:
 shutil.copy2(src,dst);rows.append({'source':str(src.relative_to(b)),'destination':str(dst.relative_to(b)),'bytes':dst.stat().st_size})
(b/'WORK/00_MATRIZ/production_spec_r11.json').write_text(json.dumps(spec,ensure_ascii=True,indent=2));(b/'WORK/04_QA/assembly_r11.json').write_text(json.dumps({'at':datetime.datetime.now().astimezone().isoformat(),'method':'byte copies; no image recompression or PSD mutation','files':rows},indent=2));print('OK|ASSEMBLED|'+str(len(rows)))
