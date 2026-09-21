# 3. Runbook: estudar, reproduzir e adaptar

## Como o JSX foi acionado na execução documentada

A integração de interface usou Computer Use/Sky por Node REPL. Há chamadas históricas com sky.get_app_state, sky.click e sky.press_key para abrir o menu Arquivo → Scripts → Procurar e selecionar o JSX. O processamento repetitivo ficou dentro do ExtendScript; o agente observou o aplicativo e revisou as saídas. Não foi um serviço headless de Photoshop ou uma chamada a modelo para cada PNG.

Exemplos rastreáveis: sessão inicial, chamadas nas linhas 311 e 455; sessão principal, registros do procedimento no entorno da linha 2546. O ledger contém os despachos e as referências; o código da produção está na V4. Menus/índices de elementos de UI pertencem àquele estado do aplicativo e não devem ser reutilizados como coordenadas universais. A pausa de Mac bloqueado mostra uma dependência operacional real dessa execução.

## A. Primeira leitura, sem Photoshop

1. Ler README, contrato e relatório original; identificar a separação entre histórico e canônico.
2. Executar na raiz do pacote `python3 tools/verify_package.py --mode text`. Confere a parte versionada.
3. Com o pacote completo, executar `python3 tools/verify_package.py --mode full`. Confere todos os hashes; lê aproximadamente 70 GB, pode demorar.
4. Abrir o spec R18, matriz, sete fichas e exemplos finais. A galeria HTML histórica também está incluída; links absolutos históricos podem exigir abertura manual dos PNGs.
5. Ler DIARIO, relatório de métricas e tabela de scripts. Identificar o que é evidência e o que é proposta antes de planejar qualquer mudança.

## B. Reexportação do mesmo conteúdo

1. Trabalhar em cópia operacional, preservando este snapshot. Manter a topologia `workspace/Projects/...` e `workspace/operacao/lib/...` com `.mkroot` em workspace.
2. Instalar/verificar fontes do INPUT, Photoshop, Python e dependências conforme documento 07. Não abrir documentos de produção de outro operador.
3. Se a cópia estiver no mesmo computador do workspace original, usar uma única raiz operacional e reconciliar ambos os locks antes de abrir Photoshop. `mkdir` coordena somente um caminho de lock, não toda a máquina.
4. Consultar `operacao/lib/pslock.sh status` a partir da raiz operacional. Lock antigo exige handoff; nunca remover automaticamente.
5. Copiar `render_request_r18.json` e `render_canonical_v2.jsx` para nomes de nova revisão na mesma estrutura. Alterar no JSX apenas REQUEST_REL para apontar ao novo pedido. Manter `revision: r18` no JSON: esse campo é validado como versão de contrato, não a data da execução.
6. No pedido, escolher IDs existentes e formatos únicos. `templates[].path` deve ser exatamente `output_templates + BYD_TPL_<formato>.psd` do spec R18. Definir output_folder, log_file e validation_output novos, sem overwrite.
7. Atenção: `validation_output` é apenas pré-checado no renderer; o script não grava esse JSON. A evidência de comparação deve ser criada por QA separado. Não esperar um arquivo que o renderer não produz.
8. Rodar `operacao/lib/check_jsx.sh <novo-script.jsx>`. O resultado só valida estaticamente; não comprova render.
9. Adquirir `operacao/lib/pslock.sh acquire <operador> byd-v4-reuso <novo-script.jsx>`.
10. No Photoshop, executar o novo JSX via Arquivo → Scripts → Procurar, sem outros documentos abertos. O script faz preflight, aplica comps, valida cinco ramos, exporta RGB8/sRGB e fecha sem salvar o template.
11. Verificar o log: ausência de ERRO, terminal OK|completed e actual_pngs igual a expected_pngs. Não usar apenas o retorno do processo: o JSX captura exceções e as grava no log.
12. Após execução/fechamento, liberar o lock do mesmo operador. Se abortar, confirmar documentos e estado do aplicativo antes do handoff.
13. Fazer QA de dimensões, perfil, nomes, contagem, pixels e revisão visual no tamanho real. Reuso sem alteração deve comparar pixels, não somente SHA256 de PNG, pois metadados podem mudar.
14. Para promoção, copiar para novo destino, conferir hashes após cópia e registrar o estado de aprovação. Não salvar por cima do canônico.


## Limite desta documentação

O teste realmente executado foi o R18, com três ofertas em 1920×1080. As etapas acima explicam como o renderer e suas guardas funcionam; a ferramenta prepare_reuse.py foi criada no handoff e testada somente com fixture, sem nova execução Photoshop. Não confundir preparação de pedido com render comprovado.
