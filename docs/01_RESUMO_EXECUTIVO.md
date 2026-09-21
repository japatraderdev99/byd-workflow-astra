# 1. O que foi construído

> **Atualização de 21/09:** leia primeiro a [auditoria ampliada](10_AUDITORIA_COMPLETA.md): seis sessões, 163.049.724 tokens, 11 Bad Request, Luna/max registrado na etapa inicial e limite semanal de 0% a 45%. Os números anteriores permanecem identificados como recorte histórico.

O objetivo foi transformar um PSD canônico de feed com ofertas e camadas heterogêneas em um sistema de composição por formato, preservando carro, identidade, texto editável, selos e condicionais. O resultado local reúne 20 ofertas em sete formatos: 1920×276, 1920×1125, 1109×1973, 1080×1080, 1080×1920, 1920×1080 e 360×80.

A unidade reutilizável é **um PSD por formato com 20 estados de oferta**, acompanhado por spec JSON, ficha e validador. Não é redimensionamento proporcional do feed, geração de imagem por IA, nem chamada a modelo por peça. O modelo decide e revisa; scripts operam o Photoshop e exportam.

## Resultados comprovados no fechamento R18

| Indicador | Evidência |
|---|---|
| 140 PNGs locais | manifesto R18 e OUTPUT datado |
| 7 PSDs reutilizáveis | templates_manifest_r18.json e QA estrutural |
| 140 revisões visuais | head_visual_review.json; revisão do Astra |
| 280 testes de estados | 20 ofertas × antes/depois da reabertura × 7 formatos |
| 3 reexports idênticos em pixels | reuse_validation_r18.json, apenas 1920×1080 |
| 48 arquivos de INPUT preservados | hashes contra baseline observado |
| 13 correções após primeira escala | relatório e assembly/layout_adjustments |

## O que ainda não foi comprovado

Custo monetário, tempo ativo completo, custo de UI isolado, economia em relação a um designer, superioridade econômica entre modelos e reexportação pixel-idêntica das 140 peças não foram medidos. A cobertura inicial de tokens tem uma lacuna de 41min37,689s. O destino de mídia do 360×80 não foi confirmado.

A aprovação de escala foi registrada no diário como interpretação da autorização expressa do usuário em 19/09 às 22:38, após pilotos e solicitação de selos. Não existe equivalência automática entre esse gate e aprovação final comercial ou de cliente. Leia o texto original do diário.

## Decisão para tecnologia

Adotar agora: matriz explícita, templates por formato, operador único, estados verificáveis, staging, QA por camada de evidência e promoção com hashes. Tratar como backlog: telemetria desde o início, benchmark controlado, cobertura de exceções, redução de peso de PSD e empacotamento do motor. O case é referência operacional comprovada em partes, não produto genérico de produção já homologado em todos os cenários.


## Ressalva de integridade do handoff

Os 140 PNGs exatos do fechamento estão em [resultado_historico_R18](../resultado_historico_R18/), recuperados e verificados por SHA-256. A V4 integral preserva o estado encontrado, incluindo cinco PNGs posteriores no OUTPUT. Os sete PSDs canônicos coincidem com o manifesto histórico. Consulte [a reconciliação de versões](12_INTEGRIDADE_E_VERSOES_POSTERIORES.md) antes de usar o OUTPUT como evidência da entrega original.
