# BYD_TPL_360x80 — ficha técnica R18

PNG: revisão visual Astra e QA técnico concluídos para 20/20 ofertas. Estado dos editáveis e do reuso: consultar `../../04_QA/production-r18/templates_manifest_r18.json`, `../../04_QA/production-r18/structural7.json` e `../../04_QA/reuse_validation_r18.json`; não inferir aprovação humana.

## 1. Partido do layout

Distribuição exclusiva para 360×80: marca e selos específicos à esquerda, oferta no centro e carro à direita. Uma faixa escura inferior separa garantias, origem e mensagem educativa.

## 2. Grade e zonas

Canvas 360×80 px. Guia de margem: 4 px; as zonas abaixo registram as posições efetivas previstas, inclusive exceções próximas à borda. Eixo de texto central. Coordenadas em `[x, y, largura, altura]`.

| Elemento | Zona em px |
|---|---|
| logo | `[8, 8, 77, 14]` |
| title | `[95, 5, 150, 9]` |
| price | `[95, 19, 145, 25]` |
| car | `[258, 6, 94, 36]` |
| benefit | `[95, 48, 255, 7]` |
| headline | `[95, 48, 255, 7]` |
| instal | `[8, 38, 77, 17]` |
| badges | `[8, 38, 77, 12]` |
| award | `[68, 23, 16, 16]` |
| tag | `[8, 23, 56, 12]` |

Rodapé nativo: fundo `[0,57,360,23]`; garantia/recompra `[7,61,96,15]`; Brasil `[108,60,36,17]`; satisfação `[150,60,19,17]`; ícone educativo `[176,61,13,16]`; mensagem `[194,66,159,9]`. A mensagem preservada é “Desacelere. Seu bem maior é a vida.”

## 3. Hierarquia e escala de texto

Ordem: marca → modelo/preço → veículo → benefício/condição → selos e legal. Títulos, preços e condicionais permanecem editáveis; o encaixe usa escala proporcional, sem condensar horizontalmente a fonte.

| Bloco | Altura geométrica nativa mínima–máxima observada, px |
|---|---|
| title | 9–9 |
| price | 19–23 |
| benefit | 6–7 |
| headline | 6–7 |

Legal extenso: oculto no micro; não há corpo aplicado no PNG deste formato.
As medidas acima são limites de tinta do bloco no Photoshop, não medição isolada da altura de caixa-alta. Não há certificação automática de legibilidade por esse número. O menor valor observado serve de alerta para novas variações; revisar o PNG a 100% antes de aceitar redução adicional. Não foi certificada uma distância percentual única entre todos os blocos.

## 4. Âncoras e regra de estouro

Modelo centralizado na sua zona; preço ancorado à esquerda na zona própria. Benefícios e condicionais são centralizados. Headlines recebem quebra por palavras com limite inicial de 100 caracteres por linha. Depois, o bloco é encaixado proporcionalmente na sua zona; não cruza a zona vizinha. Se um novo texto ficar pequeno demais, rever a quebra/grade e o piloto, sem esticar a fonte.
Ofertas `micro_dual` usam preço `[95,19,145,20]`, benefício `[95,42,255,6]` e condição `[95,50,255,6]`. Nas demais, um benefício ou condição comercial ocupa a faixa `[95,48,255,7]`; o headline genérico não disputa esse espaço.

## 5. Veículo

Escala uniforme e posição pelo centro da âncora original, dentro da zona `car`. Veículo e chão nativo permanecem juntos. Não gerar, redesenhar ou deformar o automóvel. A caixa da âncora não prova sozinha o recorte do carro: conferir a cena inteira renderizada.

## 6. Condicionais por oferta

A matriz `production_spec_r18.json` é a autoridade de IDs e substituições. Uma zona específica na oferta prevalece sobre a zona genérica abaixo; os grupos de outros estados ficam ocultos.

| Oferta | Elementos exclusivos e zonas específicas neste formato |
|---|---|
| atto-2 | tag: New, Retângulo 1 |
| dolphin-mini-5l-gs | instal [8, 38, 77, 17]; badges [8, 23, 77, 12]; detail omitido |
| king-gs | badges [8, 38, 77, 12]; award [68, 23, 16, 16] |
| sealion-26-27 | tag: New, Retângulo 1 |
| song-plus | badges [8, 38, 77, 12] |
| song-premium | badges [8, 38, 77, 12] |
| song-pro-flex | tag: New, Retângulo 1; badges [8, 38, 77, 12] |
| song-pro | tag: Group 7; badges [8, 38, 77, 12]; award [68, 23, 16, 16] |
| vd-shark | badges [8, 38, 77, 12] |

## 7. Adaptações e limites

Omitidos: tagline, legal extenso, detalhe de assinatura e headline genérico quando existe benefício/condição prioritária. Preservados: marca, modelo, preço, carro, condição selecionada, selos condicionais disponíveis e rodapé educativo. Detalhes miúdos dos prêmios têm resolução limitada. Canal/plataforma não informado; não se afirma homologação universal de display nem conformidade jurídica apenas pela presença dos selos.

## 8. Renderizar e revisar uma oferta

No Photoshop, abrir este PSD e aplicar a Layer Comp `OFERTA <offer_id>`. `#GUIAS` deve ficar oculto; exatamente um estado deve estar visível em cada ramo BG/VEICULO/LEGAL/CONDICIONAIS/OFERTA. Para exportação controlada, usar o procedimento `../../REUSO_TEMPLATES.md` e o renderizador v2 com solicitação JSON, lock e saída nova. Exportar PNG RGB8 sRGB com perfil incorporado, sem salvar alterações no PSD. Conferir oferta, formato e imagem inteira; comparação de pixels deve confirmar reexportação da mesma campanha.

Referências: spec R18; logs R03/R10 (geometria), R14/R16 (correções), R17/R20 (comps); revisão visual e QA técnico R18.
