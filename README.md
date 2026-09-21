# BYD V4 — processo executado, do primeiro prompt às imagens finais

**Escopo exclusivo: o case BYD V4 executado pelo Codex e seus agentes, em 19–20/09/2026.** Pacote documental fechado em 21/09. Não inclui o desenvolvimento posterior da plataforma, outros clientes ou roteiro para outro modelo.

## Leitura recomendada

1. [Pedido original do usuário](evidence/01_PROMPT_ORIGINAL.md).
2. [Cronologia real da execução](docs/08_CRONOLOGIA_EXECUTADA.md).
3. [Arquitetura e fontes de verdade](docs/02_ARQUITETURA.md).
4. [Agentes e competências utilizadas](docs/04_AGENTES_E_SKILLS.md).
5. [Auditoria completa: tempos, tokens, erros e plano de R$550](docs/10_AUDITORIA_COMPLETA.md).
6. [Decisões de design, falhas e correções](docs/06_DECISOES_E_LICOES.md).
7. [Reuso efetivamente validado e limites](docs/03_RUNBOOK.md).
8. [Ambiente e dependências](docs/07_AMBIENTE.md).
9. [Mapa de scripts](docs/09_MAPA_DE_SCRIPTS.md).
10. [Distribuição, GitHub e verificação](docs/11_DISTRIBUICAO.md).
11. [Integridade e cinco versões posteriores](docs/12_INTEGRIDADE_E_VERSOES_POSTERIORES.md).

## Resultado local

**140 PNGs, vinte ofertas × sete formatos, e sete PSDs canônicos editáveis.** QA técnico 140/140, revisão visual do Astra 140/140, QA estrutural 7/7, 280 verificações de estado e três reexports idênticos em pixels. Isso não equivale a aprovação final do cliente ou entrega externa em Drive.

**Do primeiro prompt à comunicação de fechamento: 14h19min10,491s**, incluindo interrupções. A auditoria ampliada cobre seis sessões (dois heads consecutivos e quatro auxiliares), 1.275 respostas com **163.049.724 tokens observados**, onze Bad Request e limite semanal observado de 0% a 45%. Custos de assinatura são cenários de rateio; não fatura do job. Leia o documento 10 antes de usar números do relatório original, cujo recorte era menor.

## Arquivos principais

- **V4 integral:** [workspace/Projects/BYD/Jobs/V4](workspace/Projects/BYD/Jobs/V4).
- **140 imagens exatas do fechamento original:** [resultado_historico_R18](resultado_historico_R18).
- **OUTPUT atual preservado:** [snapshot da V4](workspace/Projects/BYD/Jobs/V4/OUTPUT/2026-09-20-r18), com cinco imagens posteriores; consulte o documento 12.
- **PSDs canônicos:** [WORK/01_TEMPLATES/2026-09-20-r17](workspace/Projects/BYD/Jobs/V4/WORK/01_TEMPLATES/2026-09-20-r17). Contém strip R17 e seis formatos concluídos por R20.
- **Conversa pública, pedidos e respostas:** [121 mensagens](evidence/02_CONVERSA_VISIVEL.md), sem raciocínio privado ou instruções de sistema.
- **Comunicação original de fechamento:** [mensagem final](evidence/03_FECHAMENTO_IMAGENS.md).
- **Relatório histórico:** [RELATORIO_PROCESSO_E_KPIS_R18.md](workspace/Projects/BYD/Jobs/V4/RELATORIO_PROCESSO_E_KPIS_R18.md), preservado sem edição.
- **Dados auditáveis:** [data](data); [manifestos e hashes](manifests).

O pacote local inclui os binários. O GitHub contém documentação, scripts, registros e hashes, conforme a regra de manter binários fora do Git. Clone sozinho não permite abrir os PSDs; é preciso receber a pasta completa.

Não execute scripts históricos durante a leitura. Os originais foram preservados; não houve nova produção ou aprovação visual ao montar este pacote.

As ferramentas de auditoria/empacotamento em tools/ foram criadas para esta transferência e estão separadas dos scripts executados na produção, preservados em workspace/Projects/BYD/Jobs/V4/WORK/05_SCRIPTS/.

[Galeria original das 140 artes](workspace/Projects/BYD/Jobs/V4/WORK/04_QA/production-r18/REVISAO_PRODUCAO_R18.html) — preservada como evidência; pode exibir as cinco versões posteriores do OUTPUT. Para o fechamento original, use resultado_historico_R18.
