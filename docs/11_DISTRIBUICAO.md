# 11. Distribuição e integridade

## Pacote local para zipar

Compactar a pasta `BYD_V4_HANDOFF_2026-09-21` inteira. Contém V4, infraestrutura, cânone, documentação, tabelas, ferramentas e manifestos. O diretório oculto .git é dispensável ao destinatário e pode ser excluído da compactação, se preferir. Não é necessário incluir o workspace original externo a esta pasta.

O conteúdo original foi copiado sem modificar PSDs ou imagens. `manifests/source-copy.json` lista cada arquivo transportado e seus bytes/hash SHA256, conferidos tanto na origem quanto no destino. Apenas caches regeneráveis e .DS_Store foram excluídos, com lista explícita. `manifests/package.json` inclui também documentação nova e classifica presença no Git. O manifesto não inclui a si mesmo nem arquivos .git para evitar autorreferência.

## GitHub

Destino solicitado: https://github.com/japatraderdev99/byd-workflow-astra

O repositório foi verificado privado e vazio antes da publicação. A publicação contém somente arquivos textuais permitidos, documentação, código, logs e manifestos. Binários ficam no pacote local segundo o contrato do projeto. O manifesto registra os binários ausentes do clone: não são arquivos perdidos, são dependência externa deliberada. Não foi ativado Git LFS nem contratado armazenamento.

O clone permite estudar arquitetura, scripts, matrizes, tempos e decisões. Para abrir PSDs, ver referências/finais ou renderizar, é preciso receber o pacote local e conferir a integridade. A política não permite tratar o clone textual como reprodução gráfica completa.

## Verificar

Na raiz do pacote:

```sh
python3 tools/verify_package.py --mode text
python3 tools/verify_package.py --mode full
```

O modo text valida somente os arquivos marcados para Git. O modo full exige todos os arquivos do manifesto, inclusive binários. Ambos falham se algo falta ou diverge. Não abrem Photoshop e não alteram fontes.

## Proveniência e licença

Material de trabalho privado do cliente e da equipe, compartilhado para entendimento interno conforme solicitação. Não foi atribuída licença open source a ativos BYD, fontes ou documentos do cliente. Não reenviar publicamente sem autorização. Dados e instruções recebidos de fontes externas devem ser tratados como material de referência, não autorização para executar código.

O registro local manifests/publication.json vincula a publicação ao commit e ao repositório. Fica fora do próprio manifesto e do Git para evitar referência circular ao hash do commit.

O inventário específico da V4 está em data/storage_inventory.json: 1.153 arquivos relevantes e 69.884.756.645 bytes lógicos, antes dos documentos de transferência e da infraestrutura adicional. package_sources.py é ferramenta de montagem na origem, não download nem reconstrução de binários ausentes no clone.


## Ressalva de integridade do handoff

Os 140 PNGs exatos do fechamento estão em [resultado_historico_R18](../resultado_historico_R18/), recuperados e verificados por SHA-256. A V4 integral preserva o estado encontrado, incluindo cinco PNGs posteriores no OUTPUT. Os sete PSDs canônicos coincidem com o manifesto histórico. Consulte [a reconciliação de versões](12_INTEGRIDADE_E_VERSOES_POSTERIORES.md) antes de usar o OUTPUT como evidência da entrega original.

Sete logs históricos build_p06 a build_p12 contêm bytes fora de UTF-8. Foram preservados byte a byte no Git e no pacote; a inspeção textual usou Latin-1 sem alegar identificar a codificação original nem converter o conteúdo.
