# Relatório operacional BYD V4 — R18

**Estado atual:** `R18_CONCLUIDO_LOCAL`.

Produção local encerrada: 140 PNGs promovidos após QA e sete PSDs editáveis validados. Não declara aprovação humana final, aprovação comercial/jurídica ou entrega externa.

## Escopo, fonte e integridade

- Escopo fechado: **20 ofertas × 7 formatos = 140 PNGs**.
- PSD-fonte imutável: `INPUT/02_PSD_oficial todas as artes em feed/26.08.07 VAREJO BYD FEED 1080x1350.psd`.
- `INPUT/_INPUT_SHA256.json` nunca existiu. O baseline construído por observação
  é `WORK/00_MATRIZ/input_baseline_observado_sha256_v2.json`.
- `WORK/04_QA/input_integrity_final_r18.json` confirmou **48/48** arquivos de
  `INPUT` contra esse baseline observado. Isso não afirma uma comparação
  anterior ao baseline.
- A montagem R11 está completa: `WORK/04_QA/assembly_r11_v4.json` registra
  **154** cópias (140 PNGs, 7 PSDs e 7 previews). Os PNGs canônicos permanecem
  em `WORK/03_STAGING/2026-09-20-r11/`.

## Evidência já fechada

| Evidência | Resultado | Limite |
|---|---|---|
| QA técnico PNG | `WORK/04_QA/production-r18/technical_all.json`: 140/140 PASS em 7,425902 s | Não inspeciona a estrutura dos PSDs. |
| Revisão visual Astra | `WORK/04_QA/production-r18/head_visual_review.json`: 140/140 PASS | `ASTRA_AGENT_VISUAL_REVIEW`; `visual_review_is_human_approval=false`. |
| Escala | Autorizada pelo usuário após pilotos, registrada no `WORK/06_LOGS/DIARIO.md` | Não prova revisão pessoal dos 140 finais. |

A revisão Astra é uma revisão visual por agente. Não é revisão humana, do
cliente, jurídica ou aprovação de entrega.

## Templates nativos e reuso

Os PSDs de R11 não são a autoridade final de reuso. A autoridade nativa é
`WORK/01_TEMPLATES/2026-09-20-r17/`, sem criar cópias extras de PSD. O
manifesto `WORK/04_QA/production-r18/templates_manifest_r18.json` registra os
sete PSDs e seus hashes:

- R17 concluiu somente `1920x276`: 20 aplicações antes de salvar e 20 após
  reabrir, com `FORMAT_OK` em 420472 ms. O erro seguinte ocorreu antes de
  abrir a segunda fonte; o strip é a única saída R17 já válida.
- R19 falhou antes de salvar PSD ou PNG; seus resultados não são reutilizados.
- R20 concluiu os seis formatos restantes sem `ERRO`: 120 provas antes de
  salvar e 120 após reabrir, em `727056 ms`. Com R17, há 280 provas de
  visibilidade para os 140 estados nos sete formatos.
- O teste de reuso R18 aplicou `render_canonical_v2.jsx` em três ofertas de
  `1920x1080`: 3/3 PNGs, `77320 ms`, com pixels idênticos em
  `reuse_validation_r18.json`. Os SHA-256/bytes dos PNGs podem divergir por
  metadados; o teste não equivale a uma prova de pixels para os 140 PNGs.

O conjunto de sete PSDs soma **10.339.050.734 bytes**; os arquivos individuais
ficam entre aproximadamente **1,14 GB e 1,59 GB**. O fundo compartilhado evita
repetir a base em 20 estados, mas não torna os PSDs leves; bytes e hashes reais
estão no manifesto nativo.

## Formatos, decisões de layout e correções R18

Cada formato contém 20 ofertas. As decisões abaixo resumem as fichas técnicas
em `WORK/04_QA/fichas-r18/`; zonas, regras de estouro e condicionais continuam
na ficha de cada template.

