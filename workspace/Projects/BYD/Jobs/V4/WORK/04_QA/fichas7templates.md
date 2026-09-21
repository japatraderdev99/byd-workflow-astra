# Fichas QA estrutural — r02

`REFUSE_OVERWRITE`: ficha nova, derivada de `WORK/00_MATRIZ/production_spec_r02.json`. Não houve leitura dos PSDs r02 nesta ficha: a produção ainda não os gerou. Grade, visibilidade e legibilidade permanecem pendentes até a execução pós-Photoshop e a revisão humana.

| Formato | Grade estrutural | Âncoras obrigatórias | Visibilidade e estados | Layer Comps | Legibilidade mínima | Tempo |
|---|---|---|---|---|---|---|
| 1920×276 | PENDENTE_QA | `BG`, `VEICULO`, `LEGAL`, `CONDICIONAIS`, `OFERTA`, `FIXO`, `#GUIAS`; zonas `tag` e `award` | 20 estados em cada contêiner; tags extraídos fora do veículo; sem vazamento `NEW` | confirmar 20 se `psd-tools` decodificar; senão registrar indisponível | NÃO OBSERVADA | desconhecido |
| 1920×1080 | PENDENTE_QA | mesmos grupos; zonas `badges`, `tag`, `award` | mesmos testes; grupo de cena King e componentes 4131+4129 do VD Flex | mesmo passo | NÃO OBSERVADA | desconhecido |
| 1920×1125 | PENDENTE_QA | mesmos grupos; zonas `badges`, `tag`, `award` | mesmos testes | mesmo passo | NÃO OBSERVADA | desconhecido |
| 1080×1080 | PENDENTE_QA | mesmos grupos; zonas `badges`, `tag`, `award` | mesmos testes | mesmo passo | NÃO OBSERVADA | desconhecido |
| 1080×1920 | PENDENTE_QA | mesmos grupos; zonas `badges`, `tag`, `award` | mesmos testes | mesmo passo | NÃO OBSERVADA | desconhecido |
| 1109×1973 | PENDENTE_QA | mesmos grupos; zonas `badges`, `tag`, `award` | mesmos testes | mesmo passo | NÃO OBSERVADA | desconhecido |
| 360×80 | PENDENTE_QA | `BG`, `VEICULO`, `CONDICIONAIS`, `OFERTA`, `FIXO`, `#GUIAS`; zonas micro `tag`, `award`, `badges` | 20 estados; validar `micro_dual`, tags e ausência de vazamento | mesmo passo | NÃO OBSERVADA | desconhecido |

## Passos após o Photoshop encerrar

1. Confirmar lock liberado e todos os documentos fechados; então executar `python3 WORK/05_SCRIPTS/qa_templates_r01.py --revision r02 --after-photoshop-finish`.
2. Ler o JSON novo em `WORK/04_QA/qa_templates_r02.json`: canvas, hash/bytes, 20 estados, grupos fixos, texto editável, comparação normalizada com os IDs da fonte, UUID único de BG, tags e âncoras.
3. Se Layer Comps não for decodificado por `psd-tools`, registrar `UNAVAILABLE`, sem converter isso em aprovação ou reprovação.
4. Fazer a revisão humana por oferta e formato. Só ela pode preencher legibilidade mínima e aprovação visual.
