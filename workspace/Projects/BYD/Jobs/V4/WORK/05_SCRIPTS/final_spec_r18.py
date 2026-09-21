#!/usr/bin/env python3
"""Prepare R18 QA early; close native-template evidence only after R17/R20."""
from __future__ import annotations
import argparse,datetime as dt,hashlib,json,shutil
from pathlib import Path
def root(start):
 for p in (start,*start.parents):
  if (p/'.mkroot').exists():return p
 raise RuntimeError('MISSING_MKROOT')
ROOT=root(Path(__file__).resolve());V4=ROOT/'Projects/BYD/Jobs/V4';DATE='2026-09-20'
ASSEMBLY=V4/'WORK/04_QA/assembly_r11_v4.json';R11=V4/'WORK/00_MATRIZ/production_spec_r11.json';STAGING=V4/'WORK/03_STAGING'/f'{DATE}-r11';R17=V4/'WORK/01_TEMPLATES'/f'{DATE}-r17';R17LOG=V4/'WORK/06_LOGS/recapture_templates_r17.log';R19LOG=V4/'WORK/06_LOGS/recapture_templates_r19.log';R20LOG=V4/'WORK/06_LOGS/recapture_templates_r20.log';R11TPL=V4/'WORK/01_TEMPLATES'/f'{DATE}-r11';FICHAS=V4/'WORK/04_QA/fichas-r18'
OUT=V4/'WORK/00_MATRIZ/production_spec_r18.json';QA=V4/'WORK/04_QA/production-r18';MANIFEST=QA/'templates_manifest_r18.json';STRIP='1920x276';REST=('1920x1080','1920x1125','1080x1080','1080x1920','1109x1973','360x80')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def rel(p):return str(p.relative_to(V4))
def lines(p):return p.read_text(errors='replace').splitlines()
def require_r11():
 a=json.loads(ASSEMBLY.read_text());s=json.loads(R11.read_text())
 if a.get('count')!=154 or len(s.get('offers',[]))!=20 or len(s.get('formats',[]))!=7:raise RuntimeError('INVALID_R11_ASSEMBLY_SCOPE')
 expected={'byd_'+o['id']+'_'+f['id']+'.png' for f in s['formats'] for o in s['offers']};actual={p.name for p in STAGING.iterdir() if p.is_file() and p.suffix.lower()=='.png'}
 if actual!=expected:raise RuntimeError('R11_STAGING_NOT_140_EXACT')
 return s
def r17_strip():
 x=lines(R17LOG);fmt=[i for i,v in enumerate(x) if '|FORMAT_OK|'+STRIP+'|' in v];err=[i for i,v in enumerate(x) if '|ERRO|' in v];before=[v for v in x if '|COMP_APPLY_OK|before_save|'+STRIP+'|' in v];after=[v for v in x if '|COMP_APPLY_OK|after_reopen|'+STRIP+'|' in v]
 if len(fmt)!=1 or len(before)!=20 or len(after)!=20 or not err or fmt[0]>=err[0]:raise RuntimeError('R17_STRIP_EXCEPTION_INVALID')
 return {'log':rel(R17LOG),'format_ok':x[fmt[0]],'later_error':x[err[0]],'apply_tests_before_save':20,'apply_tests_after_reopen':20}
def r19_failed_zero_psd():
 x=lines(R19LOG)
 if not any('|ERRO|' in v for v in x) or any('|OUTPUT_SAVED|' in v for v in x):raise RuntimeError('R19_NOT_FAILED_ZERO_PSD')
 return {'log':rel(R19LOG),'status':'FAILED_ZERO_PSD','error_count':len([v for v in x if '|ERRO|' in v])}
def r20_rest():
 x=lines(R20LOG);done=[v for v in x if '|OK|completed|' in v]
 if len(done)!=1 or any('|ERRO|' in v for v in x):raise RuntimeError('R20_NOT_CLEANLY_COMPLETED')
 for f in REST:
  if len([v for v in x if '|FORMAT_OK|'+f+'|' in v])!=1:raise RuntimeError('R20_FORMAT_SCOPE_MISMATCH|'+f)
 if len([v for v in x if '|COMP_APPLY_OK|before_save|' in v])!=120 or len([v for v in x if '|COMP_APPLY_OK|after_reopen|' in v])!=120:raise RuntimeError('R20_APPLY_CHECKS_NOT_240')
 return {'log':rel(R20LOG),'terminal':done[0],'formats':list(REST),'apply_tests_before_save':120,'apply_tests_after_reopen':120}
