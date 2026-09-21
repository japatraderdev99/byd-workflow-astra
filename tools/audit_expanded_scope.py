"""Audit only lifecycle, usage and model metadata in the two linked BYD executions."""
from pathlib import Path
import json,collections,datetime as dt,os
P=Path(__file__).resolve().parents[1];old=json.loads((P/'data/metrics_original.json').read_text());base=Path(os.environ.get('CODEX_SESSIONS_DIR',str(Path.home()/'.codex/sessions')))/'2026/09/19'
ROOTS={'01a0ba2f-f298-7f90-8451-bbd56fa44fe9':'head_initial','01a0ba59-4230-7b12-9afe-04d440f22e6c':'head_main'}
def date(s):return dt.datetime.fromisoformat(s.replace('Z','+00:00'))
production_end=date(old['production_cutoff']);end=date('2026-09-20T05:22:56.047Z');files=[]
for f in base.glob('*.jsonl'):
 with f.open() as q:meta=json.loads(next(q)).get('payload',{})
 source=meta.get('source');parent=None;agent=None
 if isinstance(source,dict):
  spawn=(source.get('subagent') or {}).get('thread_spawn') or {};parent=spawn.get('parent_thread_id');agent=spawn.get('agent_path')
 if meta.get('id') in ROOTS or parent in ROOTS:files.append((f,meta.get('id'),ROOTS.get(meta.get('id'),agent),parent))
first=next(f for f,tid,_,_ in files if tid==list(ROOTS)[0]);starts=[]
for line in first.open():
 d=json.loads(line);a=d.get('payload',{})
 if d['type']=='event_msg' and a.get('type')=='task_started':starts.append(date(d['timestamp']))
start=min(starts);all_ids=set();total=collections.Counter();threads=[];records=[];head_events=[];limits=[];prior_observed=collections.Counter()
for f,tid,role,parent in files:
 counts=collections.Counter();models=collections.Counter();events=[];n=0;latest=None
 for ln,line in enumerate(f.open(),1):
  d=json.loads(line);t=date(d['timestamp']);a=d.get('payload',{})
  if not start<=t<=end:continue
  if d['type']=='turn_context':models[str(a.get('model'))+'/'+str(a.get('effort'))]+=1
  if d['type']=='token_usage_record':
   rid=a['response_id']
   if rid in all_ids:raise RuntimeError('DUPLICATE_RESPONSE '+rid)
   all_ids.add(rid);
   if t<=production_end and tid in {x['thread_id'] for x in old['agents']}:prior_observed.update(a['usage'])
   counts.update(a['usage']);latest=a.get('thread_token_usage');n+=1;records.append({'timestamp':d['timestamp'],'thread_id':tid,'role':role,'response_id':rid,'usage':a['usage']})
  if d['type']=='event_msg' and a.get('type') in ('task_started','task_complete'):
   e={'timestamp':d['timestamp'],'event':a['type'],'error':'Bad Request' if 'Bad Request' in str(a.get('error')) else 'other' if a.get('error') else None,'thread_id':tid,'source_file':f.name,'line':ln};events.append(e)
   if tid in ROOTS:head_events.append(e)
  if tid in ROOTS and d['type']=='event_msg' and a.get('type')=='token_count' and a.get('rate_limits'):
   lim=a['rate_limits'].get('primary') or {}
   if lim:limits.append({'timestamp':d['timestamp'],'used_percent':lim.get('used_percent'),'window_minutes':lim.get('window_minutes'),'resets_at':lim.get('resets_at')})
 assert latest and all(counts.get(k,0)==v for k,v in latest.items()),'CUMULATIVE_MISMATCH '+tid
 total.update(counts);threads.append({'thread_id':tid,'parent_thread_id':parent,'role':role,'source_file':f.name,'models':dict(models),'responses':n,'cumulative_reconciles':True,'usage':dict(counts),'bad_request_count':sum(e['error']=='Bad Request' for e in events)})
head_events.sort(key=lambda e:e['timestamp']);gaps=[]
for i,e in enumerate(head_events):
 if e['event']!='task_complete':continue
 nxt=next((v for v in head_events[i+1:] if v['event']=='task_started'),None)
 if nxt:gaps.append({'ended_at':e['timestamp'],'resumed_at':nxt['timestamp'],'seconds':(date(nxt['timestamp'])-date(e['timestamp'])).total_seconds(),'error':e['error'],'cross_thread_handoff':nxt['thread_id']!=e['thread_id']})
prior_ids={a['thread_id'] for a in old['agents']};prior=collections.Counter()
for a in threads:
 if a['thread_id'] in prior_ids:prior.update(a['usage'])
assert dict(prior_observed)==old['tokens'],(dict(prior_observed),old['tokens'])
limits.sort(key=lambda e:e['timestamp']);result={'schema':'byd-expanded-audit/v1','status':'Additional retrospective audit; original report unchanged','scope':'Two BYD head threads plus their four directly linked child threads; usage through final user-facing handoff; includes initial planning; excludes later report and platform','start':start.isoformat(),'cutoff':end.isoformat(),'production_files_closed_at':production_end.isoformat(),'final_handoff_at':end.isoformat(),'calendar_seconds':(end-start).total_seconds(),'original_documented_calendar_seconds':old['documented_wall_seconds'],'additional_initial_planning_seconds':(date(old['production_start'])-start).total_seconds(),'threads':threads,'tokens':dict(total),'response_count':len(all_ids),'original_three_thread_totals_reconcile':True,'bad_request_head_count':sum(e['error']=='Bad Request' for e in head_events),'head_events':head_events,'head_gaps':gaps,'error_to_next_turn_seconds':sum(g['seconds'] for g in gaps if g['error']=='Bad Request'),'all_between_head_turn_seconds':sum(g['seconds'] for g in gaps),'first_limit_snapshot':limits[0],'last_limit_snapshot':limits[-1],'cost_actual_brl':None,'limitations':['Two head threads are operationally consecutive; cross-thread gap includes handoff.','Usage records are processing counts, not billing.','Quota percent is rounded account telemetry, not a monetary credit balance.','No causal outage duration or active work time is inferred from gaps.']}
(P/'data/expanded_usage_records_sanitized.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');(P/'data/expanded_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['head_events','head_gaps','limitations']},ensure_ascii=False,indent=2))
