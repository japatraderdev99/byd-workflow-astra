# Piloto editável — 1920x1080

Estado: DRAFT_3_STATES. Não é o canônico completo de 20 ofertas; não aprovado para escala.
Fonte executável: `WORK/00_MATRIZ/pilot_spec_p16.json`. Geometria final: Photoshop.

## Composição e grade

Família: landscape. Alinhamento principal: left. Marca → modelo/preço → carro → benefícios → condições e rodapé. Carro original escalado uniformemente, ancorado na silhueta visível, com cena/fundo sincronizados. Horizontal recebe correção azul em camada própria com opacidade e máscara, preservando as camadas originais.

Coordenadas em pixels, [x, y, largura, altura]:

| Zona | Coordenadas |
|---|---|
| logo | 95, 80, 520, 75 |
| tagline | 95, 195, 610, 45 |
| title | 95, 300, 780, 45 |
| price | 95, 390, 770, 145 |
| benefit | 95, 630, 760, 45 |
| headline | 95, 720, 760, 100 |
| car | 950, 280, 900, 490 |
| legal | 95, 960, 1730, 65 |
| footer | 1100, 880, 700, 45 |
| badges | 1605, 790, 230, 65 |
| instal | 95, 555, 650, 40 |
| detail | 1100, 790, 450, 65 |

## Texto, limites e condicionais

Escala uniforme dentro da zona; fonte nunca comprimida horizontalmente. Headline quebra por palavras; parcelas têm tratamento próprio no banner estreito. Preços preservam os grupos e estilos mistos do PSD. Legal usa caixa de parágrafo com texto original: corpo configurado 14 px. Caixa-alta real e estouro precisam validação por estado na consolidação canônica; este piloto não implementa ainda rejeição automática abaixo do mínimo de leitura.

Condicionais do Dolphin: parcelas, prêmios e detalhe; Venda Direta: preço de/por e restrição CPF. Nenhum selo das outras 17 ofertas é considerado validado por este teste.

Adaptações/omissões propostas: Sem omissão prevista de componentes das três ofertas, exceto elementos ocultos na referência.

## Reproduzir estes três estados

Abrir `P16_TRIAL_1920x1080.psd`. Em OFERTA, CONDICIONAIS, LEGAL, VEICULO e BG, desligar todos os subgrupos e ligar apenas os que terminam no mesmo offer_id: `yuan-plus-awd-26-27`, `dolphin-mini-5l-gs` ou `vd-atto-2`. FIXO permanece visível; #GUIAS oculto. Exportar PNG24 opaco, RGB 8 bits, sRGB embutido para destino novo. Nunca salvar sobre INPUT.

## Antes de chamar este arquivo de canônico

Resolver IDs condicionais pendentes da matriz, incluir as 20 ofertas, desenhar zonas em #GUIAS, verificar respiros e mínimos em tamanho nativo, gerar preview com guias e testar reset independente da ordem das ofertas. A aprovação da composição destes três casos não substitui essas verificações.

Separadores de nomes internos ainda carregam mojibake do teste inicial. Normalização só na consulta; corrigir pela visibilidade intrínseca de cada nó durante consolidação, sem usar DOM visible sob ancestral oculto.
