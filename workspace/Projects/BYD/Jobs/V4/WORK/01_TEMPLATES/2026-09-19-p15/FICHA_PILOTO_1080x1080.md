# Piloto editável — 1080x1080

Estado: DRAFT_3_STATES. Não é o canônico completo de 20 ofertas; não aprovado para escala.
Fonte executável: `WORK/00_MATRIZ/pilot_spec_p15.json`. Geometria final: Photoshop.

## Composição e grade

Família: square. Alinhamento principal: center. Marca → modelo/preço → carro → benefícios → condições e rodapé. Carro original escalado uniformemente, ancorado na silhueta visível, com cena/fundo sincronizados. Horizontal recebe correção azul em camada própria com opacidade e máscara, preservando as camadas originais.

Coordenadas em pixels, [x, y, largura, altura]:

| Zona | Coordenadas |
|---|---|
| logo | 345, 45, 390, 60 |
| tagline | 270, 135, 540, 35 |
| title | 110, 210, 860, 36 |
| price | 230, 270, 620, 90 |
| benefit | 140, 775, 800, 35 |
| headline | 140, 830, 800, 42 |
| car | 170, 420, 740, 340 |
| legal | 60, 955, 960, 60 |
| footer | 90, 1030, 900, 30 |
| badges | 670, 890, 280, 40 |
| instal | 300, 380, 480, 27 |
| detail | 100, 875, 530, 70 |

## Texto, limites e condicionais

Escala uniforme dentro da zona; fonte nunca comprimida horizontalmente. Headline quebra por palavras; parcelas têm tratamento próprio no banner estreito. Preços preservam os grupos e estilos mistos do PSD. Legal usa caixa de parágrafo com texto original: corpo configurado 10 px. Caixa-alta real e estouro precisam validação por estado na consolidação canônica; este piloto não implementa ainda rejeição automática abaixo do mínimo de leitura.

Condicionais do Dolphin: parcelas, prêmios e detalhe; Venda Direta: preço de/por e restrição CPF. Nenhum selo das outras 17 ofertas é considerado validado por este teste.

Adaptações/omissões propostas: Sem omissão prevista de componentes das três ofertas, exceto elementos ocultos na referência.

## Reproduzir estes três estados

Abrir `P15_TRIAL_1080x1080.psd`. Em OFERTA, CONDICIONAIS, LEGAL, VEICULO e BG, desligar todos os subgrupos e ligar apenas os que terminam no mesmo offer_id: `yuan-plus-awd-26-27`, `dolphin-mini-5l-gs` ou `vd-atto-2`. FIXO permanece visível; #GUIAS oculto. Exportar PNG24 opaco, RGB 8 bits, sRGB embutido para destino novo. Nunca salvar sobre INPUT.

## Antes de chamar este arquivo de canônico

Resolver IDs condicionais pendentes da matriz, incluir as 20 ofertas, desenhar zonas em #GUIAS, verificar respiros e mínimos em tamanho nativo, gerar preview com guias e testar reset independente da ordem das ofertas. A aprovação da composição destes três casos não substitui essas verificações.
