"""Read scoped lifecycle metadata; never export transcripts or reasoning."""
from pathlib import Path
import json,datetime as dt,hashlib,os
P=Path(__file__).resolve().parents[1]
M=json.loads((P/'data/metrics_original.json').read_text())
def date(s):return dt.datetime.fromisoformat(s.replace('Z','+00:00'))
start=date(M['production_start']);end=date(M['production_cutoff'])
base=Path(os.environ.get('CODEX_SESSIONS_DIR',str(Path.home()/'.codex/sessions')))
source=next((base/'2026/09/19').glob('*01a0ba59-4230-7b12-9afe-04d440f22e6c.jsonl'))
events=[];short_user=[]
for n,line in enumerate(source.open(),1):
 d=json.loads(line);t=date(d['timestamp']);a=d.get('payload',{})
 if not start<=t<=end:continue
 if d['type']=='event_msg' and a.get('type') in ('task_started','task_complete'):
  err=a.get('error') or {};events.append({'line':n,'timestamp':t.isoformat(),'event':a['type'],'error_type':'Bad Request' if 'Bad Request' in str(err) else 'other' if err else None,'duration_ms':a.get('duration_ms')})
 if d['type']=='response_item' and a.get('type')=='message' and a.get('role')=='user':
  text=' '.join(c.get('text','') for c in a.get('content',[]) if isinstance(c,dict)).strip()
  if text.lower() in ('siga','continue','prossiga','como estamos?'):short_user.append({'line':n,'timestamp':t.isoformat(),'command':text})
gaps=[]
for i,e in enumerate(events):
 if e['event']!='task_complete':continue
 next_start=next((v for v in events[i+1:] if v['event']=='task_started'),None)
 if not next_start:continue
 command=next((u for u in short_user if 0<=(date(u['timestamp'])-date(next_start['timestamp'])).total_seconds()<5),None)
 gaps.append({'ended_at':e['timestamp'],'resumed_at':next_start['timestamp'],'seconds':(date(next_start['timestamp'])-date(e['timestamp'])).total_seconds(),'preceding_error':e['error_type'],'resume_command':command['command'] if command else 'other_user_input','source_lines':[e['line'],next_start['line']]})
intervals=[]
for i,e in enumerate(events):
 if e['event']!='task_started':continue
 close=next((v for v in events[i+1:] if v['event']=='task_complete'),None)
 stop=min(date(close['timestamp']),end) if close else end
 intervals.append((stop-date(e['timestamp'])).total_seconds())
result={'schema':'byd-interruptions-audit/v1','source_file':source.name,'production_start':start.isoformat(),'production_cutoff':end.isoformat(),'wall_seconds':(end-start).total_seconds(),'scope':'head lifecycle metadata only; no raw conversation; source line anchors','events':events,'gaps':gaps,'short_user_commands':short_user,'confirmed_bad_request_count':sum(e['error_type']=='Bad Request' for e in events),'error_to_next_turn_seconds':sum(g['seconds'] for g in gaps if g['preceding_error']=='Bad Request'),'all_between_turn_seconds':sum(g['seconds'] for g in gaps),'head_turn_window_seconds':sum(intervals),'uncovered_initial_seconds':(date(events[0]['timestamp'])-start).total_seconds(),'causal_downtime_seconds':None,'limits':['Error-to-next-turn delay is not server outage duration or pure lost production time.','Photoshop or child agents may keep working while the head turn is closed.','No error field does not prove the UI had no error.','Do not subtract gaps from calendar time and label the rest human/agent active time.']}
assert abs(result['uncovered_initial_seconds']+result['all_between_turn_seconds']+result['head_turn_window_seconds']-result['wall_seconds'])<.01
(P/'data/interruptions_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['events','short_user_commands','limits']},ensure_ascii=False,indent=2))
