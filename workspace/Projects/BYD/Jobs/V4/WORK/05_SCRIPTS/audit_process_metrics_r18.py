#!/usr/bin/env python3
"""Read only production evidence and scoped session usage metadata; never copy prompts."""
import collections
import datetime as dt
import hashlib
import json
from pathlib import Path

REFUSE_OVERWRITE = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / '.mkroot').exists())
V4 = ROOT / 'Projects/BYD/Jobs/V4'
OUT = V4 / 'WORK/04_QA/process-audit-r18'
THREADS = {
 '01a0ba59-4230-7b12-9afe-04d440f22e6c': 'head',
 '01a0ba5a-3a17-7d80-9428-39bd9fb9266a': 'audit_matrix',
 '01a0ba5f-e5f4-7d03-becb-bfebf04358a5': 'diagnose_move',
}
def read(p): return json.loads(p.read_text())
def date(s): return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 if (OUT / 'metrics.json').exists(): raise RuntimeError('REFUSE_OVERWRITE')
 manifest = read(V4 / 'WORK/04_QA/manifest.json')
 start, end = date(manifest['job_start']), date(manifest['closed_at'])
 timelines = read(V4 / 'WORK/04_QA/production_timings_r18.json')
 sessions = Path.home() / '.codex/sessions/2026/09'
 all_ids = set(); tokens = collections.Counter(); agents = []; safe_records = []; calls = collections.Counter(); compact = 0
 phases = [
  ('desenvolvimento_pilotos', start, date('2026-09-19T22:38:00-03:00')),
  ('escala_correcoes', date('2026-09-19T22:38:00-03:00'), date('2026-09-20T01:16:25-03:00')),
  ('validacao_reuso_fechamento', date('2026-09-20T01:16:25-03:00'), end),
 ]
 phase_tokens = {n: collections.Counter() for n,_,_ in phases}
 for tid, role in THREADS.items():
  matches = [p for day in ('19','20') for p in (sessions/day).glob('*'+tid+'.jsonl')]
  if len(matches)!=1: raise RuntimeError('SESSION_MATCH_COUNT|' + tid)
  p = matches[0]; usage = collections.Counter(); models = collections.Counter(); records=[]; ids=set(); latest=None; first=None; tcalls=collections.Counter(); comps=0; limits=[]
  for line in p.open():
   d=json.loads(line); timestamp=date(d['timestamp']); a=d.get('payload',{}); kind=d['type']
   if not start <= timestamp <= end: continue
   if kind=='turn_context': models[str(a.get('model'))+'/'+str(a.get('effort'))]+=1
   if kind=='compacted': comps+=1
   if kind=='response_item' and a.get('type') in ('function_call','custom_tool_call'):
    tcalls[a.get('name','unknown')]+=1
   if kind=='event_msg' and a.get('type')=='token_count' and a.get('rate_limits'):
    rate=a['rate_limits']; primary=rate.get('primary') or {}; limits.append({'timestamp':d['timestamp'],'used_percent':primary.get('used_percent'),'window_minutes':primary.get('window_minutes'),'resets_at':primary.get('resets_at')})
   if kind!='token_usage_record': continue
   rid=a['response_id']
   if rid in ids: continue
   if rid in all_ids: raise RuntimeError('CROSS_THREAD_DUPLICATE_RESPONSE')
   ids.add(rid); all_ids.add(rid); usage.update(a['usage']); latest=a.get('thread_token_usage'); first=first or d['timestamp']
   record={'timestamp':d['timestamp'],'role':role,'thread_id':tid,'response_id':rid,'usage':a['usage']};records.append(record);safe_records.append(record)
   for name,left,right in phases:
    if left<=timestamp<right:phase_tokens[name].update(a['usage'])
  usage.setdefault('cache_write_input_tokens',0)
  cumulative_matches = all(usage.get(k,0)==v for k,v in (latest or {}).items())
  if not cumulative_matches: raise RuntimeError('CUMULATIVE_MISMATCH|' + role)
  tokens.update(usage);calls.update(tcalls);compact+=comps
  agents.append({'role':role,'thread_id':tid,'source_file':p.name,'first_usage_at':first,'last_usage_at':records[-1]['timestamp'],'usage_record_count':len(records),'registered_context_models':dict(models),'tokens':dict(usage),'cumulative_reconciles':cumulative_matches,'tool_dispatches':dict(tcalls),'compactions':comps,'account_limit_first':limits[0] if limits else None,'account_limit_last':limits[-1] if limits else None})
 measured=[]; formats=collections.defaultdict(dict)
 for run in timelines['runs']:
  terminal=run.get('terminal'); completed=bool(terminal)
  chosen=[]
  if terminal:chosen=[terminal]
  else:
   chosen=[e for e in run.get('nested_events',[]) if e['event'][0]=='FORMAT_OK']
   if not chosen and run['run']=='pilot_p06':chosen=[e for e in run.get('nested_events',[]) if 'template_trial' in e['event']]
  if chosen:measured.append({'run':run['run'],'kind':'terminal' if completed else 'completed_partial_segments','elapsed_ms':sum(e['elapsed_ms'] for e in chosen)})
  for e in run.get('nested_events',[]):
   if e['event'][0]=='FORMAT_OK':formats[e['event'][1]][run['run']]=e['elapsed_ms']
 input_tokens=tokens['input_tokens']; cached=tokens['cached_input_tokens']
 result={'schema':'byd-v4-process-audit/v1','created_at':dt.datetime.now().astimezone().isoformat(),'production_start':start.isoformat(),'production_cutoff':end.isoformat(),'documented_wall_seconds':(end-start).total_seconds(),'token_scope':'3 linked threads, usage records through local production close; excludes first intake interval before current root thread and excludes this report. Not a billing statement.','first_root_usage':agents[0]['first_usage_at'],'uncovered_initial_wall_seconds':(date(agents[0]['first_usage_at'])-start).total_seconds(),'tokens':dict(tokens),'uncached_input_tokens':input_tokens-cached,'cached_input_fraction':cached/input_tokens,'response_count':len(all_ids),'agents':agents,'tool_dispatches':dict(calls),'tool_dispatch_count':sum(calls.values()),'compactions':compact,'temporal_buckets':[{'name':n,'start':l.isoformat(),'end':r.isoformat(),'wall_seconds':(r-l).total_seconds(),'usage':dict(phase_tokens[n]),'meaning':'timestamp window, not exclusive time-on-task attribution'} for n,l,r in phases],'run_status_counts':dict(collections.Counter(r['status'] for r in timelines['runs'])),'completed_terminal_ms':timelines['aggregate']['completed_terminal_elapsed_ms_total'],'selected_elapsed_segments':measured,'selected_elapsed_ms':sum(r['elapsed_ms'] for r in measured),'format_elapsed_ms':dict(formats),'counts_by_format':manifest['counts_by_format'],'png_bytes':sum(r['bytes'] for r in manifest['files']),'psd_bytes':sum(r['bytes'] for r in read(V4/'WORK/04_QA/production-r18/templates_manifest_r18.json')['files']),'metrics':{'final_outputs':140,'visual_corrections':13,'unchanged_from_first_full_scale':127,'visual_rework_fraction':13/140,'scale_first_visual_pass_fraction':127/140,'native_state_tests':280,'native_state_tests_pass':280,'pixel_reexport_pass':3,'pixel_reexport_tested':3,'pixel_reexport_scope_of_outputs':3/140,'technical_pass':140,'structural_pass':7,'input_integrity_pass':48,'root_r10_outputs_per_minute':120/(1626940/60000),'r10_amortized_seconds_per_output':1626940/1000/120},'cost':{'actual_currency':None,'subscription_usage_attributed':None,'human_hours':None,'ui_active_seconds':None,'full_job_tokens':None},'source_hashes':{str(p.relative_to(V4)):digest(p) for p in [V4/'WORK/04_QA/manifest.json',V4/'WORK/04_QA/production_timings_r18.json',V4/'WORK/06_LOGS/DIARIO.md']}}
 OUT.mkdir(parents=True,exist_ok=True)
 (OUT/'usage_records_sanitized.json').write_text(json.dumps(safe_records,ensure_ascii=False,indent=2)+'\n')
 (OUT/'metrics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['tokens','uncached_input_tokens','cached_input_fraction','response_count','tool_dispatch_count','compactions','selected_elapsed_ms','uncovered_initial_wall_seconds']},ensure_ascii=False))
 print('OK|PROCESS_AUDIT_METRICS|CUTOFF_PRODUCTION_CLOSE|NO_PROMPTS_COPIED')

if __name__=='__main__': main()
