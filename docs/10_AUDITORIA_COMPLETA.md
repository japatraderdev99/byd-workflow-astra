# 10. Auditoria completa do case — tempo, uso, erros e custos

Este é o recorte mais completo recuperado em 21/09/2026. Complementa o relatório R18 e os adendos anteriores sem reescrever os originais. A ampliação foi motivada pelo relato do usuário de erros Bad Request e consumo do plano de R$550.

## O que mudou

Foram identificadas **duas sessões principais consecutivas da BYD e quatro agentes diretamente vinculados**. O relatório anterior cobria somente a segunda sessão e seus dois agentes. O primeiro task_started disponível é de **19/09 às 12:03:44,693 BRT**, anterior em 1min37,411s ao primeiro marco persistido no job. O manifesto foi fechado às 02:22:25,837. A comunicação final ao usuário ocorreu às 02:22:56,033; o turno encerrou às 02:22:56,047. Este adendo agora inclui também essa comunicação final.

| Indicador | Recorte original | Recorte ampliado |
|---|---:|---:|
| Sessões auditadas | 3 | 6 |
| Respostas com usage | 1.158 | 1.275 |
| Tokens entrada + saída | 152.880.282 | **163.049.724** |
| Entrada | 152.277.785 | 162.392.801 |
| Entrada em cache, subconjunto | 148.857.088 | 158.576.000 |
| Entrada sem cache | 3.420.697 | 3.816.801 |
| Saída | 602.497 | 656.923 |
| Raciocínio, subconjunto da saída | 172.894 | 190.239 |
| Calendário | 14h17min03,733s | **14h19min10,491s** |
| Snapshot semanal inicial observado | 3% | **0%** |
| Snapshot final observado | 45% | **45%** |

Os 10.169.442 tokens adicionais incluem 10.042.306 da sessão inicial e seus agentes, mais 127.136 da conclusão/comunicação posterior ao corte do manifesto. As três sessões originais reconciliam exatamente com o relatório anterior. Cada tarefa reconcilia a soma por resposta com seu último acumulado. Registros repetidos não são somados. O total ainda é telemetria observada, não fatura nem garantia de cobrança capturada de cada falha de serviço. Este handoff e a plataforma ficam fora do corte.

## Modelos registrados no conjunto completo

| Tarefa | Modelo/esforço no turn_context | Respostas | Tokens |
|---|---|---:|---:|
| head_initial | gpt-6-astra/low | 61 | 6.347.843 |
| /root/intake | gpt-5.6-terra/high | 38 | 2.897.999 |
| /root/processo | gpt-5.6-luna/max | 16 | 796.464 |
| head_main | gpt-6-astra/medium | 682 | 91.438.677 |
| /root/audit_matrix | gpt-5.6-terra/high | 241 | 30.317.079 |
| /root/diagnose_move | gpt-5.6-sol/high | 237 | 31.251.662 |

**Luna/max está comprovado como configuração registrada na tarefa inicial /root/processo.** A afirmação anterior de ausência de Luna se referia ao recorte de três sessões, e permanece verdadeira apenas nesse recorte. Isso não é benchmark econômico ou prova de roteamento interno por resposta. A sessão inicial do head registrou Astra/low; a principal, Astra/medium.

## Erros e tempo de retomada

**11 Bad Request confirmados nos encerramentos dos heads:** sete na sessão inicial e quatro na principal. Soma dos intervalos de erro até o próximo turno: **8h55min46,347s**. Esse total inclui o handoff entre sessões após o último erro inicial.

Todos os intervalos entre turnos dos dois heads somam **10h06min59,962s**. A diferença para a janela técnica de lifecycle (marcos detalhados abaixo) é **4h12min11,392s** de janelas de turno, sem classificá-la como tempo ativo. Os intervalos já fazem parte das 14h19min10,491s: não somá-los novamente.

Não há medição de indisponibilidade pura do provedor. Uma retomada depende do operador, e os auxiliares/Photoshop podem trabalhar entre turnos do head. O erro genérico não permite atribuir causa raiz ao Photoshop, ao conector ou ao serviço de inferência. A captura confirma o sintoma na interface, não a camada causadora.

## Plano de R$550 e rateio atualizado

