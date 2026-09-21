# BYD TPL r03 — 360×80

`REFUSE_OVERWRITE`. Especificação: `WORK/00_MATRIZ/production_spec_r03.json`; família micro, grade de segurança 4 px, escopo planejado 20 ofertas neste formato (140 peças nos 7 formatos). Zonas previstas: tag `[8,23,56,12]`, badges `[8,38,77,12]`, award `[68,23,16,16]`. O spec omite tagline, legal, detail e generic_headline.

**Âncoras e estrutura a medir depois da produção:** `BG`, `VEICULO`, `LEGAL`, `CONDICIONAIS`, `OFERTA`, `FIXO`, `#GUIAS`; 20 estados por contêiner de estado; texto editável e conteúdo normalizado contra os IDs de fonte; um UUID único de BG compartilhado.

**Visibilidade prevista:** NEW é extraído completo de Atto 2 `[1377,1378]`, Sealion `[1376,1365]` e Song Pro Flex `[3209,3210]`; Group 7 do Song Pro `[4597]` é extraído inteiro. Os originais ficam ocultos no veículo. Os sete micro-dual são as seis ofertas VD e Song Pro. Em VD Song Pro Flex, ocultar o componente/âncora 4129 e manter somente a cena 4131 visível.

**QA posterior:** executar `WORK/05_SCRIPTS/qa_templates_r01.py --revision r03 --after-photoshop-finish`; tentar contar 20 Layer Comps se `psd-tools` expuser a estrutura, ou registrar `UNAVAILABLE`. Legibilidade mínima, aprovação visual, tempo e custo: **NÃO VALIDADOS**.
