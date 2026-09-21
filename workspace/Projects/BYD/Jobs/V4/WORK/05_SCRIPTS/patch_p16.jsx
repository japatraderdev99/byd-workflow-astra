#target photoshop
#include "../../../../../../operacao/lib/mkroot.jsxinc"
(function(){
var ROOT=MK.root(),BASE=ROOT+'/Projects/BYD/Jobs/V4/',REFUSE_OVERWRITE=true,doc=null,oldUnits=app.preferences.rulerUnits,oldDialogs=app.displayDialogs,RUN_START=new Date().getTime();
var sf=new File(BASE+'WORK/00_MATRIZ/pilot_spec_p16.json');sf.open('r');var spec=eval('('+sf.read()+')');sf.close();
var log=new File(BASE+'WORK/06_LOGS/patch_p16.log');if(log.exists)throw Error('REFUSE_OVERWRITE');log.encoding='UTF8';log.open('w');
function msg(s){log.writeln(new Date().toUTCString()+'|'+s);log.close();log.open('a');}
function box(l){var b=l.bounds;return [b[0].as('px'),b[1].as('px'),b[2].as('px'),b[3].as('px')];}
function wrapText(t,n){var words=t.replace(/[\r\n]+/g,' ').split(/\s+/),lines=[],line='';for(var i=0;i<words.length;i++){if(line.length+words[i].length+1>n&&line){lines.push(line);line=words[i];}else line+=(line?' ':'')+words[i];}if(line)lines.push(line);return lines.join('\r');}
function byName(g,n){for(var i=0;i<g.layers.length;i++){var l=g.layers[i];if(l.name.split('\u00ac\u2211').join('\u00b7')===n)return l;if(l.typename==='LayerSet'){var r=byName(l,n);if(r)return r;}}return null;}
function fit(l,z,align){var b=box(l),s=Math.min(z[2]/Math.max(1,b[2]-b[0]),z[3]/Math.max(1,b[3]-b[1]));l.resize(s*100,s*100,AnchorPosition.TOPLEFT);b=box(l);var x=z[0];if(align==='center')x+=(z[2]-(b[2]-b[0]))/2;l.translate(x-b[0],z[1]-b[1]);return l;}

try{
if(app.documents.length!==0)throw Error('PREFLIGHT_DOCS_ABERTOS');app.preferences.rulerUnits=Units.PIXELS;app.displayDialogs=DialogModes.NO;
for(var fi=0;fi<spec.formats.length;fi++){
var fmt=spec.formats[fi],t0=new Date().getTime();
var out=new File(BASE+spec.output_templates+'P16_TRIAL_'+fmt.id+'.psd');if(out.exists)throw Error('REFUSE_OVERWRITE');
doc=app.open(new File(BASE+'WORK/01_TEMPLATES/2026-09-19-p12/P12_TRIAL_'+fmt.id+'.psd'));
if(fmt.contrast_edge){
var bg=doc.layerSets.getByName('BG');
for(var bi=0;bi<bg.layerSets.length;bi++){
var dark=null;for(var qi=0;qi<bg.layerSets[bi].layerSets.length;qi++){if(bg.layerSets[bi].layerSets[qi].name.indexOf('CONTRASTE')===0)dark=bg.layerSets[bi].layerSets[qi];}if(!dark)throw Error('MISSING_CONTRAST');
for(var di=0;di<dark.layers.length;di++)dark.layers[di].visible=false;
var shade=dark.artLayers.add();shade.name='AJUSTE CONTRASTE \xb7 azul profundo \xb7 opacidade editavel';doc.activeLayer=shade;
var color=new SolidColor();color.rgb.hexValue='061D34';doc.selection.selectAll();doc.selection.fill(color,ColorBlendMode.NORMAL,100,false);doc.selection.deselect();shade.opacity=78;for(var ci=dark.layers.length-1;ci>=0;ci--){if(dark.layers[ci].id!==shade.id)dark.layers[ci].remove();}dark.name='CONTRASTE \xb7 mascara suave';
}
}
if(fmt.family==='strip'){
var cg=doc.layerSets.getByName('CONDICIONAIS');
var ex=byName(cg,'COND \xb7 instal \xb7 dolphin-mini-5l-gs');if(ex){ex.textItem.contents=wrapText(ex.textItem.contents,15);fit(ex,fmt.zones.instal,'center');}
var dt=byName(cg,'ENQUADRAMENTO \xb7 detail \xb7 dolphin-mini-5l-gs');if(dt)dt.visible=false;msg('OMISSAO_PROPOSTA|'+fmt.id+'|detail Dolphin: insignia pequena demais; preservada oculta');
}
var groups=['OFERTA','CONDICIONAIS','LEGAL','VEICULO','BG'];
for(var oi=0;oi<spec.offers.length;oi++){
var id=spec.offers[oi].id;
for(var gi=0;gi<groups.length;gi++){var g=doc.layerSets.getByName(groups[gi]);for(var li=0;li<g.layerSets.length;li++)g.layerSets[li].visible=(g.layerSets[li].name.indexOf(id)>=0);}
var pf=new File(BASE+spec.output_pilots+'p16_byd_'+id+'_'+fmt.id+'.png');if(pf.exists)throw Error('REFUSE_OVERWRITE');var eo=new ExportOptionsSaveForWeb();eo.format=SaveDocumentType.PNG;eo.PNG8=false;eo.transparency=false;eo.includeProfile=true;doc.exportDocument(pf,ExportType.SAVEFORWEB,eo);msg('OK|png|'+id+'|'+fmt.id);
}
var po=new PhotoshopSaveOptions();po.layers=true;po.embedColorProfile=true;doc.saveAs(out,po,true,Extension.LOWERCASE);msg('OK|template_trial|'+fmt.id+'|elapsed_ms='+(new Date().getTime()-t0));doc.close(SaveOptions.DONOTSAVECHANGES);doc=null;
}
msg('OK|completed|elapsed_ms='+(new Date().getTime()-RUN_START));
}catch(e){msg('ERRO|'+e.message+'|line='+e.line);}finally{if(doc)doc.close(SaveOptions.DONOTSAVECHANGES);app.preferences.rulerUnits=oldUnits;app.displayDialogs=oldDialogs;log.close();}
})();
