#target photoshop
#include "../../../../../../operacao/lib/mkroot.jsxinc"
/*
  R12 cold post-production patch for confirmed BYD review findings.

  Changes:
  1. In the two confirmed landscape formats, tighten only the bottom of the
     existing vd-song-pro-flex vehicle mask.
     The old build exposed the scene to 104% of the declared car-zone height.
     R12 keeps the full car zone (100%) and feathers the new bottom edge by at
     most two pixels. It does not transform, hide, or convert vehicle layers.
  2. For dolphin-mini-5l-gs only, reduce headline leading when the editable
     text has more than one line and its measured leading exceeds 145% of its
     font size. Contents and typeface are preserved, then the text is refit to
     the same zone from its top edge.
  3. The strip starts from immutable R03 and incorporates the already reviewed
     R08 installment wrap, avoiding a second large PSD copy.
  4. In confirmed large formats only, scale the Yuan Pro CENA ORIGINAL group to
     85% and center its hidden Layer 7 anchor in the same car zone. Vehicle and
     native ground remain one proportional unit.

  Prepared only. Run after static review and Photoshop lock acquisition.
  The approved square, micro, and strip vehicle scenes are not changed. The four
  large-format findings are required to pass their runtime diagnostics.
  R03 and R10 inputs are never overwritten. Only changed offers are exported.
*/
(function () {
var RUN_START = new Date().getTime();
var ROOT = MK.root();
var BASE = ROOT + '/Projects/BYD/Jobs/V4/';
var REFUSE_OVERWRITE = true;
var LOG_REL = 'WORK/06_LOGS/patch_controle_r12.log';
var OUT_TPL_REL = 'WORK/01_TEMPLATES/2026-09-20-r12/';
var OUT_PNG_REL = 'WORK/03_STAGING/2026-09-20-r12/';
var R03_SPEC_REL = 'WORK/00_MATRIZ/production_spec_r03.json';
var R10_SPEC_REL = 'WORK/00_MATRIZ/production_spec_r10.json';
var VD_ID = 'vd-song-pro-flex';
var DOLPHIN_ID = 'dolphin-mini-5l-gs';
var YUAN_ID = 'yuan-pro';
var MASK_BOTTOM_RATIO = 1.0;
var YUAN_SCENE_SCALE = 0.85;
var LEADING_EXCESS_RATIO = 1.45;
var LEADING_TARGET_RATIO = 1.10;
var formats = [
 { id: '1920x276',  w: 1920, h: 276,  input: 'WORK/01_TEMPLATES/2026-09-19-r03/BYD_TPL_1920x276.psd', stripInstallment: true, applyMask: false, checkHeadline: false },
 { id: '1920x1080', w: 1920, h: 1080, input: 'WORK/01_TEMPLATES/2026-09-20-r10/BYD_TPL_1920x1080.psd', applyMask: true, applyYuan: true, checkHeadline: true, requireHeadlinePatch: true },
 { id: '1920x1125', w: 1920, h: 1125, input: 'WORK/01_TEMPLATES/2026-09-20-r10/BYD_TPL_1920x1125.psd', applyMask: true, applyYuan: true, checkHeadline: true, requireHeadlinePatch: true },
 { id: '1080x1920', w: 1080, h: 1920, input: 'WORK/01_TEMPLATES/2026-09-20-r10/BYD_TPL_1080x1920.psd', applyMask: true, applyYuan: true, checkHeadline: true, requireHeadlinePatch: true },
 { id: '1109x1973', w: 1109, h: 1973, input: 'WORK/01_TEMPLATES/2026-09-20-r10/BYD_TPL_1109x1973.psd', applyMask: true, applyYuan: true, checkHeadline: true, requireHeadlinePatch: true }
];
var doc = null, log = null;
var oldUnits = app.preferences.rulerUnits;
var oldDialogs = app.displayDialogs;

function msg(s) { log.writeln(new Date().toUTCString() + '|' + s); log.close(); log.open('a'); }
function readJSON(rel) { var f = new File(BASE + rel); if (!f.exists) throw Error('MISSING_JSON|' + rel); f.encoding = 'UTF8'; f.open('r'); var v = eval('(' + f.read() + ')'); f.close(); return v; }
function cleanName(s) { return String(s).split('\u00ac\u2211').join('\u00b7'); }
function box(l) { var b = l.bounds; return [b[0].as('px'), b[1].as('px'), b[2].as('px'), b[3].as('px')]; }
function directGroup(parent, name) { var wanted = cleanName(name), hits = []; for (var i = 0; i < parent.layerSets.length; i++) if (cleanName(parent.layerSets[i].name) === wanted) hits.push(parent.layerSets[i]); if (hits.length !== 1) throw Error('EXACT_GROUP_COUNT|' + name + '|' + hits.length); return hits[0]; }
function directLayer(parent, name) { var wanted = cleanName(name), hits = []; for (var i = 0; i < parent.layers.length; i++) if (cleanName(parent.layers[i].name) === wanted) hits.push(parent.layers[i]); if (hits.length !== 1) throw Error('EXACT_LAYER_COUNT|' + name + '|' + hits.length); return hits[0]; }
function formatById(spec, id) { for (var i = 0; i < spec.formats.length; i++) if (spec.formats[i].id === id) return spec.formats[i]; throw Error('FORMAT_NOT_IN_SPEC|' + id); }
function expectedName(top, id) { if (top === 'CONDICIONAIS') return 'COND \u00b7 ' + id; if (top === 'VEICULO') return 'CAR \u00b7 ' + id; return id; }
function verifyStates() { var tops = ['BG', 'VEICULO', 'LEGAL', 'CONDICIONAIS', 'OFERTA']; for (var i = 0; i < tops.length; i++) { var g = doc.layerSets.getByName(tops[i]); if (g.layerSets.length !== 20) throw Error('STATE_COUNT|' + tops[i] + '|' + g.layerSets.length); } if (doc.layerComps.length !== 20) throw Error('LAYER_COMP_COUNT|' + doc.layerComps.length); doc.layerSets.getByName('FIXO'); doc.layerSets.getByName('#GUIAS'); }
function activate(offerId) { var tops = ['OFERTA', 'CONDICIONAIS', 'LEGAL', 'VEICULO', 'BG']; for (var ti = 0; ti < tops.length; ti++) { var top = doc.layerSets.getByName(tops[ti]), wanted = expectedName(tops[ti], offerId), found = 0; for (var gi = 0; gi < top.layerSets.length; gi++) { var yes = cleanName(top.layerSets[gi].name) === wanted; top.layerSets[gi].visible = yes; if (yes) found++; } if (found !== 1) throw Error('ACTIVATE_STATE_COUNT|' + tops[ti] + '|' + offerId + '|' + found); } doc.layerSets.getByName('#GUIAS').visible = false; }
function exportPNG(file, label) { if (file.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE|' + file.fsName); var o = new ExportOptionsSaveForWeb(); o.format = SaveDocumentType.PNG; o.PNG8 = false; o.transparency = false; o.interlaced = false; o.includeProfile = true; doc.exportDocument(file, ExportType.SAVEFORWEB, o); msg('OK|png|' + label + '|file=' + file.name); }
function wrapText(value, width) { var words = String(value).replace(/[\r\n]+/g, ' ').replace(/^\s+|\s+$/g, '').split(/\s+/), lines = [], line = ''; for (var i = 0; i < words.length; i++) { var candidate = line ? line + ' ' + words[i] : words[i]; if (line && candidate.length > width) { lines.push(line); line = words[i]; } else line = candidate; } if (line) lines.push(line); return lines.join('\r'); }
function fitProportional(layer, zone) { var before = box(layer), width = Math.max(1, before[2] - before[0]), height = Math.max(1, before[3] - before[1]), scale = Math.min(zone[2] / width, zone[3] / height); layer.resize(scale * 100, scale * 100, AnchorPosition.TOPLEFT); var after = box(layer), x = zone[0] + (zone[2] - (after[2] - after[0])) / 2, y = zone[1] + (zone[3] - (after[3] - after[1])) / 2; layer.translate(x - after[0], y - after[1]); return box(layer); }
function fitTop(layer, zone, align) { var before = box(layer), width = Math.max(1, before[2] - before[0]), height = Math.max(1, before[3] - before[1]), scale = Math.min(zone[2] / width, zone[3] / height); layer.resize(scale * 100, scale * 100, AnchorPosition.TOPLEFT); var after = box(layer), x = zone[0]; if (align === 'center') x += (zone[2] - (after[2] - after[0])) / 2; layer.translate(x - after[0], zone[1] - after[1]); return box(layer); }
function verifyInZone(layer, zone, label) { var b = box(layer), tolerance = 2; if (!layer.visible) throw Error('PATCH_LAYER_HIDDEN|' + label); if (b[0] < zone[0] - tolerance || b[1] < zone[1] - tolerance || b[2] > zone[0] + zone[2] + tolerance || b[3] > zone[1] + zone[3] + tolerance) throw Error('PATCH_OUTSIDE_ZONE|' + label + '|' + b.join(',') + '|' + zone.join(',')); return b; }
function hasUserMask(layer) { var p = stringIDToTypeID('hasUserMask'), ref = new ActionReference(); ref.putProperty(charIDToTypeID('Prpr'), p); ref.putIdentifier(charIDToTypeID('Lyr '), layer.id); var d = executeActionGet(ref); return d.hasKey(p) && d.getBoolean(p); }
function selectUserMask(layer) { doc.activeLayer = layer; var d = new ActionDescriptor(), ref = new ActionReference(); ref.putEnumerated(charIDToTypeID('Chnl'), charIDToTypeID('Chnl'), charIDToTypeID('Msk ')); d.putReference(charIDToTypeID('null'), ref); d.putBoolean(charIDToTypeID('MkVs'), false); executeAction(charIDToTypeID('slct'), d, DialogModes.NO); }
function tightenVehicleMask(fmt, carZone) {
 var vehicleRoot = doc.layerSets.getByName('VEICULO');
 var state = directGroup(vehicleRoot, 'CAR \u00b7 ' + VD_ID);
 if (!hasUserMask(state)) throw Error('VD_MASK_MISSING|' + fmt.id);
 var cutoff = carZone[1] + carZone[3] * MASK_BOTTOM_RATIO;
 var feather = Math.max(1, Math.min(2, carZone[3] * .004));
 selectUserMask(state);
 doc.selection.select([[0, cutoff], [fmt.w, cutoff], [fmt.w, fmt.h], [0, fmt.h]]);
 if (feather > 0) doc.selection.feather(feather);
 var black = new SolidColor(); black.rgb.hexValue = '000000';
 doc.selection.fill(black, ColorBlendMode.NORMAL, 100, false);
 doc.selection.deselect();
 doc.activeChannels = doc.componentChannels;
 msg('MASK_PATCH_OK|' + fmt.id + '|' + VD_ID + '|bottom_ratio=' + MASK_BOTTOM_RATIO + '|cutoff_y=' + cutoff + '|feather=' + feather + '|car_zone=' + carZone.join(','));
}
function patchYuanScene(fmt, carZone) {
 var vehicleRoot = doc.layerSets.getByName('VEICULO');
 var state = directGroup(vehicleRoot, 'CAR \u00b7 ' + YUAN_ID);
 var scene = directGroup(state, 'CENA ORIGINAL');
 var anchor = directLayer(scene, 'Layer 7');
 var before = box(anchor), beforeVisible = anchor.visible;
 scene.resize(YUAN_SCENE_SCALE * 100, YUAN_SCENE_SCALE * 100, AnchorPosition.TOPLEFT);
 anchor = directLayer(scene, 'Layer 7');
 var scaled = box(anchor), width = scaled[2] - scaled[0], height = scaled[3] - scaled[1];
 var targetX = carZone[0] + (carZone[2] - width) / 2, targetY = carZone[1] + (carZone[3] - height) / 2;
 scene.translate(targetX - scaled[0], targetY - scaled[1]);
 anchor = directLayer(scene, 'Layer 7');
 var after = box(anchor), tolerance = 2;
 if (after[0] < carZone[0] - tolerance || after[1] < carZone[1] - tolerance || after[2] > carZone[0] + carZone[2] + tolerance || after[3] > carZone[1] + carZone[3] + tolerance) throw Error('YUAN_ANCHOR_OUTSIDE_ZONE|' + fmt.id + '|' + after.join(','));
 if (anchor.visible !== beforeVisible) throw Error('YUAN_ANCHOR_VISIBILITY_CHANGED|' + fmt.id);
 msg('YUAN_SCENE_PATCH_OK|' + fmt.id + '|scale=' + YUAN_SCENE_SCALE + '|alignment=center_center|bounds_before=' + before.join(',') + '|bounds_scaled=' + scaled.join(',') + '|bounds_after=' + after.join(',') + '|car_zone=' + carZone.join(',') + '|scene_and_ground_unit=true');
}
function lineCount(value) { var normalized = String(value).replace(/\r\n/g, '\r').replace(/\n/g, '\r'); return normalized.split('\r').length; }
function measuredLeading(textItem, sizePx) { if (textItem.useAutoLeading) { try { return sizePx * Number(textItem.autoLeadingAmount) / 100; } catch (e1) { return sizePx * 1.2; } } try { return textItem.leading.as('px'); } catch (e2) { return sizePx * 1.2; } }
function patchHeadlineIfExcessive(fmt, headlineZone) {
 var conditionalRoot = doc.layerSets.getByName('CONDICIONAIS');
 var state = directGroup(conditionalRoot, 'COND \u00b7 ' + DOLPHIN_ID);
 var headline = directLayer(state, 'COND \u00b7 HEADLINE \u00b7 ' + DOLPHIN_ID);
 if (headline.typename !== 'ArtLayer' || headline.kind !== LayerKind.TEXT) throw Error('DOLPHIN_HEADLINE_NOT_EDITABLE_TEXT|' + fmt.id);
 var contents = headline.textItem.contents, lines = lineCount(contents), before = box(headline), sizePx = headline.textItem.size.as('px'), leadingPx = measuredLeading(headline.textItem, sizePx), ratio = leadingPx / sizePx;
 if (lines < 2) { msg('HEADLINE_SKIP_SINGLE_LINE|' + fmt.id + '|lines=' + lines + '|size=' + sizePx + '|leading=' + leadingPx + '|ratio=' + ratio); return false; }
 if (!(ratio > LEADING_EXCESS_RATIO)) { msg('HEADLINE_SKIP_LEADING_OK|' + fmt.id + '|lines=' + lines + '|size=' + sizePx + '|leading=' + leadingPx + '|ratio=' + ratio + '|bounds=' + before.join(',')); return false; }
 headline.textItem.useAutoLeading = false;
 headline.textItem.leading = UnitValue(sizePx * LEADING_TARGET_RATIO, 'px');
 if (headline.textItem.contents !== contents) throw Error('HEADLINE_CONTENT_CHANGED|' + fmt.id);
 var tightened = box(headline);
 if (tightened[3] - tightened[1] >= before[3] - before[1]) throw Error('HEADLINE_LEADING_DID_NOT_TIGHTEN|' + fmt.id);
 var fitted = fitTop(headline, headlineZone, fmt.align);
 var after = verifyInZone(headline, headlineZone, 'headline|' + fmt.id + '|' + DOLPHIN_ID);
 if (headline.textItem.contents !== contents) throw Error('HEADLINE_CONTENT_CHANGED_AFTER_REFIT|' + fmt.id);
 msg('HEADLINE_PATCH_OK|' + fmt.id + '|lines=' + lines + '|size_before=' + sizePx + '|leading_before=' + leadingPx + '|leading_after_ratio=' + LEADING_TARGET_RATIO + '|ratio_before=' + ratio + '|align=' + fmt.align + '|vertical=top|bounds_before=' + before.join(',') + '|bounds_tightened=' + tightened.join(',') + '|bounds_fitted=' + fitted.join(',') + '|bounds_verified=' + after.join(',') + '|contents_preserved=true');
 return true;
}
function patchStripInstallment() {
 var zone = [970, 84, 220, 55], conditionalRoot = doc.layerSets.getByName('CONDICIONAIS');
 var state = directGroup(conditionalRoot, 'COND \u00b7 ' + DOLPHIN_ID);
 var installment = directLayer(state, 'COND \u00b7 instal \u00b7 ' + DOLPHIN_ID);
 if (installment.typename !== 'ArtLayer' || installment.kind !== LayerKind.TEXT) throw Error('STRIP_INSTALLMENT_NOT_EDITABLE_TEXT');
 try { installment.unlink(); } catch (ignoreUnlink) {}
 var original = installment.textItem.contents, normalized = original.replace(/[\r\n]+/g, ' ').replace(/^\s+|\s+$/g, ''), wrapped = wrapText(normalized, 15);
 installment.textItem.kind = TextType.POINTTEXT; installment.textItem.contents = wrapped; installment.textItem.justification = Justification.CENTER; installment.visible = true;
 var b = fitProportional(installment, zone); verifyInZone(installment, zone, 'strip_installment|' + DOLPHIN_ID);
 if (lineCount(wrapped) < 2) throw Error('STRIP_INSTALLMENT_WRAP_NOT_APPLIED');
 msg('STRIP_R08_EQUIVALENT_OK|' + DOLPHIN_ID + '|original=' + normalized + '|wrapped=' + wrapped.split('\r').join('/') + '|bounds=' + b.join(',') + '|zone=' + zone.join(','));
}
function preflightOutputs() {
 var outDir = new Folder(BASE + OUT_TPL_REL), pngDir = new Folder(BASE + OUT_PNG_REL);
 if (!outDir.exists || !pngDir.exists) throw Error('MISSING_R12_OUTPUT_FOLDER');
 for (var i = 0; i < formats.length; i++) {
  var f = formats[i], input = new File(BASE + f.input), outPSD = new File(BASE + OUT_TPL_REL + 'BYD_TPL_' + f.id + '.psd');
  if (!input.exists) throw Error('MISSING_INPUT|' + f.id + '|' + f.input);
  if (outPSD.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE|' + outPSD.fsName);
  if (f.applyMask) { var vdPNG = new File(BASE + OUT_PNG_REL + 'byd_' + VD_ID + '_' + f.id + '.png'); if (vdPNG.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE|' + vdPNG.fsName); }
  if (f.applyYuan) { var yuanPNG = new File(BASE + OUT_PNG_REL + 'byd_' + YUAN_ID + '_' + f.id + '.png'); if (yuanPNG.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE|' + yuanPNG.fsName); }
  if (f.checkHeadline || f.stripInstallment) { var dolphinPNG = new File(BASE + OUT_PNG_REL + 'byd_' + DOLPHIN_ID + '_' + f.id + '.png'); if (dolphinPNG.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE|' + dolphinPNG.fsName); }
 }
}

try {
 log = new File(BASE + LOG_REL);
 if (log.exists && REFUSE_OVERWRITE) throw Error('REFUSE_OVERWRITE|' + LOG_REL);
 log.encoding = 'UTF8'; log.open('w');
 if (app.documents.length !== 0) throw Error('PREFLIGHT_DOCS_ABERTOS');
 var r03 = readJSON(R03_SPEC_REL), r10 = readJSON(R10_SPEC_REL);
 preflightOutputs();
 msg('SCRIPT_PREPARED|patch_controle_r12.jsx|sources=R03_strip_plus_R10_reviewed|mask_formats=1920x1080,1920x1125,1080x1920,1109x1973|yuan_formats=1920x1080,1920x1125,1080x1920,1109x1973|leading_formats=1920x1080,1920x1125,1080x1920,1109x1973|untouched=1080x1080,360x80,strip_vehicle|mask_bottom_ratio=' + MASK_BOTTOM_RATIO + '|yuan_scene_scale=' + YUAN_SCENE_SCALE + '|leading_excess_ratio=' + LEADING_EXCESS_RATIO + '|leading_target_ratio=' + LEADING_TARGET_RATIO + '|review_required=true');
 app.preferences.rulerUnits = Units.PIXELS; app.displayDialogs = DialogModes.NO;
 var psdCount = 0, pngCount = 0, headlineCount = 0;
 for (var fi = 0; fi < formats.length; fi++) {
  var cfg = formats[fi], fmt = formatById(cfg.stripInstallment ? r03 : r10, cfg.id), formatStart = new Date().getTime();
  doc = app.open(new File(BASE + cfg.input));
  if (doc.width.as('px') !== cfg.w || doc.height.as('px') !== cfg.h) throw Error('DIMENSION_MISMATCH|' + cfg.id + '|' + doc.width.as('px') + 'x' + doc.height.as('px'));
  if (doc.mode !== DocumentMode.RGB) throw Error('DOCUMENT_NOT_RGB|' + cfg.id);
  verifyStates();
  if (cfg.applyMask) tightenVehicleMask(fmt, fmt.zones.car);
  if (cfg.applyYuan) patchYuanScene(fmt, fmt.zones.car);
  var headlineChanged = cfg.checkHeadline ? patchHeadlineIfExcessive(fmt, fmt.zones.headline) : false;
  if (cfg.requireHeadlinePatch && !headlineChanged) throw Error('EXPECTED_HEADLINE_PATCH_NOT_TRIGGERED|' + cfg.id);
  if (headlineChanged) headlineCount++;
  if (cfg.stripInstallment) patchStripInstallment();
  var formatChanged = !!cfg.applyMask || !!cfg.applyYuan || headlineChanged || !!cfg.stripInstallment;
  if (!formatChanged) { msg('FORMAT_UNCHANGED|' + cfg.id + '|reason=headline_diagnostic_not_triggered'); doc.close(SaveOptions.DONOTSAVECHANGES); doc = null; continue; }
  var outPSD = new File(BASE + OUT_TPL_REL + 'BYD_TPL_' + cfg.id + '.psd');
  var po = new PhotoshopSaveOptions(); po.layers = true; po.embedColorProfile = true;
  doc.saveAs(outPSD, po, true, Extension.LOWERCASE); psdCount++;
  msg('OK|template|' + cfg.id + '|layer_comps=' + doc.layerComps.length + '|headline_changed=' + headlineChanged + '|strip_installment=' + (!!cfg.stripInstallment));
  if (cfg.applyMask) { activate(VD_ID); exportPNG(new File(BASE + OUT_PNG_REL + 'byd_' + VD_ID + '_' + cfg.id + '.png'), cfg.id + '|' + VD_ID); pngCount++; }
  if (cfg.applyYuan) { activate(YUAN_ID); exportPNG(new File(BASE + OUT_PNG_REL + 'byd_' + YUAN_ID + '_' + cfg.id + '.png'), cfg.id + '|' + YUAN_ID); pngCount++; }
  if (headlineChanged || cfg.stripInstallment) { activate(DOLPHIN_ID); exportPNG(new File(BASE + OUT_PNG_REL + 'byd_' + DOLPHIN_ID + '_' + cfg.id + '.png'), cfg.id + '|' + DOLPHIN_ID); pngCount++; }
  var formatExports = (cfg.applyMask ? 1 : 0) + (cfg.applyYuan ? 1 : 0) + (headlineChanged || cfg.stripInstallment ? 1 : 0);
  msg('FORMAT_OK|' + cfg.id + '|mask_changed=' + (!!cfg.applyMask) + '|yuan_scene_changed=' + (!!cfg.applyYuan) + '|headline_changed=' + headlineChanged + '|strip_installment=' + (!!cfg.stripInstallment) + '|exports=' + formatExports + '|elapsed_ms=' + (new Date().getTime() - formatStart));
  doc.close(SaveOptions.DONOTSAVECHANGES); doc = null;
 }
 msg('OK|completed|templates=' + psdCount + '|pngs=' + pngCount + '|headline_patches=' + headlineCount + '|source_r03_preserved=true|source_r10_preserved=true|elapsed_ms=' + (new Date().getTime() - RUN_START));
} catch (e) {
 if (log) msg('ERRO|' + e.message + '|line=' + e.line);
} finally {
 if (doc) doc.close(SaveOptions.DONOTSAVECHANGES);
 app.preferences.rulerUnits = oldUnits; app.displayDialogs = oldDialogs;
 if (log) log.close();
}
})();
