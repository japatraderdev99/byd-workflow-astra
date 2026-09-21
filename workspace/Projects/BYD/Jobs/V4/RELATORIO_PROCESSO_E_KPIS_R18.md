# BYD V4 — relatório completo de execução, workflow e KPIs

Auditoria retrospectiva da produção R18. Referência temporal: America/Sao_Paulo, UTC−03:00. Relatório elaborado após a produção, sem alterar imagens, PSDs ou os manifestos históricos. Os números abaixo separam fatos medidos, indicadores derivados e lacunas de instrumentação.

## 1. Resultado e avaliação executiva

Foram concluídos **140 PNGs: 20 ofertas × 7 formatos**, mais **7 PSDs editáveis reutilizáveis**, com fichas de composição, especificação de produção, matriz de conteúdo, galeria e manifestos de integridade. Os arquivos finais ocupam **142.801.952 bytes de PNGs** e **10.339.050.734 bytes de PSDs** (142,80 MB e 10,34 GB decimais).

A produção local foi encerrada com QA técnico 140/140, revisão visual do Astra 140/140, QA estrutural 7/7 e 280/280 testes nativos de troca de estado. Foram corrigidas 13 imagens após a primeira escala completa. Isso não é aprovação final do cliente, validação comercial/jurídica ou envio externo.

O objetivo de entregar e tornar o trabalho reutilizável foi atingido. **A execução ainda não comprova um processo barato, rápido ou otimizado de ponta a ponta.** Foi uma rodada de desenvolvimento do sistema com várias falhas e correções; a automação estabilizada ficou disponível ao final. A comparação entre modelos, o custo financeiro e a economia contra um designer humano não foram medidos.

Este relatório complementa o fechamento anterior: naquela ocasião tokens constavam como indisponíveis. A auditoria atual recuperou telemetria local das três tarefas vinculadas, com o recorte e as limitações da seção 7. O relatório anterior permanece preservado como registro de seu momento.

## 2. Escopo, insumos e fontes de verdade

- Fonte gráfica: `INPUT/02_PSD_oficial todas as artes em feed/26.08.07 VAREJO BYD FEED 1080x1350.psd` — 1.214.837.130 bytes; SHA-256 `8abc513ff9aa7bedea76e03bc9cdea78fc4cb263044c855be23ac5d0c66917f6`.
- Conteúdo e aparência: briefing do cliente, PSD e 20 referências de feed. Referências visuais e autoridade editável têm funções distintas.
- Intake: 48 arquivos de INPUT; 48/48 hashes finais coincidem com o baseline observado. O baseline `_INPUT_SHA256.json` mencionado na documentação não existia; não foi inventada uma comparação anterior à observação.
- Fonte operacional final: `WORK/00_MATRIZ/production_spec_r18.json`.
- PNGs finais: `OUTPUT/2026-09-20-r18/`; somente imagens nessa pasta.
- PSDs canônicos: `WORK/01_TEMPLATES/2026-09-20-r17/`; o nome da pasta é R17, mas contém o strip concluído em R17 e os seis formatos concluídos em R20.
- O micro 360×80 integra o briefing local, além dos seis formatos maiores. O canal de veiculação desse micro não foi confirmado.

Não houve geração de carros, marcas ou selos com IA, achatamento dos PSDs ou alteração intencional do INPUT. Os materiais foram reorganizados a partir das camadas nativas.

## 3. Workflow efetivamente executado

```mermaid
flowchart LR
 A[Briefing e INPUT imutável] --> B[Inventário e matriz de 20 ofertas]
 B --> C[Templates e 21 pilotos]
 C --> D[Revisão e autorização humana de escala]
 D --> E[Escala nativa por formato]
 E --> F[QA técnico e revisão visual]
 F --> G[Correções pontuais]
 G --> H[Reabrir PSDs e testar estados]
 H --> I[Reexportar e comparar pixels]
 I --> J[Hashes e promoção local]
```

