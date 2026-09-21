# Reuso dos templates BYD V4

A única via de reuso é `WORK/05_SCRIPTS/render_canonical_v2.jsx`. O teste R18
foi executado em três ofertas de `1920x1080`: o log terminou com 3 PNGs
esperados e 3 exportados em 77320 ms, e
`WORK/04_QA/reuse_validation_r18.json` confirmou pixels idênticos nos três.
Os bytes/SHA-256 dos PNGs diferem por metadados; a comparação de pixels é a
evidência aplicável.

Esse teste prova o caminho de reuso para três ofertas e um formato. Ele não
prova reexportação pixel-idêntica dos 140 PNGs. A visibilidade dos 140 estados
foi provada separadamente pelas 280 aplicações R17/R20 antes de salvar e após
reabrir, uma vez por estado em cada um dos sete formatos.

Scripts `render_canonical.jsx`, pedidos sem sufixo R18 e builds anteriores a R20
são históricos: não são autoridade para Layer Comps nem devem ser executados
para reuso.

## Contrato de solicitação R18

`WORK/00_MATRIZ/render_request_r18.json` foi o clone datado executado no teste;
`render_request.json` original é histórico e permanece preservado. Uma nova
execução exige outro clone datado e destinos novos. O mesmo script aceita de 1
a 20 IDs de oferta únicos e de 1 a 7 templates únicos. O JSX validado aponta
explicitamente para `render_request_r18.json`: copie também o JSX para uma
nova revisão e altere somente a referência de entrada para o novo JSON.
Preserve o pedido R18 e o script executado; valide a nova cópia com
`operacao/lib/check_jsx.sh` antes do lock e da execução.

Cada `offer_id` precisa existir em `production_spec_r18.json`. Cada template
precisa usar um `format` desse spec e o caminho exato indicado por
`output_templates`, no padrão `BYD_TPL_<formato>.psd`. O script confere, antes
de exportar, a dimensão nativa do PSD, RGB8/sRGB, a flag `visibility` da Layer
Comp e exatamente um estado visível em cada ramo `BG`, `VEICULO`, `LEGAL`,
`CONDICIONAIS` e `OFERTA`.

```json
{
  "revision": "r18",
  "output_folder": "WORK/03_STAGING/reuso-novo/",
  "log_file": "WORK/06_LOGS/reuso-novo.log",
  "validation_output": "WORK/04_QA/reuso-novo.json",
  "templates": [
    {
      "format": "1920x1080",
      "path": "WORK/01_TEMPLATES/2026-09-20-r17/BYD_TPL_1920x1080.psd"
    }
  ],
  "offer_ids": ["dolphin-mini-5l-gs"]
}
```

O destino, o log e o alvo de validação precisam ser novos: a recusa de
sobrescrita é deliberada. O log registra `expected_pngs` e `actual_pngs` em
cada formato, no terminal e no erro.

## Execução e validação

Antes do Photoshop: consultar o lock, validar o JSX, adquirir o lock, executar
e liberá-lo. Não compartilhar a instância com outro operador. O manifesto
nativo R18 contém os sete PSDs R17/R20; a exportação não salva alterações no
template. Fazer QA do PNG exportado e, em reuso sem mudança de conteúdo,
comparar os pixels com a fonte canônica.

## Alterar preço, oferta ou incluir outro carro

Criar nova revisão em staging. Confirmar briefing e matriz antes de substituir
conteúdo. IDs de camadas pertencem à versão inventariada; um PSD novo exige
inventário e remapeamento. Preservar os originais e atualizar texto editável,
condicionais e carro apenas nos estados necessários. Conteúdo legal, condições
de venda direta, parcelas, prêmios, ADAS, Super Híbrido, NEW e Últimas Unidades
não devem ser deduzidos do preço em destaque.

## Papéis e custo

Astra decide composição e revisa as saídas. Terra pode preparar inventário,
matriz, contagem, perfil, dimensões, hashes e fichas em escopo fechado. Os
nomes de modelos são alocações solicitadas, não uma comparação demonstrada de
qualidade ou custo. Sem telemetria de cobrança, custo monetário permanece
`null`.
