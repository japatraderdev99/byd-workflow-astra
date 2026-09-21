from pathlib import Path
import json,hashlib,datetime
REFUSE_OVERWRITE=True
b=Path(__file__).resolve().parents[2]
d=json.loads((b/'WORK/00_MATRIZ/pilot_spec_p09.json').read_text());d['revision']='p10';d['fixed']={'tagline':84,'footer':98,'background':78}
d['output_templates']='WORK/01_TEMPLATES/2026-09-19-p10/'
d['output_pilots']='WORK/02_PILOTOS/2026-09-19-p10/'
for p in [d['output_templates'],d['output_pilots']]: (b/p).mkdir(exist_ok=False)
def fmt(w,h,z,legal,wrap,horizon,family):return dict(w=w,h=h,id=f'{w}x{h}',zones=z,legal_font=legal,headline_wrap=wrap,bg_horizon=horizon,family=family,align='left' if family=='landscape' else 'center')
d['formats']=[
fmt(1920,1080,dict(logo=[95,80,520,75],tagline=[95,195,610,45],title=[95,300,780,45],price=[95,390,770,145],benefit=[95,630,760,45],headline=[95,720,760,100],car=[950,280,900,490],legal=[95,960,1730,65],footer=[1100,880,700,45],badges=[1605,790,230,65],instal=[95,555,650,40],detail=[1100,790,450,65]),14,32,440,'landscape'),
fmt(1920,1125,dict(logo=[95,90,520,75],tagline=[95,205,610,45],title=[95,315,780,45],price=[95,405,770,145],benefit=[95,645,760,45],headline=[95,735,760,100],car=[950,305,900,490],legal=[95,1000,1730,70],footer=[1100,925,700,45],badges=[1605,825,230,65],instal=[95,570,650,40],detail=[1100,825,450,65]),14,32,465,'landscape'),
fmt(1080,1080,dict(logo=[345,45,390,60],tagline=[270,135,540,35],title=[110,210,860,36],price=[230,270,620,90],benefit=[140,775,800,35],headline=[140,830,800,42],car=[170,420,740,340],legal=[60,955,960,60],footer=[90,1030,900,30],badges=[670,890,280,40],instal=[300,380,480,27],detail=[120,885,420,50]),10,45,500,'square'),
fmt(1080,1920,dict(logo=[330,115,420,70],tagline=[230,235,620,48],title=[120,350,840,52],price=[150,440,780,130],benefit=[95,1330,890,50],headline=[95,1410,890,70],car=[95,710,890,480],legal=[85,1660,910,115],footer=[90,1810,900,60],badges=[720,1240,280,65],instal=[200,605,680,35],detail=[120,1520,650,100]),15,34,840,'portrait'),
fmt(1109,1973,dict(logo=[340,120,430,72],tagline=[235,245,640,48],title=[125,365,859,54],price=[155,455,799,132],benefit=[100,1380,909,50],headline=[100,1460,909,70],car=[100,735,909,500],legal=[90,1720,929,115],footer=[95,1870,919,60],badges=[740,1285,280,65],instal=[205,620,699,36],detail=[125,1560,650,110]),15,34,875,'portrait'),
fmt(360,80,dict(logo=[8,8,74,14],title=[95,5,150,9],price=[95,21,140,22],car=[253,15,100,50],benefit=[95,48,150,8],headline=[95,62,150,13],instal=[8,43,74,24]),0,24,None,'micro')]
d['formats'][-1]['omissions']=['tagline','footer','legal','badges','detail']
for o in d['offers']:
 o['extras']=[dict(id=61,role='instal'),dict(id=67,role='badges'),dict(id=32,role='detail')] if o['id']=='dolphin-mini-5l-gs' else []
