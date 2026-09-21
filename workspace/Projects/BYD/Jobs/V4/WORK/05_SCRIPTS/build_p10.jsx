#target photoshop
#include "../../../../../../operacao/lib/mkroot.jsxinc"
(function(){
var RUN_START=new Date().getTime();var ROOT=MK.root(),BASE=ROOT+'/Projects/BYD/Jobs/V4/',REFUSE_OVERWRITE=true,src=null,doc=null,oldUnits=app.preferences.rulerUnits,oldDialogs=app.displayDialogs;
var sf=new File(BASE+'WORK/00_MATRIZ/pilot_spec_p10.json');sf.open('r');var spec=eval('('+sf.read()+')');sf.close();
var log=new File(BASE+'WORK/06_LOGS/build_p10.log');if(log.exists)throw Error('REFUSE_OVERWRITE');log.open('w');
function msg(s){log.writeln(new Date().toUTCString()+'|'+s);log.close();log.open('a');}
function find(g,id){for(var i=0;i<g.layers.length;i++){var l=g.layers[i];if(l.id===id)return l;if(l.typename==='LayerSet'){var r=find(l,id);if(r)return r;}}return null;}
function box(l){var b=l.bounds;return [b[0].as('px'),b[1].as('px'),b[2].as('px'),b[3].as('px')];}
function group(parent,n){var g=parent.layerSets.add();g.name=n;return g;}
function wrapText(t,n){var words=t.replace(/[\r\n]+/g,' ').split(/\s+/),lines=[],line='';for(var i=0;i<words.length;i++){if(line.length+words[i].length+1>n&&line){lines.push(line);line=words[i];}else line+=(line?' ':'')+words[i];}if(line)lines.push(line);return lines.join('\r');}
function byName(g,n){for(var i=0;i<g.layers.length;i++){var l=g.layers[i];if(l.name===n)return l;if(l.typename==='LayerSet'){var r=byName(l,n);if(r)return r;}}return null;}
function dup(id,parent,name,anchorId){app.activeDocument=doc;var targetId=parent?parent.id:null;msg('TARGET|'+targetId+'|'+parent.name);app.activeDocument=src;var l=find(src,id);if(!l)throw Error('MISSING '+id);var anchor=anchorId?find(l,anchorId):l;var anchorName=anchor.name;var sourceBox=box(anchor);msg('DUP_START|'+id);l.duplicate(doc);app.activeDocument=doc;var cp=doc.activeLayer;var destination=find(doc,targetId);msg('DUP_DEST|'+cp.name+'|id='+cp.id+'|target='+destination.name+'|id='+destination.id);if(destination){var marker=destination.artLayers.add();marker.name='TEMP_INSERT';cp.move(marker,ElementPlacement.PLACEBEFORE);marker.remove();msg('DUP_MOVED|'+id);}var destBox=box(anchorId?byName(cp,anchorName):cp);cp.translate(sourceBox[0]-destBox[0],sourceBox[1]-destBox[1]);if(name)cp.name=name;cp.visible=true;return cp;}
function affine(l,s,dx,dy,anchorName){var b=box(anchorName?byName(l,anchorName):l);l.resize(s*100,s*100,AnchorPosition.TOPLEFT);var a=box(anchorName?byName(l,anchorName):l);l.translate(b[0]*s+dx-a[0],b[1]*s+dy-a[1]);}
function fit(l,z,align){var b=box(l),s=Math.min(z[2]/Math.max(1,b[2]-b[0]),z[3]/Math.max(1,b[3]-b[1]));l.resize(s*100,s*100,AnchorPosition.TOPLEFT);b=box(l);var x=z[0];if(align==='center')x+=(z[2]-(b[2]-b[0]))/2;l.translate(x-b[0],z[1]-b[1]);return l;}
function sceneMask(g,z){app.activeDocument=doc;doc.activeLayer=g;var x=z[0]-Math.min(50,doc.width.as('px')*.025),y=-100,r=z[0]+z[2]+Math.min(50,doc.width.as('px')*.025),b=doc.height.as('px')+100;doc.selection.select([[x,y],[r,y],[r,b],[x,b]]);doc.selection.feather(Math.min(30,doc.width.as('px')*.012));var d=new ActionDescriptor(),ref=new ActionReference();d.putClass(charIDToTypeID('Nw  '),charIDToTypeID('Chnl'));ref.putEnumerated(charIDToTypeID('Chnl'),charIDToTypeID('Chnl'),charIDToTypeID('Msk '));d.putReference(charIDToTypeID('At  '),ref);d.putEnumerated(charIDToTypeID('Usng'),charIDToTypeID('UsrM'),charIDToTypeID('RvlS'));executeAction(charIDToTypeID('Mk  '),d,DialogModes.NO);doc.selection.deselect();}
function savepng(n){var f=new File(BASE+spec.output_pilots+n+'.png');if(f.exists)throw Error('REFUSE_OVERWRITE');var ex=new ExportOptionsSaveForWeb();ex.format=SaveDocumentType.PNG;ex.PNG8=false;ex.transparency=false;ex.interlaced=false;ex.includeProfile=true;doc.exportDocument(f,ExportType.SAVEFORWEB,ex);msg('OK|png|'+n);}
try{
 if(app.documents.length!==0)throw Error('PREFLIGHT_DOCS_ABERTOS');app.displayDialogs=DialogModes.NO;app.preferences.rulerUnits=Units.PIXELS;
 src=app.open(new File(BASE+spec.source));
 for(var fi=0;fi<spec.formats.length;fi++){
 var fmt=spec.formats[fi],z=fmt.zones,t0=new Date().getTime();
 doc=app.documents.add(fmt.w,fmt.h,72,'BYD_TRIAL_'+fmt.id,NewDocumentMode.RGB,DocumentFill.WHITE,1,BitsPerChannelType.EIGHT,'sRGB IEC61966-2.1');
 var bg=group(doc,'BG'),car=group(doc,'VEICULO'),legal=group(doc,'LEGAL'),conds=group(doc,'CONDICIONAIS'),offer=group(doc,'OFERTA'),fix=group(doc,'FIXO'),guides=group(doc,'#GUIAS');guides.visible=false;
 var tag=dup(spec.fixed.tagline,fix,'ASSINATURA');if(z.tagline)fit(tag,z.tagline,'center');else{tag.visible=false;msg('OMISSAO_PROPOSTA|'+fmt.id+'|tagline');}
 var footer=dup(spec.fixed.footer,fix,'RODAPE');if(z.footer)fit(footer,z.footer,'center');else{footer.visible=false;msg('OMISSAO_PROPOSTA|'+fmt.id+'|footer');}
 var desc=new ActionDescriptor();desc.putPath(charIDToTypeID('null'),new File(BASE+spec.logo));desc.putEnumerated(charIDToTypeID('FTcs'),charIDToTypeID('QCSt'),charIDToTypeID('Qcsa'));executeAction(charIDToTypeID('Plc '),desc,DialogModes.NO);var logo=doc.activeLayer;logo.name='LOGO';logo.move(fix,ElementPlacement.PLACEATEND);fit(logo,z.logo,'center');
 var states=[];
 for(var oi=0;oi<spec.offers.length;oi++){
  var o=spec.offers[oi],og=group(offer,o.id),cg=group(conds,'COND · '+o.id),lg=group(legal,o.id),vg=group(car,'CAR · '+o.id),bgO=group(bg,o.id);
  var cb=o.car_bounds,s=Math.min(z.car[2]/(cb[2]-cb[0]),z.car[3]/(cb[3]-cb[1])),dx=z.car[0]+(z.car[2]-(cb[2]-cb[0])*s)/2-cb[0]*s,dy=z.car[1]+(z.car[3]-(cb[3]-cb[1])*s)/2-cb[1]*s;
  var bk=dup(spec.fixed.background,bgO,'KV');var bb=box(bk),scale=Math.max(fmt.w/(bb[2]-bb[0]),fmt.h/(bb[3]-bb[1]));if(fmt.bg_horizon!==null)scale=Math.max(scale,fmt.bg_horizon/600,(fmt.h-fmt.bg_horizon)/750);bk.resize(scale*100,scale*100,AnchorPosition.TOPLEFT);bb=box(bk);bk.translate(fmt.w/2-(bb[0]+bb[2])/2,(fmt.bg_horizon===null?-100:fmt.bg_horizon-600*scale)-bb[1]);

  var vehicle=dup(o.car,vg,'CENA ORIGINAL',o.anchor_id);affine(vehicle,s,dx,dy,o.anchor_name);sceneMask(vg,z.car);
  var title=dup(o.title,og,'MODELO');fit(title,z.title,fmt.align);
  var price=dup(o.price,og,'PRECO');fit(price,z.price,fmt.align);
  var benefit=dup(o.benefit,cg,'COND · BENEFICIO · '+o.id);if(benefit.kind===LayerKind.TEXT){benefit.textItem.kind=TextType.POINTTEXT;benefit.textItem.contents=benefit.textItem.contents.replace(/[\r\n]+/g,' ');}benefit.textItem.justification=fmt.align==='center'?Justification.CENTER:Justification.LEFT;fit(benefit,z.benefit,fmt.align);
  var headline=dup(o.headline,cg,'COND · HEADLINE · '+o.id);headline.textItem.kind=TextType.POINTTEXT;headline.textItem.contents=headline.textItem.contents.replace(/[\r\n]+/g,' ');headline.textItem.contents=wrapText(headline.textItem.contents,fmt.headline_wrap);headline.textItem.justification=fmt.align==='center'?Justification.CENTER:Justification.LEFT;fit(headline,z.headline,fmt.align);
  var lt=dup(o.legal,lg,'TEXTO LEGAL');if(z.legal){lt.textItem.kind=TextType.PARAGRAPHTEXT;lt.textItem.size=UnitValue(fmt.legal_font,'px');lt.textItem.useAutoLeading=false;lt.textItem.leading=UnitValue(fmt.legal_font+2,'px');lt.textItem.width=UnitValue(z.legal[2],'px');lt.textItem.height=UnitValue(z.legal[3],'px');lt.textItem.position=[UnitValue(z.legal[0],'px'),UnitValue(z.legal[1],'px')];lt.textItem.justification=Justification.LEFT;}else{lt.visible=false;msg('OMISSAO_PROPOSTA|'+fmt.id+'|'+o.id+'|legal');}
  for(var ei=0;ei<o.extras.length;ei++){var extra=o.extras[ei],el=dup(extra.id,cg,'COND · '+extra.role+' · '+o.id);if(z[extra.role]){if(el.typename==='ArtLayer'&&el.kind===LayerKind.TEXT){el.textItem.kind=TextType.POINTTEXT;el.textItem.contents=wrapText(el.textItem.contents,fmt.family==='micro'?15:60);}fit(el,z[extra.role],'center');}else{el.visible=false;msg('OMISSAO_PROPOSTA|'+fmt.id+'|'+o.id+'|'+extra.role);}}

  states.push([og,cg,lg,vg,bgO]);og.visible=false;cg.visible=false;lg.visible=false;vg.visible=false;bgO.visible=false;
 }
 for(var oi=0;oi<states.length;oi++){for(var j=0;j<states.length;j++)for(var k=0;k<states[j].length;k++)states[j][k].visible=(j===oi);savepng('p10_byd_'+spec.offers[oi].id+'_'+fmt.id);}
 var psdf=new File(BASE+spec.output_templates+'P10_TRIAL_'+fmt.id+'.psd');if(psdf.exists)throw Error('REFUSE_OVERWRITE');var po=new PhotoshopSaveOptions();po.layers=true;po.embedColorProfile=true;doc.saveAs(psdf,po,true,Extension.LOWERCASE);
 msg('OK|template_trial|'+fmt.id+'|elapsed_ms='+((new Date().getTime())-t0));doc.close(SaveOptions.DONOTSAVECHANGES);doc=null;
 }
 msg('OK|completed|elapsed_ms='+((new Date().getTime())-RUN_START));
}catch(e){msg('ERRO|'+e.message+'|line='+e.line);}finally{if(doc)doc.close(SaveOptions.DONOTSAVECHANGES);if(src)src.close(SaveOptions.DONOTSAVECHANGES);app.preferences.rulerUnits=oldUnits;app.displayDialogs=oldDialogs;log.close();}
})();