| Etapa | Execução concreta | Critério de saída |
|---|---|---|
| F0 — Intake | Inventário com psd-tools, textos, fontes, grupos, visibilidade e hashes; geometria conferida no Photoshop | Matriz das 20 ofertas, exceções e conflitos registrados |
| F1 — Arquitetura | Um PSD por formato, zonas de composição, âncoras e condicionais | Texto editável e elementos originais preservados |
| F2 — Pilotos | Três ofertas × sete formatos; iterações de posicionamento, contraste, selos e micro | Revisão visual e autorização de escala registrada |
| F3 — Escala | ExtendScript parametrizado, um operador e uma instância do Photoshop | 140 PNGs em staging, com logs e sem sobrescrever |
| F4 — QA e correção | Revisão por formato/oferta, 13 correções; testes estruturais e de reuso | 140 imagens revistas e sete PSDs funcionais |
| F5 — Promoção | Cópia dos PNGs, SHA-256 após cópia, contagem por pasta | 140 PNGs locais, 20 em cada formato |
| F6 — Fechamento | Manifesto, fichas, galeria, relatório e protocolo de reuso | Rastreabilidade e pendências explícitas |

Os pilotos incluíram Yuan Plus AWD, Dolphin Mini GS e VD Atto 2, cobrindo título extenso, parcela/benefício e restrição de Venda Direta. A produção revelou exceções adicionais em Song Pro Flex e Yuan Pro: isso mostra que os três pilotos não cobriram todos os casos críticos. Para a próxima rodada, a seleção deve vir da matriz real de exceções, sem se limitar automaticamente a três carros.

### Operação segura e divisão de responsabilidades

Astra conduziu decisões, Photoshop, inspeção visual e fechamento. Os agentes auxiliares trabalharam em inventário, diagnóstico, scripts e documentação sem competir pelo aplicativo. A sequência foi `status → check_jsx → acquire → executar → release`. Foram usados staging datado, `REFUSE_OVERWRITE`, logs preservados e promoção por cópia.

O Photoshop foi autoridade de render e geometria; psd-tools, autoridade estrutural. A exportação mecânica não chamou um modelo por arte. Computer Use foi empregado na observação e intervenção no aplicativo; a repetição foi executada por scripts. Não existe medição isolada do tempo ou do número de ações de UI que permita precificar Computer Use neste run.

## 4. Decisões de design por formato

| Formato | Quantidade | Composição e exceções |
|---|---:|---|
| 1920×276 | 20 | Marca à esquerda, oferta central, carro à direita; legal na base; parcela Dolphin corrigida para três linhas; selos em área própria |
| 1920×1125 | 20 | Oferta e contraste à esquerda; veículo à direita; condicionais e rodapé em zonas separadas |
| 1109×1973 | 20 | Hierarquia vertical central; veículo separa preço e benefícios; rodapés próprios |
| 1080×1080 | 20 | Marca/oferta acima, carro no centro, benefícios e legal na base |
| 1080×1920 | 20 | Composição vertical equivalente, ajustada às proporções do canvas |
| 1920×1080 | 20 | Duas colunas; áreas próprias para oferta, veículo e condicionais |
| 360×80 | 20 | Composição exclusiva: marca/selos à esquerda, preço/modelo centrais, carro à direita e faixa educativa no rodapé |

No micro foram omitidos legal extenso, tagline, detalhe de assinatura e headline genérico quando substituído pela condição prioritária. Marca, modelo, preço, carro, condição selecionada e selos das referências foram preservados, com a mensagem “Desacelere. Seu bem maior é a vida.” Isso não certifica legibilidade universal nem conformidade com uma plataforma desconhecida.

As decisões de layout e os limites estão nas sete fichas e em `WORK/00_MATRIZ/layout_adjustments_r18.json`. Percentuais universais de cap-height e respiro não foram instrumentados; a revisão visual não deve ser apresentada como medição desses critérios.

## 5. Tempo total e cronologia

**Início persistido:** 19/09/2026, 12:05:22.104.  
**Fechamento local:** 20/09/2026, 02:22:25.837.  
**Tempo total de calendário documentado: 14h 17min 03.733s.**

Essa janela inclui trabalho, diagnóstico, espera, interrupções e períodos sem atividade medida. Não equivale a horas de trabalho contínuo do agente, do Photoshop ou de uma pessoa. A descoberta anterior ao primeiro carimbo e a elaboração deste relatório ficam fora dela.