s=(b/'WORK/05_SCRIPTS/build_p09.jsx').read_text().replace('p09','p10').replace('P09_TRIAL','P10_TRIAL')
s=s.replace("BASE+'WORK/02_PILOTOS/'", "BASE+spec.output_pilots").replace("BASE+'WORK/01_TEMPLATES/P10_TRIAL_'", "BASE+spec.output_templates+'P10_TRIAL_'")
s=s.replace("dup(84,fix,'ASSINATURA');fit(tag,z.tagline,'center');", "dup(spec.fixed.tagline,fix,'ASSINATURA');if(z.tagline)fit(tag,z.tagline,'center');else{tag.visible=false;msg('OMISSAO_PROPOSTA|'+fmt.id+'|tagline');}")
s=s.replace("dup(98,fix,'RODAPE');fit(footer,z.footer,'center');", "dup(spec.fixed.footer,fix,'RODAPE');if(z.footer)fit(footer,z.footer,'center');else{footer.visible=false;msg('OMISSAO_PROPOSTA|'+fmt.id+'|footer');}")
s=s.replace("dup(78,bgO,'KV')", "dup(spec.fixed.background,bgO,'KV')")
a=s.index('  var bk=');e=s.index('\n  var vehicle=',a)
s=s[:a]+'''  var bk=dup(spec.fixed.background,bgO,'KV');var bb=box(bk),scale=Math.max(fmt.w/(bb[2]-bb[0]),fmt.h/(bb[3]-bb[1]));if(fmt.bg_horizon!==null)scale=Math.max(scale,fmt.bg_horizon/600,(fmt.h-fmt.bg_horizon)/750);bk.resize(scale*100,scale*100,AnchorPosition.TOPLEFT);bb=box(bk);bk.translate(fmt.w/2-(bb[0]+bb[2])/2,(fmt.bg_horizon===null?-100:fmt.bg_horizon-600*scale)-bb[1]);
'''+s[e:]
s=s.replace("fit(title,z.title,'left');", "fit(title,z.title,fmt.align);")
s=s.replace("fit(price,o.id==='vd-atto-2'?[450,67,500,102]:z.price,'left');", "fit(price,z.price,fmt.align);")
s=s.replace("fit(benefit,z.benefit,'left');", "benefit.textItem.justification=fmt.align==='center'?Justification.CENTER:Justification.LEFT;fit(benefit,z.benefit,fmt.align);")
s=s.replace("fit(headline,z.headline,'left');", "headline.textItem.contents=wrapText(headline.textItem.contents,fmt.headline_wrap);headline.textItem.justification=fmt.align==='center'?Justification.CENTER:Justification.LEFT;fit(headline,z.headline,fmt.align);")
a=s.index('  var lt=');e=s.index('\n  states.push',a)
s=s[:a]+'''  var lt=dup(o.legal,lg,'TEXTO LEGAL');if(z.legal){lt.textItem.kind=TextType.PARAGRAPHTEXT;lt.textItem.size=UnitValue(fmt.legal_font,'px');lt.textItem.useAutoLeading=false;lt.textItem.leading=UnitValue(fmt.legal_font+2,'px');lt.textItem.width=UnitValue(z.legal[2],'px');lt.textItem.height=UnitValue(z.legal[3],'px');lt.textItem.position=[UnitValue(z.legal[0],'px'),UnitValue(z.legal[1],'px')];lt.textItem.justification=Justification.LEFT;}else{lt.visible=false;msg('OMISSAO_PROPOSTA|'+fmt.id+'|'+o.id+'|legal');}
  for(var ei=0;ei<o.extras.length;ei++){var extra=o.extras[ei],el=dup(extra.id,cg,'COND · '+extra.role+' · '+o.id);if(z[extra.role]){if(el.typename==='ArtLayer'&&el.kind===LayerKind.TEXT){el.textItem.kind=TextType.POINTTEXT;el.textItem.contents=wrapText(el.textItem.contents,fmt.family==='micro'?15:60);}fit(el,z[extra.role],'center');}else{el.visible=false;msg('OMISSAO_PROPOSTA|'+fmt.id+'|'+o.id+'|'+extra.role);}}
'''+s[e:]
s=s.replace('function byName(',"function wrapText(t,n){var words=t.replace(/[\\r\\n]+/g,' ').split(/\\s+/),lines=[],line='';for(var i=0;i<words.length;i++){if(line.length+words[i].length+1>n&&line){lines.push(line);line=words[i];}else line+=(line?' ':'')+words[i];}if(line)lines.push(line);return lines.join('\\r');}\nfunction byName(")
s=s.replace("z[0]-50,y=-100,r=z[0]+z[2]+50,b=doc.height.as('px')+100", "z[0]-Math.min(50,doc.width.as('px')*.025),y=-100,r=z[0]+z[2]+Math.min(50,doc.width.as('px')*.025),b=doc.height.as('px')+100")
s=s.replace('doc.selection.feather(30);',"doc.selection.feather(Math.min(30,doc.width.as('px')*.012));")
with (b/'WORK/00_MATRIZ/pilot_spec_p10.json').open('x') as f:json.dump(d,f,ensure_ascii=False,indent=2)
with (b/'WORK/05_SCRIPTS/build_p10.jsx').open('x') as f:f.write(s)
with (b/'WORK/06_LOGS/build_p10_provenance.json').open('x') as f:json.dump(dict(created_at=datetime.datetime.now().astimezone().isoformat(),source='build_p09.jsx',script_sha256=hashlib.sha256(s.encode()).hexdigest(),input_spec='WORK/00_MATRIZ/pilot_spec_p10.json',output_templates=d['output_templates'],output_pilots=d['output_pilots'],status='DRAFT_3_STATES_NOT_CANONICAL'),f,indent=2)
print('OK|P10 six format draft specs')
