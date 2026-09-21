# Contrato de operação — MK PSD Flow

Vale para qualquer agente que trabalhe neste workspace. `CLAUDE.md` aponta
para este arquivo; não duplique regra entre os dois, ou eles divergem.

## Divisão de papéis

| Papel | Quem | Escopo |
|---|---|---|
| **Operador** | Codex | Único que abre o Photoshop. Detém o lock, roda piloto e escala. |
| **Organização** | Claude | Inventário frio, matriz, QA, manifesto, Git, revisão de script antes da execução. |

A divisão é **por estado, não por cliente nem por camada**: dividir por
camada colide na pilha `FIXO`/KV; por cliente cria fila desnecessária.

## Antes de tocar no Photoshop

```bash
operacao/lib/pslock.sh status                                  # livre?
operacao/lib/check_jsx.sh <script.jsx>                          # script limpo?
operacao/lib/pslock.sh acquire <agente> <job> <script>          # adquirir
# ... executar ...
operacao/lib/pslock.sh release <agente>                         # liberar
```

O Photoshop é instância única e `app.activeDocument` é global. Dois agentes
no mesmo aplicativo não geram erro limpo — geram arte corrompida que **passa
no QA mecânico**. O lock usa `mkdir`, que é atômico.

Lock vencido **nunca** é removido automaticamente. Confirme com o operador e
registre o handoff.

## Regras invioláveis

1. `Inputs/` é imutável. Produção só em staging datado. Promoção é cópia, nunca overwrite.
2. Nenhuma escala sem escopo fechado em manifesto **e** piloto aprovado por humano naquele formato.
3. PSD editável nunca passa por `flatten`, `mergeVisibleLayers` ou rasterização.
4. Todo script que grava declara `REFUSE_OVERWRITE` e faz preflight de documento aberto.
5. `psd-tools` é autoridade **estrutural** (árvore, nomes, visibilidade, tipos).
   Photoshop é autoridade de **render e geometria final**. Nunca inverta.
6. Exportação declara perfil, extensão e QA explicitamente. `"final"` no nome
   de arquivo **não** é aprovação humana.
7. Binário fora do Git; hash SHA-256 no manifesto dentro.
8. Todo run gera `OK|...` ou `ERRO|motivo`, fecha documentos e preserva o log.
9. Nunca executar `.jsx` histórico direto: copie, parametrize, registre entrada/saída/hash.
10. A pasta do cliente contém somente os entregáveis vigentes — sem prancha, ZIP, PSD ou manifesto.

## Caminhos

Nunca escreva caminho absoluto. A raiz é resolvida pelo marcador `.mkroot`:

- ExtendScript: `operacao/lib/mkroot.jsxinc` → `MK.root()`
- Shell: `source operacao/lib/mkroot.sh` → `$MK_ROOT`
- Python: `from mkroot import ROOT`

O workspace já migrou de `~/Documents` para SSD externo uma vez e quebrou
188 executáveis. O marcador existe para que isso não se repita.

## Scripts históricos: a quebra é proposital

84 dos 88 `.jsx` em `operacao/` ainda apontam para o caminho antigo e **não
foram consertados de propósito**. Nove são destrutivos e 17 gravam sem guarda
de sobrescrita. O caminho morto é a trava que impede que sejam re-armados
contra dados vivos. Conserte um por vez, sob revisão, quando for usá-lo.

Diagnóstico completo: `operacao/2026-09-17_AUDITORIA_SCRIPTS.md`.

## Registros não se reescrevem

`.json`, `.md` e `.tsv` que citam o caminho antigo são **história verdadeira**
do que rodou naquele dia. Reescrevê-los falsifica a rastreabilidade. Corrija
executáveis; preserve registros.