| Formato | PNGs | Decisão de design registrada |
|---|---:|---|
| 1920×276 | 20 | Três faixas: marca à esquerda, oferta ao centro, carro à direita; legal na base e selos na lateral livre do veículo. |
| 1920×1080 | 20 | Duas colunas: oferta sobre fundo de contraste à esquerda, carro à direita, condicionais abaixo e legal no rodapé. |
| 1920×1125 | 20 | Duas colunas, com a mesma hierarquia de oferta/espaço de carro do landscape 1920×1080. |
| 1080×1080 | 20 | Hierarquia central: marca e oferta acima, veículo no miolo, benefício/condicionais abaixo e base com legal/selos. |
| 1080×1920 | 20 | Vertical central: marca e preço lideram, veículo separa oferta e benefícios, rodapés em faixas próprias. |
| 1109×1973 | 20 | Vertical central equivalente, com zonas proporcionais próprias para veículo, condicionais e rodapé. |
| 360×80 | 20 | Micro exclusivo: marca/selos à esquerda, oferta ao centro, carro à direita e faixa escura educativa no rodapé. |

No micro `360×80`, foram omitidos tagline, legal extenso, detalhe de assinatura
e headline genérico quando um benefício ou condição prioritária ocupa a mesma
faixa. Permanecem marca, modelo, preço, carro, condição selecionada, selos
disponíveis e o rodapé educativo “Desacelere. Seu bem maior é a vida.” Isso não
declara homologação universal de display ou conclusão jurídica.

As 13 correções executadas são registradas em
[layout_adjustments_r18.json](00_MATRIZ/layout_adjustments_r18.json): uma
correção de parcela do Dolphin Mini GS no strip `1920×276`; nos quatro formatos
grandes, quatro correções de headline do Dolphin Mini GS (duas linhas e
entrelinha 110%), quatro correções da máscara inferior do VD Song Pro Flex para
remover resíduos de cena e quatro reenquadramentos do Yuan Pro (escala uniforme
85% e recentramento). A revisão Astra vinculada aos hashes confirma essas
saídas, sem equivaler a aprovação humana.

Para uma reexportação controlada, consultar
[REUSO_TEMPLATES.md](REUSO_TEMPLATES.md): o teste de pixels R18 é limitado a
três ofertas em um formato e não prova reexportação pixel-idêntica dos 140 PNGs.

## Conteúdo comercial e tipografia

As discrepâncias abaixo são registros entre texto em destaque, legal e regras
comerciais consultadas. Nenhum valor, ano ou selo foi alterado por inferência.

| Oferta/condição | Evidência conflitante | Tratamento atual |
|---|---|---|
| `song-premium` | destaque R$ 269.800; legal R$ 299.800 | Preservados; requer validação comercial. |
| `vd-shark` | destaque R$ 299.990 Produtor Rural; legal R$ 344.990 | Preservados; requer validação comercial. |
| `vd-atto-2` | preço público R$ 166.660; “por” R$ 149.990; legal R$ 166.660 | Diferença entre preço público e desconto a validar; não é erro automático. |
| `vd-song-pro` | título Song Pro GL 25/26; legal 26/27 | Preservados conforme `conflitos_anos_modelo_producao.json`; requer decisão comercial. |
| Recompra Garantida | seis referências de Venda Direta exibem o selo; regras de varejo consultadas restringiam recompra | Não remover nem declarar elegibilidade a partir dessa divergência. |

Os identificadores de Seal, Sealion e Yuan Plus não são conflitos por si só e
não são listados como pendência. A leitura estrutural registrou StyleRuns
ArialMT e SourceSansPro e o pacote contém MüllerNext, mas isso não prova a
disponibilidade de cada fonte no ambiente. Os estilos de fonte foram
preservados e nenhuma substituição tipográfica foi executada.

## Papéis, modelos, duração e custo

