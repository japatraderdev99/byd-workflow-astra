# Briefing — Desdobramento Varejo BYD, Setembro 2026

Cliente: BYD Servopa. Pedido original em
`INPUT/01_PEDIDO_CLIENTE/pedido_cliente_2026-09-17.png` — ele é a
autoridade; esta página transcreve e fecha o que ficou em aberto nele.

## 1. O pedido

| Campo | Valor |
|---|---|
| Campanha | Setembro |
| Demanda | Desdobramento Varejo BYD |
| Ofertas | 20 |
| Formato final | PNG |
| Prioridade entre formatos | nenhuma |
| KV | o da montadora (o do arquivo recebido) |
| Planilha de ofertas | manter a do arquivo |
| Textos legais / condições | manter os do arquivo |
| Assinatura de loja | manter a do arquivo |
| Fontes, logos e selos | os do arquivo + os entregues em `INPUT/04` e `INPUT/05` |

"Manter o mesmo do arquivo" significa: **o conteúdo de cada oferta já está
pronto no PSD e nas referências feed**. Este job não cria oferta; ele
desdobra uma oferta aprovada em novos formatos sem perder nada dela.

## 2. Escopo fechado

O pedido estimou 162 peças. O escopo foi corrigido e fechado com o cliente
em **140 peças = 20 ofertas × 7 formatos**. Não produza peça fora desta matriz.

| Pasta de entrega | Formato | Peças |
|---|---|---:|
| `OUTPUT/BANNER DESK/1920x276/` | 1920 × 276 | 20 |
| `OUTPUT/BANNER DESK/1920x1125/` | 1920 × 1125 | 20 |
| `OUTPUT/BANNER MOBILE/360x80/` | 360 × 80 | 20 |
| `OUTPUT/BANNER MOBILE/1109x1973/` | 1109 × 1973 | 20 |
| `OUTPUT/ESTATICOS/1080x1080/` | 1080 × 1080 | 20 |
| `OUTPUT/ESTATICOS/1080x1920/` | 1080 × 1920 | 20 |
| `OUTPUT/ESTATICOS/1920x1080/` | 1920 × 1080 | 20 |

## 3. As 20 ofertas

O `offer_id` é o nome canônico da oferta em arquivos, matriz e manifesto.
A referência feed é a **autoridade do conteúdo visível** da oferta.

| offer_id | Referência feed (`INPUT/03_REFERENCIAS_FEED_1080x1350/`) |
|---|---|
| `atto-2` | `Atto 2.png` |
| `atto-8` | `Atto 8.png` |
| `dolphin-gs` | `Dolphin GS.png` |
| `dolphin-mini-5l-gs` | `Dolphin Mini 5L GS.png` |
| `dolphin-se` | `Dolphin SE.png` |
| `king-gs` | `King GS.png` |
| `seal-26-27` | `Seal 26-27.png` |
| `sealion-26-27` | `Sealion 26-27.png` |
| `song-plus` | `Song Plus.png` |
| `song-premium` | `Song Premium.png` |
| `song-pro-flex` | `Song Pro Flex.png` |
| `song-pro` | `Song Pro.png` |
| `vd-atto-2` | `VD - Atto 2.png` |
| `vd-dolphin-mini` | `VD - Dolphin Mini.png` |
| `vd-king-gl` | `VD - King GL.png` |
| `vd-shark` | `VD - Shark.png` |
| `vd-song-pro-flex` | `VD - Song Pro Flex.png` |
| `vd-song-pro` | `VD - Song Pro.png` |
| `yuan-plus-awd-26-27` | `Yuan PLUS AWD 26-27.png` |
| `yuan-pro` | `Yuan PRO.png` |

`vd-*` são ofertas de Venda Direta. O mapeamento entre cada oferta e o grupo
correspondente no PSD é trabalho seu — confira pela **arte**, não pelo nome
do grupo nem do arquivo. Nomes de camada e de arquivo podem enganar.

## 4. Material recebido (`INPUT/`, somente leitura)

| Pasta | Conteúdo |
|---|---|
| `01_PEDIDO_CLIENTE/` | print do pedido |
| `02_PSD_ABERTO/` | PSD editável 1080×1350 (~1,2 GB), com o KV fixo e um grupo por oferta |
| `03_REFERENCIAS_FEED_1080x1350/` | 20 PNGs, a arte aprovada de cada oferta no feed |
| `04_LOGOS_E_SELOS/` | `BYD SERVOPA LOGO AJUSTE.pdf` — logo novo, vetorial, 3 páginas (versões de cor) |
| `05_FONTES/` | pacote de fontes da identidade entregue pelo cliente |

Integridade: `INPUT/_INPUT_SHA256.json`. Ao fim do run, todo arquivo de
`INPUT/` precisa ter o mesmo hash. Nunca salve sobre o PSD recebido —
trabalhe sempre em cópia dentro de `WORK/`.

## 5. Diretrizes do cliente

**Conteúdo**

- Números, preços, versões, anos-modelo, condições, asteriscos e legais são
  copiados exatamente como estão na referência. Nada é reescrito, abreviado
  ou "corrigido" por conta própria.
- Se a referência e o PSD divergirem, ou se o próprio material se contradisser
  (preço de destaque × preço do legal, por exemplo), **a referência feed
  vence** e a divergência é registrada na matriz e no relatório. Não invente
  número.
- Elemento que existe só em algumas ofertas (tag, selo, faixa, benefício,
  bloco de venda direta) aparece **somente** nessas ofertas, em todos os
  formatos em que couber. Elemento de uma oferta não pode vazar para outra.

**Identidade**

- O logo de todas as peças é o **logo novo** de `INPUT/04` (BYD | SERVOPA),
  na versão de cor adequada ao fundo, proporcional, sem redesenho. Ele
  substitui o logo que estiver no PSD.
- Fontes: as usadas no PSD. Se alguma estiver ausente na máquina, registre e
  não substitua por aproximação sem declarar.
- O KV (fundo, luz, atmosfera) é o da montadora. Pode ser estendido para
  caber em formatos mais largos ou mais altos; não pode ser trocado.
- O carro é o recorte/cena original de cada oferta, proporcional, sem
  distorção, sem espelhar, com contato coerente com o piso.

**Formatos**

- Cada formato tem um layout próprio e **consistente entre as 20 ofertas**:
  o mesmo lockup (posição de título, preço, carro e selos) em todas as peças
  de um formato. Variação só onde o conteúdo da oferta exige.
- Formatos próximos do feed (1080×1080, 1080×1920, 1109×1973) podem partir
  da composição da referência e ser reequilibrados. Horizontais (1920×1080,
  1920×1125) e faixas (1920×276, 360×80) exigem recomposição — não é
  miniatura nem corte do feed.
- Nenhuma informação da oferta some em silêncio. Se um formato não comporta
  um elemento de forma legível, a decisão de reduzir ou omitir é explícita,
  justificada e apresentada no portão de aprovação.

**Entrega**

- PNG, RGB 8 bits, perfil sRGB IEC61966-2.1 embutido, opaco, dimensão exata.
- Nome: `byd_<offer_id>_<largura>x<altura>.png` — ex.:
  `byd_vd-king-gl_1920x276.png`.
- `OUTPUT/` contém **somente** os 140 PNGs vigentes. Nada de PSD, prancha,
  JPG, manifesto, relatório ou `.DS_Store`.
- Prazo de referência do cliente: mesmo dia. Eficiência conta.
