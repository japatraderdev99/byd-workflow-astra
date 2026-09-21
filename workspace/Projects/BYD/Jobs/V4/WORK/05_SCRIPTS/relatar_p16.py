from pathlib import Path
import json,re,datetime
REFUSE_OVERWRITE=True
b=Path(__file__).resolve().parents[2];w=b/'WORK';qa=json.loads((w/'04_QA/qa_p16_20260919.json').read_text());log=(w/'06_LOGS/patch_p16.log').read_text();now=datetime.datetime.now().astimezone()
assert qa['png_pass']==21 and qa['coverage_ok'] and len(qa['psds'])==7
assert all(all(x['visibility_checks'].values()) for x in qa['psds'])
rows=re.findall(r'OK\|template_trial\|([^|]+)\|elapsed_ms=(\d+)',log);elapsed=int(re.search(r'OK\|completed\|elapsed_ms=(\d+)',log)[1]);times='\n'.join('| '+fmt+' | '+str(round(int(ms)/1000,2))+' s |' for fmt,ms in rows)
sizes='\n'.join('| '+Path(x['file']).stem+' | '+str(round(x['bytes']/1e6,1))+' MB | '+str(x['text_layers'])+' | '+str(x['smart_objects'])+' |' for x in qa['psds'])
text=f"""# BYD V4 — revisão visual P16

Registro: {now.isoformat()}. Estado: PILOTOS PARA REVISAO; F1 completo e escala pendentes.

## Abrir

- Prancha: `WORK/02_PILOTOS/2026-09-19-p16/PRANCHA_21_PILOTOS_P16.jpg`
- Galeria com PNGs nativos: `WORK/02_PILOTOS/2026-09-19-p16/REVISAO_P16.html`
- PSDs e fichas: `WORK/01_TEMPLATES/2026-09-19-p16/`
- Matriz: `WORK/00_MATRIZ/matriz_visual_20_20260919.json`

## O que existe e o que não existe ainda

21 PNGs, três ofertas em sete formatos; sete PSDs de TRÊS estados. Não são os canônicos de 20 ofertas. Nenhum dos 140 PNGs foi promovido a OUTPUT. Nenhuma aprovação humana foi registrada.

Dolphin Mini reúne o título mais longo observado e a composição mais densa, com parcelas, prêmios e detalhe. Yuan Plus testa uma oferta simples e outra silhueta. Atto VD testa preço de/por e restrição CPF. Carros, textos, selos e fundo vêm do PSD original; logo vem do PDF oficial. Sem imagem generativa, achatamento ou rasterização dos textos existentes.

## Decisões por formato

| Formato | Adaptação e omissão proposta |
|---|---|
| 1920×276 | Marca à esquerda, oferta central, veículo à direita e legal em faixa própria. Parcelas quebradas em bloco. Detalhe decorativo Dolphin oculto por falta de leitura; prêmios mantidos pequenos. |
| 1920×1080 | Oferta à esquerda, carro à direita, correção de contraste mascarada no fundo; conteúdo dos três casos preservado. |
| 1920×1125 | Grade horizontal própria, mesma lógica; conteúdo dos três casos preservado. |
| 1080×1080 | Pilha vertical compacta, detalhe e prêmios do Dolphin abaixo do benefício; conteúdo preservado. |
| 1080×1920 | Pilha vertical espaçada, carro inteiro, de/por e CPF preservados. |
| 1109×1973 | Grade vertical própria para mobile; conteúdo preservado. |
| 360×80 | Prioriza marca, modelo, preço, carro e benefício; para VD, restrição CPF substitui benefício. Omite legal integral, tagline, rodapé, prêmios, detalhe e headline genérica. Parcelas Dolphin preservadas. Omissões dependem de aprovação. |

## Conflitos de origem

Song Premium: hero R$269.800 versus legal R$299.800. VD Shark: hero R$299.990 versus legal R$344.990. Atto VD: hero de R$166.660 por R$149.990, legal menciona R$166.660. Nenhum valor foi corrigido por suposição. Pacote de fontes Müller diverge de SourceSansPro/Arial usados no PSD; estilos do PSD foram preservados.

## QA e limites

QA técnico: {qa['png_pass']}/21 PNGs nas dimensões corretas, RGB8, opacos, sRGB embutido; 7/7 PSDs com grupos obrigatórios. Flags estruturais de NEW oculto e exclusividade do micro verificadas. Manifesto com hashes: `WORK/04_QA/qa_p16_20260919.json`. Esse resultado não aprova composição ou conteúdo.

O INPUT permaneceu igual na conferência de 48 arquivos (`input_integrity_p14_20260919.json`); P16 só abriu cópias P12. A comparação dos nove PNGs quadrados/verticais com P12 não deu igualdade pixel a pixel: diferenças pequenas localizadas no texto (média inferior a 0,1 por canal no quadrado). O conteúdo visual foi revisado; não reivindicar identidade exata de pixels. Revisões anteriores preservadas; P14 e P15 reprovadas visualmente. Não usar suas pranchas.

Ainda faltam: associação de quatro conjuntos de camadas listados na auditoria; 20 estados por PSD; redução do peso dos Smart Objects; guias desenhadas e preview de guias; mínimos de leitura e rejeição de estouro; normalização de separadores dos nomes internos com flags intrínsecas. O ativador de três pilotos usa busca parcial no nome; na expansão deve ser substituído por associação exata de ID, pois `atto-2` e `vd-atto-2` não podem se ativar juntos. Tudo isso precede escala, mesmo após uma aprovação da direção visual.

| PSD | Peso | Textos editáveis | Smart Objects |
|---|---:|---:|---:|
{sizes}

Diagnóstico de peso: no micro, três Smart Objects de fundo têm o mesmo hash, 164.184.212 bytes cada. São 492.552.636 bytes (68,8% do PSD), com potencial de economizar duas cópias redundantes por template. A consolidação deve reutilizar uma origem de Smart Object em instâncias, preservando transformações. Evidência: `WORK/04_QA/PESO_PSD_PILOTO_P16.md`.

## Tempo e custo

P12, construção de sete rascunhos/21 renders: 588,109 s. P16, ajuste/reabertura/salvamento/exportação: {elapsed/1000:.3f} s. QA técnico P16: {qa['elapsed_seconds']} s. Os tempos abaixo são trechos do script P16; incluem I/O. Não são tempo por template aprovado.

| Formato | Tempo de ajuste e export dos 3 casos |
|---|---:|
{times}

Primeiro carimbo do run: 19/09/2026 12:05:22 -03:00. Este registro: {now.strftime('%d/%m/%Y %H:%M:%S %z')}. A janela inclui intervalos não instrumentados; tempo ativo total e custo por tarefa não estão medidos. Tokens/custo monetário/modelo observado: não estimados. Há retrabalho relevante: esta primeira execução ainda não comprova o custo-benefício pretendido.

## Fluxo recomendado

Astra: direção, piloto e exceções. Terra: inventário/matriz/revisão fria, após conferir qualidade no mesmo contrato. Scripts: repetição, exportação, cobertura e hashes. Luna apenas se interpretação textual simples for necessária; não criar agente por peça. Um único operador Photoshop com lock. Esforços e modelos mais baratos são proposta a calibrar, não benchmark concluído.

A aprovação solicitada nesta rodada é da direção visual e das omissões. Ela não dispensa a consolidação e validação técnica dos canônicos antes dos 140 exports. Regras de aprovação: `00_LEIA_PRIMEIRO.md`, seção Portão humano; `AGENTS.md`, regra 2.
"""
with (w/'RELATORIO_PILOTOS_P16.md').open('x') as f:f.write(text)
with (w/'06_LOGS/DIARIO.md').open('a') as f:f.write('\n'+now.isoformat()+' — P16 consolidado em relatório de pilotos, 21 PNGs/7 PSDs de três estados; QA técnico e flags de visibilidade passaram. Ainda sem aprovação humana; canônicos 20 estados e F3–F6 pendentes.\n')
print('OK|report P16|seconds='+str(elapsed/1000))
