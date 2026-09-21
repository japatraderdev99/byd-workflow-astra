# Padrão do template canônico

`WORK/` é a fase que decide o resultado. Um bom template faz as 20 ofertas
de um formato saírem certas por construção; um template fraco obriga a
consertar peça por peça, e o conserto por peça é onde nascem as colisões,
os selos trocados e os preços errados.

Um template canônico é o equivalente ao que um designer faz à mão quando
monta o piloto de um formato: organiza as camadas, define margens e
espaçamentos, equilibra carro e oferta, e deixa o arquivo pronto para
qualquer oferta entrar sem quebrar. A diferença é que aqui ele precisa ser
**legível por outra pessoa e reexecutável por script**.

## 1. O que entregar em `WORK/01_TEMPLATES/`

Para cada um dos 7 formatos:

| Arquivo | Conteúdo |
|---|---|
| `BYD_TPL_<L>x<A>.psd` | template editável, com o fixo e **todas as variáveis das 20 ofertas** endereçáveis |
| `BYD_TPL_<L>x<A>.md` | ficha técnica do template (seção 4) |
| `BYD_TPL_<L>x<A>_preview.png` | render do template com uma oferta ativa e as guias visíveis |

E uma vez, em `WORK/00_MATRIZ/`:

| Arquivo | Conteúdo |
|---|---|
| `matriz_ofertas.json` (ou `.tsv`) | oferta × elemento: valor de cada texto, qual carro, quais elementos condicionais ligados, qual grupo de origem no PSD |
| `inventario_psd.md` | árvore do PSD recebido, o que é fixo, o que é variável, o que foi descartado e por quê |
| `conflitos.md` | divergências no material do cliente e a decisão tomada |

A matriz é a **fonte única** da escala: o script da F3 lê a matriz e o
template, e nada mais. Se um valor só existe dentro de um script, está no
lugar errado.

## 2. Arquitetura mínima de camadas

Os nomes abaixo são obrigatórios no nível de topo, para que qualquer
operador abra qualquer template e se localize. Dentro de cada grupo, a
organização é decisão sua — e é avaliada.

```
BYD_TPL_<L>x<A>.psd
├── #GUIAS            oculto no export: margem segura, zonas, eixos
├── FIXO              igual em todas as ofertas do formato
│   ├── LOGO          logo novo BYD | SERVOPA
│   ├── ...           tagline, selos de rodapé, assinatura — o que for fixo
├── OFERTA            texto variável presente em todas as ofertas
│   ├── MODELO
│   ├── PRECO
│   ├── ...           condição, benefício, headline — o que for comum
├── CONDICIONAIS      elementos que só existem em algumas ofertas
│   ├── COND · <elemento> · <offer_id>,<offer_id>
│   └── ...
├── LEGAL             texto legal da oferta
├── VEICULO
│   ├── CAR · <offer_id>   um por oferta, só um visível por vez
│   └── ...
└── BG                KV da montadora, estendido ao formato
```

Regras:

- **Texto continua texto.** Nada de rasterizar texto, `flatten`,
  `mergeVisibleLayers` ou mesclar grupo que o script precisa endereçar.
- **Condicional se declara no nome.** `COND · NEW · atto-2,atto-8` diz ao
  leitor e ao script quando ligar a camada. Nenhum elemento condicional
  pode depender de "lembrar de desligar".
- **Um carro por oferta**, nomeado pelo `offer_id`, já posicionado e
  escalado para aquele formato. O carro do feed raramente serve sem ajuste
  num 1920×276.
- **Estados reproduzíveis.** Qualquer oferta precisa ser renderizável a
  partir do template limpo, só com a matriz — sem depender do estado em que
  a oferta anterior deixou o documento.
- **Arquivo enxuto.** Não arraste o KV inteiro de 1,2 GB para cada template.
  Leve o que o formato usa.

## 3. Responsividade — o template tem de absorver a variação

As 20 ofertas não têm o mesmo tamanho de texto nem os mesmos elementos. O
template é bom quando absorve essa variação sem intervenção manual:

- **Zonas exclusivas.** Marca, modelo/oferta, veículo e selos têm zonas
  próprias por formato, desenhadas em `#GUIAS`. Limite visível de carro não
  cruza limite de texto.
- **Respiro mínimo** entre grupos principais: 3% do lado menor em formatos
  verticais e quadrados; 2% da largura em banners horizontais (cânone em
  `psd-editor/02 Padrões de Design/01 Composição, carro e copy.md`).
- **Ancoragem.** Cada bloco de texto tem ponto de âncora declarado
  (ex.: PRECO ancorado à esquerda na base óptica de MODELO). Título longo
  cresce para o lado livre, não por cima do carro.
- **Regra de estouro** declarada: o que acontece quando o texto é maior que
  a zona — reduzir corpo até um mínimo legível, quebrar linha, ou ampliar a
  caixa. Nunca comprimir horizontalmente a fonte.
- **Mínimo legível por formato**, declarado na ficha, em px de altura de
  caixa-alta, e conferido no PNG a 100% — não na prancha.
- **Teste de estresse.** O template só está pronto quando renderiza sem
  colisão a oferta de título mais longo, a mais densa e uma de Venda Direta.

## 4. Ficha técnica `BYD_TPL_<L>x<A>.md`

Curta e objetiva. Precisa responder:

1. **Partido do layout** — de onde ele parte (referência feed reequilibrada
   ou recomposição) e por quê, em duas ou três frases.
2. **Grade** — margem segura em px, zonas com coordenadas, eixos de
   alinhamento.
3. **Hierarquia** — ordem de leitura e corpo de cada nível.
4. **Âncoras e estouro** — por bloco de texto.
5. **Veículo** — regra de escala/posição e a faixa aceitável (ex.: altura
   do carro entre X% e Y% da altura útil).
6. **Condicionais** — cada elemento, em quais ofertas, onde entra, o que
   ele desloca.
7. **Adaptações do formato** — o que foi reduzido ou omitido em relação ao
   feed, com justificativa. Para 360×80 e 1920×276 isso é obrigatório.
8. **Como renderizar uma oferta** — comando ou passo exato.

## 5. O que não fazer

- Não reaproveitar coordenadas de um formato em outro por proporção. Cada
  formato é redistribuído.
- Não resolver colisão só na peça que colidiu. Se colidiu, a regra do
  template está errada: corrija a regra e re-renderize a família.
- Não esconder informação para "fechar" o layout sem declarar.
- Não usar a referência feed exportada como imagem de fundo das peças. Ela
  é referência de conteúdo e de composição, não matéria-prima de pixel.
