from pathlib import Path
import json,hashlib,datetime
REFUSE_OVERWRITE=True
b=Path(__file__).resolve().parents[2]
d=json.loads((b/'WORK/00_MATRIZ/pilot_spec_p11.json').read_text());old=json.loads((b/'WORK/00_MATRIZ/pilot_spec_p10.json').read_text());d['revision']='p12';d['formats']=old['formats']
banner=json.loads((b/'WORK/00_MATRIZ/pilot_spec_p09.json').read_text())['formats'][0];banner.update(dict(family='strip',align='left',headline_wrap=100,bg_horizon=90));banner['zones']['instal']=[970,84,220,55];banner['zones']['detail']=[1765,150,110,40];d['formats'].insert(0,banner)
for f in d['formats']:
 if f['id']=='1080x1080':f['zones']['detail']=[100,875,530,70]
 if f['family']=='landscape':f['contrast_edge']=820;f['contrast_feather']=150
 if f['family']=='strip':f['contrast_edge']=1130;f['contrast_feather']=170
 if f['family']=='micro':
  f['zones']=dict(logo=[8,8,77,14],title=[95,5,150,9],price=[95,22,145,26],car=[258,6,94,45],benefit=[95,60,255,10],headline=[95,60,255,11],instal=[8,35,78,32]);f['headline_wrap']=100;f['contrast_edge']=238;f['contrast_feather']=32
  f['omissions']=['tagline','footer','legal','badges','detail','generic_headline','benefit_when_vd_restriction_occupies_slot']
d['output_templates']='WORK/01_TEMPLATES/2026-09-19-p12/';d['output_pilots']='WORK/02_PILOTOS/2026-09-19-p12/'
for k in ['output_templates','output_pilots']:(b/d[k]).mkdir(exist_ok=False)
s=(b/'WORK/05_SCRIPTS/build_p11.jsx').read_text().replace('p11','p12').replace('P11_TRIAL','P12_TRIAL')
s=s.replace('function rectMask(g,r){','function rectMask(g,r,feather){')
s=s.replace("[r[0],r[3]]]);var d=", "[r[0],r[3]]]);if(feather)doc.selection.feather(feather);var d=")
s=s.replace("affine(bk,bgS,bgDX,horizon-600*bgS);", "affine(bk,bgS,bgDX,horizon-600*bgS);if(fmt.contrast_edge){var dark=group(bgO,'CONTRASTE · KV MULTIPLICADO');for(var di=0;di<2;di++){var dl=bk.duplicate(),marker=dark.artLayers.add();dl.move(marker,ElementPlacement.PLACEBEFORE);marker.remove();dl.blendMode=BlendMode.MULTIPLY;}rectMask(dark,[-300,-300,fmt.contrast_edge,fmt.h+300],fmt.contrast_feather);}")
s=s.replace("fit(headline,z.headline,fmt.align);", "fit(headline,z.headline,fmt.align);if(fmt.family==='micro'){if(o.id.indexOf('vd-')===0){benefit.visible=false;msg('OMISSAO_PROPOSTA|'+fmt.id+'|'+o.id+'|benefit para priorizar restricao');}else{headline.visible=false;msg('OMISSAO_PROPOSTA|'+fmt.id+'|'+o.id+'|headline generica');}}")
s=s.replace("fmt.family==='micro'?15:60", "fmt.family==='micro'?12:60")
with (b/'WORK/00_MATRIZ/pilot_spec_p12.json').open('x') as f:json.dump(d,f,ensure_ascii=True,indent=2)
with (b/'WORK/05_SCRIPTS/build_p12.jsx').open('x') as f:f.write(s)
with (b/'WORK/06_LOGS/build_p12_provenance.json').open('x') as f:json.dump(dict(created_at=datetime.datetime.now().astimezone().isoformat(),script_sha256=hashlib.sha256(s.encode()).hexdigest(),source='build_p11.jsx',purpose='seven pilot grades; contrast using original KV; micro hierarchy',input='pilot_spec_p12.json',outputs=[d['output_templates'],d['output_pilots']]),f,indent=2)
print('OK|P12 seven format pilot spec')
