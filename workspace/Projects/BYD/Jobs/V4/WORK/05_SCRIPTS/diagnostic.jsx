#target photoshop
#include "../../../../../../operacao/lib/mkroot.jsxinc"
(function(){var ROOT=MK.root(),BASE=ROOT+'/Projects/BYD/Jobs/V4/',REFUSE_OVERWRITE=true,src=null,out=null;
var log=new File(BASE+'WORK/06_LOGS/diagnostic.log');if(log.exists)throw Error('REFUSE_OVERWRITE');log.open('w');
function msg(s){log.writeln(s);log.close();log.open('a');}
function find(g,id){for(var i=0;i<g.layers.length;i++){var l=g.layers[i];if(l.id===id)return l;if(l.typename==='LayerSet'){var r=find(l,id);if(r)return r;}}return null;}
function png(d,n){var f=new File(BASE+'WORK/00_MATRIZ/'+n+'.png');if(f.exists)throw Error('REFUSE_OVERWRITE '+n);var opt=new PNGSaveOptions();d.saveAs(f,opt,true,Extension.LOWERCASE);msg('OK|'+n);}
try{if(app.documents.length!==0)throw Error('PREFLIGHT_DOCS_ABERTOS');app.displayDialogs=DialogModes.NO;
 src=app.open(new Folder(BASE+'INPUT/02_PSD_oficial todas as artes em feed').getFiles('*.psd')[0]);
 var fonts={};for(var f=0;f<app.fonts.length;f++){var nm=app.fonts[f].postScriptName;if(/SourceSans|Arial|Myriad/.test(nm))msg('FONT|'+nm);}
 var ids=[78,231,232,2952,2953,21];
 for(var i=0;i<ids.length;i++){
  out=app.documents.add(1080,1350,72,'diagnostic_'+ids[i],NewDocumentMode.RGB,DocumentFill.TRANSPARENT,1,BitsPerChannelType.EIGHT,'sRGB IEC61966-2.1');
  app.activeDocument=src;var l=find(src,ids[i]);var copy=l.duplicate(out,ElementPlacement.PLACEATBEGINNING);app.activeDocument=out;copy.visible=true;
  png(out,'asset_'+ids[i]);out.close(SaveOptions.DONOTSAVECHANGES);out=null;
 }
 msg('OK|diagnostic_completed');
}catch(e){msg('ERRO|'+e.message+'|line='+e.line);}finally{if(out)out.close(SaveOptions.DONOTSAVECHANGES);if(src)src.close(SaveOptions.DONOTSAVECHANGES);log.close();}})();
