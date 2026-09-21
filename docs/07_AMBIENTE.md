# 7. Ambiente e portabilidade

## Dependências e limites conhecidos

- macOS e Adobe Photoshop desktop, com ExtendScript e exportação PNG. A versão exata do Photoshop do run não foi consolidada em um lockfile reproduzível; validar no computador de destino.
- Python 3, psd-tools **1.19.0** registrado no intake; Pillow usado no QA. A versão histórica de Pillow e a versão exata de Python não estão provadas pelo relatório. Não usar versões atuais como se fossem histórico.
- Node.js para `node --check` em check_jsx.sh; Bash e utilitários macOS para lock, caminhos e hashes.
- Fontes recebidas em INPUT/05_FONTES; conferir disponibilidade e licenciamento no destino. Não substituí-las silenciosamente.
- Perfil sRGB IEC61966-2.1, documento RGB de 8 bits. PSDs finais somam 10,34 GB; reservar espaço para cópia, staging e scratch do Photoshop. O pacote completo ocupa cerca de 70 GB decimais, antes de compactar.

## Resolução de caminhos

A raiz operacional é `workspace/`, identificada por `.mkroot`. Os scripts ExtendScript incluem `operacao/lib/mkroot.jsxinc` por caminho relativo. Python usa mkroot.py; quando necessário, na raiz operacional: `PYTHONPATH=operacao/lib python3 <script>`. Não executar essa forma em scripts históricos de gravação sem cloná-los e revisar destinos.

Registros com caminhos antigos são história; foram preservados. Nem todo script histórico é portátil: cada um deve ser classificado antes do uso. O renderer canônico usa MK.root; a ferramenta nova `prepare_reuse.py` cria pedido e cópia de JSX com novos destinos, sem abrir Photoshop. Não resolve a aprovação ou o lock por você.

## Lock em cópias do workspace

O mecanismo original usa `mkdir` atômico dentro de cada raiz. Duas cópias possuem locks independentes e podem competir pela mesma instância global do Photoshop. Nesta transferência, escolha uma única cópia operacional por computador e encerre o outro operador antes de executar. Uma futura padronização pode migrar o mutex para escopo de máquina; isso não foi alterado nos arquivos históricos.

## O que não foi transportado

Sessões brutas de agentes, raciocínio privado, chaves de API, cookies, arquivos .env, backups D1 com usuários, caches Python e metadados Finder. A medição de uso foi transportada em sua forma sanitizada já existente. O extrator histórico aponta para fontes de sessão que não acompanham o pacote; o JSON de resultados e suas fórmulas permitem inspecionar a auditoria, mas refazer a extração requer acesso autorizado à telemetria original.

## Skills recuperadas da execução

Os snapshots de quatro skills em evidence/skills/ foram comparados integralmente com as saídas históricas das leituras, conforme data/skill_reads.json. As versões de diretório observadas foram Computer Use 1.0.1001103, Browser 26.915.31945 e PDF 26.909.61513; openai-docs veio de .system, sem versão de pacote exposta no caminho. Isso documenta a configuração lida, não transporta o runtime de ferramentas/plugins nem garante sua disponibilidade em outro ambiente.

Datas de modificação das cópias não são tempos de execução. Os timestamps de logs, eventos e manifests são as fontes para a cronologia.

## Tipografia realmente referenciada

O inventário tipografia_psd_origem.json registra 151 camadas de texto e style runs com ArialMT, SourceSansPro-Black, SourceSansPro-BoldIt, SourceSansPro-Regular e SourceSansPro-Semibold. Já INPUT/05_FONTES contém arquivos MullerNext Trial. **O conteúdo da pasta de fontes não equivale à lista de fontes usada pelo PSD.** Para compreender/reproduzir o case, consultar os style runs; FontSet também pode listar fallbacks não usados. A transferência preserva os arquivos recebidos e não afirma que eles bastam para instalar todas as fontes necessárias. Fontes do ambiente fora do INPUT não foram redistribuídas como se fossem insumos recebidos.

A infraestrutura operacao/lib e o cânone psd-editor foram copiados do workspace na data do handoff. Os hashes registram esse snapshot; sem um lockfile histórico não se deve afirmar que cada dependência do ambiente permaneceu byte a byte igual desde 19/09. Os scripts e logs da própria V4 foram preservados com suas revisões, e as quatro skills tiveram correspondência textual histórica confirmada separadamente.
