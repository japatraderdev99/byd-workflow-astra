# Auditoria fria de preparação — BYD V4

`REFUSE_OVERWRITE`: este relatório foi criado em 2026-09-19; uma nova
auditoria deve usar outro nome ou revisão, nunca reescrever este registro.

## Escopo e evidência

- Início real da leitura: `2026-09-19T12:48:12-03:00`.
- Fim da leitura e consolidação: `2026-09-19T12:50:03-03:00`.
- Leitura restrita a `Projects/BYD/Jobs/V4/`, `operacao/lib/` e aos trechos
  permitidos do cânone. Não houve Photoshop, UI, execução de JSX nem alteração
  de artefato existente.
- Artefatos auditados: briefing, padrão de template, critérios, matriz
  estrutural, `pilot_spec_p01.json`, `build_p01.jsx`, logs do P01 e inventário
  estrutural. `check_jsx.sh` retornou `OK`; isso valida as guardas estáticas,
  não a semântica visual nem a execução no Photoshop.
- Modelo solicitado no job: `gpt-5.6-terra/high`. O campo da matriz e o
  `DIARIO.md` registram `gpt-6-astra / inherited-default`; esta auditoria não
  mediu runtime de modelo e não trata esse registro prévio como medição nova.

## Achados que bloqueiam piloto fiel ou escala

1. **F2 incompleto por especificação.** `pilot_spec_p01.json` contém apenas
   `1920x276`. Com três ofertas, `build_p01.jsx` só pode gerar 3 PNGs e 1 PSD;
   o portão exige 21 PNGs e piloto nos 7 formatos. Completar as seis zonas e
   regras de cada formato antes de chamar P01 de piloto do run.

2. **A matriz não é ainda fonte de verdade para a escala.** As 20 ofertas
   estão em `CANDIDATE_REQUIRES_REFERENCE_VALIDATION`; a própria matriz proíbe
   ativar grupos a partir dela. Validar contra cada PNG feed e gravar a fonte
   escolhida por `offer_id`, inclusive conteúdo, carro e condicionais, antes
   de produzir uma matriz consumível por F3.

3. **Exceções estruturais precisam ficar fechadas na matriz.**
   `vd-shark` possui dois grupos candidatos: ID `2986` (`PR - SHARK`) e ID
   `493` (`SHARK`). O operador informou por handoff que a referência aprovada
   mostra R$299.990 / Produtor Rural, consistente com ID `2986`; registrar essa
   decisão e a evidência. `vd-song-pro-flex` (grupo ID `611`) não tem
   `car_cutout_candidates`, portanto a fonte de seu veículo permanece bloqueio
   explícito de escala.

4. **P01 ainda não seleciona uma cena de veículo por oferta.** A spec aponta
   para grupos `CARRO`/`carro` (IDs `233`, `21`, `2954`), não para um recorte
   aprovado. Seus filhos candidatos são múltiplos e localmente visíveis. A
   cópia do grupo pode transportar vistas, sombras ou detalhes concorrentes.
   Registrar para cada oferta o grupo/camada final, sombra e estado de
   visibilidade, depois validar a renderização do piloto.

5. **Omissão/ativação do Dolphin Mini não está aprovada.** O script duplica e
   oculta o grupo `DETALHE` ID `32`, logando `OMISSAO_PROPOSTA`; o inventário o
   identifica como `DOLPHIN MINI 5L GS / DOLPHIN MINI / DETALHE`. Ao mesmo
   tempo ativa a parcela ID `61` (raw=false) e o grupo de selos ID `67`.
   Confirmar os três contra a referência e declarar a decisão por formato no
   portão humano.

6. **Condicionais não estão modelados como regras completas.** P01 não duplica
   `New` ID `2951` de `vd-atto-2`; se a referência VD o mostrar, é omissão.
   Para escala, a matriz deve declarar os `New` observados: IDs `1378`
   (`atto-2`), `1365` (`sealion-26-27`) e `3210` (`song-pro-flex`), além dos
   selos e blocos de Venda Direta. A confirmação visual dessas três tags veio
   do handoff do operador, não desta leitura estrutural.

7. **A regra de layout não prova legibilidade nem não-colisão.** `fit()` só
   reduz e posiciona o limite de camada; o script não mede bounds finais de
   título/preço/legal, respiro, sobreposição ou mínimo de caixa-alta. Também
   remove quebras de linha de benefício/headline. Declarar mínimos, âncoras,
   regra de estouro e QA a 100% por formato, especialmente 1920x276 e 360x80.

8. **Tipografia ainda exige preflight humano/técnico.** O inventário de
   StyleRuns observou `SourceSansPro-*` e `ArialMT`; o pacote recebido contém
   MüllerNext. Não houve evidência de disponibilidade das fontes do PSD no
   Photoshop. Antes do piloto, verificar a fonte efetivamente aplicada e
   registrar qualquer ausência, sem substituição aproximada.

9. **O export não contém prova técnica da saída.** O documento nasce RGB 8-bit
   com perfil sRGB, mas P01 não faz QA pós-export de perfil embutido, opacidade,
   dimensões, abertura ou SHA-256. `PNGSaveOptions` e uma camada de fundo não
   substituem essas verificações. Prever manifesto e checagens por PNG antes de
   considerar F2 concluída.

10. **P01 falhou antes de qualquer artefato.** `WORK/06_LOGS/build_p01.log`
    registra `ERRO|Argumento Ilegal|line=11`, no `duplicate(...,
    PLACEATBEGINNING)`/movimentação. Não há piloto renderizado a aprovar.
    Preservar P01 e sua proveniência; a revisão P02 deve ter nome, hash,
    preflight e log próprios, sem sobrescrita.

## Condição para avançar

O próximo piloto só fica apto a revisão humana quando houver uma matriz
aprovada pela referência para as três ofertas de estresse, uma spec com as
sete famílias, seleção explícita de carro/condicionais, fonte disponível e
21 PNGs com QA técnico e visual registrado. Isso não autoriza F3: a escala
continua condicionada ao `APROVADO` humano do portão F2.