| Campo | Evidência | Valor/limite |
|---|---|---|
| Modelo solicitado | `DIARIO.md` nos runs de intake | `gpt-5.6-terra/high`. |
| Runtime observado no intake | `DIARIO.md` | `gpt-6-astra/esforço herdado-padrão`; essa observação não é telemetria de Photoshop. |
| Início do job | `DIARIO.md` | `2026-09-19T12:05:22.103668-03:00`. Descoberta anterior não foi cronometrada. |
| Fim da produção local | Manifesto canônico | `2026-09-20T02:22:25.837061-03:00`. |
| Janela de parede documentada | Início até fechamento | 14.284 h; inclui espera e interrupções. Tempo ativo total não medido. |
| Custos/tokens/custo humano | — | `null`: não existe telemetria de cobrança ou esforço humano. |

`WORK/04_QA/production_timings_r18.json` foi gerado após o encerramento dos
logs. Ele registra 33 runs, inclusive erros, tentativas parciais e lacunas de
parede. A soma limitada a 18 terminais únicos `OK|completed` é `5543698 ms`;
ela não mede tempo ativo humano, não inclui logs sem terminal e não deve ser
apresentada como duração total. R17 é uma exceção parcial válida no strip
(`420472 ms`) seguida por erro; R19 falhou antes de salvar; R20 terminou em
`727056 ms`; o reuso R18 terminou em `77320 ms`.

## Tempos disponíveis por etapa

| Etapa | Medida disponível | Limite |
|---|---|---|
| Intake e arquitetura | início documentado no diário | Tempo ativo isolado não medido. |
| Pilotos e ajustes de template | duração por run e eventos por formato em `production_timings_r18.json` | Inclui iterações; não representa uma única geração por template. |
| Escala de seis formatos R10 | 27 min 06,940 s para 120 PNGs e seis PSDs | Os 20 strips vieram de run anterior parcialmente concluído. |
| Correções de quatro formatos R16 | 6 min 47,897 s para 12 PNGs e quatro PSDs | A correção adicional do strip foi concluída em run parcial separado. |
| Reparo e teste das Layer Comps | strip R17: 7 min 00,472 s; seis formatos R20: 12 min 07,056 s | Formatos distintos; não é comparação controlada de performance. |
| Reuso validado | 1 min 17,320 s para três PNGs em um formato | Inclui abertura e fechamento; não extrapolar linearmente para 140. |
| QA técnico PNG | 7,426 s para 140 imagens | Não inclui revisão visual ou estrutural. |
| Revisão visual e promoção | evidências e horários registrados | Tempo ativo independente não medido. |

## Limites de método ainda relevantes

- O incidente de perímetro registrado no `DIARIO.md` impede alegar benchmark
  isolado limpo, embora o processo e suas evidências continuem utilizáveis.
- Percentual de cap-height e respiro não foram instrumentados universalmente;
  não há métrica geral para declarar esses critérios aprovados.
- A primeira QA estrutural produziu falsos `FAIL` porque `state_groups` não
  interpretava os prefixos dos grupos de estado. O histórico é preservado;
  a v2 corrigiu esse mapeamento e concluiu 7/7 PASS, vinculados aos hashes atuais e às 280 provas nativas.

## Fechamento local

QA estrutural v2: **7/7 PASS**. Promoção concluída em `OUTPUT/2026-09-20-r18/`: **140 PNGs, 20 por formato**, com SHA-256 conferido após cópia. Somente PNGs na pasta de saída. Manifesto canônico: `WORK/04_QA/manifest.json`.

Restam para veiculação as decisões comerciais indicadas acima. Não houve envio externo. Photoshop encerrado sem documentos de produção e lock liberado.

Fontes: `00_LEIA_PRIMEIRO.md`, `WORK/06_LOGS/DIARIO.md`, logs R17/R19/R20,
`input_integrity_final_r18.json`, `assembly_r11_v4.json`, QA R18 e scripts de
guarda R18.
