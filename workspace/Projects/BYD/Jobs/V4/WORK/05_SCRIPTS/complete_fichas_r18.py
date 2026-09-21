"""Complete the live R18 technical sheets from the closed scope and native geometry."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve()
while not(ROOT/'.mkroot').exists():ROOT=ROOT.parent
B=ROOT/'Projects/BYD/Jobs/V4';s=json.loads((B/'WORK/00_MATRIZ/production_spec_r18.json').read_text())
geom=[]
for name in ['build_production_r03.log','build_production_r10.log']:
 for line in (B/'WORK/06_LOGS'/name).read_text().splitlines():
  m=re.search(r'\|GEOM\|([^|]+)\|([^|]+)\|([^|]+)\|bounds=([^|]+).*\|visible=true',line)
  if m:
   fmt,offer,role,coords=m.groups();a=list(map(float,coords.split(',')));geom.append((fmt,offer,role,a[3]-a[1]))
partido={'strip':'Recomposição em três faixas: marca à esquerda, oferta ao centro e carro à direita. O legal ocupa a base; selos específicos usam a lateral livre do veículo.', 'landscape':'Recomposição em duas colunas. A oferta fica à esquerda com fundo de contraste; o carro ocupa a direita, com condicionais abaixo e texto legal no rodapé.', 'square':'Hierarquia central: marca e oferta acima, veículo no miolo, benefício e condicionais abaixo. O texto legal e os selos fecham a base.', 'portrait':'Referência vertical reequilibrada com eixo central. Marca e preço lideram, veículo separa oferta de benefícios e os rodapés permanecem em faixas próprias.', 'micro':'Distribuição exclusiva para 360×80: marca e selos específicos à esquerda, oferta no centro e carro à direita. Uma faixa escura inferior separa garantias, origem e mensagem educativa.'}
for f in s['formats']:
 fid=f['id'];fam=f['family'];z=f['zones'];align='central' if f['align']=='center' else 'à esquerda'
 lines=[f'# BYD_TPL_{fid} — ficha técnica R18', '', 'PNG: revisão visual Astra e QA técnico concluídos para 20/20 ofertas. Estado dos editáveis e do reuso: consultar `../../04_QA/production-r18/templates_manifest_r18.json`, `../../04_QA/production-r18/structural7.json` e `../../04_QA/reuse_validation_r18.json`; não inferir aprovação humana.', '', '## 1. Partido do layout', '',partido[fam], '', '## 2. Grade e zonas', '', f'Canvas {f["w"]}×{f["h"]} px. Guia de margem: {f["safe_margin"]} px; as zonas abaixo registram as posições efetivas previstas, inclusive exceções próximas à borda. Eixo de texto {align}. Coordenadas em `[x, y, largura, altura]`.', '', '| Elemento | Zona em px |','|---|---|']
 for role,zone in z.items():lines.append(f'| {role} | `{zone}` |')
 if fam=='micro':
  lines+=['','Rodapé nativo: fundo `[0,57,360,23]`; garantia/recompra `[7,61,96,15]`; Brasil `[108,60,36,17]`; satisfação `[150,60,19,17]`; ícone educativo `[176,61,13,16]`; mensagem `[194,66,159,9]`. A mensagem preservada é “Desacelere. Seu bem maior é a vida.”']
 lines+=['','## 3. Hierarquia e escala de texto','','Ordem: marca → modelo/preço → veículo → benefício/condição → selos e legal. Títulos, preços e condicionais permanecem editáveis; o encaixe usa escala proporcional, sem condensar horizontalmente a fonte.', '', '| Bloco | Altura geométrica nativa mínima–máxima observada, px |','|---|---|']
 for role in ['title','price','benefit','headline']:
  vals=[h for fmt,o,r,h in geom if fmt==fid and r==role and not(o=='dolphin-mini-5l-gs' and role=='headline' and fam in ('landscape','portrait'))]
  if vals:lines.append(f'| {role} | {min(vals):g}–{max(vals):g} |')
 lines+=['',f'Legal: corpo {f["legal_font"]} px'+(' (oculto no micro).' if fam=='micro' else ', com entrelinha corpo + 2 px.'),'As medidas acima são limites de tinta do bloco no Photoshop, não medição isolada da altura de caixa-alta. Não há certificação automática de legibilidade por esse número. O menor valor observado serve de alerta para novas variações; revisar o PNG a 100% antes de aceitar redução adicional. Não foi certificada uma distância percentual única entre todos os blocos.', '', '## 4. Âncoras e regra de estouro','',f'Modelo e preço usam a zona própria com alinhamento {align}; benefícios e condicionais também. Headlines recebem quebra por palavras com limite inicial de {f["headline_wrap"]} caracteres por linha. Depois, o bloco é encaixado proporcionalmente na sua zona; não cruza a zona vizinha. Se um novo texto ficar pequeno demais, rever a quebra/grade e o piloto, sem esticar a fonte.']
 if fam in ('landscape','portrait'):lines+=['Dolphin Mini GS: headline em duas linhas, entrelinha automática 110%, alinhamento pelo topo da zona; correção R16 revisada.']
 if fam=='strip':lines+=['Dolphin Mini GS: parcela em três linhas (“Parcelas a / partir de / R$999,00”), na zona `instal`; correção R14 revisada.']
 if fam=='micro':lines+=['Ofertas `micro_dual` usam preço `[95,19,145,20]`, benefício `[95,42,255,6]` e condição `[95,50,255,6]`. Nas demais, um benefício ou condição comercial ocupa a faixa `[95,48,255,7]`; o headline genérico não disputa esse espaço.']
 lines+=['','## 5. Veículo','','Escala uniforme e posição pelo centro da âncora original, dentro da zona `car`. Veículo e chão nativo permanecem juntos. Não gerar, redesenhar ou deformar o automóvel. A caixa da âncora não prova sozinha o recorte do carro: conferir a cena inteira renderizada.']
 if fam in ('landscape','portrait'):lines+=['Yuan Pro: cena e chão a 85% da escala inicial, com novo ajuste da âncora à zona, para preservar a frente. VD Song Pro Flex: limite inferior da máscara na base da zona `car`, removendo cópia residual incorporada à cena e preservando o carro.']
 lines+=['','## 6. Condicionais por oferta','','A matriz `production_spec_r18.json` é a autoridade de IDs e substituições. Uma zona específica na oferta prevalece sobre a zona genérica abaixo; os grupos de outros estados ficam ocultos.', '', '| Oferta | Elementos exclusivos e zonas específicas neste formato |','|---|---|']
 for o in s['offers']:
  extras=[]
  if o.get('car_tag_names'):extras.append('tag: '+', '.join(o['car_tag_names']))
  for e in o.get('extras',[]):
   zone=e.get('zones',{}).get(fid,e.get('zone',z.get(e['role'])))
   extras.append(e['role']+(' em cena original' if e.get('embedded_in_car') else ' '+str(zone)))
  if extras:lines.append('| '+o['id']+' | '+'; '.join(extras)+' |')
 lines+=['','## 7. Adaptações e limites','']
 if fam=='micro':lines+=['Omitidos: tagline, legal extenso, detalhe de assinatura e headline genérico quando existe benefício/condição prioritária. Preservados: marca, modelo, preço, carro, condição selecionada, selos condicionais disponíveis e rodapé educativo. Detalhes miúdos dos prêmios têm resolução limitada. Canal/plataforma não informado; não se afirma homologação universal de display nem conformidade jurídica apenas pela presença dos selos.']
 elif fam=='strip':lines+=['Tipografia reduzida e blocos reorganizados em colunas; detalhe decorativo da assinatura Dolphin omitido. Oferta, benefício, condição aplicável, selos e legal mantidos. O legal e detalhes dos selos ficam pequenos nesta altura; a adequação ao veículo de mídia depende da especificação de veiculação.']
 else:lines+=['Conteúdo repartido em zonas próprias sem redimensionar o feed inteiro. Condicionais exclusivos são preservados conforme a matriz; textos longos recebem quebras controladas. Preço, ano e legal divergentes na fonte são preservados e registrados no relatório comercial, não corrigidos por inferência.']
 lines+=['','## 8. Renderizar e revisar uma oferta','','No Photoshop, abrir este PSD e aplicar a Layer Comp `OFERTA <offer_id>`. `#GUIAS` deve ficar oculto; exatamente um estado deve estar visível em cada ramo BG/VEICULO/LEGAL/CONDICIONAIS/OFERTA. Para exportação controlada, usar o procedimento `../../REUSO_TEMPLATES.md` e o renderizador v2 com solicitação JSON, lock e saída nova. Exportar PNG RGB8 sRGB com perfil incorporado, sem salvar alterações no PSD. Conferir oferta, formato e imagem inteira; comparação de pixels deve confirmar reexportação da mesma campanha.','','Referências: spec R18; logs R03/R10 (geometria), R14/R16 (correções), R17/R20 (comps); revisão visual e QA técnico R18.']
 text='\n'.join(lines)+'\n'
 if fam=='micro':text=text.replace('Legal: corpo 0 px (oculto no micro).','Legal extenso: oculto no micro; não há corpo aplicado no PNG deste formato.').replace('Modelo e preço usam a zona própria com alinhamento central; benefícios e condicionais também.','Modelo centralizado na sua zona; preço ancorado à esquerda na zona própria. Benefícios e condicionais são centralizados.').replace('detail None','detail omitido')
 (B/'WORK/04_QA/fichas-r18'/('FICHA_R18_'+fid+'.md')).write_text(text)
print('OK|LIVE_TECHNICAL_SHEETS|7')
