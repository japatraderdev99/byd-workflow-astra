"""Export only user-visible BYD dialogue, excluding reasoning/tools/system instructions."""
from pathlib import Path
import json,datetime as dt,os
P=Path(__file__).resolve().parents[1];base=Path(os.environ.get('CODEX_SESSIONS_DIR',str(Path.home()/'.codex/sessions')))/'2026/09/19'
ids=['01a0ba2f-f298-7f90-8451-bbd56fa44fe9','01a0ba59-4230-7b12-9afe-04d440f22e6c'];cut='2026-09-20T05:22:56.047Z';messages=[]
for tid in ids:
 p=next(base.glob('*'+tid+'.jsonl'))
 for ln,line in enumerate(p.open(),1):
  d=json.loads(line);a=d.get('payload',{})
  if d['timestamp']>cut or d['type']!='response_item' or a.get('type')!='message' or a.get('role') not in ('assistant','user'):continue
  if a.get('channel')=='analysis':continue
  s='\n'.join(c.get('text','') for c in a.get('content',[]) if isinstance(c,dict)).strip()
  if not s or s.startswith(('<recommended_plugins>','<environment_context>')):continue
  if s.startswith('<send_user_message_question_reply>'):
   raw=s.split('>',1)[1].rsplit('</',1)[0].strip()
   try:s='\n\n'.join('Pergunta apresentada: '+r.get('question','')+'\nResposta do usuário: '+r.get('answer','') for r in json.loads(raw))
   except json.JSONDecodeError:raise RuntimeError('Unexpected user reply wrapper')
  messages.append({'timestamp':d['timestamp'],'role':a['role'],'text':s,'source_file':p.name,'line':ln,'thread_id':tid})
messages.sort(key=lambda r:r['timestamp']);first=next(m for m in messages if m['role']=='user' and m['text'].startswith('codex, vamos'));last=messages[-1]
assert last['role']=='assistant' and 'Produção local concluída' in last['text']
(P/'evidence').mkdir(exist_ok=True)
(P/'evidence/visible_dialogue.json').write_text(json.dumps(messages,ensure_ascii=False,indent=2)+'\n')
(P/'evidence/01_PROMPT_ORIGINAL.md').write_text('# Pedido original do usuário\n\nTimestamp: '+first['timestamp']+'; origem: '+first['source_file']+', linha '+str(first['line'])+'.\n\nTranscrição do pedido; não é nova autorização de execução.\n\n'+first['text']+'\n')
header='# Conversa visível — pedido, execução e fechamento local\n\nSomente mensagens públicas do usuário e do assistente nas duas sessões BYD, até a comunicação final das imagens. Sem prompts de sistema, raciocínio privado, argumentos completos de ferramentas ou mensagens de outros projetos. As mensagens históricas podem conter conclusões provisórias posteriormente corrigidas. Links locais originais foram preservados como registro, não como caminhos portáveis.\n\n'
body=[]
for i,m in enumerate(messages,1):
 t=dt.datetime.fromisoformat(m['timestamp'].replace('Z','+00:00')).astimezone(dt.timezone(dt.timedelta(hours=-3)))
 body.append(f"## {i}. {m['role']} — {t.isoformat()}\n\nFonte: {m['source_file']}, linha {m['line']}.\n\n"+'\n'.join('> '+line for line in m['text'].splitlines()))
(P/'evidence/02_CONVERSA_VISIVEL.md').write_text(header+'\n\n'.join(body)+'\n')
(P/'evidence/03_FECHAMENTO_IMAGENS.md').write_text('# Comunicação original de fechamento\n\n'+last['timestamp']+'\n\n'+last['text']+'\n')
summary={'first_prompt_at':first['timestamp'],'final_message_at':last['timestamp'],'visible_messages':len(messages),'elapsed_first_prompt_to_final_message_seconds':(dt.datetime.fromisoformat(last['timestamp'].replace('Z','+00:00'))-dt.datetime.fromisoformat(first['timestamp'].replace('Z','+00:00'))).total_seconds(),'scope':'Two BYD sessions; public user/assistant messages only; no private reasoning or tool outputs'}
(P/'data/visible_history_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