def main(a):
 if a.prepare_qa:
  if OUT.exists() or QA.exists() or MANIFEST.exists():raise RuntimeError('REFUSE_OVERWRITE_R18_PREPARE')
  s=require_r11();QA.mkdir();s.update(revision='r18',template_revision='r17',native_template_status='WAITING_NATIVE_CHECKS',output_templates='WORK/01_TEMPLATES/'+DATE+'-r17/',output_staging='WORK/03_STAGING/'+DATE+'-r11/',r18_provenance={'assembly':rel(ASSEMBLY),'policy':'QA may inspect fixed R11 staging; R17/R20 native-template evidence remains open.'});OUT.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');print('OK|PREPARE_QA_R18|staging_pngs=140|native_templates=WAITING_NATIVE_CHECKS');return
 if not OUT.exists() or not QA.is_dir() or MANIFEST.exists():raise RuntimeError('FINALIZE_R18_PRECONDITION')
 s=require_r11();current=json.loads(OUT.read_text())
 if current.get('revision')!='r18' or current.get('native_template_status')!='WAITING_NATIVE_CHECKS':raise RuntimeError('R18_NOT_WAITING_NATIVE_CHECKS')
 ev17=r17_strip();ev19=r19_failed_zero_psd();ev20=r20_rest();expected={'BYD_TPL_'+f['id']+'.psd' for f in s['formats']};psds=sorted(p for p in R17.iterdir() if p.is_file() and p.suffix.lower()=='.psd')
 if len(psds)!=7 or {p.name for p in psds}!=expected:raise RuntimeError('COMBINED_R17_R19_PSD_SCOPE_MISMATCH')
 plan=[]
 for f in s['formats']:
  fid=f['id'];srcp=R11TPL/('BYD_TPL_'+fid+'_preview.png');srcf=FICHAS/('FICHA_R18_'+fid+'.md');dstp=R17/srcp.name;dstf=R17/('BYD_TPL_'+fid+'.md')
  if not srcp.is_file() or not srcf.is_file():raise RuntimeError('MISSING_PREVIEW_OR_FICHA|'+fid)
  if dstp.exists() or dstf.exists():raise RuntimeError('REFUSE_OVERWRITE_R17_SUPPORTING_ASSET|'+fid)
  plan += [(srcp,dstp,'preview'),(srcf,dstf,'ficha')]
 supporting=[]
 for src,dst,kind in plan:
  shutil.copy2(src,dst)
  if sha(src)!=sha(dst):raise RuntimeError('POSTCOPY_HASH_MISMATCH|'+dst.name)
  supporting.append({'kind':kind,'source':rel(src),'file':rel(dst),'bytes':dst.stat().st_size,'sha256':sha(dst),'byte_identical_to_source':kind=='preview'})
 current['native_template_status']='NATIVE_CHECKS_CLOSED';current['r18_provenance'].update({'r17_strip_exception':ev17,'r19_failed_zero_psd':ev19,'r20_rest':ev20,'policy':'No PSD copied. R17 strip plus R20 six formats form seven PSDs.'});OUT.write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
 rows=[{'file':rel(p),'bytes':p.stat().st_size,'sha256':sha(p),'template_revision':'r17_r20_combined'} for p in psds];MANIFEST.write_text(json.dumps({'revision':'r18','created_at':dt.datetime.now().astimezone().isoformat(),'count':7,'files':rows,'supporting_assets':supporting,'r17_strip_exception':ev17,'r19_failed_zero_psd':ev19,'r20_rest':ev20,'scope':'Native PSD/support hashes only; not technical, Astra visual, human, or delivery approval'},ensure_ascii=False,indent=2)+'\n');print('OK|FINALIZE_TEMPLATES_R18|psds=7|checks=280')
if __name__=='__main__':
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--prepare-qa',action='store_true');g.add_argument('--finalize-templates',action='store_true');main(p.parse_args())
