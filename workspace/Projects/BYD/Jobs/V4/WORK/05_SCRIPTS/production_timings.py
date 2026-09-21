from pathlib import Path
import re,json,csv
ROOT=Path(__file__).resolve()
while not(ROOT/'.mkroot').exists():ROOT=ROOT.parent
b=ROOT/'Projects/BYD/Jobs/V4';out=b/'WORK/04_QA/tempos_producao.json'
if out.exists():raise RuntimeError('REFUSE_OVERWRITE')
rows=[];errors=[]
for name in ['build_production_r01.log','probe_r02.log','probe_r03.log','build_production_r03.log','patch_micro_r04.log']:
 p=b/'WORK/06_LOGS'/name
 if not p.exists():continue
 for l in p.read_text().splitlines():
  if '|ERRO|' in l:errors.append({'run':name,'line':l})
  m=re.search(r'\|elapsed_ms=(\d+)',l)
  if m:rows.append({'run':name,'at':l.split('|')[0],'event':l.split('|')[1],'context':l.split('|')[2:-1],'seconds':int(m[1])/1000})
out.write_text(json.dumps({'measurements':rows,'errors':errors,'limits':'Native script time only. Events are nested; do not sum offer+format+run totals. No token, billing or active human time measured.'},indent=2))
print('OK|timings|'+str(len(rows)))
