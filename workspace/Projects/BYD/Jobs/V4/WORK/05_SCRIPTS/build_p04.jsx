#target photoshop
#include "../../../../../../operacao/lib/mkroot.jsxinc"
(function(){
var ROOT=MK.root(),BASE=ROOT+'/Projects/BYD/Jobs/V4/',REFUSE_OVERWRITE=true,src=null,doc=null,oldUnits=app.preferences.rulerUnits,oldDialogs=app.displayDialogs;
var sf=new File(BASE+'WORK/00_MATRIZ/pilot_spec_p04.json');sf.open('r');var spec=eval('('+sf.read()+')');sf.close();
var log=new File(BASE+'WORK/06_LOGS/build_p04.log');if(log.exists)throw Error('REFUSE_OVERWRITE');log.open('w');
function msg(s){log.writeln(new Date().toUTCString()+'|'+s);log.close();log.open('a');}
function find(g,id){for(var i=0;i<g.layers.length;i++){var l=g.layers[i];if(l.id===id)return l;if(l.typename==='LayerSet'){var r=find(l,id);if(r)return r;}}return null;}
function box(l){var b=l.bounds;return [b[0].as('px'),b[1].as('px'),b[2].as('px'),b[3].as('px')];}
function group(parent,n){var g=parent.layerSets.add();g.name=n;return g;}
function dup(id,parent,name){app.activeDocument=src;var l=find(src,id);if(!l)throw Error('MISSING '+id);msg("DUP_START|"+id);var cp=l.duplicate(doc);msg("DUP_COPIED|"+id);app.activeDocument=doc;cp=doc.activeLayer;msg('DUP_DEST|'+cp.name+'|parent='+cp.parent.name+'|target='+parent.name);if(parent){cp.move(parent,ElementPlacement.PLACEATEND);msg('DUP_MOVED|'+id);}if(name)cp.name=name;cp.visible=true;return cp;}
function affine(l,s,dx,dy){var b=box(l);l.resize(s*100,s*100,AnchorPosition.TOPLEFT);var a=box(l);l.translate(b[0]*s+dx-a[0],b[1]*s+dy-a[1]);}
function fit(l,z,align){var b=box(l),s=Math.min(z[2]/Math.max(1,b[2]-b[0]),z[3]/Math.max(1,b[3]-b[1]));l.resize(s*100,s*100,AnchorPosition.TOPLEFT);b=box(l);var x=z[0];if(align==='center')x+=(z[2]-(b[2]-b[0]))/2;l.translate(x-b[0],z[1]-b[1]);return l;}
function savepng(n){var f=new File(BASE+'WORK/02_PILOTOS/'+n+'.png');if(f.exists)throw Error('REFUSE_OVERWRITE');doc.saveAs(f,new PNGSaveOptions(),true,Extension.LOWERCASE);msg('OK|png|'+n);}
try{
 if(app.documents.length!==0)throw Error('PREFLIGHT_DOCS_ABERTOS');app.displayDialogs=DialogModes.NO;app.preferences.rulerUnits=Units.PIXELS;
 src=app.open(new File(BASE+spec.source));
 for(var fi=0;fi<spec.formats.length;fi++){
 var fmt=spec.formats[fi],z=fmt.zones,t0=new Date().getTime();
 doc=app.documents.add(fmt.w,fmt.h,72,'BYD_TRIAL_'+fmt.id,NewDocumentMode.RGB,DocumentFill.TRANSPARENT,1,BitsPerChannelType.EIGHT,'sRGB IEC61966-2.1');
 var bg=group(doc,'BG'),car=group(doc,'VEICULO'),legal=group(doc,'LEGAL'),conds=group(doc,'CONDICIONAIS'),offer=group(doc,'OFERTA'),fix=group(doc,'FIXO'),guides=group(doc,'#GUIAS');guides.visible=false;
 var tag=dup(84,fix,'ASSINATURA');fit(tag,z.tagline,'center');
 var footer=dup(98,fix,'RODAPE');fit(footer,z.footer,'center');
 var desc=new ActionDescriptor();desc.putPath(charIDToTypeID('null'),new File(BASE+spec.logo));desc.putEnumerated(charIDToTypeID('FTcs'),charIDToTypeID('QCSt'),charIDToTypeID('Qcsa'));executeAction(charIDToTypeID('Plc '),desc,DialogModes.NO);var logo=doc.activeLayer;logo.name='LOGO';logo.move(fix,ElementPlacement.PLACEATEND);fit(logo,z.logo,'center');
 var states=[];
 for(var oi=0;oi<spec.offers.length;oi++){
  var o=spec.offers[oi],og=group(offer,o.id),cg=group(conds,'COND · '+o.id),lg=group(legal,o.id),vg=group(car,'CAR · '+o.id),bgO=group(bg,o.id);
  var cb=o.car_bounds,s=Math.min(z.car[2]/(cb[2]-cb[0]),z.car[3]/(cb[3]-cb[1])),dx=z.car[0]+(z.car[2]-(cb[2]-cb[0])*s)/2-cb[0]*s,dy=z.car[1]+(z.car[3]-(cb[3]-cb[1])*s)/2-cb[1]*s;
  var bk=dup(78,bgO,'KV');affine(bk,s,dx,dy);
  // Native KV fills remaining canvas independently without stretching.
  var bb=box(bk);if(bb[0]>0||bb[1]>0||bb[2]<fmt.w||bb[3]<fmt.h){var scale=Math.max(fmt.w/(bb[2]-bb[0]),fmt.h/(bb[3]-bb[1]));bk.resize(scale*100,scale*100,AnchorPosition.MIDDLECENTER);bb=box(bk);bk.translate(fmt.w/2-(bb[0]+bb[2])/2,fmt.h/2-(bb[1]+bb[3])/2);}
  var vehicle=dup(o.car,vg,'CENA ORIGINAL');affine(vehicle,s,dx,dy);
  var title=dup(o.title,og,'MODELO');fit(title,z.title,'left');
  var price=dup(o.price,og,'PRECO');fit(price,z.price,'left');
  var benefit=dup(o.benefit,cg,'COND · BENEFICIO · '+o.id);if(benefit.kind===LayerKind.TEXT)benefit.textItem.contents=benefit.textItem.contents.replace(/[\r\n]+/g,' ');fit(benefit,z.benefit,'left');
  var headline=dup(o.headline,cg,'COND · HEADLINE · '+o.id);headline.textItem.contents=headline.textItem.contents.replace(/[\r\n]+/g,' ');fit(headline,z.headline,'left');
  var lt=dup(o.legal,lg,'TEXTO LEGAL');lt.textItem.kind=TextType.PARAGRAPHTEXT;lt.textItem.size=UnitValue(fmt.legal_font,'px');lt.textItem.useAutoLeading=false;lt.textItem.leading=UnitValue(fmt.legal_font+1,'px');lt.textItem.width=UnitValue(z.legal[2],'px');lt.textItem.height=UnitValue(z.legal[3],'px');lt.textItem.position=[UnitValue(z.legal[0],'px'),UnitValue(z.legal[1],'px')];lt.textItem.justification=Justification.LEFT;
  if(o.id==='dolphin-mini-5l-gs'){var instal=dup(61,cg,'COND · PARCELAS · '+o.id);fit(instal,[970,84,220,55],'left');var seals=dup(67,cg,'COND · PREMIOS · '+o.id);fit(seals,z.badges,'center');var detail=dup(32,cg,'COND · DETALHE · '+o.id);detail.visible=false;msg('OMISSAO_PROPOSTA|'+fmt.id+'|'+o.id+'|detalhe rodape amarelo');}
  states.push([og,cg,lg,vg,bgO]);og.visible=false;cg.visible=false;lg.visible=false;vg.visible=false;bgO.visible=false;
 }
 for(var oi=0;oi<states.length;oi++){for(var j=0;j<states.length;j++)for(var k=0;k<states[j].length;k++)states[j][k].visible=(j===oi);savepng('p04_byd_'+spec.offers[oi].id+'_'+fmt.id);}
 var psdf=new File(BASE+'WORK/01_TEMPLATES/P04_TRIAL_'+fmt.id+'.psd');if(psdf.exists)throw Error('REFUSE_OVERWRITE');var po=new PhotoshopSaveOptions();po.layers=true;po.embedColorProfile=true;doc.saveAs(psdf,po,true,Extension.LOWERCASE);
 msg('OK|template_trial|'+fmt.id+'|elapsed_ms='+((new Date().getTime())-t0));doc.close(SaveOptions.DONOTSAVECHANGES);doc=null;
 }
 msg('OK|completed');
}catch(e){msg('ERRO|'+e.message+'|line='+e.line);}finally{if(doc)doc.close(SaveOptions.DONOTSAVECHANGES);if(src)src.close(SaveOptions.DONOTSAVECHANGES);app.preferences.rulerUnits=oldUnits;app.displayDialogs=oldDialogs;log.close();}
})();
