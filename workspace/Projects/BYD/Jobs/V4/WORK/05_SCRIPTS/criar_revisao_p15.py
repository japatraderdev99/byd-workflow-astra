from pathlib import Path
import json,html
from PIL import Image,ImageOps,ImageDraw,ImageFont
REFUSE_OVERWRITE=True
b=Path(__file__).resolve().parents[2];w=b/'WORK';d=json.loads((w/'00_MATRIZ/pilot_spec_p15.json').read_text());out=w/'02_PILOTOS/2026-09-19-p15';sheet=out/'PRANCHA_21_PILOTOS_P15.jpg';page=out/'REVISAO_P15.html'
if sheet.exists() or page.exists():raise RuntimeError('REFUSE_OVERWRITE')
files=list(out.glob('p15_byd_*.png'))
if len(files)!=21:raise RuntimeError('EXPECTED_21_PNG')
font=ImageFont.load_default(size=20)
canvas=Image.new('RGB',(1800,3300),'#101820');draw=ImageDraw.Draw(canvas);draw.text((30,20),'BYD V4 / P15 — 21 PILOTOS · AGUARDANDO REVISAO HUMANA',font=font,fill='white')
blocks=[]
order=['1920x276','1920x1080','1920x1125','1080x1080','1080x1920','1109x1973','360x80']
d['formats'].sort(key=lambda x:order.index(x['id']))
for row,f in enumerate(d['formats']):
 y=75+row*455;draw.text((30,y),f['id']+' / '+f['family'],font=font,fill='#e9f38c');cards=[]
 for col,o in enumerate(d['offers']):
  name='p15_byd_'+o['id']+'_'+f['id']+'.png';p=out/name
  with Image.open(p) as im:
   im.thumbnail((560,385));canvas.paste(im,(20+col*595+(560-im.width)//2,y+35+(385-im.height)//2))
  draw.text((20+col*595,y+424),o['id'],font=font,fill='white')
  cards.append('<figure><a href="'+name+'" target="_blank"><img src="'+name+'" alt="'+html.escape(o['id'])+'"></a><figcaption>'+html.escape(o['id'])+' · <a href="'+name+'" target="_blank">abrir PNG em tamanho nativo</a></figcaption></figure>')
 blocks.append('<section><h2>'+f['id']+'</h2><div class="grid">'+''.join(cards)+'</div></section>')
canvas.save(sheet,quality=94)
page.write_text("""<!doctype html><html lang="pt-br"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>BYD V4 — Revisão P15</title><style>body{background:#101820;color:#f4f5ed;font:16px system-ui;margin:32px}h1{font-size:36px}p{max-width:1000px;line-height:1.6}a{color:#e9f38c}section{border-top:1px solid #435361;padding:24px 0}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}figure{margin:0}img{max-width:100%;max-height:650px;object-fit:contain}figcaption{padding:12px 0;font-size:13px} .note{background:#253340;padding:16px;border-left:4px solid #e9f38c}@media(max-width:900px){.grid{grid-template-columns:1fr}}</style><h1>BYD V4 · Pilotos P15</h1><p class="note">21 composições de teste · 7 PSDs com 3 estados cada. Sem aprovação humana. Não são ainda os templates canônicos de 20 ofertas. A prancha serve para comparação; abra cada PNG para leitura em 100%.</p><p>Casos: Yuan Plus AWD (título longo), Dolphin Mini (parcelas, prêmios e detalhe) e Atto 2 Venda Direta (de/por e CPF). No 360×80, proposta de omissão de legal, assinatura, rodapé, prêmios e detalhe; prioriza a restrição CPF. No 1920×276, omite apenas o detalhe do Dolphin. Conteúdo original preservado nas camadas ocultas.</p>"""+''.join(blocks),encoding='utf-8')
print('OK|review|21 PNGs|'+str(page.relative_to(b)))