| Janela cronológica | Duração de calendário | Tokens observados no intervalo |
| --- | --- | --- |
| desenvolvimento_pilotos | 10h 32min 37.896s | 37.494.827 |
| escala_correcoes | 02h 38min 25.000s | 68.863.599 |
| validacao_reuso_fechamento | 01h 06min 00.837s | 46.521.856 |

As janelas são cortes por horário: não constituem apontamento exclusivo por atividade. Dentro delas podem coexistir revisão, espera e agentes paralelos. A fronteira de autorização da escala foi registrada às 22:38, com precisão de minuto.

Marcos relevantes: intake entre 12:05 e 12:14; primeiro strip piloto concluído e reprovado às 13:03; consolidação P16 às 22:12; autorização e ajuste de selos às 22:38; produção R10 encerrada às 00:56:20; correções R16 às 01:16:25; reparo R20 às 01:57:12; teste de reuso às 02:00:46; fechamento às 02:22:25. Os intervalos entre marcos não são classificados automaticamente como ociosidade.

### Tempo instrumentado de scripts

- **18 runs com terminal único `OK|completed`: 01h 32min 23.698s.** Essa soma inclui um teste de reuso que terminou tecnicamente, mas foi reprovado visualmente.
- **22 runs com terminais ou trechos concluídos aproveitáveis, sem somar eventos aninhados: 02h 55min 41.444s.** Inclui, adicionalmente, P06, strip R03, strip corrigido R14 e strip reparado R17. É uma soma parcial de durações registradas, não o tempo ativo total.
- **R10: 120 PNGs + seis PSDs em 27min06,940s**; média amortizada de 13.56s por PNG, ou 4.43 PNGs/min. Inclui montagem/salvamento; não é latência pura de exportação.
- **QA técnico das 140 imagens: 7,426s.** Não inclui QA visual, estrutural ou integridade dos PSDs.
- **Teste de reuso: três imagens de um formato em 1min17,320s.** Não extrapolar para 140 imagens sem outro benchmark.

O strip R03 levou 1h13min56,135s no seu evento `FORMAT_OK`, sob lógica lenta e em uma execução com interrupção/estação bloqueada registrada. É evidência do custo desta execução, não meta de desempenho futuro. O restante do run terminou com erro; o trecho validamente concluído foi preservado.

### Tempo registrado por formato

| Formato | Construção + PSD + 20 PNGs | Patch seletivo | Reparo de comps + 40 testes |
| --- | --- | --- | --- |
| 1920x276 | 01h 13min 56.135s | 00h 01min 07.709s | 00h 07min 00.472s |
| 1920x1080 | 00h 04min 47.240s | 00h 01min 42.234s | 00h 02min 04.090s |
| 1920x1125 | 00h 04min 44.741s | 00h 01min 42.025s | 00h 02min 17.412s |
| 1080x1080 | 00h 04min 18.269s | Sem patch visual de escala | 00h 01min 48.318s |
| 1080x1920 | 00h 04min 35.488s | 00h 01min 40.838s | 00h 02min 14.820s |
| 1109x1973 | 00h 04min 32.664s | 00h 01min 42.655s | 00h 02min 17.477s |
| 360x80 | 00h 03min 35.817s | Sem patch visual de escala | 00h 01min 24.920s |

Os tempos de formato são eventos dentro dos runs. Não somá-los novamente aos terminais. Tampouco representam o custo completo de conceber o template: pilotos, tentativas, diagnóstico e revisão ficam fora desses eventos.

## 6. Falhas, retrabalho e causas

