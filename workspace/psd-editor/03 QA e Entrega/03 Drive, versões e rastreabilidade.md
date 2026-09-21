---
type: delivery-standard
status: canonico
---

# Drive, versões e rastreabilidade

## Estrutura de entrega

```text
CLIENTE_ENTREGAVEIS_FINAIS/
├── 01_REFERENCIAS_APROVADAS/
├── 02_REVISAO_INTERNA/
├── 03_QA_MANIFESTO/
└── 04_APENAS_JPGS_FINAIS/
```

A pasta `04_APENAS_JPGS_FINAIS` é a pasta do cliente: deve ter exatamente os JPGs vigentes e nenhum arquivo auxiliar.

## Passos antes de comunicar entrega

1. Copiar JPGs aprovados.
2. Confirmar a quantidade esperada.
3. Garantir que todos os arquivos diretos são `.jpg`.
4. Conferir checksum entre origem e pasta sincronizada.
5. Atualizar prancha e manifesto fora da pasta de envio.
6. Só então informar o caminho/link de entrega.

## Versionamento

- A versão no nome representa mudança real no JPG.
- Sobrescrever apenas a mesma versão quando o arquivo ainda não foi compartilhado como aprovado.
- Depois de uma revisão publicada, gerar `vN+1` e manter o histórico em QA/revisão, não na pasta “apenas JPGs”.
