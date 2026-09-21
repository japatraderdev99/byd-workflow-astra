# 6. Decisões, falhas e lições

| Decisão/incidente | Evidência | Consequência para padrão |
|---|---|---|
| Fonte editável e aparência têm autoridades distintas | PSD original e referências | proteger ambos; não tratar JPG como camadas |
| JSX passou no check mas falhou com Argumento Ilegal | build_p01 e pilotos seguintes | preflight estático não é prova de runtime |
| Posição incorreta ao duplicar | diagnóstico de geometria e logs | normalizar geometria e conferir render nativo |
| Máscara altera área visível | QA R07 e geometry | bounds brutos não bastam; justificar tolerâncias |
| Visibilidade oculta reaparecia | patches e diário | considerar ancestrais e estados, não só getter de camada |
| Micro com colisões | P17/P18 e diretrizes de selos | separar zonas e desvincular cópias antes de reposicionar |
| Varredura DOM lenta | R03/R05/R10 | cache de árvore estável; benchmark do mesmo resultado |
| Reuso exportava oferta errada | R13 e reuse_validation | Layer Comp precisa capturar visibilidade corretamente |
| Cache de Layer Comp inválido | R19/R20 | buscar comp fresca pelo nome durante coleção mutável |
| Primeira escala exigiu 13 correções | patches e assembly R11 | piloto precisa cobrir Flex, resíduos da cena e exceções |
| PSDs finais somam 10,34 GB | templates manifest | editabilidade preservada, peso ainda é oportunidade |

## Responsividade e conteúdo

Cada formato recebeu composição própria. O strip separa marca, oferta, carro e legal; grandes horizontais usam áreas de texto/carro; verticais e quadrado distribuem leitura e benefícios em altura. Micro prioriza marca/modelo/preço/carro/condição e selos, com mensagem educativa no rodapé. Omite legal extenso e outros elementos declarados nas fichas. Isso é uma decisão de composição registrada, não certificação legal nem aprovação da plataforma de mídia.

Selos vêm das referências e do PSD; a pesquisa externa não substituiu preços nem condições. Consulte DIRETRIZES_SELOS_E_BENCHMARKS_20260919.md e SELOS_POR_OFERTA_20260919.md. Conflitos de ano, recompra e VD estão no QA; não resolver automaticamente por plausibilidade.


## Limites observados para padronizar

O case não mediu tempo ativo de UI, custo real ou benchmark entre modelos. A construção final ainda depende de ajustes/patches além do spec. Três reexports não cobrem 140 combinações. Esses são limites encontrados nesta execução; não melhorias já implementadas.