| Ocorrência | Causa ou evidência | Correção / aprendizado |
|---|---|---|
| Primeiros pilotos com `Argumento Ilegal` | Script passou no verificador estático e falhou no Photoshop | Validação sintática não substitui execução nativa |
| Carros fora do canvas e limites de cena visíveis | Coordenadas ao duplicar entre documentos | Normalização de posição e nova revisão |
| Preço sem contraste | Horizonte claro atrás da oferta | Camada nativa de contraste com máscara |
| Conteúdo oculto reapareceu | Renomeação e leitura inadequada da visibilidade sob ancestrais ocultos | Preservar estados; não reconstruir visibilidade só pelo getter DOM |
| Micro com colisões de selos/textos | Espaço insuficiente e elementos vinculados movidos em conjunto | Zonas explícitas, prioridade de conteúdo e desvinculação nas cópias |
| Song Pro Flex com âncora inválida / VD com carro duplicado | Estrutura real diferente da hipótese; grupo vazio e irmãos específicos | Mapeamento nativo e tratamento da cena por oferta |
| Lentidão em loops | Varreduras recursivas repetidas no DOM | Cache de referências estáveis, evitando buscas desnecessárias |
| Falsos bloqueios geométricos | Limite bruto versus máscara e bearing de texto | QA considera máscara e tolerância justificada, mantendo checks reais |
| 13 imagens com defeitos na escala | Parcela, entrelinha, resíduos da cena e enquadramento | Uma correção de parcela + quatro de headline + quatro de máscara + quatro de carro |
| Reuso R13 exportou duas ofertas erradas | Ordem incorreta dos argumentos de `layerComps.add` | Recriação de comps com visibilidade e teste após reabertura |
| R19 falhou no segundo apply | Cache de objetos de comps durante crescimento da coleção | Busca fresca da comp pelo nome; cache só da árvore estável |
| QA estrutural v1 acusou falsos FAIL | Verificador não reconhecia prefixos `car-` e `cond-` | Corrigir parser exato e repetir QA sem alterar os PSDs |

A taxa de correção visual na primeira escala completa foi **13/140 = 9,29%**. As outras **127/140 = 90,71%** imagens permaneceram sem correção visual nessa etapa. Essa métrica exclui as rodadas anteriores de pilotos e não mede aprovação do cliente.

A planilha de tempos contém **33 runs de construção/patch/probe/reuso selecionados: 18 com terminal completo, 14 com erro sem terminal e um incompleto**. A taxa de encerramento técnico é 54,55% nesse conjunto, mas não é taxa de qualidade: há sucesso técnico com falha visual e runs com erro que produziram um trecho válido. Não representa todos os comandos, análises e tarefas do projeto.

## 7. Tokens, modelos e uso

### Escopo e método da medição

Foram lidos somente metadados de uso da tarefa principal e de seus dois agentes identificados pelo vínculo `parent_thread_id`. Nenhum prompt, raciocínio ou transcript foi copiado para o pacote de auditoria. A inspeção desses metadados externos ao job ocorreu nesta auditoria de consumo solicitada pelo usuário; não foi usada como referência de design ou implementação da produção.

A contagem usa **`token_usage_record.payload.usage` por `response_id` único**, com corte no fechamento da produção. Não soma snapshots cumulativos, `token_count`, `turn_token_usage` ou `thread_token_usage` como se fossem consumos adicionais. A soma de cada tarefa reconciliou com o último acumulado da mesma tarefa; não houve response_id repetido entre as três.

O primeiro registro de uso recuperado é de 19/09 às 12:46:59.793: há **00h 41min 37.689s iniciais sem cobertura nesta coleta**. Portanto o total abaixo é o consumo comprovado do trecho auditado, e o total integral do job permanece não determinado. Eventos após 02:22:25.837 — inclusive a resposta de encerramento e este relatório — não entram.

| Métrica | Valor observado | Interpretação |
| --- | --- | --- |
| Entrada total | 152.277.785 | Inclui cache; processamento acumulado de contexto em múltiplas respostas |
| Entrada em cache | 148.857.088 | Subconjunto da entrada; não somar novamente |
| Entrada sem cache | 3.420.697 | Entrada total menos entrada em cache |
| Saída | 602.497 | Total de saída registrado |
| Raciocínio na saída | 172.894 | Subconjunto da saída; não somar novamente |
| Total | 152.880.282 | Entrada + saída, não texto único do projeto |
| Proporção de entrada em cache | 97.75% | Não equivale a desconto financeiro medido |
| Respostas com registro de uso | 1.158 | Respostas intermediárias do agente; não mensagens do usuário |
| Compactações registradas | 10 | Somadas nas três tarefas |

### Distribuição por agente e modelo registrado

