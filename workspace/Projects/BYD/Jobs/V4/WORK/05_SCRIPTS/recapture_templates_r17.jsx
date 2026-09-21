#target photoshop
#include "../../../../../../operacao/lib/mkroot.jsxinc"
/*
  R17 repairs only the Layer Comp visibility snapshots in the seven approved
  BYD templates. It does not export PNGs and does not change layer geometry,
  text, masks, effects, or approved raster output.

  Root cause: production builds called LayerComps.add(name, comment, true,
  false, false). The three booleans are appearance, position, visibility, so
  those comps recorded appearance and did not record visibility.

  R17 activates each offer by exact direct-child names, replaces the invalid
  comps with visibility-only comps using false, false, true, tests every comp
  against a deliberately different state, saves a new copy, reopens it, and
  repeats all 20 apply tests to prove persistence.

  Prepared cold. Requires Photoshop lock and static check before execution.
*/
(function () {
var RUN_START = new Date().getTime();
var ROOT = MK.root();
var BASE = ROOT + '/Projects/BYD/Jobs/V4/';
var REFUSE_OVERWRITE = true;
var LOG_REL = 'WORK/06_LOGS/recapture_templates_r17.log';
var SPEC_REL = 'WORK/00_MATRIZ/production_spec_r10.json';
var OUT_REL = 'WORK/01_TEMPLATES/2026-09-20-r17/';
var formats = [
 { id: '1920x276', w: 1920, h: 276, source: 'WORK/01_TEMPLATES/2026-09-20-r14/BYD_TPL_1920x276.psd', sourceRevision: 'r14_exception_strip' },
 { id: '1920x1080', w: 1920, h: 1080, source: 'WORK/01_TEMPLATES/2026-09-20-r16/BYD_TPL_1920x1080.psd', sourceRevision: 'r16' },
 { id: '1920x1125', w: 1920, h: 1125, source: 'WORK/01_TEMPLATES/2026-09-20-r16/BYD_TPL_1920x1125.psd', sourceRevision: 'r16' },
 { id: '1080x1080', w: 1080, h: 1080, source: 'WORK/01_TEMPLATES/2026-09-20-r10/BYD_TPL_1080x1080.psd', sourceRevision: 'r10' },
 { id: '1080x1920', w: 1080, h: 1920, source: 'WORK/01_TEMPLATES/2026-09-20-r16/BYD_TPL_1080x1920.psd', sourceRevision: 'r16' },
 { id: '1109x1973', w: 1109, h: 1973, source: 'WORK/01_TEMPLATES/2026-09-20-r16/BYD_TPL_1109x1973.psd', sourceRevision: 'r16' },
 { id: '360x80', w: 360, h: 80, source: 'WORK/01_TEMPLATES/2026-09-20-r10/BYD_TPL_360x80.psd', sourceRevision: 'r10' }
];
var TOPS = ['OFERTA', 'CONDICIONAIS', 'LEGAL', 'VEICULO', 'BG'];
var doc = null;
var log = null;
var oldDialogs = app.displayDialogs;

function msg(s) { if (log) { log.writeln(new Date().toUTCString() + '|' + s); log.close(); log.open('a'); } }
function readJSON(rel) { var f = new File(BASE + rel); if (!f.exists) throw Error('MISSING_JSON|' + rel); f.encoding = 'UTF8'; if (!f.open('r')) throw Error('OPEN_JSON_FAILED|' + rel); var value = eval('(' + f.read() + ')'); f.close(); return value; }
function cleanName(value) { return String(value).split('\u00ac\u2211').join('\u00b7'); }
function expectedName(top, offerId) { if (top === 'CONDICIONAIS') return 'COND \u00b7 ' + offerId; if (top === 'VEICULO') return 'CAR \u00b7 ' + offerId; return offerId; }
function exactRootGroup(name) { var hits = []; for (var i = 0; i < doc.layerSets.length; i++) if (cleanName(doc.layerSets[i].name) === cleanName(name)) hits.push(doc.layerSets[i]); if (hits.length !== 1) throw Error('ROOT_GROUP_COUNT|' + name + '|' + hits.length); return hits[0]; }
function exactDirectGroup(parent, name) { var hits = []; for (var i = 0; i < parent.layerSets.length; i++) if (cleanName(parent.layerSets[i].name) === cleanName(name)) hits.push(parent.layerSets[i]); if (hits.length !== 1) throw Error('DIRECT_GROUP_COUNT|' + parent.name + '|' + name + '|' + hits.length); return hits[0]; }
function compByName(name) { var found = null, count = 0; for (var i = 0; i < doc.layerComps.length; i++) if (doc.layerComps[i].name === name) { found = doc.layerComps[i]; count++; } if (count !== 1) throw Error('LAYER_COMP_NAME_COUNT|' + name + '|' + count); return found; }
function validateOfferIds(offers) {
 if (!offers || offers.length !== 20) throw Error('OFFER_COUNT|' + (offers ? offers.length : 0));
 var seen = {};
 for (var i = 0; i < offers.length; i++) { var id = offers[i].id; if (!id || seen[id]) throw Error('INVALID_OR_DUPLICATE_OFFER_ID|' + id); seen[id] = true; }
}
function validateDocument(fmt, offers) {
 if (doc.width.as('px') !== fmt.w || doc.height.as('px') !== fmt.h) throw Error('DIMENSION_MISMATCH|' + fmt.id + '|' + doc.width.as('px') + 'x' + doc.height.as('px'));
 if (doc.mode !== DocumentMode.RGB) throw Error('DOCUMENT_NOT_RGB|' + fmt.id);
 exactRootGroup('FIXO'); exactRootGroup('#GUIAS');
 if (!exactRootGroup('FIXO').visible) throw Error('FIXO_HIDDEN|' + fmt.id);
 for (var ti = 0; ti < TOPS.length; ti++) {
  var top = exactRootGroup(TOPS[ti]);
  if (top.layerSets.length !== offers.length) throw Error('STATE_COUNT|' + fmt.id + '|' + TOPS[ti] + '|' + top.layerSets.length);
  for (var oi = 0; oi < offers.length; oi++) exactDirectGroup(top, expectedName(TOPS[ti], offers[oi].id));
 }
}
function activate(offerId) {
 for (var ti = 0; ti < TOPS.length; ti++) {
  var top = exactRootGroup(TOPS[ti]);
  top.visible = true;
  var wanted = expectedName(TOPS[ti], offerId), found = 0;
  for (var gi = 0; gi < top.layerSets.length; gi++) { var yes = cleanName(top.layerSets[gi].name) === wanted; top.layerSets[gi].visible = yes; if (yes) found++; }
  if (found !== 1) throw Error('ACTIVATE_STATE_COUNT|' + TOPS[ti] + '|' + offerId + '|' + found);
 }
 exactRootGroup('#GUIAS').visible = false;
 verifyActive(offerId, 'activate');
}
function verifyActive(offerId, phase) {
 for (var ti = 0; ti < TOPS.length; ti++) {
  var top = exactRootGroup(TOPS[ti]), wanted = expectedName(TOPS[ti], offerId), visibleCount = 0, visibleName = '';
  if (!top.visible) throw Error('TOP_HIDDEN|' + phase + '|' + TOPS[ti] + '|' + offerId);
  for (var gi = 0; gi < top.layerSets.length; gi++) if (top.layerSets[gi].visible) { visibleCount++; visibleName = cleanName(top.layerSets[gi].name); }
  if (visibleCount !== 1 || visibleName !== wanted) throw Error('ACTIVE_STATE_MISMATCH|' + phase + '|' + TOPS[ti] + '|expected=' + wanted + '|count=' + visibleCount + '|actual=' + visibleName);
 }
 if (exactRootGroup('#GUIAS').visible) throw Error('GUIDES_VISIBLE|' + phase + '|' + offerId);
}
function removeExistingComps(fmtId) {
 var before = doc.layerComps.length;
 for (var i = before - 1; i >= 0; i--) doc.layerComps[i].remove();
 if (doc.layerComps.length !== 0) throw Error('LAYER_COMP_REMOVE_FAILED|' + fmtId + '|' + doc.layerComps.length);
 msg('INVALID_COMPS_REMOVED|' + fmtId + '|count=' + before);
}
function makeComps(fmtId, offers) {
 for (var i = 0; i < offers.length; i++) {
  var id = offers[i].id;
  activate(id);
  doc.layerComps.add('OFERTA ' + id, 'offer_id=' + id + '|r17_visibility_only=true', false, false, true);
  var comp = compByName('OFERTA ' + id);
  if (comp.appearance !== false || comp.position !== false || comp.visibility !== true) throw Error('LAYER_COMP_FLAGS|' + fmtId + '|' + id + '|appearance=' + comp.appearance + '|position=' + comp.position + '|visibility=' + comp.visibility);
 }
 if (doc.layerComps.length !== offers.length) throw Error('LAYER_COMP_COUNT_AFTER_CREATE|' + fmtId + '|' + doc.layerComps.length);
}
function testAllComps(fmtId, offers, phase) {
 for (var i = 0; i < offers.length; i++) {
  var target = offers[i].id, decoy = offers[(i + 1) % offers.length].id;
  activate(decoy);
  var comp = compByName('OFERTA ' + target);
  if (comp.appearance !== false || comp.position !== false || comp.visibility !== true) throw Error('LAYER_COMP_FLAGS|' + phase + '|' + fmtId + '|' + target);
  comp.apply();
  verifyActive(target, phase + '|apply');
  msg('COMP_APPLY_OK|' + phase + '|' + fmtId + '|' + target + '|decoy=' + decoy);
 }
}
function preflight(offers) {
 var outDir = new Folder(BASE + OUT_REL);
 if (!outDir.exists) throw Error('MISSING_OUTPUT_FOLDER|' + OUT_REL);
 for (var i = 0; i < formats.length; i++) {
  var input = new File(BASE + formats[i].source), output = new File(BASE + OUT_REL + 'BYD_TPL_' + formats[i].id + '.psd');
  if (!input.exists) throw Error('MISSING_SOURCE|' + formats[i].id + '|' + formats[i].source);
  if (output.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE|' + output.fsName);
 }
 validateOfferIds(offers);
}

try {
 log = new File(BASE + LOG_REL);
 if (log.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE|' + LOG_REL);
 log.encoding = 'UTF8'; if (!log.open('w')) throw Error('LOG_OPEN_FAILED|' + LOG_REL);
 if (app.documents.length !== 0) throw Error('PREFLIGHT_DOCS_ABERTOS');
 var spec = readJSON(SPEC_REL), offers = spec.offers;
 preflight(offers);
 app.displayDialogs = DialogModes.NO;
 msg('SCRIPT_PREPARED|recapture_templates_r17.jsx|scope=layer_comps_visibility_only|png_exports=0|sources=r14_strip,r16_large4,r10_square_micro|outputs=7_psd|approved_pngs_untouched=true|root_cause=LayerComps_add_boolean_order|correct_flags=appearance_false_position_false_visibility_true');
 for (var fi = 0; fi < formats.length; fi++) {
  var fmt = formats[fi], formatStart = new Date().getTime(), source = new File(BASE + fmt.source), output = new File(BASE + OUT_REL + 'BYD_TPL_' + fmt.id + '.psd');
  doc = app.open(source);
  validateDocument(fmt, offers);
  msg('SOURCE_OPEN_OK|' + fmt.id + '|revision=' + fmt.sourceRevision + '|path=' + fmt.source + '|old_comps=' + doc.layerComps.length);
  removeExistingComps(fmt.id);
  makeComps(fmt.id, offers);
  testAllComps(fmt.id, offers, 'before_save');
  activate(offers[0].id);
  var options = new PhotoshopSaveOptions(); options.layers = true; options.embedColorProfile = true;
  doc.saveAs(output, options, true, Extension.LOWERCASE);
  msg('OUTPUT_SAVED|' + fmt.id + '|path=' + OUT_REL + output.name + '|comps=' + doc.layerComps.length + '|resting_state=' + offers[0].id);
  doc.close(SaveOptions.DONOTSAVECHANGES); doc = null;
  doc = app.open(output);
  validateDocument(fmt, offers);
  if (doc.layerComps.length !== offers.length) throw Error('PERSISTED_COMP_COUNT|' + fmt.id + '|' + doc.layerComps.length);
  testAllComps(fmt.id, offers, 'after_reopen');
  doc.close(SaveOptions.DONOTSAVECHANGES); doc = null;
  msg('FORMAT_OK|' + fmt.id + '|source_revision=' + fmt.sourceRevision + '|comps=20|apply_tests_before_save=20|apply_tests_after_reopen=20|pixel_edits=0|png_exports=0|elapsed_ms=' + (new Date().getTime() - formatStart));
 }
 msg('OK|completed|templates=7|comps_per_template=20|apply_tests=280|pngs=0|approved_pngs_untouched=true|elapsed_ms=' + (new Date().getTime() - RUN_START));
} catch (e) {
 if (log) msg('ERRO|' + e.message + '|line=' + e.line);
} finally {
 if (doc) doc.close(SaveOptions.DONOTSAVECHANGES);
 app.displayDialogs = oldDialogs;
 if (log) log.close();
}
})();
