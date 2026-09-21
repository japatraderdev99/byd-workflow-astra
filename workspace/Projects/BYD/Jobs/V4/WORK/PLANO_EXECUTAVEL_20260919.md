# BYD V4 — plano de execução e calibração

Status: preparação e diagnóstico de piloto. Nenhum template canônico aprovado.
Este documento complementa FLUXO_ORQUESTRADO.md; não altera registros anteriores.

## Contrato de resultado

20 ofertas × 7 formatos = 140 PNGs opacos, RGB 8 bits, sRGB embutido.
7 PSDs editáveis, cada um contendo os estados endereçáveis das 20 ofertas.
21 pilotos: Yuan Plus AWD (título longo), Dolphin Mini 5L GS (parcelas, prêmios e detalhe exclusivo) e VD Atto 2 (preço de/por e restrição CPF).
Os três não cobrem todas as exceções: antes de escala, a matriz deve também mapear NEW, últimas unidades, ADAS, Flex e Produtor Rural. PNG de referência é autoridade visual, nunca matéria-prima da composição.

## Organização com o menor número de agentes

| Trabalho | Responsável inicial | Critério de conclusão |
|---|---|---|
| Direção de arte, conflitos e revisão do piloto | Head Astra | composição comparada à referência em tamanho nativo |
| Inventário, matriz, revisão de scripts e diagnóstico delimitado | Terra high no primeiro caso; medium após estabilização | dados rastreáveis e validáveis por script |
| Nomes, cobertura, logs e resumo de resultados | script; Luna apenas quando há interpretação textual | contrato fechado, sem decisões de conteúdo/layout |
| Photoshop | um operador com lock | cópia, render, log e fechamento controlado |
| QA visual de exceções | Astra no piloto; Sol high como alternativa a calibrar | leitura integral, hierarquia, geometria e fidelidade |
| Aprovação de template | humano | APROVADO por versão/formato |

Não criar agente por carro ou por peça. Paralelizar somente auditoria fria enquanto o operador desenha. Não acrescentar um revisor a cada export. O custo de delegação inclui contexto, revisão e retrabalho.
Luna max não é padrão de economia: começar com o menor esforço que passe na mesma tarefa controlada; max é candidato de experimento, não garantia de menor custo. Não há benchmark local concluído nem preço por tarefa observado.
Fonte de orientação de modelos: https://learn.chatgpt.com/docs/models (consultada nesta execução).

## A sequência prática

1. Fechar matriz: offer_id, referência/hash, grupo/ID de origem, textos exatos, carro/cena, componentes condicionais e visibilidade explícita de descendentes. Registrar cada divergência.
2. Resolver tipografia e logo oficial uma vez. Pacote entregue MullerNext diverge das fontes dos textos existentes (SourceSansPro/Arial); conferir fontes reais no Photoshop, preservar estilos.
3. Desenhar primeiro 1920×276. Resolver grade, preço de/por, restrição e cena original sem deformação. Renderizar as três ofertas e corrigir a regra comum.
4. Elaborar 360×80 como composição própria. Não existe garantia de comportar o legal integral com leitura: registrar cada adaptação no piloto e submeter ao humano. Nunca reduzir até ficar ilegível e chamar de aprovado.
5. Construir 1920×1080 e 1920×1125 com fichas independentes, mesmo compartilhando lógica. Depois 1080×1080, 1080×1920 e 1109×1973. Cada formato recebe três testes de estresse.
6. Consolidar templates de 20 estados. Resetar todos os variáveis/condicionais antes de ativar uma oferta; export não pode depender do estado anterior. Fixo somente para elementos comprovadamente comuns.
7. Apresentar 21 PNGs, prancha, decisões por formato e tempos. Somente após APROVADO executar lote determinístico.
8. QA de todos os arquivos por código e conteúdo; revisão visual a 100% dos pilotos, exceções e todas as famílias. Erros de regra corrigem família; erros de associação corrigem oferta. Promover cópias sem overwrite, somente PNGs na entrega.

## Regras de composição por família

| Formato | Partido de layout a testar |
|---|---|
| 1920×276 | marca à esquerda, oferta no centro, carro à direita, legal em faixa própria; evitar carro reduzido demais e selos colidindo |
| 360×80 | marca compacta, oferta essencial e carro; proposta explícita de conteúdo reduzido sujeita ao portão |
| 1920×1080 | marca superior; oferta e benefícios em coluna; veículo dominante ao lado com piso/atmosfera coerentes |
| 1920×1125 | mesma família horizontal com grade própria e área inferior maior para condições |
| 1080×1080 | composição feed reequilibrada; carro e oferta com prioridade sem cortar rodapé |
| 1080×1920 | distribuição vertical com respiro; não ampliar o carro para ocupar toda a altura |
| 1109×1973 | família vertical com zonas e mínimos definidos em pixels próprios |

