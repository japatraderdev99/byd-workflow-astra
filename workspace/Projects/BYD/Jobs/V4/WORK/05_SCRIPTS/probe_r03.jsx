#target photoshop
#include "../../../../../../operacao/lib/mkroot.jsxinc"
/*
  PROVENANCE
  Derived from build_p12.jsx.
  Incorporates the P16 contrast treatment and the P18 micro/footer geometry.
  Prepared for production_spec_probe_r03.json. Static review required before execution.
  This file does not approve production and must run under the workspace lock.

  R02 CHANGELOG
  Resolve duplicated anchors by their recursive source index path, with name
  lookup only as fallback. Restore only the copied anchor name and visibility.
  Preserve a duplicated root ArtLayer source name when no root alias is given.

  R03 CHANGELOG
  Hide selected car components only after group geometry is resolved.
  Add optional vertical scene clipping for source scenes with baked lower text.
  Prefer format role zones over legacy micro fallback zones for extras.
  Separate micro dual price, benefit, and headline zones.
*/
(function () {
var RUN_START = new Date().getTime();
var ROOT = MK.root();
var BASE = ROOT + '/Projects/BYD/Jobs/V4/';
var REFUSE_OVERWRITE = true;
var src = null, doc = null, log = null;
var oldUnits = app.preferences.rulerUnits, oldDialogs = app.displayDialogs;
var currentFmt = '', currentOffer = '', pngCount = 0;

var sf = new File(BASE + 'WORK/00_MATRIZ/production_spec_probe_r03.json');
if (!sf.exists) throw Error('MISSING_SPEC');
sf.encoding = 'UTF8'; sf.open('r'); var spec = eval('(' + sf.read() + ')'); sf.close();
log = new File(BASE + 'WORK/06_LOGS/probe_r03.log');
if (log.exists) throw Error('REFUSE_OVERWRITE');
log.encoding = 'UTF8'; log.open('w');

function msg(s) { log.writeln(new Date().toUTCString() + '|' + s); log.close(); log.open('a'); }
function cleanName(s) { return String(s).split('\u00ac\u2211').join('\u00b7'); }
function find(g, id) { if (!g || !g.layers) return null; for (var i = 0; i < g.layers.length; i++) { var l = g.layers[i]; if (l.id === id) return l; if (l.typename === 'LayerSet') { var r = find(l, id); if (r) return r; } } return null; }
function byName(g, n) { if (!g || !g.layers) return null; n = cleanName(n); for (var i = 0; i < g.layers.length; i++) { var l = g.layers[i]; if (cleanName(l.name) === n) return l; if (l.typename === 'LayerSet') { var r = byName(l, n); if (r) return r; } } return null; }
function directByName(g, n) { if (!g || !g.layers) return null; for (var i = 0; i < g.layers.length; i++) if (cleanName(g.layers[i].name) === cleanName(n)) return g.layers[i]; return null; }
function idPath(g, id) { if (!g) return null; if (sameId(g.id, id)) return []; if (!g.layers) return null; for (var i = 0; i < g.layers.length; i++) { var l = g.layers[i]; if (sameId(l.id, id)) return [i]; if (l.typename === 'LayerSet') { var tail = idPath(l, id); if (tail !== null) return [i].concat(tail); } } return null; }
function byIndexPath(g, path) { var l = g; if (!path) return null; for (var i = 0; i < path.length; i++) { if (!l.layers || path[i] < 0 || path[i] >= l.layers.length) return null; l = l.layers[path[i]]; } return l; }
function box(l) { if (!l) throw Error('BOX_NULL'); var b = l.bounds; return [b[0].as('px'), b[1].as('px'), b[2].as('px'), b[3].as('px')]; }
function rect(z) { return [z[0], z[1], z[0] + z[2], z[1] + z[3]]; }
function sameId(a, b) { return Number(a) === Number(b); }
function fresh(id) { var l = find(doc, id); if (!l) throw Error('DEST_ID_NOT_FOUND|' + id); return l; }
function makeGroup(parentId, n) { var p = parentId === null ? doc : fresh(parentId); var g = p.layerSets.add(); g.name = n; return g.id; }
function unlinkTree(g) { try { g.unlink(); } catch (e0) {} if (g.typename !== 'LayerSet') return; var ids = [], i, l; for (i = 0; i < g.layers.length; i++) ids.push(g.layers[i].id); for (i = 0; i < ids.length; i++) { l = find(g, ids[i]); if (l) unlinkTree(l); } }
function moveInto(movingId, targetId) { app.activeDocument = doc; var dst = fresh(targetId); if (dst.typename !== 'LayerSet') throw Error('MOVE_TARGET_NOT_GROUP|' + targetId); var marker = dst.artLayers.add(); marker.name = '__MK_MOVE_ANCHOR__'; var markerId = marker.id; try { fresh(movingId).move(fresh(markerId), ElementPlacement.PLACEBEFORE); } finally { var rest = find(doc, markerId); if (rest) rest.remove(); } var moved = fresh(movingId); if (!sameId(moved.parent.id, targetId)) throw Error('MOVE_VERIFY_FAILED|' + movingId + '|' + targetId); return moved; }
function moveManyInto(movingIds, targetId) { app.activeDocument = doc; var dst = fresh(targetId), marker = dst.artLayers.add(), markerId = marker.id; marker.name = '__MK_MOVE_ANCHOR__'; try { for (var i = 0; i < movingIds.length; i++) fresh(movingIds[i]).move(fresh(markerId), ElementPlacement.PLACEBEFORE); } finally { var rest = find(doc, markerId); if (rest) rest.remove(); } for (var j = 0; j < movingIds.length; j++) if (!sameId(fresh(movingIds[j]).parent.id, targetId)) throw Error('MOVE_VERIFY_FAILED|' + movingIds[j] + '|' + targetId); }
function sourceLayer(id) { app.activeDocument = src; var l = find(src, id); if (!l) throw Error('SOURCE_ID_NOT_FOUND|' + id); return l; }
function dupSource(id, parentId, name, anchorId, anchorName) { var l = sourceLayer(id), sourceRootName = l.name, anchorIsRoot = anchorId && sameId(l.id, anchorId), anchorPath = anchorId ? idPath(l, anchorId) : [], sourceAnchor = anchorId ? (anchorIsRoot ? l : find(l, anchorId)) : l; if (!sourceAnchor) throw Error('SOURCE_ANCHOR_NOT_FOUND|' + id + '|' + anchorId); if (anchorId && anchorPath === null) throw Error('SOURCE_ANCHOR_PATH_NOT_FOUND|' + id + '|' + anchorId); var sourceBox = box(sourceAnchor), sourceAnchorName = anchorName || sourceAnchor.name, sourceAnchorVisible = sourceAnchor.visible; msg('DUP_SOURCE_START|' + id + '|target=' + parentId + '|anchor_path=' + anchorPath.join('.')); l.duplicate(doc); app.activeDocument = doc; var cpId = doc.activeLayer.id; moveInto(cpId, parentId); var cp = fresh(cpId); unlinkTree(cp); var destAnchor = anchorId ? (anchorIsRoot ? cp : byIndexPath(cp, anchorPath)) : cp; if (!destAnchor && anchorId) { destAnchor = byName(cp, cleanName(sourceAnchorName)); msg('ANCHOR_PATH_FALLBACK_NAME|' + id + '|' + sourceAnchorName); } if (!destAnchor) throw Error('DEST_ANCHOR_NOT_FOUND|' + id + '|' + sourceAnchorName); if (anchorId && anchorName) { destAnchor.name = anchorName; destAnchor.visible = sourceAnchorVisible; } var destBox = box(destAnchor); cp.translate(sourceBox[0] - destBox[0], sourceBox[1] - destBox[1]); cp = fresh(cpId); if (name) cp.name = name; else if (cp.typename === 'ArtLayer') cp.name = sourceRootName; cp.visible = true; msg('DUP_SOURCE_OK|' + id + '|copy=' + cpId + '|target=' + parentId + '|anchor=' + cleanName(destAnchor.name)); return cpId; }
function dupLocal(id, parentId, name) { app.activeDocument = doc; var base = fresh(id), cp = base.duplicate(), cpId = cp.id; moveInto(cpId, parentId); cp = fresh(cpId); unlinkTree(cp); if (name) cp.name = name; cp.visible = true; return cpId; }
function affine(id, s, dx, dy, anchorName) { var l = fresh(id), a0 = anchorName ? byName(l, cleanName(anchorName)) : l; if (!a0) throw Error('AFFINE_ANCHOR_NOT_FOUND|' + anchorName); var b = box(a0); l.resize(s * 100, s * 100, AnchorPosition.TOPLEFT); l = fresh(id); var a1 = anchorName ? byName(l, cleanName(anchorName)) : l; var q = box(a1); l.translate(b[0] * s + dx - q[0], b[1] * s + dy - q[1]); }
function fit(id, z, align) { var l = fresh(id), b = box(l), s = Math.min(z[2] / Math.max(1, b[2] - b[0]), z[3] / Math.max(1, b[3] - b[1])); l.resize(s * 100, s * 100, AnchorPosition.TOPLEFT); l = fresh(id); b = box(l); var x = z[0]; if (align === 'center') x += (z[2] - (b[2] - b[0])) / 2; l.translate(x - b[0], z[1] - b[1]); return id; }
function wrapText(t, n) { var words = t.replace(/[\r\n]+/g, ' ').split(/\s+/), lines = [], line = ''; for (var i = 0; i < words.length; i++) { if (line.length + words[i].length + 1 > n && line) { lines.push(line); line = words[i]; } else line += (line ? ' ' : '') + words[i]; } if (line) lines.push(line); return lines.join('\r'); }
function rectMask(groupId, r, feather) { app.activeDocument = doc; doc.activeLayer = fresh(groupId); doc.selection.select([[r[0], r[1]], [r[2], r[1]], [r[2], r[3]], [r[0], r[3]]]); if (feather) doc.selection.feather(feather); var d = new ActionDescriptor(), ref = new ActionReference(); d.putClass(charIDToTypeID('Nw  '), charIDToTypeID('Chnl')); ref.putEnumerated(charIDToTypeID('Chnl'), charIDToTypeID('Chnl'), charIDToTypeID('Msk ')); d.putReference(charIDToTypeID('At  '), ref); d.putEnumerated(charIDToTypeID('Usng'), charIDToTypeID('UsrM'), charIDToTypeID('RvlS')); executeAction(charIDToTypeID('Mk  '), d, DialogModes.NO); doc.selection.deselect(); }
function sceneMask(groupId, z, verticalClip) { app.activeDocument = doc; doc.activeLayer = fresh(groupId); var x = z[0] - Math.min(50, doc.width.as('px') * .025), r = z[0] + z[2] + Math.min(50, doc.width.as('px') * .025), y = -100, b = doc.height.as('px') + 100, feather = Math.min(30, doc.width.as('px') * .012); if (verticalClip) { var pad = z[3] * .04; y = z[1] - pad; b = z[1] + z[3] + pad; feather = Math.max(1, Math.min(8, z[3] * .02)); msg('SCENE_VERTICAL_CLIP|' + currentFmt + '|' + currentOffer + '|rect=' + [x, y, r, b].join(',') + '|feather=' + feather); } doc.selection.select([[x, y], [r, y], [r, b], [x, b]]); doc.selection.feather(feather); var d = new ActionDescriptor(), ref = new ActionReference(); d.putClass(charIDToTypeID('Nw  '), charIDToTypeID('Chnl')); ref.putEnumerated(charIDToTypeID('Chnl'), charIDToTypeID('Chnl'), charIDToTypeID('Msk ')); d.putReference(charIDToTypeID('At  '), ref); d.putEnumerated(charIDToTypeID('Usng'), charIDToTypeID('UsrM'), charIDToTypeID('RvlS')); executeAction(charIDToTypeID('Mk  '), d, DialogModes.NO); doc.selection.deselect(); }
function addContrast(parentId, fmt) { if (!fmt.contrast_edge) return null; var darkId = makeGroup(parentId, 'CONTRASTE \u00b7 mascara suave'), dark = fresh(darkId), shade = dark.artLayers.add(); shade.name = 'AJUSTE CONTRASTE \u00b7 azul profundo \u00b7 opacidade editavel'; doc.activeLayer = shade; var color = new SolidColor(); color.rgb.hexValue = '061D34'; doc.selection.selectAll(); doc.selection.fill(color, ColorBlendMode.NORMAL, 100, false); doc.selection.deselect(); shade.opacity = 78; rectMask(darkId, [-300, -300, fmt.contrast_edge, fmt.h + 300], fmt.contrast_feather || 0); return darkId; }
function guideRect(fmt) { var m = fmt.safe_margin || fmt.guide_margin; if (m && m.length === 4) return [m[0], m[1], fmt.w - m[2], fmt.h - m[3]]; if (m && typeof m === 'object') return [m.left, m.top, fmt.w - m.right, fmt.h - m.bottom]; if (typeof m !== 'number') m = Math.max(4, Math.round(Math.min(fmt.w, fmt.h) * .05)); return [m, m, fmt.w - m, fmt.h - m]; }
function addGuideOutline(guidesId, fmt) { var g = fresh(guidesId), l = g.artLayers.add(); l.name = 'MARGEM SEGURA EDITAVEL'; doc.activeLayer = l; var r = guideRect(fmt), color = new SolidColor(); color.rgb.hexValue = '00FFFF'; doc.selection.select([[r[0], r[1]], [r[2], r[1]], [r[2], r[3]], [r[0], r[3]]]); doc.selection.stroke(color, 1, StrokeLocation.INSIDE, ColorBlendMode.NORMAL, 100, false); doc.selection.deselect(); g.visible = false; msg('GUIDE|' + fmt.id + '|rect=' + r.join(',')); }
function fillRectLayer(parentId, name, r, hex) { var p = fresh(parentId), l = p.artLayers.add(); l.name = name; doc.activeLayer = l; var color = new SolidColor(); color.rgb.hexValue = hex; doc.selection.select([[r[0], r[1]], [r[2], r[1]], [r[2], r[3]], [r[0], r[3]]]); doc.selection.fill(color, ColorBlendMode.NORMAL, 100, false); doc.selection.deselect(); return l.id; }
function fitNamed(rootId, n, z, align) { var l = byName(fresh(rootId), n); if (!l) throw Error('NAMED_LAYER_NOT_FOUND|' + n); return fit(l.id, z, align); }
function applyMicroFooter(fixId, footerId) { var footer = fresh(footerId); footer.visible = true; var bandId = fillRectLayer(fixId, 'FUNDO FAIXA SELOS', [0, 57, 360, 80], '071D31'); fresh(bandId).move(fresh(footerId), ElementPlacement.PLACEAFTER); fitNamed(footerId, 'SELOS GARANTIA E RECOMPRA', [7, 61, 96, 15], 'left'); fitNamed(footerId, 'brasil', [108, 60, 36, 17], 'center'); fitNamed(footerId, 'Clientes Satisfeitos Negativo', [150, 60, 19, 17], 'center'); var ib = byName(fresh(footerId), 'IBAMA'); if (!ib) throw Error('MISSING_IBAMA'); var icon = byName(ib, 'Vector Smart Object copy'); if (!icon) throw Error('MISSING_IBAMA_ICON'); fit(icon.id, [176, 61, 13, 16], 'center'); var educational = null; for (var i = 0; i < ib.artLayers.length; i++) if (ib.artLayers[i].kind === LayerKind.TEXT) educational = ib.artLayers[i]; if (!educational) throw Error('MISSING_TRAFFIC_MESSAGE'); educational.textItem.kind = TextType.POINTTEXT; fit(educational.id, [194, 66, 159, 9], 'left'); msg('MICRO_FOOTER_OK|text=' + educational.textItem.contents.replace(/[\r\n]+/g, ' ')); }
function extraZone(extra, fmt, z) { if (extra.zones && extra.zones[fmt.id]) return extra.zones[fmt.id]; if (extra.zone) return extra.zone; if (z[extra.role]) return z[extra.role]; if (fmt.family === 'micro' && extra.role === 'badges') return [8, 38, 77, 12]; if (fmt.family === 'micro' && extra.role === 'instal') return [8, 38, 77, 17]; return null; }
function carTagZone(o, fmt, z) { if (o.car_tag_zones && o.car_tag_zones[fmt.id]) return o.car_tag_zones[fmt.id]; return z.tag || null; }
function hasExplicitExtraZone(extra, fmt) { return !!((extra.zones && extra.zones[fmt.id]) || extra.zone); }
function verifyZone(label, id, z, tol, force) { var l = fresh(id), b = box(l), rr = rect(z), visible = l.visible; msg('GEOM|' + currentFmt + '|' + currentOffer + '|' + label + '|bounds=' + b.join(',') + '|zone=' + z.join(',') + '|visible=' + visible); if ((visible || force) && (b[0] < rr[0] - tol || b[1] < rr[1] - tol || b[2] > rr[2] + tol || b[3] > rr[3] + tol)) throw Error('GEOM_OUTSIDE_ZONE|' + currentFmt + '|' + currentOffer + '|' + label); }
function verifyTextCanvas(g, path, ancestorsVisible) { var effective = ancestorsVisible && g.visible; if (g.typename === 'ArtLayer') { if (effective && g.kind === LayerKind.TEXT) { var b = box(g), w = doc.width.as('px'), h = doc.height.as('px'); if (b[0] < -2 || b[1] < -2 || b[2] > w + 2 || b[3] > h + 2) throw Error('TEXT_OUTSIDE_CANVAS|' + currentFmt + '|' + currentOffer + '|' + path); } return; } for (var i = 0; i < g.layers.length; i++) verifyTextCanvas(g.layers[i], path + '/' + cleanName(g.layers[i].name), effective); }
function verifyLegal(id, z) { var l = fresh(id), t = l.textItem.contents, b = box(l); if (!t || !t.replace(/\s+/g, '')) throw Error('LEGAL_EMPTY|' + currentOffer); msg('LEGAL_DIAG|' + currentFmt + '|' + currentOffer + '|chars=' + t.length + '|bounds=' + b.join(',') + '|zone_h=' + z[3]); if (b[3] - b[1] > z[3] + 2) throw Error('LEGAL_OVERSET_SUSPECT|' + currentFmt + '|' + currentOffer); }
function activateState(states, activeIndex, guidesId) { for (var i = 0; i < states.length; i++) for (var j = 0; j < states[i].length; j++) fresh(states[i][j]).visible = (i === activeIndex); fresh(guidesId).visible = false; }
function exportPNG(file, label) { if (file.exists) throw Error('REFUSE_OVERWRITE|' + file.fsName); var eo = new ExportOptionsSaveForWeb(); eo.format = SaveDocumentType.PNG; eo.PNG8 = false; eo.transparency = false; eo.interlaced = false; eo.includeProfile = true; doc.exportDocument(file, ExportType.SAVEFORWEB, eo); msg('OK|png|' + label); }
function requireFolder(rel) { var f = new Folder(BASE + rel); if (!f.exists) throw Error('MISSING_OUTPUT_FOLDER|' + rel); }
function preflightOutputs() { requireFolder(spec.output_templates); requireFolder(spec.output_staging); for (var fi = 0; fi < spec.formats.length; fi++) { var fmt = spec.formats[fi], psd = new File(BASE + spec.output_templates + 'BYD_TPL_' + fmt.id + '.psd'), preview = new File(BASE + spec.output_templates + 'BYD_TPL_' + fmt.id + '_preview.png'); if (psd.exists || preview.exists) throw Error('REFUSE_OVERWRITE|' + fmt.id); for (var oi = 0; oi < spec.offers.length; oi++) if (new File(BASE + spec.output_staging + 'byd_' + spec.offers[oi].id + '_' + fmt.id + '.png').exists) throw Error('REFUSE_OVERWRITE|' + spec.offers[oi].id + '|' + fmt.id); } }

try {
 if (app.documents.length !== 0) throw Error('PREFLIGHT_DOCS_ABERTOS');
 if (!spec.formats || spec.formats.length !== 1) throw Error('EXPECTED_7_FORMATS');
 if (!spec.offers || spec.offers.length !== 2) throw Error('EXPECTED_20_OFFERS');
 if (!spec.fixed || !spec.fixed.background) throw Error('MISSING_FIXED_BACKGROUND');
 preflightOutputs();
 msg('SCRIPT_PREPARED|build_production_r03.jsx|derived=build_production_r02|fix=hidden_component_vertical_clip_extra_zone_micro_dual|patches=p16,p18|review_required=true');
 app.displayDialogs = DialogModes.NO; app.preferences.rulerUnits = Units.PIXELS;
 src = app.open(new File(BASE + spec.source));

 for (var fi = 0; fi < spec.formats.length; fi++) {
  var fmt = spec.formats[fi], z = fmt.zones, formatStart = new Date().getTime(); currentFmt = fmt.id;
  msg('FORMAT_START|' + fmt.id);
  doc = app.documents.add(fmt.w, fmt.h, 72, 'BYD_TPL_' + fmt.id, NewDocumentMode.RGB, DocumentFill.WHITE, 1, BitsPerChannelType.EIGHT, 'sRGB IEC61966-2.1');
  var bgId = makeGroup(null, 'BG'), carId = makeGroup(null, 'VEICULO'), legalId = makeGroup(null, 'LEGAL'), condsId = makeGroup(null, 'CONDICIONAIS'), offerId = makeGroup(null, 'OFERTA'), fixId = makeGroup(null, 'FIXO'), guidesId = makeGroup(null, '#GUIAS');
  addGuideOutline(guidesId, fmt);

  var tagId = null, footerId = null;
  if (spec.fixed.tagline) { tagId = dupSource(spec.fixed.tagline, fixId, 'ASSINATURA'); if (z.tagline) fit(tagId, z.tagline, 'center'); else { fresh(tagId).visible = false; msg('OMISSAO_PROPOSTA|' + fmt.id + '|tagline'); } }
  if (spec.fixed.footer) { footerId = dupSource(spec.fixed.footer, fixId, 'RODAPE'); if (fmt.family === 'micro') applyMicroFooter(fixId, footerId); else if (z.footer) fit(footerId, z.footer, 'center'); else { fresh(footerId).visible = false; msg('OMISSAO_PROPOSTA|' + fmt.id + '|footer'); } }
  var place = new ActionDescriptor(); place.putPath(charIDToTypeID('null'), new File(BASE + spec.logo)); place.putEnumerated(charIDToTypeID('FTcs'), charIDToTypeID('QCSt'), charIDToTypeID('Qcsa')); executeAction(charIDToTypeID('Plc '), place, DialogModes.NO); var logoId = doc.activeLayer.id; moveInto(logoId, fixId); unlinkTree(fresh(logoId)); fresh(logoId).name = 'LOGO'; fit(logoId, z.logo, 'center');

  var bgCacheId = dupSource(spec.fixed.background, guidesId, '#KV_CACHE_ORIGINAL'); fresh(bgCacheId).visible = true; fresh(guidesId).visible = false;
  var states = [], records = [];
  for (var oi = 0; oi < spec.offers.length; oi++) {
   var offerStart = new Date().getTime(), o = spec.offers[oi]; currentOffer = o.id; msg('OFFER_BUILD_START|' + fmt.id + '|' + o.id);
   var ogId = makeGroup(offerId, o.id), cgId = makeGroup(condsId, 'COND \u00b7 ' + o.id), lgId = makeGroup(legalId, o.id), vgId = makeGroup(carId, 'CAR \u00b7 ' + o.id), bgOId = makeGroup(bgId, o.id);
   var cb = o.car_bounds, s = Math.min(z.car[2] / (cb[2] - cb[0]), z.car[3] / (cb[3] - cb[1])), dx = z.car[0] + (z.car[2] - (cb[2] - cb[0]) * s) / 2 - cb[0] * s, dy = z.car[1] + (z.car[3] - (cb[3] - cb[1]) * s) / 2 - cb[1] * s;

   var bkId = dupLocal(bgCacheId, bgOId, 'KV'), bb = box(fresh(bkId)), bgS = s, bgDX = dx, horizon = 600 * s + dy; bgS = Math.max(bgS, bgDX / (-bb[0]), (fmt.w - bgDX) / bb[2], horizon / (600 - bb[1]), (fmt.h - horizon) / (bb[3] - 600)); affine(bkId, bgS, bgDX, horizon - 600 * bgS); addContrast(bgOId, fmt);

   var vehicleId, componentCopies = {};
   if (o.car_components && o.car_components.length) { vehicleId = makeGroup(vgId, 'CENA ORIGINAL'); for (var cc = 0; cc < o.car_components.length; cc++) { var componentSourceId = o.car_components[cc], componentCopyId = dupSource(componentSourceId, vehicleId, null); componentCopies[String(componentSourceId)] = componentCopyId; } msg('CAR_COMPONENTS|' + fmt.id + '|' + o.id + '|ids=' + o.car_components.join(',')); }
   else vehicleId = dupSource(o.car, vgId, 'CENA ORIGINAL', o.anchor_id, o.anchor_name);
   affine(vehicleId, s, dx, dy, o.anchor_name);
   if (o.hide_car_component_ids && o.hide_car_component_ids.length) { for (var hc = 0; hc < o.hide_car_component_ids.length; hc++) { var hiddenSourceId = o.hide_car_component_ids[hc], hiddenCopyId = componentCopies[String(hiddenSourceId)]; if (!hiddenCopyId) throw Error('HIDE_COMPONENT_NOT_COPIED|' + o.id + '|' + hiddenSourceId); fresh(hiddenCopyId).visible = false; msg('CAR_COMPONENT_HIDDEN|' + fmt.id + '|' + o.id + '|source=' + hiddenSourceId + '|copy=' + hiddenCopyId); } }
   var carTagId = null, carTagZ = null;
   if (o.car_tag_names && o.car_tag_names.length) { carTagZ = carTagZone(o, fmt, z); if (!carTagZ) throw Error('MISSING_CAR_TAG_ZONE|' + fmt.id + '|' + o.id); carTagId = makeGroup(cgId, 'COND \u00b7 tag \u00b7 ' + o.id); var wanted = {}, tagIds = [], vehicleNow = fresh(vehicleId); for (var wn = 0; wn < o.car_tag_names.length; wn++) wanted[cleanName(o.car_tag_names[wn])] = true; for (var vl = 0; vl < vehicleNow.layers.length; vl++) if (wanted[cleanName(vehicleNow.layers[vl].name)]) tagIds.push(vehicleNow.layers[vl].id); if (tagIds.length !== o.car_tag_names.length) throw Error('MISSING_DIRECT_CAR_TAG|' + o.id + '|expected=' + o.car_tag_names.length + '|found=' + tagIds.length); moveManyInto(tagIds, carTagId); fit(carTagId, carTagZ, 'center'); msg('CAR_TAG_EXTRACTED|' + fmt.id + '|' + o.id + '|names=' + o.car_tag_names.join(',')); }
   sceneMask(vgId, z.car, o.scene_vertical_clip === true);
   var titleId = dupSource(o.title, ogId, 'MODELO'); fit(titleId, z.title, fmt.align);
   var priceZone = fmt.family === 'micro' ? (o.micro_dual ? [95, 19, 145, 20] : [95, 19, 145, 25]) : z.price;
   var priceId = dupSource(o.price, ogId, 'PRECO'); fit(priceId, priceZone, fmt.align === 'center' && fmt.family !== 'micro' ? 'center' : 'left');
   var benefitId = null, headlineId = null;
   if (o.benefit) { benefitId = dupSource(o.benefit, cgId, 'COND \u00b7 BENEFICIO \u00b7 ' + o.id); var benefit = fresh(benefitId); if (benefit.typename === 'ArtLayer' && benefit.kind === LayerKind.TEXT) { benefit.textItem.kind = TextType.POINTTEXT; benefit.textItem.contents = benefit.textItem.contents.replace(/[\r\n]+/g, ' '); benefit.textItem.justification = fmt.align === 'center' ? Justification.CENTER : Justification.LEFT; } fit(benefitId, z.benefit, fmt.align); }
   if (o.headline) { headlineId = dupSource(o.headline, cgId, 'COND \u00b7 HEADLINE \u00b7 ' + o.id); var headline = fresh(headlineId); if (headline.typename === 'ArtLayer' && headline.kind === LayerKind.TEXT) { headline.textItem.kind = TextType.POINTTEXT; headline.textItem.contents = headline.textItem.contents.replace(/[\r\n]+/g, ' '); headline.textItem.contents = wrapText(headline.textItem.contents, fmt.headline_wrap); headline.textItem.justification = fmt.align === 'center' ? Justification.CENTER : Justification.LEFT; } fit(headlineId, z.headline, fmt.align); }
   var benefitZone = z.benefit, headlineZone = z.headline;
   if (fmt.family === 'micro') { var vd = o.id.indexOf('vd-') === 0; if (o.micro_dual) { if (!benefitId || !headlineId) throw Error('MICRO_DUAL_REQUIRES_BOTH|' + o.id); benefitZone = [95, 42, 255, 6]; headlineZone = [95, 50, 255, 6]; fresh(benefitId).visible = true; fresh(headlineId).visible = true; fit(benefitId, benefitZone, 'center'); fit(headlineId, headlineZone, 'center'); msg('MICRO_DUAL|' + o.id); } else { benefitZone = [95, 48, 255, 7]; headlineZone = [95, 48, 255, 7]; var chosenId = vd && headlineId ? headlineId : (benefitId || headlineId); if (benefitId) fresh(benefitId).visible = sameId(benefitId, chosenId); if (headlineId) fresh(headlineId).visible = sameId(headlineId, chosenId); if (chosenId) fit(chosenId, sameId(chosenId, headlineId) ? headlineZone : benefitZone, 'center'); if (vd && !headlineId) msg('MICRO_FALLBACK|' + o.id + '|headline_null_using_benefit'); } }

   var legalLayerId = dupSource(o.legal, lgId, 'TEXTO LEGAL'); var lt = fresh(legalLayerId); if (z.legal) { lt.textItem.kind = TextType.PARAGRAPHTEXT; lt.textItem.size = UnitValue(fmt.legal_font, 'px'); lt.textItem.useAutoLeading = false; lt.textItem.leading = UnitValue(fmt.legal_font + 2, 'px'); lt.textItem.width = UnitValue(z.legal[2], 'px'); lt.textItem.height = UnitValue(z.legal[3], 'px'); lt.textItem.position = [UnitValue(z.legal[0], 'px'), UnitValue(z.legal[1], 'px')]; lt.textItem.justification = Justification.LEFT; } else { lt.visible = false; msg('OMISSAO_PROPOSTA|' + fmt.id + '|' + o.id + '|legal'); }

   var extras = o.extras || [], roles = {}, extraRecords = [];
   for (var rc = 0; rc < extras.length; rc++) if (!extras[rc].embedded_in_car) roles[extras[rc].role] = (roles[extras[rc].role] || 0) + 1;
   for (var ei = 0; ei < extras.length; ei++) {
    var extra = extras[ei];
    if (extra.embedded_in_car) { msg('EXTRA_EMBEDDED_IN_CAR|' + fmt.id + '|' + o.id + '|' + extra.id + '|' + extra.role); continue; }
    if (roles[extra.role] > 1 && !hasExplicitExtraZone(extra, fmt)) throw Error('EXTRA_ZONE_COLLISION|' + fmt.id + '|' + o.id + '|' + extra.role);
    var ez = extraZone(extra, fmt, z), elId = dupSource(extra.id, cgId, 'COND \u00b7 ' + extra.role + ' \u00b7 ' + o.id, extra.anchor_id, extra.anchor_name);
    if (ez) {
     if (extra.crop) { var ec = extra.crop, es = Math.min(ez[2] / (ec[2] - ec[0]), ez[3] / (ec[3] - ec[1])), ex = ez[0] + (ez[2] - (ec[2] - ec[0]) * es) / 2 - ec[0] * es, ey = ez[1] - ec[1] * es; affine(elId, es, ex, ey, extra.anchor_name); var frameId = makeGroup(cgId, 'ENQUADRAMENTO \u00b7 ' + extra.role + ' \u00b7 ' + o.id); moveInto(elId, frameId); rectMask(frameId, rect(ez), 0); extraRecords.push({ label: 'extra:' + extra.role, id: frameId, zone: ez }); }
     else { var el = fresh(elId); if (el.typename === 'ArtLayer' && el.kind === LayerKind.TEXT) { el.textItem.kind = TextType.POINTTEXT; el.textItem.contents = wrapText(el.textItem.contents, fmt.family === 'micro' && extra.role === 'instal' ? 16 : (fmt.family === 'micro' ? 12 : 60)); } fit(elId, ez, extra.align || 'center'); extraRecords.push({ label: 'extra:' + extra.role, id: elId, zone: ez }); }
    } else { fresh(elId).visible = false; msg('OMISSAO_PROPOSTA|' + fmt.id + '|' + o.id + '|' + extra.role); extraRecords.push({ label: 'extra:' + extra.role, id: elId, zone: null }); }
   }

   currentOffer = o.id;
   verifyZone('title', titleId, z.title, 2); verifyZone('price', priceId, priceZone, 2);
   if (benefitId) verifyZone('benefit', benefitId, benefitZone, 2);
   if (headlineId) verifyZone('headline', headlineId, headlineZone, 2);
   var carAnchor = byName(fresh(vehicleId), cleanName(o.anchor_name)); if (!carAnchor) throw Error('CAR_ANCHOR_NOT_FOUND|' + o.id); verifyZone('car_anchor', carAnchor.id, z.car, 2, true);
   if (carTagId) verifyZone('car_tag', carTagId, carTagZ, 2);
   if (z.legal) { verifyZone('legal', legalLayerId, z.legal, 2); verifyLegal(legalLayerId, z.legal); }
   for (var er = 0; er < extraRecords.length; er++) if (extraRecords[er].zone) verifyZone(extraRecords[er].label, extraRecords[er].id, extraRecords[er].zone, 2);
   verifyTextCanvas(fresh(ogId), 'OFERTA/' + o.id, true); verifyTextCanvas(fresh(cgId), 'CONDICIONAIS/' + o.id, true); verifyTextCanvas(fresh(lgId), 'LEGAL/' + o.id, true);
   records.push({ offer: o, title: titleId, price: priceId, benefit: benefitId, headline: headlineId, legal: legalLayerId, vehicle: vehicleId, extras: extraRecords });
   states.push([ogId, cgId, lgId, vgId, bgOId]); fresh(ogId).visible = false; fresh(cgId).visible = false; fresh(lgId).visible = false; fresh(vgId).visible = false; fresh(bgOId).visible = false;
   msg('OFFER_BUILD_OK|' + fmt.id + '|' + o.id + '|elapsed_ms=' + (new Date().getTime() - offerStart));
  }

  var cache = find(doc, bgCacheId); if (cache) cache.remove(); fresh(guidesId).visible = false;
  for (var ci = 0; ci < states.length; ci++) { activateState(states, ci, guidesId); doc.layerComps.add('OFERTA ' + spec.offers[ci].id, 'offer_id=' + spec.offers[ci].id, true, false, false); }
  activateState(states, 0, guidesId);

  var psdf = new File(BASE + spec.output_templates + 'BYD_TPL_' + fmt.id + '.psd'); if (psdf.exists) throw Error('REFUSE_OVERWRITE'); var po = new PhotoshopSaveOptions(); po.layers = true; po.embedColorProfile = true; doc.saveAs(psdf, po, true, Extension.LOWERCASE); msg('OK|template|' + fmt.id + '|layer_comps=' + doc.layerComps.length);
  fresh(guidesId).visible = true; exportPNG(new File(BASE + spec.output_templates + 'BYD_TPL_' + fmt.id + '_preview.png'), 'preview|' + fmt.id + '|' + spec.offers[0].id); fresh(guidesId).visible = false;
  for (var xo = 0; xo < states.length; xo++) { var exportStart = new Date().getTime(); currentOffer = spec.offers[xo].id; activateState(states, xo, guidesId); exportPNG(new File(BASE + spec.output_staging + 'byd_' + currentOffer + '_' + fmt.id + '.png'), currentOffer + '|' + fmt.id); pngCount++; msg('OFFER_EXPORT_OK|' + fmt.id + '|' + currentOffer + '|elapsed_ms=' + (new Date().getTime() - exportStart)); }
  msg('FORMAT_OK|' + fmt.id + '|offers=' + states.length + '|elapsed_ms=' + (new Date().getTime() - formatStart));
  doc.close(SaveOptions.DONOTSAVECHANGES); doc = null;
 }
 if (pngCount !== 2) throw Error('PNG_COUNT_MISMATCH|' + pngCount);
 msg('OK|completed|formats=1|offers=2|pngs=' + pngCount + '|elapsed_ms=' + (new Date().getTime() - RUN_START));
} catch (e) {
 if (log) msg('ERRO|' + e.message + '|line=' + e.line + '|format=' + currentFmt + '|offer=' + currentOffer);
} finally {
 if (doc) doc.close(SaveOptions.DONOTSAVECHANGES);
 if (src) src.close(SaveOptions.DONOTSAVECHANGES);
 app.preferences.rulerUnits = oldUnits; app.displayDialogs = oldDialogs;
 if (log) log.close();
}
})();
