# Resolução nativa de mapeamento r01

`REFUSE_OVERWRITE`: relatório novo, sem alteração de PSD, PNG ou especificação existente.

| Caso | Evidência nativa recebida | Conferência com `production_spec_r01.json` | Resultado para QA |
|---|---|---|---|
| King GS / Qual Comprar 2026 | `source_exception_award_323.png` com a camada global 4364 reproduz exatamente o selo de referência; a variante sem 4364 não o contém. | `king-gs.extras` inclui `{id:4364, role:"award"}`; `car_bounds` voltou ao bounds original da âncora. | Associação provada; não tratar o selo como baked no carro. |
| VD Song Pro Flex / veículo | `source_exception_611.png` renderiza corretamente com os Smart Objects diretos 4131 e 4129 sob o estado 611; o grupo 616 vazio não participa. | `vd-song-pro-flex.car_components` é `[4131,4129]`, com `build_status:"READY"`; 616 permanece apenas como ID histórico do campo `car`. | Copiar os dois componentes na ordem especificada; não usar 616 como contêiner. |

O arquivo r01 já reflete ambas as resoluções. Esta nota só confere schema contra evidência nativa comunicada nesta rodada; não certifica legibilidade, aprovação humana ou entrega.
