#!/usr/bin/env python3
"""Create a local R18 Astra-agent review gallery from R11 staging, without promotion."""
from __future__ import annotations
import argparse,html,json
from pathlib import Path
def root(start):
 for p in (start,*start.parents):
  if (p/'.mkroot').exists():return p
 raise RuntimeError('MISSING_MKROOT')
ROOT=root(Path(__file__).resolve());V4=ROOT/'Projects/BYD/Jobs/V4';SPEC=V4/'WORK/00_MATRIZ/production_spec_r18.json';QA=V4/'WORK/04_QA/production-r18';OUT=QA/'REVISAO_PRODUCAO_R18.html'
def status_map():
 p=QA/'head_visual_review.json'
 if not p.is_file():return {},'no status manifest available'
 d=json.loads(p.read_text())
 if d.get('review_type')!='ASTRA_AGENT_VISUAL_REVIEW':return {},'head_visual_review.json:invalid_review_type'
 return {x['file']:'ASTRA_AGENT_'+str(x.get('status','STATUS_UNKNOWN')) for x in d.get('files',[]) if isinstance(x.get('file'),str)},'head_visual_review.json'
def main():
 p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');a=p.parse_args()
 if not a.execute:raise RuntimeError('REFUSE_WRITE_WITHOUT_--execute')
 if OUT.exists():raise RuntimeError('REFUSE_OVERWRITE')
 s=json.loads(SPEC.read_text());
 if s.get('revision')!='r18' or len(s['offers'])!=20 or len(s['formats'])!=7:raise RuntimeError('INVALID_R18_SCOPE')
 statuses,source=status_map(); stage=s['output_staging'].rstrip('/'); relstage='../../03_STAGING/'+stage.split('/')[-1]; values=sorted(set(statuses.values())|{'PENDING_ASTRA_AGENT_REVIEW'})
 h=['<!doctype html><meta charset="utf-8"><title>BYD · Galeria das 140 artes</title><style>body{background:#0e1922;color:#e7eef4;font:15px system-ui;margin:24px}article{display:inline-block;vertical-align:top;background:#142631;padding:10px;margin:0 10px 14px 0;width:min(43vw,900px)}img{width:100%;display:block}.strip article{display:block;width:min(95vw,1920px)}.micro article{width:360px}.hidden{display:none!important}.status{display:inline-block;background:#25485a;padding:3px 6px;margin:4px 0}</style><h1>BYD Servopa · 20 ofertas, 7 formatos</h1><p>Revisão visual do Astra. Clique na imagem para abrir em tamanho original. A revisão não substitui a validação comercial dos conflitos registrados no relatório.</p><label>Oferta <select id="o"><option value="">Todas</option>']
 h += ['<option>'+html.escape(o['id'])+'</option>' for o in s['offers']];h += ['</select></label><label>Revisão <select id="t"><option value="">Todas</option>']+['<option>'+html.escape(v)+'</option>' for v in values]+['</select></label>']
 h += ['<label>Formato <select id="m"><option value="">Todos</option>'] + ['<option>'+html.escape(f['id'])+'</option>' for f in s['formats']] + ['</select></label>']
 for f in s['formats']:
  fmt=f['id'];h.append('<section data-f="'+fmt+'" class="'+f['family']+'"><h2>'+fmt+'</h2>')
  for o in s['offers']:
   oid=o['id'];name='byd_'+oid+'_'+fmt+'.png';key=stage+'/'+name;st=statuses.get(key,'PENDING_ASTRA_AGENT_REVIEW');img=relstage+'/'+name
   h.append('<article data-o="'+html.escape(oid,quote=True)+'" data-t="'+html.escape(st,quote=True)+'"><b>'+html.escape(oid)+' — '+fmt+'</b><br><span class="status">'+('Revisada pelo Astra' if st=='ASTRA_AGENT_PASS' else html.escape(st))+'</span><a href="'+img+'"><img loading="lazy" src="'+img+'"></a></article>')
  h.append('</section>')
 h.append('<script>const f=()=>{let o=document.querySelector("#o").value,t=document.querySelector("#t").value,m=document.querySelector("#m").value;document.querySelectorAll("section").forEach(s=>s.classList.toggle("hidden",!!m&&s.dataset.f!==m));document.querySelectorAll("article").forEach(a=>a.classList.toggle("hidden",!!o&&a.dataset.o!==o||!!t&&a.dataset.t!==t))};document.querySelectorAll("select").forEach(e=>e.onchange=f)</script>')
 OUT.write_text(''.join(h));print('OK|review_html_r18')
if __name__=='__main__':main()
