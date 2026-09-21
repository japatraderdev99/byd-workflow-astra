#target photoshop
#include "../../../../../../operacao/lib/mkroot.jsxinc"
/*
  R20 is the cached-tree continuation of R17 for the six formats after strip.
  It keeps all 40 deterministic apply tests per format. No Action Manager is
  used. Layer content, geometry, text, masks, and approved PNGs are untouched.

  The five root groups and 100 offer-state groups are indexed once per open
  document. After one full initialization, activation changes only the prior
  and target state in each root group (ten visibility writes). Verification
  reads the cached 100 state references without rescanning layer collections.
  LayerComp objects are deliberately not cached: R19 proved that references
  returned while the LayerComps collection grows can resolve to another comp.
  Every test resolves its comp by exact name immediately before apply, matching
  the R17 method that completed all 40 strip tests.
*/
(function () {
var RUN_START = new Date().getTime();
var ROOT = MK.root();
var BASE = ROOT + '/Projects/BYD/Jobs/V4/';
var REFUSE_OVERWRITE = true;
var LOG_REL = 'WORK/06_LOGS/recapture_templates_r20.log';
var R17_LOG_REL = 'WORK/06_LOGS/recapture_templates_r17.log';
var R19_LOG_REL = 'WORK/06_LOGS/recapture_templates_r19.log';
var SPEC_REL = 'WORK/00_MATRIZ/production_spec_r10.json';
var OUT_REL = 'WORK/01_TEMPLATES/2026-09-20-r17/';
var formats = [
 { id: '1920x1080', w: 1920, h: 1080, source: 'WORK/01_TEMPLATES/2026-09-20-r16/BYD_TPL_1920x1080.psd', sourceRevision: 'r16' },
 { id: '1920x1125', w: 1920, h: 1125, source: 'WORK/01_TEMPLATES/2026-09-20-r16/BYD_TPL_1920x1125.psd', sourceRevision: 'r16' },
 { id: '1080x1080', w: 1080, h: 1080, source: 'WORK/01_TEMPLATES/2026-09-20-r10/BYD_TPL_1080x1080.psd', sourceRevision: 'r10' },
 { id: '1080x1920', w: 1080, h: 1920, source: 'WORK/01_TEMPLATES/2026-09-20-r16/BYD_TPL_1080x1920.psd', sourceRevision: 'r16' },
 { id: '1109x1973', w: 1109, h: 1973, source: 'WORK/01_TEMPLATES/2026-09-20-r16/BYD_TPL_1109x1973.psd', sourceRevision: 'r16' },
 { id: '360x80', w: 360, h: 80, source: 'WORK/01_TEMPLATES/2026-09-20-r10/BYD_TPL_360x80.psd', sourceRevision: 'r10' }
];
var TOP_NAMES = ['OFERTA', 'CONDICIONAIS', 'LEGAL', 'VEICULO', 'BG'];
var doc = null;
var log = null;
var stateCache = null;
var oldDialogs = app.displayDialogs;

function msg(s) { if (log) { log.writeln(new Date().toUTCString() + '|' + s); log.close(); log.open('a'); } }
function readJSON(rel) { var f = new File(BASE + rel); if (!f.exists) throw Error('MISSING_JSON|' + rel); f.encoding = 'UTF8'; if (!f.open('r')) throw Error('OPEN_JSON_FAILED|' + rel); var value = eval('(' + f.read() + ')'); f.close(); return value; }
function cleanName(value) { return String(value).split('\u00ac\u2211').join('\u00b7'); }
function expectedName(top, offerId) { if (top === 'CONDICIONAIS') return 'COND \u00b7 ' + offerId; if (top === 'VEICULO') return 'CAR \u00b7 ' + offerId; return offerId; }
function validateOfferIds(offers) {
 if (!offers || offers.length !== 20) throw Error('OFFER_COUNT|' + (offers ? offers.length : 0));
 var seen = {};
 for (var i = 0; i < offers.length; i++) { var id = offers[i].id; if (!id || seen[id]) throw Error('INVALID_OR_DUPLICATE_OFFER_ID|' + id); seen[id] = true; }
}
function buildStateCache(fmt, offers) {
 var roots = {}, rootCounts = {}, required = ['FIXO', '#GUIAS', 'OFERTA', 'CONDICIONAIS', 'LEGAL', 'VEICULO', 'BG'];
 for (var ri = 0; ri < doc.layerSets.length; ri++) { var rootName = cleanName(doc.layerSets[ri].name); roots[rootName] = doc.layerSets[ri]; rootCounts[rootName] = (rootCounts[rootName] || 0) + 1; }
 for (var rq = 0; rq < required.length; rq++) if (rootCounts[required[rq]] !== 1) throw Error('ROOT_GROUP_COUNT|' + fmt.id + '|' + required[rq] + '|' + (rootCounts[required[rq]] || 0));
 if (!roots.FIXO.visible) throw Error('FIXO_HIDDEN|' + fmt.id);
 var cache = { roots: roots, tops: [], states: [], current: null };
 for (var ti = 0; ti < TOP_NAMES.length; ti++) {
  var topName = TOP_NAMES[ti], top = roots[topName], byName = {}, nameCount = {};
  if (top.layerSets.length !== offers.length) throw Error('STATE_COUNT|' + fmt.id + '|' + topName + '|' + top.layerSets.length);
  for (var gi = 0; gi < top.layerSets.length; gi++) { var childName = cleanName(top.layerSets[gi].name); byName[childName] = top.layerSets[gi]; nameCount[childName] = (nameCount[childName] || 0) + 1; }
  var ordered = [];
  for (var oi = 0; oi < offers.length; oi++) { var wanted = expectedName(topName, offers[oi].id); if (nameCount[wanted] !== 1) throw Error('DIRECT_GROUP_COUNT|' + fmt.id + '|' + topName + '|' + wanted + '|' + (nameCount[wanted] || 0)); ordered.push(byName[wanted]); }
  cache.tops.push(top); cache.states.push(ordered);
 }
 return cache;
}
function initializeActive(index, offers) {
 for (var ti = 0; ti < stateCache.tops.length; ti++) {
  stateCache.tops[ti].visible = true;
  for (var oi = 0; oi < offers.length; oi++) stateCache.states[ti][oi].visible = oi === index;
 }
 stateCache.roots['#GUIAS'].visible = false;
 stateCache.current = index;
 verifyActive(index, offers, 'initialize');
}
function activate(index, offers) {
 if (stateCache.current === null) { initializeActive(index, offers); return; }
 if (stateCache.current !== index) {
  for (var ti = 0; ti < stateCache.tops.length; ti++) { stateCache.states[ti][stateCache.current].visible = false; stateCache.states[ti][index].visible = true; }
  stateCache.current = index;
 }
 stateCache.roots['#GUIAS'].visible = false;
}
function verifyActive(index, offers, phase) {
 for (var ti = 0; ti < stateCache.tops.length; ti++) {
  if (!stateCache.tops[ti].visible) throw Error('TOP_HIDDEN|' + phase + '|' + TOP_NAMES[ti] + '|' + offers[index].id);
  var count = 0, visibleIndex = -1;
  for (var oi = 0; oi < offers.length; oi++) if (stateCache.states[ti][oi].visible) { count++; visibleIndex = oi; }
  if (count !== 1 || visibleIndex !== index) throw Error('ACTIVE_STATE_MISMATCH|' + phase + '|' + TOP_NAMES[ti] + '|expected=' + offers[index].id + '|count=' + count + '|actual_index=' + visibleIndex);
 }
 if (stateCache.roots['#GUIAS'].visible) throw Error('GUIDES_VISIBLE|' + phase + '|' + offers[index].id);
}
function validateDocument(fmt, offers) {
 if (doc.width.as('px') !== fmt.w || doc.height.as('px') !== fmt.h) throw Error('DIMENSION_MISMATCH|' + fmt.id + '|' + doc.width.as('px') + 'x' + doc.height.as('px'));
 if (doc.mode !== DocumentMode.RGB) throw Error('DOCUMENT_NOT_RGB|' + fmt.id);
 stateCache = buildStateCache(fmt, offers);
}
function removeExistingComps(fmtId) {
 var before = doc.layerComps.length;
 for (var i = before - 1; i >= 0; i--) doc.layerComps[i].remove();
 if (doc.layerComps.length !== 0) throw Error('LAYER_COMP_REMOVE_FAILED|' + fmtId + '|' + doc.layerComps.length);
 msg('INVALID_COMPS_REMOVED|' + fmtId + '|count=' + before);
}
function compByName(name) {
 var found = null, count = 0;
 for (var i = 0; i < doc.layerComps.length; i++) if (doc.layerComps[i].name === name) { found = doc.layerComps[i]; count++; }
 if (count !== 1) throw Error('LAYER_COMP_NAME_COUNT|' + name + '|' + count);
 return found;
}
function makeComps(fmtId, offers) {
 for (var i = 0; i < offers.length; i++) {
  activate(i, offers); verifyActive(i, offers, 'capture');
  var id = offers[i].id;
  doc.layerComps.add('OFERTA ' + id, 'offer_id=' + id + '|r20_visibility_only=true', false, false, true);
  var comp = compByName('OFERTA ' + id);
  if (comp.appearance !== false || comp.position !== false || comp.visibility !== true) throw Error('LAYER_COMP_FLAGS|' + fmtId + '|' + id + '|appearance=' + comp.appearance + '|position=' + comp.position + '|visibility=' + comp.visibility);
 }
 if (doc.layerComps.length !== offers.length) throw Error('LAYER_COMP_COUNT_AFTER_CREATE|' + fmtId + '|' + doc.layerComps.length);
}
function testAllComps(fmtId, offers, phase) {
 for (var i = 0; i < offers.length; i++) {
  var target = i, decoy = (i + 1) % offers.length, id = offers[target].id;
  activate(decoy, offers);
  var comp = compByName('OFERTA ' + id);
  if (comp.appearance !== false || comp.position !== false || comp.visibility !== true) throw Error('LAYER_COMP_FLAGS|' + phase + '|' + fmtId + '|' + id);
  comp.apply();
  stateCache.current = target;
  verifyActive(target, offers, phase + '|apply');
  msg('COMP_APPLY_OK|' + phase + '|' + fmtId + '|' + id + '|decoy=' + offers[decoy].id);
 }
}
function preflight(offers) {
 var outDir = new Folder(BASE + OUT_REL);
 if (!outDir.exists) throw Error('MISSING_OUTPUT_FOLDER|' + OUT_REL);
 var strip = new File(BASE + OUT_REL + 'BYD_TPL_1920x276.psd');
 if (!strip.exists) throw Error('MISSING_COMPLETED_R17_STRIP|' + strip.fsName);
 var existingPSDs = outDir.getFiles('*.psd');
 if (existingPSDs.length !== 1 || existingPSDs[0].name !== strip.name) throw Error('R17_DESTINATION_SCOPE|expected_only=' + strip.name + '|actual_psds=' + existingPSDs.length);
 var r17log = new File(BASE + R17_LOG_REL);
 if (!r17log.exists) throw Error('MISSING_R17_LOG|' + R17_LOG_REL);
 r17log.encoding = 'UTF8'; if (!r17log.open('r')) throw Error('OPEN_R17_LOG_FAILED'); var r17text = r17log.read(); r17log.close();
 var formatMarker = '|FORMAT_OK|1920x276|', errorMarker = '|ERRO|';
 if (r17text.indexOf(formatMarker) < 0) throw Error('R17_STRIP_FORMAT_OK_MISSING');
 if (r17text.indexOf(formatMarker) > r17text.lastIndexOf(errorMarker)) throw Error('R17_ERROR_NOT_AFTER_STRIP_FORMAT_OK');
 var r19log = new File(BASE + R19_LOG_REL);
 if (!r19log.exists) throw Error('MISSING_R19_LOG|' + R19_LOG_REL);
 r19log.encoding = 'UTF8'; if (!r19log.open('r')) throw Error('OPEN_R19_LOG_FAILED'); var r19text = r19log.read(); r19log.close();
 if (r19text.indexOf('|ERRO|ACTIVE_STATE_MISMATCH|before_save|apply|OFERTA|expected=atto-8|') < 0) throw Error('R19_EXPECTED_COMP_REFERENCE_FAILURE_MISSING');
 if (r19text.indexOf('|OUTPUT_SAVED|') >= 0 || r19text.indexOf('|FORMAT_OK|') >= 0) throw Error('R19_UNEXPECTED_SAVED_OUTPUT_EVIDENCE');
 for (var i = 0; i < formats.length; i++) { var input = new File(BASE + formats[i].source), output = new File(BASE + OUT_REL + 'BYD_TPL_' + formats[i].id + '.psd'); if (!input.exists) throw Error('MISSING_SOURCE|' + formats[i].id + '|' + formats[i].source); if (output.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE|' + output.fsName); }
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
 msg('SCRIPT_PREPARED|recapture_templates_r20.jsx|scope=remaining_6_templates_continuing_R17_destination|r17_strip_format_ok=true|r19_failed_before_save=true|optimization=cached_tree_references_and_previous_target_visibility_switch|layer_comp_cache=false|layer_comp_lookup=exact_name_each_test|action_manager=false|tests_per_format=40|png_exports=0|approved_pngs_untouched=true');
 for (var fi = 0; fi < formats.length; fi++) {
  var fmt = formats[fi], formatStart = new Date().getTime(), source = new File(BASE + fmt.source), output = new File(BASE + OUT_REL + 'BYD_TPL_' + fmt.id + '.psd');
  doc = app.open(source); validateDocument(fmt, offers);
  msg('SOURCE_OPEN_OK|' + fmt.id + '|revision=' + fmt.sourceRevision + '|path=' + fmt.source + '|old_comps=' + doc.layerComps.length + '|cached_state_refs=100');
  removeExistingComps(fmt.id);
  initializeActive(0, offers);
  makeComps(fmt.id, offers);
  testAllComps(fmt.id, offers, 'before_save');
  activate(0, offers); verifyActive(0, offers, 'resting_state');
  var options = new PhotoshopSaveOptions(); options.layers = true; options.embedColorProfile = true;
  doc.saveAs(output, options, true, Extension.LOWERCASE);
  msg('OUTPUT_SAVED|' + fmt.id + '|path=' + OUT_REL + output.name + '|comps=' + doc.layerComps.length + '|resting_state=' + offers[0].id);
  doc.close(SaveOptions.DONOTSAVECHANGES); doc = null; stateCache = null;
  doc = app.open(output); validateDocument(fmt, offers);
  if (doc.layerComps.length !== offers.length) throw Error('PERSISTED_COMP_COUNT|' + fmt.id + '|' + doc.layerComps.length);
  initializeActive(0, offers);
  testAllComps(fmt.id, offers, 'after_reopen');
  doc.close(SaveOptions.DONOTSAVECHANGES); doc = null; stateCache = null;
  msg('FORMAT_OK|' + fmt.id + '|source_revision=' + fmt.sourceRevision + '|comps=20|apply_tests_before_save=20|apply_tests_after_reopen=20|cached_state_refs=100|pixel_edits=0|png_exports=0|elapsed_ms=' + (new Date().getTime() - formatStart));
 }
 msg('OK|completed|templates=6|comps_per_template=20|apply_tests=240|pngs=0|approved_pngs_untouched=true|elapsed_ms=' + (new Date().getTime() - RUN_START));
} catch (e) {
 if (log) msg('ERRO|' + e.message + '|line=' + e.line);
} finally {
 if (doc) doc.close(SaveOptions.DONOTSAVECHANGES);
 stateCache = null; app.displayDialogs = oldDialogs;
 if (log) log.close();
}
})();
