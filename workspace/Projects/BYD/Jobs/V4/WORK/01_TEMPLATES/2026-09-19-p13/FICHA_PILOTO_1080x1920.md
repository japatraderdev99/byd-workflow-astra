# Piloto editável — 1080x1920

Estado: DRAFT_3_STATES. Não é o canônico completo de 20 ofertas; não aprovado para escala.
Fonte executável: `WORK/00_MATRIZ/pilot_spec_p13.json`. Geometria final: Photoshop.

## Composição e grade

Família: portrait. Alinhamento principal: center. Marca → modelo/preço → carro → benefícios → condições e rodapé. Carro original escalado uniformemente, ancorado na silhueta visível, com cena/fundo sincronizados. Horizontal recebe correção azul em camada própria com opacidade e máscara, preservando as camadas originais.

Coordenadas em pixels, [x, y, largura, altura]:

| Zona | Coordenadas |
|---|---|
| logo | 330, 115, 420, 70 |
| tagline | 230, 235, 620, 48 |
| title | 120, 350, 840, 52 |
| price | 150, 440, 780, 130 |
| benefit | 95, 1330, 890, 50 |
| headline | 95, 1410, 890, 70 |
| car | 95, 710, 890, 480 |
| legal | 85, 1660, 910, 115 |
| footer | 90, 1810, 900, 60 |
| badges | 720, 1240, 280, 65 |
| instal | 200, 605, 680, 35 |
| detail | 120, 1520, 650, 100 |

## Texto, limites e condicionais

Escala uniforme dentro da zona; fonte nunca comprimida horizontalmente. Headline quebra por palavras; parcelas têm tratamento próprio no banner estreito. Preços preservam os grupos e estilos mistos do PSD. Legal usa caixa de parágrafo com texto original: corpo configurado 15 px. Caixa-alta real e estouro precisam validação por estado na consolidação canônica; este piloto não implementa ainda rejeição automática abaixo do mínimo de leitura.

Condicionais do Dolphin: parcelas, prêmios e detalhe; Venda Direta: preço de/por e restrição CPF. Nenhum selo das outras 17 ofertas é considerado validado por este teste.

Adaptações/omissões propostas: Sem omissão prevista de componentes das três ofertas, exceto elementos ocultos na referência.

## Reproduzir estes três estados

Abrir `P13_TRIAL_1080x1920.psd`. Em OFERTA, CONDICIONAIS, LEGAL, VEICULO e BG, desligar todos os subgrupos e ligar apenas os que terminam no mesmo offer_id: `yuan-plus-awd-26-27`, `dolphin-mini-5l-gs` ou `vd-atto-2`. FIXO permanece visível; #GUIAS oculto. Exportar PNG24 opaco, RGB 8 bits, sRGB embutido para destino novo. Nunca salvar sobre INPUT.

## Antes de chamar este arquivo de canônico

Resolver IDs condicionais pendentes da matriz, incluir as 20 ofertas, desenhar zonas em #GUIAS, verificar respiros e mínimos em tamanho nativo, gerar preview com guias e testar reset independente da ordem das ofertas. A aprovação da composição destes três casos não substitui essas verificações.
