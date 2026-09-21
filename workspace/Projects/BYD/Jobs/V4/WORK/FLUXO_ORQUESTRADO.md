# Fluxo orquestrado — BYD V4

Proposta de execução de baixo custo operacional, mantendo os portões de
qualidade do run. O escopo é fechado em 20 ofertas × 7 formatos = 140 PNGs.
Os slots de modelo abaixo são hipóteses de alocação; não são benchmark e não
autorizam alegação de economia medida.

## Papéis e alocação

| Papel | Slot hipotético | Uso permitido |
|---|---|---|
| Head e decisão | Astra | fechar escopo/matriz, resolver conflitos, consolidar QA e conduzir o portão humano |
| Tarefas delimitadas | Terra médio/alto | inventário, checagens de matriz, dimensões/perfil/hash e triagem mecânica por formato; sempre com saída verificável |
| Tarefas simples com contrato fechado | Luna max (a calibrar) | conferir nomes, contagens, completude de logs e organizar relatórios com resultado verificável |
| Design e revisão visual crítica | Astra; Sol alto como alternativa a validar | resolver composição, fidelidade, legibilidade e exceções; revisar pilotos antes do humano |
| Photoshop | operador único | deter o `pslock`, abrir o Photoshop, rodar piloto/escala e registrar o resultado |

Um JavaScript determinístico, parametrizado pela matriz e pelos templates, faz
o trabalho mecânico de render/exportação/checagens. Não há chamada LLM por
peça. O operador único segue `status → check_jsx → acquire → execução →
release`; nenhum agente paralelo abre Photoshop.

## Sequência e portões

```text
F0 Intake → F1 7 PSDs → F2 21 PNGs → APROVADO humano → F3 140 PNGs
                                                    → F4 QA → F5 promoção
```

- **F0 — Intake:** inventário estrutural do `INPUT/`, matriz oferta × elemento,
  conflitos e escopo fechado. Saída: matriz e manifesto que a escala possa
  ler e lista de decisões pendentes.
- **F1 — Templates:** sete PSDs canônicos editáveis, um por formato, com
  variáveis endereçáveis, fichas técnicas e regra de estouro. Texto permanece
  texto; não usar `flatten`, `mergeVisibleLayers` ou rasterização.
- **F2 — Pilotos:** três ofertas-teste × sete formatos = 21 PNGs, escolhidas
  para cobrir título longo, maior densidade e Venda Direta. Render mecânico,
  QA técnico e revisão visual por formato.
- **Portão humano:** apresentar a prancha, ofertas e justificativas, adaptações
  (especialmente 360×80 e 1920×276), conflitos e tempo decorrido. Só
  `APROVADO` libera a escala; `AJUSTAR: ...` corrige a regra do template e
  conta uma nova rodada.
- **F3 — Escala:** gerar 20 × 7 = 140 PNGs a partir somente da matriz e dos
  templates aprovados, em staging. A execução é determinística e reprodutível.
- **F4 — QA:** conferir visualmente e mecanicamente cada família e os casos de
  estresse; produzir manifesto com dimensão, modo, perfil, bytes e SHA-256.
- **F5 — Promoção:** copiar para `OUTPUT/` apenas os PNGs aprovados no QA;
  preservar os registros e deixar a pasta somente com os 140 entregáveis.

Em todas as fases: `INPUT/` é imutável, produção ocorre em staging datado,
promoção não sobrescreve, scripts de gravação declaram `REFUSE_OVERWRITE`, e
cada execução preserva `OK|...` ou `ERRO|motivo`.

## Medição antes de comparar custo

Registrar no log próprio, desde o início até a promoção, por fase e por
formato:

| Medida | Registro |
|---|---|
| `wall_clock` | timestamps ISO de início/fim e duração humana do run |
| `script_time` | tempo do JavaScript/processo mecânico, incluindo retries |
| `ui_time` | tempo efetivo no Photoshop e intervenções do operador |
| `retrabalho` | correções, re-renderizações e rodadas `AJUSTAR` |
| `aprovação` | status, rodada e tempo de aprovação por formato |
| `custo` | tokens, cobrança e custo total do run, com a fonte da medição |

Se tokens ou cobrança não tiverem telemetria, registrar `null`; não estimar.
`custo_por_arte_aprovada` é `custo_total_do_run_incluindo_correções ÷ número
de PNGs aprovados no QA`, e não custo de token isolado. Sem custo total
observável, esse campo permanece `null` e nenhuma economia é declarada.

## Escalonamento

Uma falha repetida (o mesmo defeito após a correção/retry, ou o mesmo erro em
duas saídas) sobe ao head com evidência do log. O head decide a correção e, se
necessário, aciona Sol alto para diagnóstico delimitado; não se cria uma fila de agentes revisando a mesma
peça. A escala fica bloqueada enquanto a falha não tiver causa, correção e
reteste registrados.

## Registro desta elaboração

- **Solicitado:** Luna, esforço `max`.
- **Observado pelo ambiente:** identificador Luna/Terra/Astra não foi exposto
  de forma verificável nesta execução; portanto não registro que Luna max foi
  efetivamente usado. Há relato divergente de outro spawn (`Terra`/`Astra`),
  mantido apenas como observação não verificada, sem uso como benchmark.
- **Execução deste documento:** sem Photoshop e sem execução ou alteração de
  scripts de produção; `DIARIO.md` permanece intocado. Uma listagem inicial de
  nomes sob `.claude/worktrees` e `operacao/desafio-byd-v4` ocorreram por
  acidente, sem leitura de conteúdo;
  isso fica registrado no log próprio.
