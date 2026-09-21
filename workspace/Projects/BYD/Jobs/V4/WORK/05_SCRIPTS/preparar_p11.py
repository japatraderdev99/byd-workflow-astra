from pathlib import Path
import json,hashlib,datetime
REFUSE_OVERWRITE=True
b=Path(__file__).resolve().parents[2]
d=json.loads((b/'WORK/00_MATRIZ/pilot_spec_p10.json').read_text());d['revision']='p11';d['formats']=[f for f in d['formats'] if f['id'] in ['1920x1080','1080x1080','1080x1920']]
d['output_templates']='WORK/01_TEMPLATES/2026-09-19-p11/';d['output_pilots']='WORK/02_PILOTOS/2026-09-19-p11/'
for k in ['output_templates','output_pilots']:(b/d[k]).mkdir(exist_ok=False)
for o in d['offers']:
 if o['id']=='yuan-plus-awd-26-27':o['anchor_id']=231;o['anchor_name']='Layer 8'
 if o['id']=='vd-atto-2':o['anchor_id']=2952;o['anchor_name']='04.ATTO 2 DMi_LHD_Midnight Blue_High-end Wheels_Left 45°_download_PSB_RGB'
 for e in o['extras']:
  if e['role']=='detail':e['crop']=[0,1150,1080,1350];e['anchor_id']=23;e['anchor_name']='It’s not a car, it’s a BYD'
for f in d['formats']:
 if f['id']=='1080x1080':f['zones']['detail']=[100,875,530,70]
s=(b/'WORK/05_SCRIPTS/build_p10.jsx').read_text().replace('p10','p11').replace('P10_TRIAL','P11_TRIAL')
a=s.index('  var bk=');e=s.index('\n  var vehicle=',a)
s=s[:a]+'''  var bk=dup(spec.fixed.background,bgO,'KV'),bb=box(bk);var bgS=s;var bgDX=dx;var horizon=600*s+dy;bgS=Math.max(bgS,bgDX/(-bb[0]),(fmt.w-bgDX)/bb[2],horizon/(600-bb[1]),(fmt.h-horizon)/(bb[3]-600));affine(bk,bgS,bgDX,horizon-600*bgS);
'''+s[e:]
a=s.index('  for(var ei=');e=s.index('\n\n  states.push',a)
s=s[:a]+'''  for(var ei=0;ei<o.extras.length;ei++){var extra=o.extras[ei],el=dup(extra.id,cg,'COND · '+extra.role+' · '+o.id,extra.anchor_id);if(z[extra.role]){if(extra.crop){var ec=extra.crop,ez=z[extra.role],es=Math.min(ez[2]/(ec[2]-ec[0]),ez[3]/(ec[3]-ec[1])),ex=ez[0]+(ez[2]-(ec[2]-ec[0])*es)/2-ec[0]*es,ey=ez[1]-ec[1]*es;affine(el,es,ex,ey,extra.anchor_name);rectMask(el,[ec[0]*es+ex,ec[1]*es+ey,ec[2]*es+ex,ec[3]*es+ey]);}else{if(el.typename==='ArtLayer'&&el.kind===LayerKind.TEXT){el.textItem.kind=TextType.POINTTEXT;el.textItem.contents=wrapText(el.textItem.contents,fmt.family==='micro'?15:60);}fit(el,z[extra.role],'center');}}else{el.visible=false;msg('OMISSAO_PROPOSTA|'+fmt.id+'|'+o.id+'|'+extra.role);}}
'''+s[e:]
s=s.replace('function sceneMask(','''function rectMask(g,r){app.activeDocument=doc;doc.activeLayer=g;doc.selection.select([[r[0],r[1]],[r[2],r[1]],[r[2],r[3]],[r[0],r[3]]]);var d=new ActionDescriptor(),ref=new ActionReference();d.putClass(charIDToTypeID('Nw  '),charIDToTypeID('Chnl'));ref.putEnumerated(charIDToTypeID('Chnl'),charIDToTypeID('Chnl'),charIDToTypeID('Msk '));d.putReference(charIDToTypeID('At  '),ref);d.putEnumerated(charIDToTypeID('Usng'),charIDToTypeID('UsrM'),charIDToTypeID('RvlS'));executeAction(charIDToTypeID('Mk  '),d,DialogModes.NO);doc.selection.deselect();}\nfunction sceneMask(''')
# Existing detail may have its own mask: wrap in fresh group before adding framing mask.
s=s.replace("rectMask(el,[ec[0]*es+ex,ec[1]*es+ey,ec[2]*es+ex,ec[3]*es+ey]);", "var frame=group(cg,'ENQUADRAMENTO · '+extra.role+' · '+o.id),marker=frame.artLayers.add();el.move(marker,ElementPlacement.PLACEBEFORE);marker.remove();rectMask(frame,[ec[0]*es+ex,ec[1]*es+ey,ec[2]*es+ex,ec[3]*es+ey]);")
with (b/'WORK/00_MATRIZ/pilot_spec_p11.json').open('x') as f:json.dump(d,f,ensure_ascii=True,indent=2)
with (b/'WORK/05_SCRIPTS/build_p11.jsx').open('x') as f:f.write(s)
with (b/'WORK/06_LOGS/build_p11_provenance.json').open('x') as f:json.dump(dict(created_at=datetime.datetime.now().astimezone().isoformat(),script_sha256=hashlib.sha256(s.encode()).hexdigest(),source='build_p10.jsx',purpose='original KV bleed geometry; source child anchors; detail framing',input='pilot_spec_p11.json',outputs=[d['output_templates'],d['output_pilots']]),f,indent=2)
print('OK|P11 source geometry correction')