O usuário informou uso exclusivo da conta para a janela BYD. O baseline recuperado marca **0% às 12:04:04**, e o último snapshot **45% às 02:22:56**. Assim, a melhor variação observada para o conjunto é **aproximadamente 45 pontos percentuais do limite semanal**, em vez dos 42 do recorte anterior. Os percentuais são arredondados; os horários de reset oscilam alguns segundos nos snapshots, sem evidência de uma nova semana nesse intervalo.

| Hipótese de rateio gerencial | Fórmula | Custo alocado | Por 140 PNGs |
|---|---|---:|---:|
| R$550 mensais, semana média anual | 550 × 12 ÷ 52 × 0,45 | **R$57,12** | **R$0,41** |
| R$550 mensais, convenção de quatro semanas | 550 ÷ 4 × 0,45 | R$61,88 | R$0,44 |
| R$550 semanais | 550 × 0,45 | R$247,50 | R$1,77 |

**A periodicidade dos R$550 não foi confirmada inequivocamente.** A resposta do usuário confirmou exclusividade de uso na janela, e não é tomada como confirmação separada da mensalidade. Os cenários são alternativas, não parcelas a somar. O primeiro pode ser usado para planejamento caso R$550 seja mensal, com essa hipótese visível.

Mesmo com mensalidade confirmada, limite semanal não é crédito em reais com conversão contratual proporcional demonstrada. Portanto **R$57,12 seria alocação gerencial da assinatura**, não custo real faturado do job. Não inclui máquina, Photoshop, tempo humano ou infraestrutura. Não há evidência de cobrança incremental de R$550 provocada por esse trabalho.

## Dados e reprodução da auditoria

- [expanded_audit.json](../data/expanded_audit.json): escopo, horários, agentes, tokens, eventos e limites.
- [expanded_usage_records_sanitized.json](../data/expanded_usage_records_sanitized.json): 1.275 registros sem prompts/raciocínio.
- [audit_expanded_scope.py](../tools/audit_expanded_scope.py): extrator por vínculos parent_thread_id, corte e deduplicação.
- [cost_allocation_expanded.json](../data/cost_allocation_expanded.json): hipóteses e fórmulas de rateio.

A reprodução do extrator requer as sessões locais originais, que não acompanham a transferência. Os registros sanitizados acompanham o pacote para recomputar as somas sem acessar conversas privadas.

## Fronteiras temporais exatas

O primeiro prompt está em 19/09 12:03:45,542 BRT; a mensagem final, em 20/09 02:22:56,033 BRT: **14h19min10,491s**. A janela técnica de lifecycle vai de 12:03:44,693 a 02:22:56,047: **14h19min11,354s**. O primeiro intervalo começa antes da mensagem por preparação do turno. Subtraindo os intervalos entre turnos da janela técnica, restam **4h12min11,392s** com turnos abertos; isso não mede trabalho ativo. Os tempos são diferentes porque têm marcos diferentes, não por arredondamento ou soma de espera.

## Despachos de ferramentas no recorte completo

Foram registrados 1.220 despachos externos: 1.010 exec, quatro spawn_agent, 114 send_message, 38 followup_task, três request_user_input_async, quatro list_agents, 32 sleep, 12 wait_agent e três wait. Uma chamada exec pode conter várias ferramentas; não equivale a uma chamada nativa, ação de UI ou evento faturável. A planilha de tempo Photoshop continua separada desses contadores.

O ledger em data/tool_dispatch_ledger.json preserva tarefa, horário, tipo, referência de chamada, linha de origem e caminhos do case citados. Não exporta argumentos completos ou resultados que possam misturar conteúdo externo. A lógica de produção persistida está nos scripts da V4. Nenhuma conclusão de custo usa a simples contagem de ferramentas.

A imagem evidence/user_bad_request.png foi fornecida pelo usuário em 21/09 para esta auditoria retrospectiva; não foi criada por um script de produção. A referência de pilotos recebida durante a execução está em evidence/user_pilot_strip_reference.png. Ambas ficam no pacote local, fora do Git.

Foram localizadas **9 mensagens do usuário compostas apenas por “siga”**, sem contar a autorização mais longa para produzir as finais. Nem toda retomada usou essa palavra: houve pergunta sobre Bad Request, repetição do pedido em outra sessão e “como estamos?”. Essa contagem não deve ser igualada ao número de falhas.
