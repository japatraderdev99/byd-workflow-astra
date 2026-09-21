"""Transfer existing Astra visual reviews only across identical SHA-256 files."""
from pathlib import Path
import json, hashlib
from datetime import datetime, timezone

ROOT = Path(__file__).resolve()
while not (ROOT / '.mkroot').exists():
    ROOT = ROOT.parent
B = ROOT / 'Projects/BYD/Jobs/V4'
OUT = B / 'WORK/04_QA/production-r18/head_visual_review.json'
assert not OUT.exists(), 'REFUSE_OVERWRITE'
reports = [B/'WORK/04_QA/production-r03/head_strip_review.json']
reports += sorted((B/'WORK/04_QA/production-r10').glob('head_*x*.json'))
reports += [B/'WORK/04_QA/production-r14/head_visual_review.json']
reports += sorted((B/'WORK/04_QA/production-r16').glob('head_*x*.json'))
reviews = {}
for p in reports:
    d = json.loads(p.read_text())
    for r in d.get('files', d.get('rows', [])):
        reviews[r['file']] = dict(r, evidence=str(p.relative_to(B)))
amendment = json.loads((B/'WORK/04_QA/production-r10/head_amendment_yuan.json').read_text())
for r in amendment['overrides']:
    key = 'WORK/03_STAGING/2026-09-20-r10/byd_'+r['offer_id']+'_'+r['format']+'.png'
    reviews[key]['visual_status'] = r['visual_status']
assembly = json.loads((B/'WORK/04_QA/assembly_r11_v4.json').read_text())
origins = {r['destination']: r for r in assembly['files'] if r['kind'].startswith('png:')}
technical = json.loads((B/'WORK/04_QA/production-r18/technical_all.json').read_text())
assert technical['pass'] == 140 and len(origins) == 140
files = []
for t in technical['rows']:
    origin = origins[t['file']]
    r = reviews[origin['source']]
    assert r.get('visual_status', r.get('status')) == 'PASS', origin['source']
    actual = hashlib.sha256((B/t['file']).read_bytes()).hexdigest()
    assert actual == t['sha256'] == origin['sha256'] == r['sha256'], t['file']
    files.append(dict(file=t['file'], sha256=actual, offer_id=t['offer_id'], format=t['format'],
                      status='PASS', reviewer='Astra head', source_file=origin['source'],
                      review_evidence=r['evidence'],
                      notes=r.get('head_note', r.get('notes', '')),
                      method='Existing visual review transferred through byte-identical SHA-256; corrected images reviewed separately.'))
assert len(files) == len({r['file'] for r in files}) == 140
OUT.write_text(json.dumps(dict(at=datetime.now(timezone.utc).isoformat(), reviewer='Astra head',
    review_type='ASTRA_AGENT_VISUAL_REVIEW', visual_review_is_human_approval=False, scope='Visual composition review by agent, not client or legal approval; no external delivery.',
    amendment_applied='WORK/04_QA/production-r10/head_amendment_yuan.json',
    count=140, files=files), ensure_ascii=False, indent=2))
print('OK|HEAD_REVIEW_CONSOLIDATED|140')