| Agente | Modelo/esforço em turn_context | Respostas | Entrada | Cache | Saída | Total |
| --- | --- | --- | --- | --- | --- | --- |
| head | gpt-6-astra/medium | 680 | 91.076.710 | 89.658.240 | 234.831 | 91.311.541 |
| audit_matrix | gpt-5.6-terra/high | 241 | 30.101.799 | 28.647.680 | 215.280 | 30.317.079 |
| diagnose_move | gpt-5.6-sol/high | 237 | 31.099.276 | 30.551.168 | 152.386 | 31.251.662 |

Esta evidência confirma a configuração registrada nas tarefas: **Astra medium no head, Terra high em audit_matrix e Sol high em diagnose_move**. Ela não comprova roteamento interno de cada resposta pelo provedor. Não há tarefa Luna comprovada neste recorte. Relatos do intake anterior sobre modelo solicitado versus observado continuam históricos e fora da cobertura da coleta atual.

### Ferramentas e coordenação

| Tipo de despacho registrado | Quantidade |
| --- | --- |
| exec | 908 |
| send_message | 106 |
| followup_task | 37 |
| sleep | 32 |
| wait_agent | 12 |
| list_agents | 4 |
| request_user_input_async | 3 |
| wait | 3 |
| spawn_agent | 2 |

Total: **1107 despachos diretos registrados**, incluindo 908 chamadas ao orquestrador `exec`. Uma chamada exec pode conter várias ferramentas; estes números não são o total de chamadas nativas do Photoshop, ações de UI ou requisições faturáveis. Os 106 envios entre agentes e 37 follow-ups mostram que a coordenação teve peso operacional relevante. Não é possível atribuir todo token excedente a essa coordenação sem instrumentação por chamada/atividade.

### Uso da conta e custo financeiro

A janela semanal global passou de **3% no primeiro snapshot observado para 45% no último**, com o mesmo horário de reset. A diferença de 42 pontos percentuais **não pode ser atribuída exclusivamente ao job**: não há isolamento da conta nem baseline no início do intake. A consulta posterior da conta também retornou 45% consumido e 55% restante.

**Custo monetário real: não disponível. Custo por arte: não disponível.** Não existe fatura atribuída ao job, tarifa contratada aplicada por resposta, nem apontamento de custo humano/máquina. Não converter os tokens em preço de API como se fossem cobrança real do plano utilizado. Créditos sem saldo não significam execução gratuita.

