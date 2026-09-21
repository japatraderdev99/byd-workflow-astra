#!/usr/bin/env python3
"""Locally promote R18 PNGs only after complete technical, structural, and Astra QA."""
from __future__ import annotations
import argparse,datetime as dt,hashlib,json,shutil
from pathlib import Path
def root(start):
 for p in (start,*start.parents):
  if (p/'.mkroot').exists():return p
 raise RuntimeError('MISSING_MKROOT')
ROOT=root(Path(__file__).resolve());V4=ROOT/'Projects/BYD/Jobs/V4';QA=V4/'WORK/04_QA/production-r18';SPEC=V4/'WORK/00_MATRIZ/production_spec_r18.json';OUT=V4/'OUTPUT/2026-09-20-r18';MANIFEST=QA/'manifest_r18.json';TEMPLATES=QA/'templates_manifest_r18.json';REUSE=V4/'WORK/04_QA/reuse_validation_r18.json'
DEST={'1920x276':'BANNER DESK','1920x1125':'BANNER DESK','360x80':'BANNER MOBILE','1109x1973':'BANNER MOBILE','1080x1080':'ESTATICOS','1080x1920':'ESTATICOS','1920x1080':'ESTATICOS'}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');a=p.parse_args()
 if not a.execute:raise RuntimeError('REFUSE_PROMOTION_WITHOUT_--execute')
 if MANIFEST.exists():raise RuntimeError('REFUSE_OVERWRITE_MANIFEST')
 s=json.loads(SPEC.read_text());tech=json.loads((QA/'technical_all.json').read_text());struct=json.loads((QA/'structural7.json').read_text());visual=json.loads((QA/'head_visual_review.json').read_text());templates=json.loads(TEMPLATES.read_text());reuse=json.loads(REUSE.read_text())
 if s.get('revision')!='r18' or len(s['offers'])!=20 or len(s['formats'])!=7:raise RuntimeError('INVALID_R18_SCOPE')
 if s.get('native_template_status')!='NATIVE_CHECKS_CLOSED':raise RuntimeError('NATIVE_TEMPLATES_NOT_CLOSED')
 if templates.get('revision')!='r18' or templates.get('count')!=7 or len(templates.get('files',[]))!=7:raise RuntimeError('TEMPLATES_MANIFEST_NOT_7')
 for template in templates['files']:
  path=V4/template['file']
  if not path.is_file() or sha(path)!=template.get('sha256'):raise RuntimeError('TEMPLATE_HASH_MISMATCH|'+template['file'])
 if reuse.get('count')!=3 or reuse.get('all_pixels_identical') is not True:raise RuntimeError('REUSE_R18_NOT_PASS')
 if tech.get('pass')!=140 or len(tech.get('rows',[]))!=140:raise RuntimeError('TECHNICAL_QA_NOT_140_PASS')
 if struct.get('pass')!=7 or len(struct.get('rows',[]))!=7:raise RuntimeError('STRUCTURAL_QA_NOT_7_PASS')
 if visual.get('review_type')!='ASTRA_AGENT_VISUAL_REVIEW':raise RuntimeError('INVALID_REVIEW_TYPE_EXPECTED_ASTRA_AGENT')
 approved={x['file']:x for x in visual.get('files',[]) if x.get('status')=='PASS'}
 if len(approved)!=140:raise RuntimeError('ASTRA_VISUAL_REVIEW_NOT_140_PASS')
 plan=[]
 for row in tech['rows']:
  src=V4/row['file']; rev=approved.get(row['file']);fmt=row['format'];dst=OUT/DEST[fmt]/fmt/src.name
  if not rev or not src.is_file() or sha(src)!=row.get('sha256') or sha(src)!=rev.get('sha256'):raise RuntimeError('SOURCE_OR_HASH_MISMATCH|'+row['file'])
  if dst.exists():raise RuntimeError('REFUSE_OVERWRITE|'+str(dst.relative_to(V4)))
  plan.append((src,dst,row))
 done=[]
 for src,dst,row in plan:
  dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
  if sha(dst)!=row['sha256']:raise RuntimeError('POSTCOPY_HASH_MISMATCH')
  done.append({**row,'output_file':str(dst.relative_to(V4)),'visual_status':'ASTRA_AGENT_VISUAL_REVIEW_PASS','visual_review_is_human_approval':False,'delivery_status':'LOCAL_OUTPUT_NOT_EXTERNALLY_SENT'})
 MANIFEST.write_text(json.dumps({'revision':'r18','created_at':dt.datetime.now().astimezone().isoformat(),'count':140,'files':done,'visual_review_type':'ASTRA_AGENT_VISUAL_REVIEW','visual_review_is_human_approval':False,'delivery_status':'LOCAL_ONLY'},ensure_ascii=False,indent=2)+'\n');print('OK|PROMOTED_R18|140')
if __name__=='__main__':main()
