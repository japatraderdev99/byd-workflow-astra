#!/bin/bash
# check_jsx.sh — verificação fria de ExtendScript antes da execução.
#
# Papel: o agente de organização roda isto ANTES de o operador abrir o
# Photoshop. Pega erro de sintaxe, caminho quebrado e operação destrutiva
# sem custar um round-trip de aplicativo.
#
#   operacao/lib/check_jsx.sh <arquivo.jsx> [mais.jsx ...]
#   operacao/lib/check_jsx.sh operacao/2026-09-17/photoshop/*.jsx
set -u
source "$(dirname "${BASH_SOURCE[0]}")/mkroot.sh"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
fail=0; total=0

for src in "$@"; do
  total=$((total + 1)); name="$(basename "$src")"; problems=()

  # 1. Sintaxe. Diretivas ExtendScript (#target, #include) não são JS.
  sed -E 's/^[[:space:]]*#(target|include|includepath|strict|script).*$//' "$src" > "$TMP/c.js"
  node --check "$TMP/c.js" 2>"$TMP/e" || problems+=("SINTAXE: $(grep -m1 -E '^[A-Za-z]*Error' "$TMP/e")")

  # 2. Caminho absoluto fora da raiz atual: quebra silenciosa após migração.
  if grep -qE "'/(Users|Volumes)/" "$src"; then
    grep -oE "'/(Users|Volumes)/[^']*'" "$src" | sort -u | head -3 | while read -r p; do
      case "$p" in *"$MK_ROOT"*) ;; *) echo "    caminho externo: $p" ;; esac
    done | grep -q . && problems+=("CAMINHO: absoluto fora da raiz (use o marcador .mkroot)")
  fi

  # 3. Operações que destroem editabilidade. O cânone proíbe em PSD entregável.
  for op in 'flatten()' 'mergeVisibleLayers' 'rasterize'; do
    grep -q "$op" "$src" && problems+=("DESTRUTIVO: $op — confirme que a saída não é PSD editável")
  done

  # 4. Guarda de sobrescrita. Todo script que grava deve recusar overwrite.
  if grep -qE 'saveAs|exportDocument' "$src" && ! grep -q 'REFUSE_OVERWRITE' "$src"; then
    problems+=("SEM GUARDA: grava sem REFUSE_OVERWRITE")
  fi

  # 5. Preflight de documento aberto. Grava sem preflight = bloqueio;
  #    só leitura sem preflight = aviso (app.activeDocument é global).
  if ! grep -q 'app.documents.length' "$src"; then
    if grep -qE 'saveAs|exportDocument' "$src"; then
      problems+=("BLOQUEIO — SEM PREFLIGHT: grava com documento possivelmente aberto")
    else
      problems+=("aviso — sem preflight: leitura com documento aberto é tolerável, não ideal")
    fi
  fi

  if [ ${#problems[@]} -eq 0 ]; then
    printf 'OK    %s\n' "$name"
  else
    fail=$((fail + 1)); printf 'AVISO %s\n' "$name"
    for p in "${problems[@]}"; do printf '        %s\n' "$p"; done
  fi
done

printf '\n%s script(s) verificado(s), %s com apontamentos.\n' "$total" "$fail"
[ "$fail" -eq 0 ]
