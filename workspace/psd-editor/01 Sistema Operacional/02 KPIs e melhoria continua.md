# KPIs, benchmark de modelos e melhoria contínua

Proposta arquitetada em 21/09/2026. Ainda não substitui o SOP nem autoriza execução de benchmarks ou gastos.

O pacote canônico está em [Plano executivo](../../operacao/2026-09-21-kpis-benchmark/00_PLANO_EXECUTIVO.md).

- [12 KPIs centrais e 12 diagnósticos, com fatores e ações](../../operacao/2026-09-21-kpis-benchmark/01_DICIONARIO_KPIS.md)
- [Comparação Astra, Opus e Sonnet](../../operacao/2026-09-21-kpis-benchmark/02_PROTOCOLO_BENCHMARK.md)
- [Contratos de instrumentação](../../operacao/2026-09-21-kpis-benchmark/03_INSTRUMENTACAO.md)
- [Prompts e julgamento cego](../../operacao/2026-09-21-kpis-benchmark/04_PROMPTS_E_JULGAMENTO.md)

Decisões centrais: qualidade e integridade antes de custo/tempo; separar construir do zero, operar templates e orquestrar modelos; restaurar a mesma semente em vez de reutilizar soluções do teste anterior; tratar R18 como referência histórica, não controle de modelo único. O Photoshop exige um lock global do host, mesmo em raízes isoladas. Os números da plataforma atual continuam snapshots; os KPIs aqui propostos só passam a ser medidos após a implementação dos coletores.
