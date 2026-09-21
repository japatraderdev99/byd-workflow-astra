# BYD V4 — regras do run

Este diretório é um **run isolado** do desdobramento Varejo BYD Setembro.
Você recebe o material do cliente, constrói os templates canônicos e entrega
os PNGs finais. Outros operadores vão resolver o mesmo caso, com o mesmo
material, antes ou depois de você. Tudo o que você precisa está aqui ou na
infraestrutura listada abaixo.

Ordem de leitura:

1. `00_LEIA_PRIMEIRO.md` (este arquivo) — regras, fases, portões.
2. `01_BRIEFING_CLIENTE.md` — o pedido, o escopo, as ofertas e as diretrizes.
3. `02_PADRAO_TEMPLATE_CANONICO.md` — o que é um template canônico aqui.
4. `03_CRITERIOS_DE_AVALIACAO.md` — como o run será julgado.
5. `AGENTS.md` na raiz do workspace — contrato de operação (lock, regras invioláveis, caminhos).

## 1. Seu papel neste run

Você é o **operador único** deste run: organização, Photoshop, QA e entrega.
Isto substitui, só para este diretório, a divisão de papéis Codex/Claude do
`AGENTS.md`. Todas as outras regras do `AGENTS.md` continuam valendo — lock,
`INPUT/` imutável, nada de `flatten`, `REFUSE_OVERWRITE`, `OK|`/`ERRO|`,
caminhos resolvidos pelo `.mkroot`.

Para o lock, use como nome de agente o seu modelo e modo de esforço, em
minúsculas e com hífen (ex.: `opus-medio`, `codex-sol-alto`):

```bash
operacao/lib/pslock.sh status
operacao/lib/check_jsx.sh <script.jsx>
operacao/lib/pslock.sh acquire <agente> byd-v4 <script>
operacao/lib/pslock.sh release <agente>
```

## 2. Perímetro — o que você pode ler e onde pode escrever

**Pode ler:**

- `Projects/BYD/Jobs/V4/` (este diretório);
- `AGENTS.md`, `CLAUDE.md`, `.mkroot`;
- `operacao/lib/` (infraestrutura: lock, check_jsx, mkroot);
- `psd-editor/01 Sistema Operacional/`, `02 Padrões de Design/`,
  `03 QA e Entrega/`, `06 Automação e Scripts/` (cânone de qualidade).

**Não pode ler, listar nem executar** — nem para "consultar como foi feito":

- qualquer outro job da BYD: `Projects/BYD/Jobs/V3`, `v2`, `2026-09-retail`,
  ou qualquer pasta `V4*` que não seja esta;
- `operacao/2026-09-1*` e `operacao/desafio-byd-v4/`;
- `psd-editor/04 Cases/` e `psd-editor/90 Arquivo/`;
- jobs de outros clientes em `Projects/`;
- pastas do Google Drive, Downloads e histórico de sessões anteriores.

O objetivo é medir o seu raciocínio sobre este material, não a sua
capacidade de achar uma resposta pronta. Leitura fora do perímetro
**desclassifica o run**. Se você esbarrar em algo fora dele por acidente,
registre em `WORK/06_LOGS/DIARIO.md` e siga.

**Só escreve dentro de `Projects/BYD/Jobs/V4/`** — exceto o lock em
`operacao/.ps.lock/`, que é gerido pelo `pslock.sh`. Scripts vão em
`WORK/05_SCRIPTS/`, não em `operacao/`.

**Ferramentas:** Photoshop (ExtendScript/UXP, recursos nativos inclusive
Preenchimento Generativo para estender fundo), `psd-tools`, Pillow e
utilitários locais. **Proibido:** gerar ou redesenhar carro, logo, selo ou
texto com IA; usar API externa paga; baixar ativos da internet.
O carro é sempre o pixel original do PSD do cliente.

## 3. Fases e portões

| Fase | Entrega | Onde |
|---|---|---|
| F0 — Intake | inventário do INPUT, leitura estrutural do PSD, matriz de variáveis oferta × elemento, conflitos de conteúdo | `WORK/00_MATRIZ/` |
| F1 — Templates canônicos | 7 PSDs editáveis, um por formato, + ficha técnica de cada um | `WORK/01_TEMPLATES/` |
| F2 — Pilotos | 1 PNG por formato de **3 ofertas-teste** (21 PNGs) + prancha | `WORK/02_PILOTOS/` |
| **Portão humano** | pare e peça aprovação (ver abaixo) | — |
| F3 — Escala | 140 PNGs gerados a partir dos templates | `WORK/03_STAGING/` |
| F4 — QA | QA visual e técnico, pranchas, manifesto com SHA-256 | `WORK/04_QA/` |
| F5 — Promoção | só os PNGs aprovados no QA, copiados | `OUTPUT/` |
| F6 — Fechamento | relatório final | `RELATORIO_FINAL.md` |

### Ofertas-teste do piloto

Escolha você as três, e justifique a escolha na matriz. Elas devem cobrir,
juntas, o pior caso do conjunto: o título mais longo, a oferta mais densa
(mais elementos exclusivos) e uma oferta de Venda Direta. Um piloto que só
prova o caso fácil não prova o template.

### O portão humano

Existe **um** portão obrigatório: ao terminar F2, pare e apresente ao
humano, numa única mensagem:

1. caminho da prancha dos 21 pilotos;
2. as três ofertas-teste e por que foram escolhidas;
3. por formato, o que foi adaptado, reduzido ou omitido e por quê
   (em especial 360x80 e 1920x276);
4. conflitos de conteúdo encontrados no material do cliente;
5. tempo decorrido até aqui.

O humano responde com `APROVADO` (escalar tudo) ou `AJUSTAR: <itens>`.
Não escale antes de `APROVADO`. Cada rodada de `AJUSTAR` é contada.

Fora desse portão, não pergunte o que você pode decidir e registrar.
Pergunte só o que bloqueia de verdade, uma vez, de forma objetiva.

## 4. Registro obrigatório

- `WORK/06_LOGS/DIARIO.md`: início e fim de cada fase com horário
  (`date -Iseconds`), decisões e motivos, erros e como foram resolvidos.
- Todo script: entrada, saída, `OK|...` ou `ERRO|motivo`, log preservado em
  `WORK/06_LOGS/`.
- `WORK/04_QA/manifest.json`: uma entrada por PNG entregue — arquivo,
  `offer_id`, formato, dimensões, modo, perfil, bytes, SHA-256, template de
  origem.

## 5. Fechamento

`RELATORIO_FINAL.md` na raiz deste run, com:

- início, fim e duração total; tempo por fase;
- contagem final por formato (esperado 20 × 7 = 140);
- decisões de design por formato, em uma linha cada;
- omissões ou adaptações de conteúdo e sua justificativa;
- conflitos no material do cliente e como foram tratados;
- defeitos que você achou no seu próprio QA e corrigiu;
- o que ficou pendente, sem arredondar para cima.

Declare o que foi verificado e como. "Final" no nome não é aprovação;
`OK` mecânico não é QA visual.