A documentação oficial distingue atualizações de tokens da tarefa, resumos de atividade da conta e limites de uso. Referência: [OpenAI — App Server, tokens e limites](https://learn.chatgpt.com/docs/app-server). A telemetria efetivamente encontrada é a fonte dos números deste relatório; a documentação não atesta seu custo financeiro.

## 8. KPIs fundamentais e suas definições

| KPI | Fórmula / denominador | Resultado | Status / limite |
| --- | --- | --- | --- |
| Completude | PNGs finais / 140 esperados | 100% | Medido |
| QA técnico | 140 PASS / 140 | 100% | Dimensões, RGB8, sRGB |
| Cobertura da revisão visual | 140 revisados / 140 | 100% | Revisão Astra; não aprovação humana |
| Primeira passagem visual da escala | 127 sem correção / 140 | 90,71% | Derivado; exclui pilotos |
| Retrabalho visual da escala | 13 corrigidos / 140 | 9,29% | Derivado; exclui retrabalho estrutural |
| QA estrutural | 7 PASS / 7 PSDs | 100% | Fonte atual e hashes vinculados |
| Teste de estados | 280 PASS / 280 testes | 100% | 20 estados antes + depois, em sete formatos |
| Reexportação idêntica | 3 PASS / 3 testados | 100% da amostra | Amostra não aleatória de um formato |
| Cobertura do teste de pixels | 3 / 140 imagens; 1 / 7 formatos | 2,14%; 14,29% | Não extrapolar para o universo |
| Integridade INPUT | 48 hashes iguais / 48 | 100% | Contra baseline observado |
| Integridade da promoção | 140 hashes iguais / 140 | 100% | Após cópia |
| Encerramento técnico dos runs | 18 / 33 runs selecionados | 54,55% | Não é qualidade nem taxa de produção |
| Vazão R10 | 120 PNGs / 27,116min | 4,43 PNGs/min | Somente trecho estabilizado de seis formatos |
| Tempo total de calendário | fim − início | 14h17min03,733s | Inclui esperas; ativo não medido |
| Tokens por PNG final | 152.880.282 / 140 | 1.092.002,01 | Rateio de desenvolvimento auditado; não custo marginal |
| Reuso funcional dos estados | 140 estados com teste nativo / 140 | 100% | Não significa identidade de pixels de todos os estados |
| Custo por PNG aprovado | custo integral / aprovação definida | N/D | Sem custo real e sem aprovação final do cliente |
| Economia contra processo manual | 1 − custo automatizado / custo manual | N/D | Sem baseline comparável |
| Tempo ativo UI / humano | intervalos efetivos, sem sobreposição | N/D | Não instrumentado |
| Aprovação final do cliente | aprovados pelo cliente / entregues à revisão | N/D | Não foi registrada nesta produção |

## 9. Pendências de conteúdo e limites da entrega

| Tema | Divergência preservada | Ação necessária antes de veicular |
|---|---|---|
| Song Premium | Destaque R$269.800 × legal R$299.800 | Confirmar condição e valor com o cliente |
| VD Shark | Destaque R$299.990 Produtor Rural × legal R$344.990 | Validar a relação entre condição e legal |
| VD Atto 2 | Público/legal R$166.660 × “por” R$149.990 | Confirmar redação do desconto; não é erro automático |
| VD Song Pro | Título 25/26 × legal 26/27 | Confirmar ano/modelo |
| Recompra | Selo em seis referências VD × regras de varejo consultadas | Confirmar elegibilidade |
| 360×80 | Canal desconhecido e legal extenso omitido | Validar exigências do destino real |

Fontes tipográficas de StyleRuns foram preservadas; isso não prova disponibilidade de toda fonte no ambiente. O incidente de leitura/listagem fora do perímetro no início foi registrado no diário: este run não deve ser apresentado como benchmark competitivo isolado limpo. Nenhum dos conflitos foi resolvido inventando conteúdo.

## 10. O que funcionou e o que precisa melhorar

**Funcionou:** reaproveitar o PSD original, separar variável por oferta, compor por formato, usar um único operador do Photoshop, automatizar a repetição, revisar visualmente antes de promover e testar o arquivo reaberto. A separação entre render correto e template realmente reutilizável detectou um defeito que o QA de PNG não encontraria.

**Precisou de retrabalho excessivo:** modelagem inicial de âncoras e visibilidade; validação tardia das Layer Comps; cobertura insuficiente das exceções nos pilotos; varreduras DOM custosas; agentes com muitas rodadas de coordenação e contexto extenso. O percentual alto de cache mostra contexto repetido, mas não prova sozinho onde houve desperdício.

Os 7 PSDs totalizam 10,34 GB: preservam editabilidade, mas seu peso tem impacto em abertura, salvamento e hashing. A otimização de tamanho deve ser um experimento separado, com teste de pixel e estrutura, sem remover camadas úteis dos canônicos atuais.

## 11. Workflow recomendado para os próximos jobs

1. **Fechar conteúdo antes de compor:** extrair preços, anos, selos e restrições para uma matriz; listar conflitos de uma vez. Não transferir decisões comerciais ao renderizador.
2. **Usar os templates atuais como ponto de partida:** copiar para uma nova revisão e aplicar apenas mudanças de conteúdo e exceções. Um novo PSD-fonte exige novo inventário e mapeamento.
3. **Testar reuso já no primeiro piloto:** criar a comp, salvar, fechar, reabrir, alternar duas ofertas muito diferentes e comparar PNGs. Isso antecipa o defeito descoberto em R13.
4. **Escolher pilotos por exceção:** cobrir título longo, parcela, VD, benefício exclusivo, carro largo, cena com texto embutido e selos adicionais. Consolidar casos em poucos pilotos quando possível, sem cobertura fictícia.
5. **Manter um operador de Photoshop:** auxiliares só em trabalho frio. Cachear a árvore estável; buscar comps por nome após alterações na coleção.
6. **Renderizar em lote por formato:** abrir o PSD uma vez, exportar as ofertas da solicitação e fechar sem salvar. Repetição determinística não precisa de LLM por arte.
7. **Separar os controles:** técnico, visual, estrutural, reuso e integridade. Promover apenas quando todos os controles aplicáveis passarem.
8. **Reduzir coordenação:** um pedido de subagente com entrada, saída, critérios de aceitação e regra de escalonamento; evitar sucessivas mensagens para microtarefas verificáveis por script.
9. **Medir desde o primeiro evento:** fases, respostas, modelos, ferramentas, espera, UI e retrabalho. Fechar o período de produção antes da elaboração dos relatórios posteriores.

### Alocação de modelos a testar, sem alegar economia já provada

Astra permanece responsável pela direção visual, decisões ambíguas e inspeção das exceções. Terra pode receber inventário, matriz, documentação e auditorias delimitadas. Sol entra em diagnóstico difícil quando uma tarefa delimitada não resolver a causa. Luna pode ser testado para nomes, contagens e organização, sempre com verificador determinístico; ainda não foi validado neste recorte.

O próximo benchmark deve usar o mesmo conjunto de entradas e critérios, registrar modelo efetivo/configurado, tempo, retrabalho e consumo por tarefa. Comparar qualidade primeiro; custo e latência só entre execuções com o mesmo nível de aprovação. Não é possível concluir que um modelo substitui outro apenas pelo preço nominal ou pela presença nesta execução.

## 12. Instrumentação mínima para tornar o processo comparável

| Registro | Campos mínimos | KPI habilitado |
|---|---|---|
| Job | job_id, início, fim, versão do briefing, hashes, escopo | Lead time e completude |
| Etapa | phase_id, começo/fim, estado ativo/espera, motivo de espera | Tempo ativo e gargalos |
| IA | response_id, parent_thread_id, modelo registrado/servido se exposto, esforço, input/cache/output/reasoning | Tokens e distribuição sem duplicação |
| Ferramenta | call_id, tipo, início/fim, duração, sucesso/erro, fase | Tempo e falha por ferramenta |
| Photoshop | lock, documento, formato, operação, abertura/render/salvamento separados | Tempo real por template e exportação |
| Arte | oferta, formato, revisão, checks, defeito, correção, aprovador | First pass, retrabalho e aprovação |
| Financeiro | fonte de cobrança, período, moeda, valor efetivo, regra de alocação; hora humana contratada | Custo por job e por arte |

`cached_input_tokens` é subconjunto de `input_tokens`; `reasoning_output_tokens` é subconjunto de `output_tokens`. Nunca somar novamente. Guardar consumo por resposta e derivar totais; usar snapshots de conta somente para limites globais. Quando não medido, armazenar `null`, nunca zero.

Para projeção de outro job, decompor: abertura por formato + atualização de estados + exportação por arte + QA + exceções + fechamento. Hoje há observações parciais desses componentes; não há base para prometer duração ou economia exatas do próximo trabalho.

## 13. Artefatos e trilha de auditoria

- [PNGs finais](OUTPUT/2026-09-20-r18/)
- [Galeria de revisão](WORK/04_QA/production-r18/REVISAO_PRODUCAO_R18.html)
- [PSDs e fichas](WORK/01_TEMPLATES/2026-09-20-r17/)
- [Instruções de reuso](WORK/REUSO_TEMPLATES.md)
- [Manifesto final](WORK/04_QA/manifest.json)
- [Diário de execução](WORK/06_LOGS/DIARIO.md)
- [Tempos dos runs](WORK/04_QA/production_timings_r18.json)
- [Métricas desta auditoria em JSON](WORK/04_QA/process-audit-r18/metrics.json)
- [Registros de tokens sanitizados](WORK/04_QA/process-audit-r18/usage_records_sanitized.json)
- [Snapshot global da conta](WORK/04_QA/process-audit-r18/account_usage_snapshot.json)
- [Extrator reproduzível](WORK/05_SCRIPTS/audit_process_metrics_r18.py)

A auditoria não alterou os entregáveis. Os JSONs contêm fontes, fórmulas, escopo, hashes dos documentos usados e o corte temporal; a cobrança real continua não determinada.

## Apêndice — 33 runs presentes no levantamento de tempos

As durações abaixo são terminais completos; traço significa ausência de terminal, não execução de duração zero. Trechos concluídos de runs parciais estão registrados separadamente em `metrics.json`. Um terminal OK não implica aprovação visual.

| Run | Estado registrado | Tempo terminal | Log |
| --- | --- | --- | --- |
| pilot_p01 | ERROR_NO_TERMINAL | — | WORK/06_LOGS/build_p01.log |
| pilot_p02 | ERROR_NO_TERMINAL | — | WORK/06_LOGS/build_p02.log |
| pilot_p03 | ERROR_NO_TERMINAL | — | WORK/06_LOGS/build_p03.log |
| pilot_p04 | ERROR_NO_TERMINAL | — | WORK/06_LOGS/build_p04.log |
| pilot_p05 | ERROR_NO_TERMINAL | — | WORK/06_LOGS/build_p05.log |
| pilot_p06 | INCOMPLETE_NO_TERMINAL | — | WORK/06_LOGS/build_p06.log |
| pilot_p07 | COMPLETED | 00h 01min 46.623s | WORK/06_LOGS/build_p07.log |
| pilot_p08 | COMPLETED | 00h 01min 47.196s | WORK/06_LOGS/build_p08.log |
| pilot_p09 | COMPLETED | 00h 01min 47.689s | WORK/06_LOGS/build_p09.log |
| pilot_p10 | COMPLETED | 00h 08min 02.934s | WORK/06_LOGS/build_p10.log |
| pilot_p11 | COMPLETED | 00h 04min 19.304s | WORK/06_LOGS/build_p11.log |
| pilot_p12 | COMPLETED | 00h 09min 48.109s | WORK/06_LOGS/build_p12.log |
| pilot_patch_p13 | ERROR_NO_TERMINAL | — | WORK/06_LOGS/patch_p13.log |
| pilot_patch_p14 | COMPLETED | 00h 05min 52.392s | WORK/06_LOGS/patch_p14.log |
| pilot_patch_p15 | ERROR_NO_TERMINAL | — | WORK/06_LOGS/patch_p15.log |
| pilot_patch_p16 | COMPLETED | 00h 05min 30.937s | WORK/06_LOGS/patch_p16.log |
| pilot_patch_p17 | COMPLETED | 00h 00min 38.465s | WORK/06_LOGS/patch_p17.log |
| pilot_patch_p18 | COMPLETED | 00h 00min 38.654s | WORK/06_LOGS/patch_p18.log |
| r01 | ERROR_NO_TERMINAL | — | WORK/06_LOGS/build_production_r01.log |
| probe_r02 | COMPLETED | 00h 01min 16.336s | WORK/06_LOGS/probe_r02.log |
| probe_r03 | COMPLETED | 00h 01min 16.361s | WORK/06_LOGS/probe_r03.log |
| r03 | ERROR_NO_TERMINAL | — | WORK/06_LOGS/build_production_r03.log |
| probe_r05 | COMPLETED | 00h 00min 56.004s | WORK/06_LOGS/probe_r05.log |
| r07 | ERROR_NO_TERMINAL | — | WORK/06_LOGS/build_production_r07.log |
| r10 | COMPLETED | 00h 27min 06.940s | WORK/06_LOGS/build_production_r10.log |
| r12_failed | ERROR_NO_TERMINAL | — | WORK/06_LOGS/patch_controle_r12.log |
| r14 | ERROR_NO_TERMINAL | — | WORK/06_LOGS/patch_controle_r14.log |
| r16 | COMPLETED | 00h 06min 47.897s | WORK/06_LOGS/patch_controle_r16.log |
| reuse_r13_failed_visual | COMPLETED | 00h 01min 23.481s | WORK/06_LOGS/render_reuse_r13.log |
| r17_partial_strip | ERROR_NO_TERMINAL | — | WORK/06_LOGS/recapture_templates_r17.log |
| r19_failed | ERROR_NO_TERMINAL | — | WORK/06_LOGS/recapture_templates_r19.log |
| r20 | COMPLETED | 00h 12min 07.056s | WORK/06_LOGS/recapture_templates_r20.log |
| reuse_r18 | COMPLETED | 00h 01min 17.320s | WORK/06_LOGS/render_reuse_r18.log |
