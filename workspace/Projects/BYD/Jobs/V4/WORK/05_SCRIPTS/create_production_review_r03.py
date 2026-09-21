from pathlib import Path
import json,html
ROOT=Path(__file__).resolve()
while not(ROOT/'.mkroot').exists():ROOT=ROOT.parent
b=ROOT/'Projects/BYD/Jobs/V4';s=json.loads((b/'WORK/00_MATRIZ/production_spec_r03.json').read_text());out=b/'WORK/04_QA/REVISAO_PRODUCAO_R03.html'
if out.exists():raise RuntimeError('REFUSE_OVERWRITE')
parts=['''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>BYD · revisão de produção</title><style>body{background:#0e1922;color:#e7eef4;font:15px system-ui;margin:24px}h1{font-size:25px}nav{position:sticky;top:0;background:#0e1922;padding:12px 0;display:flex;gap:10px;flex-wrap:wrap}a{color:#c4ecf5}select{padding:8px;background:#1d3444;color:white}section{margin:28px 0}section h2{font-size:20px}article{display:inline-block;vertical-align:top;background:#142631;padding:12px;margin:0 12px 18px 0;width:min(43vw,900px)}img{display:block;width:100%;height:auto}figcaption{padding:10px 0;font-size:13px}p{max-width:1000px;line-height:1.5}.micro article{width:360px}.strip article{display:block;width:min(95vw,1920px)}.hidden{display:none}</style><h1>BYD · produção dos 7 formatos</h1><p>20 ofertas por formato. Imagens em staging para revisão de composição; a presença nesta página não significa aprovação ou envio ao cliente. Clique na imagem para inspecionar o PNG. Selos, textos e condições preservam as referências fornecidas; limitações e conflitos constam no relatório.</p><nav><label>Oferta <select id="of"><option value="">Todas</option>''']
for o in s['offers']:parts.append(f'<option>{html.escape(o["id"])}</option>')
parts.append('</select></label>')
for f in s['formats']:parts.append(f'<a href="#{f["id"]}">{f["id"]}</a>')
parts.append('</nav>')
for f in s['formats']:
 parts.append(f'<section id="{f["id"]}" class="{f["family"]}"><h2>{f["id"]} · <a href="../01_TEMPLATES/2026-09-19-r03/BYD_TPL_{f["id"]}.psd">PSD editável</a></h2>')
 for o in s['offers']:
  src=f'../03_STAGING/2026-09-19-r03/byd_{o["id"]}_{f["id"]}.png';parts.append(f'<article data-offer="{o["id"]}"><figcaption>{o["id"]} · {f["id"]}</figcaption><a href="{src}"><img loading="lazy" src="{src}" alt="{o["id"]} {f["id"]}"></a></article>')
 parts.append('</section>')
parts.append('''<script>document.querySelector('#of').onchange=e=>document.querySelectorAll('article').forEach(a=>a.classList.toggle('hidden',!!e.target.value&&a.dataset.offer!==e.target.value))</script></html>''');out.write_text(''.join(parts));print('OK|review_html')
