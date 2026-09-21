# 12. Fechamento histórico e versões posteriores

O pacote preserva duas evidências distintas: a V4 integral como encontrada na montagem do handoff e os 140 PNGs exatos do fechamento R18. A referência para estudar o resultado daquela execução é [resultado_historico_R18](../resultado_historico_R18/).

A comparação com o manifesto histórico encontrou 135 PNGs iguais e cinco divergentes no OUTPUT atual. Todos os sete PSDs canônicos e o PSD de input correspondem aos hashes registrados. Os cinco PNGs divergentes são do Dolphin Mini 5L GS; têm as mesmas dimensões, mas pixels diferentes, conforme data/post_delivery_pixel_comparison.json.

| Formato | Modificação observada na origem (UTC) |
|---|---|
| 1920x1080 | 2026-09-20T23:42:16.158493+00:00 |
| 1920x1125 | 2026-09-20T23:36:27.747013+00:00 |
| 1080x1080 | 2026-09-20T23:40:05.133841+00:00 |
| 1080x1920 | 2026-09-20T23:42:03.460892+00:00 |
| 1109x1973 | 2026-09-20T23:37:57.845268+00:00 |

Esses horários equivalem a aproximadamente 20h36–20h42 de 20/09 em Brasília, posteriores ao fechamento local às 02h22. O horário de filesystem não prova autoria nem causa. Não foi possível atribuir essas alterações a um operador. Elas não foram incorporadas aos tempos e tokens da execução histórica delimitada no documento 10.

As cinco versões originais ainda estavam no staging R11. Foram recuperadas por correspondência exata de SHA-256 com o manifesto R18, sem renderizar, editar ou substituir imagens. Junto às outras 135, formam o conjunto separado de 140 arquivos em resultado_historico_R18. A V4 copiada permanece intacta, inclusive seu OUTPUT com cinco versões posteriores e seus manifestos históricos.

## Evidências

- [Confronto original](../data/final_artifact_reconciliation.json): conserva a falha encontrada; não foi reescrito como aprovação.
- [Recuperação por hash](../data/historical_delivery_recovery.json): 140 arquivos verificados, hashes esperados e encontrados, caminhos de recuperação e diferenças.
- [Comparação de pixels](../data/post_delivery_pixel_comparison.json): confirma que as cinco diferenças não se limitam a metadados.
- [Estado consolidado](../data/handoff_final_status.json): separa integridade da cópia, divergência da pasta atual e recuperação histórica.

A galeria original preservada dentro da V4 pode apontar para o OUTPUT atual. Para avaliar os bytes do fechamento original, use resultado_historico_R18. O CSV imagens_finais_140.csv reproduz o manifesto histórico; seus caminhos OUTPUT são os caminhos da época, não garantia de identidade do snapshot posterior.

Esta recuperação é trabalho documental do handoff, não nova produção nem nova aprovação visual.
