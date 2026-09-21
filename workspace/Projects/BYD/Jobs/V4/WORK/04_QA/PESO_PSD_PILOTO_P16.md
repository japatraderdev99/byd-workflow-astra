# Peso do PSD — piloto P16 360x80

`REFUSE_OVERWRITE`: relatório novo. Nenhum arquivo existente foi alterado.

## Escopo e evidência

Leitura fria concluída em 2026-09-19T22:09:31-0300, somente com
`psd-tools 1.19.0`; sem Photoshop, render, extração ou conversão. Fonte
inspecionada: `WORK/01_TEMPLATES/2026-09-19-p16/P16_TRIAL_360x80.psd`.

| Item | Evidência |
|---|---:|
| Arquivo PSD | 715.557.587 bytes (715,6 MB decimal; 682,4 MiB) |
| SHA-256 do PSD | `36fb02b03d9a6f989ed8eb28bfcf887409a370d9741f37bcced8f59efa410783` |
| Canvas / estrutura | 360×80 px, RGB 8-bit, 23 camadas Smart Object, 21 recursos internos por UUID |
| Dados internos únicos declarados | 696.799.939 bytes |

O aviso `Unknown metadata key b'caiM'` emitido pelo leitor não impediu a
enumeração de camadas, UUIDs, tamanhos ou hashes; não é base para concluir
algo sobre aparência ou integridade de render.

## Diagnóstico

O peso vem principalmente de três cópias internas distintas do mesmo
`Generative Fill.psb`, uma em cada estado atual de `BG`:

| Camada / estado | UUID interno | Tamanho declarado | SHA-256 do conteúdo |
|---|---|---:|---|
| 48 / `yuan-plus-awd-26-27` | `4890ae3c-0a3d-0245-bb6d-e1a4a58d2def` | 164.184.212 B | `6dd33d2448ccdf155a7477862ead5a329cf233b4599af2149f419618ffafc60c` |
| 84 / `dolphin-mini-5l-gs` | `37c0aea7-32b3-3a4d-a720-65cc495923d9` | 164.184.212 B | mesmo hash |
| 144 / `vd-atto-2` | `4aed0631-0117-034a-80a9-3590a33bbc8b` | 164.184.212 B | mesmo hash |

Essas três instâncias ocupam 492.552.636 B, ou 68,8% do PSD. São recursos
independentes pelo UUID, embora o hash prove que o conteúdo é idêntico. É a
causa material do tamanho, não texto, vetores, legais ou as camadas de preço.

Os próximos recursos únicos são o detalhe condicional `using_the_provided_202604221111.psb`
(85.615.886 B), `Layer 1.psb` do veículo Yuan (52.422.860 B) e o PNG do
veículo Atto 2 (34.447.052 B). Os dois usos do PNG Atto 2 (camadas 157 e 158)
e os dois usos da pessoa do Dolphin (104 e 105) já compartilham UUID; não
devem ser tratados como quatro recursos independentes.

Se cada um dos 17 estados adicionais receber mais uma cópia interna desse
mesmo KV de 164.184.212 B, o PSD iria a pelo menos 3.506.689.191 B
(3,27 GiB), antes de veículos, condicionais e texto novos. Isso ultrapassa o
limite de 2 GiB. Essa projeção é deliberadamente restrita a essa repetição
comprovada; não estima o custo variável dos 20 veículos.

## Recomendação para os 20 estados

1. Antes de escalar, consolidar o `Generative Fill.psb` repetido em uma única
origem reutilizável, mantendo em cada estado somente o posicionamento e a
visibilidade necessários. A implementação deve provar depois que os 20 usos
referenciam o mesmo conteúdo, por UUID e SHA-256, sem duplicar o payload
embutido.
2. Se a transformação específica de cada estado exigir Smart Objects
separados, usar uma fonte vinculada única e versionada no pacote do template,
com hash e caminho relativo no manifesto. Não depender de arquivo externo
sem esse empacotamento verificável.
3. Fazer preflight estrutural de tamanho antes de adicionar cada família:
contar UUIDs, somar `filesize` dos recursos únicos e bloquear a expansão ao
criar uma nova cópia de hash já existente acima de 10 MB. A meta operacional
deve permanecer abaixo de 2 GiB com margem, pois o tamanho final também inclui
metadados e dados de camada.

Esta leitura identifica o risco de capacidade e a duplicação comprovada; não
aprova visualmente o piloto nem autoriza escala, conforme as regras V4.
