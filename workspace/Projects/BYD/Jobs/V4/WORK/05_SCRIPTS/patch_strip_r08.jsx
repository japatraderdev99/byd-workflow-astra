#target photoshop
#include "../../../../../../operacao/lib/mkroot.jsxinc"
/*
  R08 is a cold, single-offer correction for the R03 1920x276 strip.
  It changes only the Dolphin Mini installment conditional, saves a new PSD,
  and exports only its canonical PNG. R03 files are never overwritten.
  Run only after static review, Photoshop lock acquisition, and no open docs.
*/
(function () {
var RUN_START = new Date().getTime();
var ROOT = MK.root();
var BASE = ROOT + '/Projects/BYD/Jobs/V4/';
var REFUSE_OVERWRITE = true;
var FORMAT = '1920x276';
var OFFER_ID = 'dolphin-mini-5l-gs';
var TARGET_NAME = 'COND \u00b7 instal \u00b7 dolphin-mini-5l-gs';
var TARGET_ZONE = [970, 84, 220, 55];
var INPUT_REL = 'WORK/01_TEMPLATES/2026-09-19-r03/BYD_TPL_1920x276.psd';
var TEMPLATE_REL = 'WORK/01_TEMPLATES/2026-09-20-r08/';
var STAGING_REL = 'WORK/03_STAGING/2026-09-20-r08/';
var LOG_REL = 'WORK/06_LOGS/patch_strip_r08.log';
var doc = null, log = null;
var oldUnits = app.preferences.rulerUnits;
var oldDialogs = app.displayDialogs;

function msg(s) { log.writeln(new Date().toUTCString() + '|' + s); log.close(); log.open('a'); }
function cleanName(s) { return String(s).split('\u00ac\u2211').join('\u00b7'); }
function box(layer) { var b = layer.bounds; return [b[0].as('px'), b[1].as('px'), b[2].as('px'), b[3].as('px')]; }
function directGroup(parent, name) { var wanted = cleanName(name); for (var i = 0; i < parent.layerSets.length; i++) if (cleanName(parent.layerSets[i].name) === wanted) return parent.layerSets[i]; return null; }
function directLayer(parent, name) { var wanted = cleanName(name), hits = []; for (var i = 0; i < parent.layers.length; i++) if (cleanName(parent.layers[i].name) === wanted) hits.push(parent.layers[i]); if (hits.length !== 1) throw Error('EXACT_LAYER_COUNT|' + name + '|' + hits.length); return hits[0]; }
function wrapText(value, width) { var words = String(value).replace(/[\r\n]+/g, ' ').replace(/^\s+|\s+$/g, '').split(/\s+/); var lines = [], line = ''; for (var i = 0; i < words.length; i++) { var candidate = line ? line + ' ' + words[i] : words[i]; if (line && candidate.length > width) { lines.push(line); line = words[i]; } else line = candidate; } if (line) lines.push(line); return lines.join('\r'); }
function fitProportional(layer, zone) { var before = box(layer), width = Math.max(1, before[2] - before[0]), height = Math.max(1, before[3] - before[1]); var scale = Math.min(zone[2] / width, zone[3] / height); layer.resize(scale * 100, scale * 100, AnchorPosition.TOPLEFT); var after = box(layer), afterWidth = after[2] - after[0], afterHeight = after[3] - after[1]; var x = zone[0] + (zone[2] - afterWidth) / 2, y = zone[1] + (zone[3] - afterHeight) / 2; layer.translate(x - after[0], y - after[1]); return box(layer); }
function verifyInZone(layer, zone) { var b = box(layer), x2 = zone[0] + zone[2], y2 = zone[1] + zone[3], tolerance = 2; if (!layer.visible) throw Error('TARGET_HIDDEN'); if (b[0] < zone[0] - tolerance || b[1] < zone[1] - tolerance || b[2] > x2 + tolerance || b[3] > y2 + tolerance) throw Error('TARGET_OUTSIDE_ZONE|' + b.join(',') + '|' + zone.join(',')); return b; }
function requireFolder(rel) { var f = new Folder(BASE + rel); if (!f.exists && !f.create()) throw Error('CANNOT_CREATE_OUTPUT_FOLDER|' + rel); return f; }
function stateName(top, offer) { if (top === 'CONDICIONAIS') return 'COND \u00b7 ' + offer; if (top === 'VEICULO') return 'CAR \u00b7 ' + offer; return offer; }
function verifyTwentyStates() { var tops = ['BG', 'VEICULO', 'LEGAL', 'CONDICIONAIS', 'OFERTA']; for (var ti = 0; ti < tops.length; ti++) { var top = doc.layerSets.getByName(tops[ti]); if (top.layerSets.length !== 20) throw Error('STATE_COUNT|' + tops[ti] + '|' + top.layerSets.length); } if (!doc.layerSets.getByName('FIXO') || !doc.layerSets.getByName('#GUIAS')) throw Error('MISSING_FIXED_OR_GUIDES'); }
function activate(offer) { var tops = ['BG', 'VEICULO', 'LEGAL', 'CONDICIONAIS', 'OFERTA']; for (var ti = 0; ti < tops.length; ti++) { var top = doc.layerSets.getByName(tops[ti]), wanted = stateName(tops[ti], offer), matches = 0; for (var i = 0; i < top.layerSets.length; i++) { var isWanted = cleanName(top.layerSets[i].name) === wanted; top.layerSets[i].visible = isWanted; if (isWanted) matches++; } if (matches !== 1) throw Error('ACTIVATE_STATE_COUNT|' + tops[ti] + '|' + offer + '|' + matches); } doc.layerSets.getByName('#GUIAS').visible = false; }
function exportPNG(file) { if (file.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE|' + file.fsName); var options = new ExportOptionsSaveForWeb(); options.format = SaveDocumentType.PNG; options.PNG8 = false; options.transparency = false; options.interlaced = false; options.includeProfile = true; doc.exportDocument(file, ExportType.SAVEFORWEB, options); }

try {
 log = new File(BASE + LOG_REL);
 if (log.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE|' + LOG_REL);
 log.encoding = 'UTF8'; log.open('w');
 if (app.documents.length !== 0) throw Error('PREFLIGHT_DOCS_ABERTOS');
 requireFolder(TEMPLATE_REL); requireFolder(STAGING_REL);
 var input = new File(BASE + INPUT_REL);
 var outPSD = new File(BASE + TEMPLATE_REL + 'BYD_TPL_1920x276.psd');
 var outPNG = new File(BASE + STAGING_REL + 'byd_dolphin-mini-5l-gs_1920x276.png');
 if (!input.exists) throw Error('MISSING_R03_STRIP');
 if ((outPSD.exists || outPNG.exists) && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE|R08_OUTPUT');
 msg('SCRIPT_PREPARED|patch_strip_r08.jsx|source=' + INPUT_REL + '|format=' + FORMAT + '|offer=' + OFFER_ID + '|ascii_source=true');
 app.preferences.rulerUnits = Units.PIXELS; app.displayDialogs = DialogModes.NO;
 doc = app.open(input);
 if (doc.width.as('px') !== 1920 || doc.height.as('px') !== 276) throw Error('DIMENSION_MISMATCH|' + doc.width.as('px') + 'x' + doc.height.as('px'));
 if (doc.layerComps.length !== 20) throw Error('LAYER_COMP_COUNT_BEFORE|' + doc.layerComps.length);
 verifyTwentyStates();
 var conditionalRoot = doc.layerSets.getByName('CONDICIONAIS');
 var conditionalState = directGroup(conditionalRoot, 'COND \u00b7 dolphin-mini-5l-gs');
 if (!conditionalState) throw Error('MISSING_DOLPHIN_CONDITIONAL_STATE');
 var installment = directLayer(conditionalState, TARGET_NAME);
 if (installment.typename !== 'ArtLayer' || installment.kind !== LayerKind.TEXT) throw Error('TARGET_NOT_EDITABLE_TEXT');
 try { installment.unlink(); msg('TARGET_UNLINKED|' + installment.id); } catch (unlinkError) { msg('TARGET_UNLINK_NOT_NEEDED|' + installment.id); }
 var original = installment.textItem.contents;
 var normalized = original.replace(/[\r\n]+/g, ' ').replace(/^\s+|\s+$/g, '');
 var wrapped = wrapText(normalized, 15);
 installment.textItem.kind = TextType.POINTTEXT;
 installment.textItem.contents = wrapped;
 installment.textItem.justification = Justification.CENTER;
 installment.visible = true;
 var fitted = fitProportional(installment, TARGET_ZONE);
 var verified = verifyInZone(installment, TARGET_ZONE);
 var lineCount = wrapped.split('\r').length;
 if (lineCount < 2) throw Error('WRAP_NOT_APPLIED|' + lineCount);
 msg('PATCH_OK|' + OFFER_ID + '|original=' + normalized + '|wrapped=' + wrapped.split('\r').join('/') + '|lines=' + lineCount + '|bounds=' + verified.join(',') + '|zone=' + TARGET_ZONE.join(','));
 if (doc.layerComps.length !== 20) throw Error('LAYER_COMP_COUNT_AFTER_PATCH|' + doc.layerComps.length);
 var saveOptions = new PhotoshopSaveOptions(); saveOptions.layers = true; saveOptions.embedColorProfile = true;
 doc.saveAs(outPSD, saveOptions, true, Extension.LOWERCASE);
 if (doc.layerComps.length !== 20) throw Error('LAYER_COMP_COUNT_AFTER_SAVE|' + doc.layerComps.length);
 msg('OK|template|' + FORMAT + '|states=20|layer_comps=' + doc.layerComps.length + '|elapsed_ms=' + (new Date().getTime() - RUN_START));
 activate(OFFER_ID);
 exportPNG(outPNG);
 msg('OK|png|' + FORMAT + '|' + OFFER_ID + '|canonical=' + outPNG.name + '|elapsed_ms=' + (new Date().getTime() - RUN_START));
 msg('OK|completed|changed_layers=1|source_r03_preserved=true|r03_other_pngs_untouched=true|elapsed_ms=' + (new Date().getTime() - RUN_START));
} catch (e) {
 if (log) msg('ERRO|' + e.message + '|line=' + e.line);
} finally {
 if (doc) doc.close(SaveOptions.DONOTSAVECHANGES);
 app.preferences.rulerUnits = oldUnits; app.displayDialogs = oldDialogs;
 if (log) log.close();
}
})();
