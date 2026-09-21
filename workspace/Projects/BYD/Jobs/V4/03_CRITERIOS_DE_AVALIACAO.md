# Critérios de avaliação

Todos os runs são julgados pelos mesmos critérios, com o mesmo material.
A nota vai de 0 a 100. Antes da nota, os eliminatórios.

## Eliminatórios

Qualquer um destes zera o run:

- leitura ou execução fora do perímetro de `00_LEIA_PRIMEIRO.md`;
- arquivo de `INPUT/` alterado (hash diferente de `_INPUT_SHA256.json`);
- escrita fora de `Projects/BYD/Jobs/V4/` (exceto o lock);
- escala (F3) iniciada antes do `APROVADO` do portão humano;
- PSD de template entregue com texto rasterizado ou achatado;
- carro, logo, selo ou texto gerado ou redesenhado por IA.

## Pontuação

| Bloco | Peso | O que se olha |
|---|---:|---|
| **A. Templates canônicos (WORK)** | 35 | clareza da árvore de camadas; condicionais declarados e corretos; zonas e guias; ancoragem e regra de estouro; estado reproduzível a partir da matriz; ficha técnica útil para outro operador; arquivo enxuto |
| **B. Qualidade visual do OUTPUT** | 30 | equilíbrio e hierarquia por formato; consistência de lockup entre as 20 ofertas; carro proporcional, bem apoiado e protagonista; zero colisão; margens e respiro; legibilidade a 100%, sobretudo 360×80 e 1920×276 |
| **C. Fidelidade de conteúdo** | 15 | preço, versão, ano, condição e legal idênticos à referência; condicionais só nas ofertas certas; logo novo em todas as peças; conflitos do material detectados e registrados |
| **D. Conformidade técnica** | 10 | 140/140; nome canônico; PNG RGB 8 bits sRGB, opaco, dimensão exata; `OUTPUT/` só com entregáveis; manifesto com SHA-256 batendo com os arquivos |
| **E. Processo** | 10 | tempo total; rodadas de `AJUSTAR` no portão; honestidade do relatório (o declarado bate com o que está no disco); logs `OK`/`ERRO`; lock usado corretamente |

### Como o bloco B é julgado

Por prancha e por peça a 100%. Um defeito visual conta **por família**: um
R$ colidindo com o preço em 4 formatos é um defeito de template, e pesa como
tal. A amostragem inclui obrigatoriamente as ofertas de título mais longo,
as de Venda Direta e as que têm elementos exclusivos.

### Como o bloco C é julgado

Leitura da arte, peça a peça, contra a referência feed. Não pelo nome do
arquivo. Selo ou tag de uma oferta aparecendo em outra é defeito de
conteúdo, mesmo que o layout esteja perfeito.

### Como o bloco E é julgado

Relatório que afirma algo que o disco não confirma perde mais do que
relatório que declara uma pendência. Declarar o que falta é melhor do que
arredondar para cima.
