#target photoshop
#include "../../../../../../operacao/lib/mkroot.jsxinc"
/*
  R18 guarded canonical re-render. Prepared only; do not run while another
  Photoshop job is active. It reads render_request_r18.json and refuses to
  export unless the named Layer Comp records visibility and, after apply(),
  exactly one matching state is active in each variable branch.
*/
(function () {
var ROOT = MK.root();
var BASE = ROOT + '/Projects/BYD/Jobs/V4/';
var REQUEST_REL = 'WORK/00_MATRIZ/render_request_r18.json';
var REFUSE_OVERWRITE = true;
var doc = null, log = null, oldDialogs = app.displayDialogs, started = new Date().getTime(), expectedPNGs = 0, actualPNGs = 0;
function msg(s) { if (log) { log.writeln(new Date().toUTCString() + '|' + s); log.close(); log.open('a'); } }
function readJSON(rel) { var f = new File(BASE + rel); if (!f.exists) throw Error('MISSING_JSON|' + rel); f.encoding = 'UTF8'; f.open('r'); var value = eval('(' + f.read() + ')'); f.close(); return value; }
function clean(s) { return String(s).replace(/\u00ac\u2211/g, '\u00b7'); }
function isArray(value) { return value instanceof Array; }
function uniqueStrings(values, label) { var seen = {}, out = []; if (!isArray(values) || values.length < 1) throw Error('INVALID_' + label); for (var i = 0; i < values.length; i++) { var value = values[i]; if (typeof value !== 'string' || value.length === 0 || seen[value]) throw Error('DUPLICATE_OR_INVALID_' + label + '|' + value); seen[value] = true; out.push(value); } return out; }
function mapFormats(spec) { var out = {}; if (!isArray(spec.formats)) throw Error('INVALID_R18_SPEC_FORMATS'); for (var i = 0; i < spec.formats.length; i++) { var format = spec.formats[i]; if (!format || typeof format.id !== 'string' || typeof format.w !== 'number' || typeof format.h !== 'number' || out[format.id]) throw Error('INVALID_R18_SPEC_FORMAT|' + (format ? format.id : 'null')); out[format.id] = format; } return out; }
function mapOffers(spec) { var out = {}; if (!isArray(spec.offers)) throw Error('INVALID_R18_SPEC_OFFERS'); for (var i = 0; i < spec.offers.length; i++) { var offer = spec.offers[i]; if (!offer || typeof offer.id !== 'string' || out[offer.id]) throw Error('INVALID_R18_SPEC_OFFER|' + (offer ? offer.id : 'null')); out[offer.id] = true; } return out; }
function expectedName(root, id) { if (root === 'VEICULO') return 'CAR \u00b7 ' + id; if (root === 'CONDICIONAIS') return 'COND \u00b7 ' + id; return id; }
function exactComp(id) { var hits = [], wanted = 'OFERTA ' + id; for (var i = 0; i < doc.layerComps.length; i++) if (doc.layerComps[i].name === wanted) hits.push(doc.layerComps[i]); if (hits.length !== 1) throw Error('EXACT_COMP_COUNT|' + id + '|' + hits.length); return hits[0]; }
function verifyCompFlags(comp, id) { if (comp.visibility !== true) throw Error('COMP_VISIBILITY_FALSE|' + id); msg('COMP_FLAGS_OK|' + id + '|visibility=' + comp.visibility + '|appearance=' + comp.appearance + '|position=' + comp.position); }
function verifyActiveBranch(rootName, id) { var root = doc.layerSets.getByName(rootName), wanted = clean(expectedName(rootName, id)), matching = 0, visible = 0, active = false; for (var i = 0; i < root.layerSets.length; i++) { var state = root.layerSets[i], name = clean(state.name); if (state.visible) visible++; if (name === wanted) { matching++; if (state.visible) active = true; } } if (matching !== 1 || visible !== 1 || !active) throw Error('ACTIVE_STATE_MISMATCH|' + rootName + '|' + id + '|matching=' + matching + '|visible=' + visible + '|active=' + active); return rootName + ':' + wanted; }
function verifyAppliedState(id) { var roots = ['BG', 'VEICULO', 'LEGAL', 'CONDICIONAIS', 'OFERTA'], verified = []; for (var i = 0; i < roots.length; i++) verified.push(verifyActiveBranch(roots[i], id)); msg('ACTIVE_STATES_OK|' + id + '|branches=' + verified.join(',')); }
function exportPNG(file, id, fmt) { if (file.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE_PNG|' + file.fsName); var options = new ExportOptionsSaveForWeb(); options.format = SaveDocumentType.PNG; options.PNG8 = false; options.transparency = false; options.interlaced = false; options.includeProfile = true; doc.exportDocument(file, ExportType.SAVEFORWEB, options); actualPNGs++; msg('OK|png|' + id + '|' + fmt + '|state_verified=true|actual_pngs=' + actualPNGs); }
try {
 if (app.documents.length !== 0) throw Error('PREFLIGHT_DOCS_ABERTOS');
 var job = readJSON(REQUEST_REL), spec = readJSON('WORK/00_MATRIZ/production_spec_r18.json');
 if (job.revision !== 'r18' || !job.output_folder || !job.log_file || !job.validation_output || !job.templates || !job.offer_ids) throw Error('INVALID_R18_REQUEST');
 var offerIDs = uniqueStrings(job.offer_ids, 'OFFER_IDS'), templates = job.templates, knownOffers = mapOffers(spec), knownFormats = mapFormats(spec);
 if (offerIDs.length > 20 || !isArray(templates) || templates.length < 1 || templates.length > 7) throw Error('R18_SCOPE_MISMATCH');
 if (spec.revision !== 'r18' || !spec.output_templates) throw Error('INVALID_R18_SPEC');
 var templateFormats = {};
 for (var tv = 0; tv < templates.length; tv++) { var requestedTemplate = templates[tv]; if (!requestedTemplate || typeof requestedTemplate.format !== 'string' || typeof requestedTemplate.path !== 'string' || !knownFormats[requestedTemplate.format] || templateFormats[requestedTemplate.format]) throw Error('DUPLICATE_OR_UNKNOWN_TEMPLATE|' + (requestedTemplate ? requestedTemplate.format : 'null')); var exactPath = spec.output_templates + 'BYD_TPL_' + requestedTemplate.format + '.psd'; if (requestedTemplate.path !== exactPath) throw Error('TEMPLATE_PATH_NOT_CANONICAL|' + requestedTemplate.format); templateFormats[requestedTemplate.format] = true; }
 for (var ov = 0; ov < offerIDs.length; ov++) if (!knownOffers[offerIDs[ov]]) throw Error('UNKNOWN_OFFER_ID|' + offerIDs[ov]);
 expectedPNGs = offerIDs.length * templates.length;
 var output = new Folder(BASE + job.output_folder), logfile = new File(BASE + job.log_file), validation = new File(BASE + job.validation_output);
 if (output.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE_OUTPUT_FOLDER');
 if (logfile.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE_LOG');
 if (validation.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE_VALIDATION_TARGET');
 for (var ti = 0; ti < templates.length; ti++) if (!(new File(BASE + templates[ti].path)).exists) throw Error('MISSING_TEMPLATE|' + templates[ti].path);
 if (!output.create()) throw Error('CANNOT_CREATE_OUTPUT_FOLDER');
 log = logfile; log.encoding = 'UTF8'; log.open('w'); app.displayDialogs = DialogModes.NO;
 msg('SCRIPT_PREPARED|render_canonical_v2.jsx|revision=r18|request=' + REQUEST_REL + '|visibility_required=true|branches=BG,VEICULO,LEGAL,CONDICIONAIS,OFERTA|expected_pngs=' + expectedPNGs);
 for (var f = 0; f < templates.length; f++) {
  var template = templates[f], expectedFormat = knownFormats[template.format], formatStart = new Date().getTime(); doc = app.open(new File(BASE + template.path));
  if (doc.mode !== DocumentMode.RGB || doc.bitsPerChannel !== BitsPerChannelType.EIGHT || doc.colorProfileName !== 'sRGB IEC61966-2.1') throw Error('MODE_PROFILE_PREFLIGHT|' + template.format);
  if (Math.round(doc.width.as('px')) !== expectedFormat.w || Math.round(doc.height.as('px')) !== expectedFormat.h) throw Error('DIMENSIONS_MISMATCH|' + template.format + '|actual=' + Math.round(doc.width.as('px')) + 'x' + Math.round(doc.height.as('px')) + '|expected=' + expectedFormat.w + 'x' + expectedFormat.h);
  msg('DIMENSIONS_OK|' + template.format + '|width=' + expectedFormat.w + '|height=' + expectedFormat.h);
  for (var oi = 0; oi < offerIDs.length; oi++) { var id = offerIDs[oi], comp = exactComp(id); verifyCompFlags(comp, id); comp.apply(); verifyAppliedState(id); doc.layerSets.getByName('#GUIAS').visible = false; exportPNG(new File(output.fsName + '/byd_' + id + '_' + template.format + '.png'), id, template.format); }
  doc.close(SaveOptions.DONOTSAVECHANGES); doc = null; msg('OK|format|' + template.format + '|offers=' + offerIDs.length + '|expected_pngs=' + expectedPNGs + '|actual_pngs=' + actualPNGs + '|elapsed_ms=' + (new Date().getTime() - formatStart));
 }
 if (actualPNGs !== expectedPNGs) throw Error('PNG_COUNT_MISMATCH|expected=' + expectedPNGs + '|actual=' + actualPNGs);
 msg('OK|completed|revision=r18|expected_pngs=' + expectedPNGs + '|actual_pngs=' + actualPNGs + '|elapsed_ms=' + (new Date().getTime() - started));
} catch (e) { msg('ERRO|' + e.message + '|line=' + e.line + '|expected_pngs=' + expectedPNGs + '|actual_pngs=' + actualPNGs); } finally { if (doc) doc.close(SaveOptions.DONOTSAVECHANGES); app.displayDialogs = oldDialogs; if (log) log.close(); }
}());
