---
type: design-standard
status: canonico
---

# Composição, carro e copy

## Fundo e contraste

- O fundo aprovado é preservado; ajuste apenas brilho, contraste ou camada de reforço que já exista no PSD.
- Para texto azul e branco em fundo complexo, a solução preferida é aumentar contraste do fundo/camada de apoio, não aplicar sombra pesada ao texto.
- Validar a leitura em escala de entrega. Uma copy que parece boa em zoom pode falhar no celular.

## Carro

- Usar o recorte oficial do modelo, versão e cor solicitados.
- Respeitar direção de pista, luz e perspectiva. Não espelhar automaticamente.
- Escalar proporcionalmente; não distorcer.
- O carro deve tocar um piso compatível. Se estiver em gramado e a composição pede pavimento, corrigir primeiro o fundo, não mascarar a roda.
- Em Stories, aumentar o carro até sustentar a peça, sem invadir a oferta ou o rodapé.

## Copy e oferta

- Copiar texto aprovado sem alterar números, asteriscos, condições ou grafia.
- Manter a hierarquia: modelo → valor/oferta → condição → legais.
- Usar caixas já existentes; ampliar a caixa, não comprimir a copy, quando faltar respiro.
- Toda caixa de oferta deve conter a copy com margem interna equilibrada.
- Conferir que azul, branco e legais permanecem legíveis contra o fundo real da exportação.

## Margens e cortes

- Nenhum logo, selo, legal ou elemento de oferta encosta no corte.
- A margem precisa ser considerada no JPG final, não apenas na área de trabalho do mockup.
- Não exportar moldura de visualização, área externa de prancheta ou CTA de interface.

## Responsividade e zonas de respiro

- Antes de posicionar, dividir a peça em zonas exclusivas para `marca`, `modelo/oferta`, `veículo` e `selo`. Elementos principais não podem disputar a mesma zona.
- O limite visível do veículo não pode cruzar o limite do nome, preço, condição, legal ou selo. Sombra de contato pode ocupar a zona do veículo, mas não encobrir texto.
- Manter entre grupos principais pelo menos 3% do lado menor em formatos verticais/quadrados e 2% da largura em banners horizontais, salvo quando a referência aprovada exigir mais.
- Em 728×90 e 320×50, tratar modelo, oferta, veículo e selo como quatro colunas independentes. Reduzir tipografia ou veículo proporcionalmente antes de comprimir as colunas.
- Para banners horizontais, usar uma grade tipográfica de três níveis: linha 1 com apoios (`Volkswagen` e `Por R$`), linha 2 com os elementos principais (`modelo` e `preço`) alinhados pela mesma base óptica, e linha 3 com `condição` e `legal` em ritmo vertical regular.
- No 320×50, não reduzir a condição a uma linha ilegível para preservar a grade. Quebrar a condição em duas linhas, ampliar modelo/preço e reforçar o contraste local; a checagem decisiva é sempre no arquivo nativo 320×50, não somente na ampliação da prancha.
- Quando o recorte permitir, o veículo deve ocupar aproximadamente 52% a 62% da altura útil do banner. Abaixo disso tende a perder protagonismo; acima disso não pode invadir oferta, marcas ou selo.
- Não avaliar responsividade apenas na prancha: abrir cada JPG a 100% e conferir leitura, distância entre blocos, contato com o piso e margens de corte.
- Se a mudança de formato provocar colisão, reconstruir a distribuição. Não reutilizar mecanicamente coordenadas ou escala de outro formato.
