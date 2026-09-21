from pathlib import Path
import json,re,itertools
ROOT=Path(__file__).resolve()
while not(ROOT/'.mkroot').exists():ROOT=ROOT.parent
b=ROOT/'Projects/BYD/Jobs/V4';lines=(b/'WORK/06_LOGS/build_production_r03.log').read_text().splitlines();rows=[]
for line in lines:
 if '|GEOM|' not in line:continue
 p=line.split('|');rows.append({'format':p[2],'offer_id':p[3],'role':p[4],'bounds':list(map(float,p[5].split('=')[1].split(','))),'visible':p[7]=='visible=true'})
collisions=[]
for a,c in itertools.combinations(rows,2):
 if (a['format'],a['offer_id'])!=(c['format'],c['offer_id']) or not(a['visible'] and c['visible']):continue
 x,y=a['bounds'],c['bounds'];w=min(x[2],y[2])-max(x[0],y[0]);h=min(x[3],y[3])-max(x[1],y[1])
 if w>1 and h>1:collisions.append({'format':a['format'],'offer_id':a['offer_id'],'roles':[a['role'],c['role']],'overlap':[w,h]})
q=b/'WORK/04_QA/production-r03';q.mkdir(exist_ok=True);out=q/f'geometry_{len(rows)}.json'
if out.exists():raise RuntimeError('REFUSE_OVERWRITE')
out.write_text(json.dumps({'geometry_rows':rows,'collisions':collisions},indent=2));print(json.dumps({'rows':len(rows),'collisions':collisions},indent=2))
