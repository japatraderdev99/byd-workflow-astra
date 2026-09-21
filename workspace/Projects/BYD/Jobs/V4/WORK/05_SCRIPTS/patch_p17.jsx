#target photoshop
#include "../../../../../../operacao/lib/mkroot.jsxinc"
(function(){var ROOT=MK.root(),BASE=ROOT+'/Projects/BYD/Jobs/V4/',REFUSE_OVERWRITE=true,doc=null,oldUnits=app.preferences.rulerUnits,oldDialogs=app.displayDialogs,start=new Date().getTime();
var log=new File(BASE+'WORK/06_LOGS/patch_p17.log');if(log.exists)throw Error('REFUSE_OVERWRITE');log.encoding='UTF8';log.open('w');function msg(s){log.writeln(new Date().toUTCString()+'|'+s);log.close();log.open('a');}
function box(l){var b=l.bounds;return [b[0].as('px'),b[1].as('px'),b[2].as('px'),b[3].as('px')];}
function wrapText(t,n){var words=t.replace(/[\r\n]+/g,' ').split(/\s+/),lines=[],line='';for(var i=0;i<words.length;i++){if(line.length+words[i].length+1>n&&line){lines.push(line);line=words[i];}else line+=(line?' ':'')+words[i];}if(line)lines.push(line);return lines.join('\r');}
function byName(g,n){for(var i=0;i<g.layers.length;i++){var l=g.layers[i];if(l.name.split('\u00ac\u2211').join('\u00b7')===n)return l;if(l.typename==='LayerSet'){var r=byName(l,n);if(r)return r;}}return null;}
function fit(l,z,align){var b=box(l),s=Math.min(z[2]/Math.max(1,b[2]-b[0]),z[3]/Math.max(1,b[3]-b[1]));l.resize(s*100,s*100,AnchorPosition.TOPLEFT);b=box(l);var x=z[0];if(align==='center')x+=(z[2]-(b[2]-b[0]))/2;l.translate(x-b[0],z[1]-b[1]);return l;}

try{if(app.documents.length)throw Error('PREFLIGHT_DOCS_ABERTOS');app.preferences.rulerUnits=Units.PIXELS;app.displayDialogs=DialogModes.NO;
var out=new File(BASE+'WORK/01_TEMPLATES/2026-09-19-p17/P17_TRIAL_360x80.psd');if(out.exists)throw Error('REFUSE_OVERWRITE');
doc=app.open(new File(BASE+'WORK/01_TEMPLATES/2026-09-19-p16/P16_TRIAL_360x80.psd'));
var fix=doc.layerSets.getByName('FIXO'),footer=byName(fix,'RODAPE');footer.visible=true;
var band=fix.artLayers.add();band.name='FUNDO FAIXA SELOS';doc.activeLayer=band;var color=new SolidColor();color.rgb.hexValue='071D31';doc.selection.select([[0,57],[360,57],[360,80],[0,80]]);doc.selection.fill(color);doc.selection.deselect();band.move(footer,ElementPlacement.PLACEAFTER);
fit(byName(footer,'SELOS GARANTIA E RECOMPRA'),[7,61,96,15],'left');
fit(byName(footer,'brasil'),[108,60,36,17],'center');
fit(byName(footer,'Clientes Satisfeitos Negativo'),[150,60,19,17],'center');
var ib=byName(footer,'IBAMA');fit(byName(ib,'Vector Smart Object copy'),[176,61,13,16],'center');
var educational=null;for(var ti=0;ti<ib.artLayers.length;ti++)if(ib.artLayers[ti].kind===LayerKind.TEXT)educational=ib.artLayers[ti];if(!educational)throw Error('MISSING_TRAFFIC_MESSAGE');
educational.textItem.kind=TextType.POINTTEXT;fit(educational,[194,66,159,9],'left');msg('OK|mensagem|'+educational.textItem.contents+'|bounds='+box(educational).join(','));
var ids=['yuan-plus-awd-26-27','dolphin-mini-5l-gs','vd-atto-2'],groups=['OFERTA','CONDICIONAIS','LEGAL','VEICULO','BG'];
for(var oi=0;oi<ids.length;oi++){var id=ids[oi];for(var gi=0;gi<groups.length;gi++){var g=doc.layerSets.getByName(groups[gi]);for(var li=0;li<g.layerSets.length;li++){var nm=g.layerSets[li].name.split('\u00ac\u2211').join('\u00b7');g.layerSets[li].visible=(nm===id||nm==='COND \u00b7 '+id||nm==='CAR \u00b7 '+id);}}
var cg=doc.layerSets.getByName('CONDICIONAIS'),be=byName(cg,'COND \u00b7 BENEFICIO \u00b7 '+id),he=byName(cg,'COND \u00b7 HEADLINE \u00b7 '+id);fit(id.indexOf('vd-')===0?he:be,[95,46,255,8],'center');be.visible=id.indexOf('vd-')!==0;he.visible=id.indexOf('vd-')===0;
if(id==='dolphin-mini-5l-gs'){var badges=byName(cg,'COND \u00b7 badges \u00b7 '+id);badges.visible=true;fit(badges,[8,23,77,12],'center');var ins=byName(cg,'COND \u00b7 instal \u00b7 '+id);ins.textItem.contents=wrapText(ins.textItem.contents,16);fit(ins,[8,38,77,17],'left');}
var f=new File(BASE+'WORK/02_PILOTOS/2026-09-19-p17/p17_byd_'+id+'_360x80.png');if(f.exists)throw Error('REFUSE_OVERWRITE');var eo=new ExportOptionsSaveForWeb();eo.format=SaveDocumentType.PNG;eo.PNG8=false;eo.transparency=false;eo.includeProfile=true;doc.exportDocument(f,ExportType.SAVEFORWEB,eo);msg('OK|png|'+id);
}
var po=new PhotoshopSaveOptions();po.layers=true;po.embedColorProfile=true;doc.saveAs(out,po,true,Extension.LOWERCASE);msg('OK|completed|elapsed_ms='+(new Date().getTime()-start));
}catch(e){msg('ERRO|'+e.message+'|line='+e.line);}finally{if(doc)doc.close(SaveOptions.DONOTSAVECHANGES);app.preferences.rulerUnits=oldUnits;app.displayDialogs=oldDialogs;log.close();}})();
