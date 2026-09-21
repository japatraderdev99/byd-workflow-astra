#target photoshop
#include "../../../../../../operacao/lib/mkroot.jsxinc"
/*
  PROVENANCE
  Micro-only correction after build_production_r03.jsx.
  Authority: WORK/04_QA/micro_commercial_conditions_r04.json.
  Keeps R03 immutable and writes only the R04 360x80 template and renders.
  Prepared only. Static review and the Photoshop lock are required before run.
*/
(function () {
var RUN_START = new Date().getTime();
var ROOT = MK.root(), BASE = ROOT + '/Projects/BYD/Jobs/V4/';
var REFUSE_OVERWRITE = true, doc = null;
var oldUnits = app.preferences.rulerUnits, oldDialogs = app.displayDialogs;
var LOG_REL = 'WORK/06_LOGS/patch_micro_r04.log';
var INPUT_REL = 'WORK/01_TEMPLATES/2026-09-19-r03/BYD_TPL_360x80.psd';
var TPL_REL = 'WORK/01_TEMPLATES/2026-09-19-r04/';
var PNG_REL = 'WORK/03_STAGING/2026-09-19-r04/';
var log = new File(BASE + LOG_REL);
if (log.exists) throw Error('REFUSE_OVERWRITE');
log.encoding = 'UTF8'; log.open('w');

function msg(s) { log.writeln(new Date().toUTCString() + '|' + s); log.close(); log.open('a'); }
function readJSON(rel) { var f = new File(BASE + rel); if (!f.exists) throw Error('MISSING_JSON|' + rel); f.encoding = 'UTF8'; f.open('r'); var v = eval('(' + f.read() + ')'); f.close(); return v; }
function cleanName(s) { return String(s).split('\u00ac\u2211').join('\u00b7'); }
function find(g, id) { if (!g || !g.layers) return null; for (var i = 0; i < g.layers.length; i++) { var l = g.layers[i]; if (l.id === id) return l; if (l.typename === 'LayerSet') { var r = find(l, id); if (r) return r; } } return null; }
function byName(g, n) { if (!g || !g.layers) return null; n = cleanName(n); for (var i = 0; i < g.layers.length; i++) { var l = g.layers[i]; if (cleanName(l.name) === n) return l; if (l.typename === 'LayerSet') { var r = byName(l, n); if (r) return r; } } return null; }
function directGroup(g, n) { n = cleanName(n); for (var i = 0; i < g.layerSets.length; i++) if (cleanName(g.layerSets[i].name) === n) return g.layerSets[i]; return null; }
function box(l) { var b = l.bounds; return [b[0].as('px'), b[1].as('px'), b[2].as('px'), b[3].as('px')]; }
function fit(id, z, align) { var l = find(doc, id); if (!l) throw Error('FIT_ID_NOT_FOUND|' + id); var b = box(l), s = Math.min(z[2] / Math.max(1, b[2] - b[0]), z[3] / Math.max(1, b[3] - b[1])); l.resize(s * 100, s * 100, AnchorPosition.TOPLEFT); l = find(doc, id); b = box(l); var x = z[0]; if (align === 'center') x += (z[2] - (b[2] - b[0])) / 2; l.translate(x - b[0], z[1] - b[1]); }
function verify(label, id, z, offerId) { var l = find(doc, id), b = box(l), x2 = z[0] + z[2], y2 = z[1] + z[3]; msg('GEOM|360x80|' + offerId + '|' + label + '|bounds=' + b.join(',') + '|zone=' + z.join(',') + '|visible=' + l.visible); if (!l.visible) throw Error('PATCH_LAYER_HIDDEN|' + offerId + '|' + label); if (b[0] < z[0] - 2 || b[1] < z[1] - 2 || b[2] > x2 + 2 || b[3] > y2 + 2) throw Error('GEOM_OUTSIDE_ZONE|' + offerId + '|' + label); }
function expectedName(top, id) { if (top === 'CONDICIONAIS') return 'COND \u00b7 ' + id; if (top === 'VEICULO') return 'CAR \u00b7 ' + id; return id; }
function activate(offerId) { var tops = ['OFERTA', 'CONDICIONAIS', 'LEGAL', 'VEICULO', 'BG']; for (var ti = 0; ti < tops.length; ti++) { var top = doc.layerSets.getByName(tops[ti]), wanted = expectedName(tops[ti], offerId), found = 0; for (var gi = 0; gi < top.layerSets.length; gi++) { var yes = cleanName(top.layerSets[gi].name) === wanted; top.layerSets[gi].visible = yes; if (yes) found++; } if (found !== 1) throw Error('STATE_GROUP_COUNT|' + offerId + '|' + tops[ti] + '|' + found); } doc.layerSets.getByName('#GUIAS').visible = false; }
function removeLayerComps() { while (doc.layerComps.length) doc.layerComps[doc.layerComps.length - 1].remove(); }
function exportPNG(f, label) { if (f.exists) throw Error('REFUSE_OVERWRITE|' + f.fsName); var eo = new ExportOptionsSaveForWeb(); eo.format = SaveDocumentType.PNG; eo.PNG8 = false; eo.transparency = false; eo.interlaced = false; eo.includeProfile = true; doc.exportDocument(f, ExportType.SAVEFORWEB, eo); msg('OK|png|' + label); }
function requireFolder(rel) { var f = new Folder(BASE + rel); if (!f.exists) throw Error('MISSING_OUTPUT_FOLDER|' + rel); }

try {
 if (app.documents.length !== 0) throw Error('PREFLIGHT_DOCS_ABERTOS');
 var spec = readJSON('WORK/00_MATRIZ/production_spec_r03.json');
 var correction = readJSON('WORK/04_QA/micro_commercial_conditions_r04.json');
 if (!spec.offers || spec.offers.length !== 20) throw Error('EXPECTED_20_OFFERS');
 if (!correction.offer_ids || correction.offer_ids.length !== 5) throw Error('EXPECTED_5_PATCH_OFFERS');
 requireFolder(TPL_REL); requireFolder(PNG_REL);
 var input = new File(BASE + INPUT_REL); if (!input.exists) throw Error('MISSING_R03_MICRO_TEMPLATE');
 var outPSD = new File(BASE + TPL_REL + 'BYD_TPL_360x80.psd');
 var outPreview = new File(BASE + TPL_REL + 'BYD_TPL_360x80_preview.png');
 if (outPSD.exists || outPreview.exists) throw Error('REFUSE_OVERWRITE|R04_TEMPLATE_OR_PREVIEW');
 for (var pi = 0; pi < spec.offers.length; pi++) if (new File(BASE + PNG_REL + 'byd_' + spec.offers[pi].id + '_360x80.png').exists) throw Error('REFUSE_OVERWRITE|' + spec.offers[pi].id);
 msg('SCRIPT_PREPARED|patch_micro_r04.jsx|source=R03_360x80|authority=micro_commercial_conditions_r04.json|review_required=true');
 app.preferences.rulerUnits = Units.PIXELS; app.displayDialogs = DialogModes.NO;
 doc = app.open(input);
 var patched = {}, patchCount = 0;
 for (var ci = 0; ci < correction.offer_ids.length; ci++) {
  var id = correction.offer_ids[ci], og = directGroup(doc.layerSets.getByName('OFERTA'), id), cg = directGroup(doc.layerSets.getByName('CONDICIONAIS'), 'COND \u00b7 ' + id);
  if (patched[id]) throw Error('DUPLICATE_PATCH_ID|' + id);
  if (!og || !cg) throw Error('PATCH_STATE_NOT_FOUND|' + id);
  var price = byName(og, 'PRECO'), benefit = byName(cg, 'COND \u00b7 BENEFICIO \u00b7 ' + id), headline = byName(cg, 'COND \u00b7 HEADLINE \u00b7 ' + id);
  if (!price || !benefit || !headline) throw Error('PATCH_ELEMENT_NOT_FOUND|' + id);
  if (headline.typename !== 'ArtLayer' || headline.kind !== LayerKind.TEXT) throw Error('PATCH_HEADLINE_NOT_TEXT|' + id);
  var singleLine = headline.textItem.contents.replace(/\r\n/g, ' ').replace(/[\r\n]/g, ' ');
  headline.textItem.contents = singleLine;
  benefit.visible = true; headline.visible = true;
  fit(price.id, correction.zones.price, 'left'); fit(benefit.id, correction.zones.benefit, 'center'); fit(headline.id, correction.zones.headline, 'center');
  verify('price', price.id, correction.zones.price, id); verify('benefit', benefit.id, correction.zones.benefit, id); verify('headline', headline.id, correction.zones.headline, id);
  msg('PATCH_OK|' + id + '|headline_chars=' + singleLine.length); patched[id] = true; patchCount++;
 }
 if (patchCount !== 5) throw Error('PATCH_COUNT_MISMATCH|' + patchCount);
 removeLayerComps();
 for (var li = 0; li < spec.offers.length; li++) { var offerId = spec.offers[li].id; activate(offerId); doc.layerComps.add('OFERTA ' + offerId, 'offer_id=' + offerId + (patched[offerId] ? '|micro_r04_dual=true' : ''), true, false, false); }
 if (doc.layerComps.length !== 20) throw Error('LAYER_COMP_COUNT|' + doc.layerComps.length);
 activate(spec.offers[0].id);
 var po = new PhotoshopSaveOptions(); po.layers = true; po.embedColorProfile = true; doc.saveAs(outPSD, po, true, Extension.LOWERCASE); msg('OK|template|360x80|layer_comps=' + doc.layerComps.length);
 doc.layerSets.getByName('#GUIAS').visible = true; exportPNG(outPreview, 'preview|360x80|' + spec.offers[0].id); doc.layerSets.getByName('#GUIAS').visible = false;
 for (var oi = 0; oi < spec.offers.length; oi++) { var exportStart = new Date().getTime(), oid = spec.offers[oi].id; activate(oid); exportPNG(new File(BASE + PNG_REL + 'byd_' + oid + '_360x80.png'), oid + '|360x80'); msg('OFFER_EXPORT_OK|360x80|' + oid + '|elapsed_ms=' + (new Date().getTime() - exportStart)); }
 msg('OK|completed|patched=5|states=20|pngs=20|elapsed_ms=' + (new Date().getTime() - RUN_START));
} catch (e) {
 if (log) msg('ERRO|' + e.message + '|line=' + e.line);
} finally {
 if (doc) doc.close(SaveOptions.DONOTSAVECHANGES);
 app.preferences.rulerUnits = oldUnits; app.displayDialogs = oldDialogs;
 if (log) log.close();
}
})();
