# 8. Cronologia do trabalho que foi executado

Horários BRT, UTC−03. As mensagens públicas completas, com timestamps e linhas de origem, estão em evidence/02_CONVERSA_VISIVEL.md. O diário e os logs continuam preservados na V4. Esta narrativa separa o pedido, o que foi executado, os incidentes e o resultado.

| Momento | Ação/decisão efetiva | Evidência |
|---|---|---|
| 19/09 12:03:45,542 | Primeiro prompt: organizar desdobramento do PSD nativo, templates por formato, revisão sênior, agentes e medição de eficiência | evidence/01_PROMPT_ORIGINAL.md |
| 12:05–12:14 | Inventário, matriz, plano de orquestração; head inicial Astra/low, intake Terra/high e processo Luna/max registrados | expanded_audit.json, logs de intake e FLUXO_ORQUESTRADO |
| 12:13–12:31 | Sete encerramentos Bad Request na sessão inicial, seguidos de comandos e tentativas de retomada | head_events da auditoria ampliada e conversa |
| 12:46 | Continuação em outra sessão principal; head Astra/medium; audit_matrix Terra/high e diagnose_move Sol/high | vínculos de tarefas no expanded_audit.json |
| 12:48:06,945 | Usuário confirmou que podia assumir o Photoshop e o lock anterior | resposta à pergunta na conversa |
| Primeiros pilotos | Erros nativos apesar da sintaxe aprovada; diagnóstico de deslocamento, bounds, âncoras e estado | build_p01…p06, diário e relatório |
| Rodadas P07–P16 | Renderização, revisão e correção de contraste, textos, carro, selos e micro; 21 pilotos como conjunto de referência | specs, pilotos, fichas e QA |
| 15:17–15:18 | Mensagem sobre extensão do KV e âncora do Atto corresponde à captura enviada; turno terminou Bad Request | conversa, linhas 648/670 da sessão principal |
| 21:36 | Retomada após erro anterior; continuidade da revisão | task_started e mensagem Siga |
| 22:20:38,934 | Usuário pediu conferir selos e revisar detalhes de cada carro/formato | conversa pública e captura de referência |
| 22:22:12,883 | Usuário informou não conhecer canal do micro e autorizou pesquisar briefing e referências BYD | resposta registrada |
| 22:31:57,738 | Usuário instruiu seguir a produção das imagens finais com cuidado e revisão | mensagem explícita de autorização |
| 22:38 no diário | Registro operacional de produção autorizada; P17 rejeitado por colisão, P18 corrigiu micro/rodapé | DIARIO.md, seção Produção autorizada |
| Escala R03/R10 | Geração nativa em staging; diagnóstico de cenas e cache de DOM para reduzir varreduras | logs e specs de produção |
| 23:15–00:19 | Encerramento pediu desbloquear o Mac; retomada com siga. Não há Bad Request no campo de encerramento desse turno | conversa e interruptions_audit.json |
| 20/09 00:56, aproximadamente | R10 completo: 120 PNGs e seis PSDs em 27min06,940s | build_production_r10.log |
| Até 01:16, aproximadamente | Correções pontuais e montagem do conjunto; 13 PNGs corrigidos após a primeira escala | patch_controle_r14/r16 e assembly_r11_v4 |
| R13/R17/R19/R20 | Reuso revelou comps incorretas; reparo, falha em cache de comps, busca fresca e testes antes/depois de reabrir | logs de reuso/recapture e QA |
| 02:00, aproximadamente | Teste R18 de três reexports em 1920×1080; pixels idênticos | reuse_validation_r18.json |
| 02:22:25,837 | Fechamento do manifesto local e PNGs promovidos por cópia | manifest.json |
| 02:22:56,033 | Comunicação ao usuário: produção local concluída, links de imagens, galeria, PSDs e relatório | evidence/03_FECHAMENTO_IMAGENS.md |

## Reconciliações importantes

O horário de 22:38 usado no relatório original é o registro operacional do diário. A mensagem de autorização está às 22:31:57,738. Não são o mesmo evento; manter os dois evita falsa precisão de fase. O fluxo exigia aprovação humana; o operador registrou explicitamente a interpretação dessa autorização como permissão de escala. Não inventar um clique ou literal APROVADO inexistente na evidência.

O primeiro prompt foi repetido na sessão principal após a sessão inicial com falhas. A transferência entre sessões faz parte da execução, não representa outro case. A auditoria agora cobre ambas e seus auxiliares.

A palavra entrega nesta documentação significa disponibilização **local** dos 140 PNGs e comunicação ao usuário. Não foi encontrada nesta janela uma comprovação de envio externo ou aprovação final comercial do cliente. A auditoria anterior de Drive de V3 não deve ser atribuída a V4.

Os erros Bad Request são eventos de serviço/interface distintos dos erros de JSX e dos defeitos visuais. Logs de scripts não são inventário completo de falhas do chat; a auditoria de lifecycle complementa os logs Photoshop.


## Ressalva de integridade do handoff

Os 140 PNGs exatos do fechamento estão em [resultado_historico_R18](../resultado_historico_R18/), recuperados e verificados por SHA-256. A V4 integral preserva o estado encontrado, incluindo cinco PNGs posteriores no OUTPUT. Os sete PSDs canônicos coincidem com o manifesto histórico. Consulte [a reconciliação de versões](12_INTEGRIDADE_E_VERSOES_POSTERIORES.md) antes de usar o OUTPUT como evidência da entrega original.
