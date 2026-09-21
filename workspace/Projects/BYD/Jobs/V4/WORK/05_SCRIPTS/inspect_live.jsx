#target photoshop
#include "../../../../../../operacao/lib/mkroot.jsxinc"
(function(){
var ROOT=MK.root(), BASE=ROOT+'/Projects/BYD/Jobs/V4/', REFUSE_OVERWRITE=true;
var log=new File(BASE+'WORK/06_LOGS/photoshop_inspect.tsv');
if(log.exists)throw Error('REFUSE_OVERWRITE');
log.encoding='UTF8';log.open('w');
var doc=null, start=new Date().getTime();
try {
 if(app.documents.length!==0)throw Error('PREFLIGHT_DOCS_ABERTOS='+app.documents.length);
 app.displayDialogs=DialogModes.NO;
 var folder=new Folder(BASE+'INPUT/02_PSD_oficial todas as artes em feed');
 var inputs=folder.getFiles('*.psd'); if(inputs.length!==1)throw Error('PSD_AMBIGUO');
 doc=app.open(inputs[0]);
 log.writeln('DOC\t'+doc.width.as('px')+'\t'+doc.height.as('px')+'\t'+doc.colorProfileName);
 function walk(g,p){for(var i=0;i<g.layers.length;i++){var l=g.layers[i],path=p+'/'+l.name,b=l.bounds;
 var row=[path,l.id,l.typename,l.visible,b[0].as('px'),b[1].as('px'),b[2].as('px'),b[3].as('px')];
 if(l.typename==='ArtLayer'&&l.kind===LayerKind.TEXT){row.push(l.textItem.font);row.push(l.textItem.contents.replace(/[\r\n\t]/g,' '));}
 log.writeln(row.join('\t'));if(l.typename==='LayerSet')walk(l,path);
 }}walk(doc,'');
 log.writeln('FONTS_AVAILABLE');for(var f=0;f<app.fonts.length;f++){if(/Muller/i.test(app.fonts[f].postScriptName))log.writeln(app.fonts[f].postScriptName);}
 log.writeln('OK|inspect|elapsed_ms='+((new Date().getTime())-start));
}catch(e){log.writeln('ERRO|'+e.message+'|line='+e.line);}
finally {if(doc)doc.close(SaveOptions.DONOTSAVECHANGES);log.close();}
})();
