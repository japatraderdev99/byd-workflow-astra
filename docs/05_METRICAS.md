# 5. KPIs, tempos, tokens e custo

> **Atualização de 21/09:** leia primeiro a [auditoria ampliada](10_AUDITORIA_COMPLETA.md): seis sessões, 163.049.724 tokens, 11 Bad Request, Luna/max registrado na etapa inicial e limite semanal de 0% a 45%. Os números anteriores permanecem identificados como recorte histórico.

Fonte quantitativa: `workspace/Projects/BYD/Jobs/V4/WORK/04_QA/process-audit-r18/metrics.json`. O relatório original contém tabelas por formato, 33 runs, fórmulas e limites. As tabelas em `data/` são extrações para facilitar análise; não adicionam nova telemetria.

| Medida | Resultado | Interpretação |
|---|---:|---|
| Janela de produção | 14h17min03,733s | 19/09 12:05:22 a 20/09 02:22:25, UTC−03; inclui espera |
| Soma de 18 terminais completos | 1h32min23,698s | parcial; inclui sucesso técnico reprovado visualmente |
| Soma de 22 trechos aproveitáveis | 2h55min41,444s | sem duplicar eventos aninhados; não tempo ativo total |
| R10 | 120 PNGs + 6 PSDs / 27min06,940s | seis formatos; construção e salvamento incluídos |
| Vazão R10 | 4,43 PNGs/min | somente trecho observado |
| QA técnico | 7,426s | 140 imagens; não inclui revisão visual |
| Retrabalho após escala | 13/140 = 9,29% | exclui pilotos e reparo estrutural |
| Entrada de tokens | 152.277.785 | inclui cache |
| Entrada em cache | 148.857.088 | subconjunto, não somar |
| Entrada sem cache | 3.420.697 | diferença |
| Saída | 602.497 | inclui 172.894 de raciocínio |
| Total observado | 152.880.282 | consumo acumulado de 1.158 respostas |
| Custo financeiro / por arte | não medido | não converter em fatura estimada |

## Regras de agregação

Deduplicar `token_usage_record.payload.usage` por response_id. Não somar snapshots cumulativos, token_count, turn_token_usage ou thread_token_usage ao mesmo consumo. Conferir totais por tarefa contra o acumulado final. Cache é subconjunto da entrada; raciocínio é subconjunto da saída.

Recorte: três tarefas vinculadas, primeiro usage recuperado às 12:46:59,793 de 19/09, corte às 02:22:25,837 de 20/09. Ficam fora 41min37,689s iniciais, respostas posteriores, relatório, plataforma e este handoff. Portanto o consumo integral do job é desconhecido. A variação de limite semanal da conta não equivale ao uso exclusivo da BYD.

Tokens por imagem são rateio do desenvolvimento observado, não custo marginal para gerar mais uma imagem. Tempos de formato estão dentro de runs: não somar ambos. Janelas de agentes podem se sobrepor: soma de tempo de agentes não é lead time.


## Recorte completo atualizado

Consultar documento 10: pedido inicial até comunicação dos arquivos finais, incluindo seis sessões, erros e informação do plano. O relatório R18 permanece histórico.