A ficha de cada template deve declarar coordenadas, âncoras, mínimos de caixa-alta legível, limites do veículo e regra de estouro. Esses valores só viram canônicos após render e revisão. Sem escalas não uniformes, sem reconstruir carro/texto/selos e sem usar a referência achatada como fundo.
Texto excedente: quebra autorizada → ajuste de caixa → redução uniforme até mínimo → exceção. Falha ao exceder mínimo, sem export silencioso. Preservar estilo misto de grupos de preço.
Sombras/reflexos são componentes de cena; limites da cena não equivalem à silhueta do carro. Avaliar ambos e registrar bounds do veículo visível.

## Uso econômico do Photoshop

Preparar scripts e dados fora da UI. Uma chamada UI inicia um script delimitado; o Photoshop efetua as duplicações, transformações e exportações. Rever o PNG retornado e fazer ajuste pontual na configuração. Evitar arrastar dezenas de elementos por oferta.
Antes de cada execução: verificação fria, preflight sem documentos abertos, guarda de todos os destinos, perfil explicitado. Guardar preferências e restaurar ao encerrar. O log informa etapa/ID causador da falha. Não reexecutar arquivo histórico nem sobrescrever revisão rejeitada.

## Medição simples e honesta

Arquivo de eventos JSONL, append-only: task_id, fase, formato, revisão, modelo solicitado, modelo observado (se comprovável), início/fim, duração de parede, tempo de script, tempo UI observado, tentativas, resultado, artefatos, motivo de retrabalho, tokens e custo com fonte.
Ausente = null. Tempo de processo não é tempo de raciocínio; soma de tarefas paralelas não é duração total. Não reconstruir tempo anterior por suposição. Espera por usuário fica separada.
Indicadores: tempo até primeiro piloto aceitável; tempo por template aprovado; taxa de primeira aprovação; retrabalho por família; tempo marginal por oferta; custo completo por peça aprovada quando observável. Ainda não há denominador de templates aprovados.
Calibração: uma tarefa de matriz com resposta conferível e uma família visual já revisada pelo head. Testar Terra medium/high e Luna no trabalho delimitado somente quando houver volume que amortize o teste; erro crítico exige correção e nova verificação. Uma falha de conteúdo não é compensada por velocidade.

## Estado de retomada

Inventário e esboços anteriores foram encontrados, não gerados nesta retomada. P01 terminou com Argumento Ilegal na transferência/organização de camada. P02 isolou falha após duplicação, ao mover para grupo. P03 confirmou camada no documento de destino e repetiu falha no movimento. P04 testa posicionamento de grupo com PLACEATEND. Isso é diagnóstico, não produção aprovada.
O lock anterior foi liberado somente após confirmação explícita do usuário. O PID salvo é do shell do lock, não prova que o Photoshop estava livre.
O primeiro levantamento listou nomes fora do perímetro antes de ler as regras; incidente registrado no diário. Não reivindicar execução competitiva isolada.

## Atualização após a calibração visual

A hipótese econômica só está parcialmente demonstrada: scripts concentram as operações repetitivas e o patch P14 levou 352392 ms, mas foi reprovado visualmente. Não usar esse tempo como produção aprovada. Houve retrabalho relevante de geometria, codificação e estado de camadas; o run não é benchmark de custo estabilizado.

Regra aprendida: renomeação, organização e export devem ser etapas separadas. O DOM Photoshop pode alterar a visibilidade ao atribuir nomes e `visible` sob ancestral oculto não serve como inventário de estado local. Usar árvore estrutural com flags intrínsecas, depois verificar o render no Photoshop. A escala precisa resetar também descendentes condicionais, não só grupos de oferta.

Dolphin Mini é o título mais longo do conjunto observado, além de reunir parcelas/prêmios/detalhe. Yuan Plus testa a silhueta e a composição de oferta simples; Atto VD testa de/por e CPF. Os três cobrem os critérios do piloto em conjunto.

Antes de consolidar 20 estados: resolver quatro associações de camadas pendentes, reduzir redundância dos Smart Objects, desenhar guias, impor mínimos legíveis e testar ordem de ativação. A direção visual pode ser revisada nos 21 pilotos; aprovação visual não converte automaticamente o rascunho de três estados em canônico.
