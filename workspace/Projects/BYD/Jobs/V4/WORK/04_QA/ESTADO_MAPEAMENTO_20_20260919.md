# Estado do mapeamento visual das 20 ofertas

`REFUSE_OVERWRITE`: este é um retrato datado. Uma nova conferência deve criar
outro arquivo, sem reescrever este registro.

Leitura fria em `2026-09-19T21:48:56-03:00` a
`2026-09-19T21:50:43-03:00`, limitada a V4. A fonte é
`WORK/00_MATRIZ/matriz_visual_20_20260919.json`; não houve Photoshop, UI ou
alteração de artefato existente. A matriz mapeia as 20 ofertas, mas não é
aprovação de template, piloto, conteúdo ou escala.

## Pendências de ID que impedem expansão mecânica 3→20

| Oferta | ID não resolvido | Consequência exata | Observação ao vivo necessária |
|---|---|---|---|
| `king-gs` | componentes isolados de **ADAS 2** e **Qual Comprar 2026** | O template não pode declarar/ativar esses dois elementos por camada ao expandir a oferta para os 7 formatos. Ativar só `SELOS` ID 312 arrisca carregar conteúdo sem controle. | Com o PSD aberto e lock, identificar os filhos visíveis do selo e comparar com a referência. |
| `song-pro-flex` | componente isolado de **ADAS 2** | O grupo de selos ID 369 é candidato, mas não permite ligar/desligar ADAS por regra. A expansão 3→20 não deve assumir que todo `SELOS` cabe ou aparece nos 7 formatos. | Inspecionar a árvore renderizada do grupo 369, registrar o ID do ADAS e sua dependência visual. |
| `song-pro` | componente isolado de **ADAS 2** | IDs 358 (Super Híbrido), 360 (Melhor Compra 2025) e 4596/4599 (Últimas Unidades) estão mapeados, mas ADAS não. A matriz continuaria incompleta para o conjunto de condicionais da oferta. | Inspecionar os filhos de `SELOS` ID 361 no PSD e registrar o ID específico. |
| `vd-song-pro-flex` | relação do carro ID 4129 com grupo `CARRO` ID 616 | A silhueta/bbox de 4129 coincide com a referência, mas o Smart Object é irmão do grupo 616. Uma cópia automática de 616 pode não carregar o carro; uma cópia de 4129 pode quebrar a arquitetura do template. | Abrir o PSD sob lock, testar a visibilidade de 4129/4131/616 em cópia e registrar o vínculo reproduzível. |

As fontes observadas nas camadas são `SourceSansPro-*`; o pacote entregue é
MüllerNext. Antes de qualquer piloto novo, a observação ao vivo deve confirmar
a fonte efetivamente resolvida no Photoshop. Não substitua por aproximação.

## Conflitos de conteúdo e decisões ainda necessárias

| Oferta | Evidência | Consequência |
|---|---|---|
| `dolphin-mini-5l-gs` | A referência mostra `DETALHE` ID 32 e prêmios ID 67; P06–P10 propõem omitir o detalhe em 1920x276 e, em 360x80, também legal/selos/detalhe. | Não esconder esses itens silenciosamente na expansão. O portão humano deve decidir, por formato, o que pode ser reduzido ou omitido. |
| `song-premium` | Hero da referência: R$269.800; legal ID 467: preço público sugerido R$299.800. | Conflito de material, não correção de mapeamento. Confirmar a redação/preço com a autoridade do cliente antes de escalar. |
| `vd-shark` | Referência e handoff resolvem o grupo 2986 / R$299.990 / Produtor Rural; legal ID 2981 diz R$344.990. | Manter o grupo 2986 e registrar ambas as cifras. Solicitar decisão do cliente sobre o legal; não editar número por conta própria. |
| `360x80` | P10 e P12 registram propostas de omitir tagline, rodapé e elementos específicos. P12 não tem sentinela `OK|completed`. | A família não está pronta para a regra “nenhuma informação some em silêncio”; requer revisão visual e decisão humana antes de qualquer lote. |

## Evidência de execução P06–P12

Os tempos completos estão em
`WORK/04_QA/tempos_photoshop_20260919.json`. `elapsed_ms` mede trechos do
script; a coluna “span UTC” mede somente a distância entre primeira e última
linha do log. Nenhuma delas mede tempo humano, token ou custo.

| Run | `template_trial` / PNGs log | span UTC | `OK|completed` | Situação da iteração |
|---|---:|---:|---|---|
| P06 | 1 / 3 | 73 s | sem elapsed global | Reprovado visualmente no diário. |
| P07 | 1 / 3 | 76 s | 106.623 ms | Sucessor de P06, sem aprovação humana. |
| P08 | 1 / 3 | 76 s | 107.196 ms | Sucessor de P07, sem aprovação humana. |
| P09 | 1 / 3 | 77 s | 107.689 ms | Sucessor de P08, sem aprovação humana. |
| P10 | 6 / 18 | 452 s | 482.934 ms | `DRAFT_3_STATES_NOT_CANONICAL`. |
| P11 | 3 / 9 | 228 s | 259.304 ms | Há P12 posterior; sem `APROVADO` registrado. |
| P12 | 6 / 18 no log; 7 PSDs / 21 PNGs no disco | 536 s | ausente | Log incompleto: faltam 360x80 `template_trial`, `OK` de 3 PNGs e `OK|completed`. |

P06 é a única iteração explicitamente reprovada. P07–P09 e P11 são
predecessoras com sucessor numerado, mas não há prova de descarte nem de
aprovação; por isso não são contabilizadas como entregáveis. P10 é rascunho
por evidência explícita. P12 tem arquivos no disco, porém a lacuna do log e a
ausência do portão humano impedem tratá-la como concluída.

Tokens, custo do modelo, custo humano e duração real de parede não foram
registrados. Qualquer KPI que os utilize deve ficar `null` até haver
instrumentação própria. Não há autorização de escala: o próximo passo seguro
é resolver os quatro pontos ao vivo, reconciliar o P12 e apresentar os 21
pilotos ao portão humano.

## Adendo posterior ao snapshot

Após o encerramento desta leitura, o operador confirmou que `build_p12.log`
recebeu as duas linhas seguintes: `Sunday, 20 Sep 2026 00:50:04 GMT|
OK|template_trial|360x80|elapsed_ms=69331` e
`OK|completed|elapsed_ms=588109`. Este adendo corrige somente o estado final
informado pelo operador; o snapshot e o JSON de tempos acima preservam a
lacuna observada no momento de sua criação. P13 falhou por
`MISSING_CONTRAST`; P14 foi reprovado por visibilidade após renomear; P15 foi
interrompido. Nenhum desses estados autoriza escala ou aprovação humana.
