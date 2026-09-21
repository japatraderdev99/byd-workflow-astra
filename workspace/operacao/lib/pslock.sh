#!/bin/bash
# pslock.sh — exclusão mútua para o Photoshop.
#
# O Photoshop é instância única e app.activeDocument é global. Dois agentes
# dirigindo o mesmo aplicativo não produzem erro limpo: produzem arte
# corrompida que passa no QA mecânico.
#
# Usa mkdir, que é atômico no sistema de arquivos. Um arquivo comum não é:
# entre "existe?" e "escreve" cabe outro processo.
#
#   operacao/lib/pslock.sh acquire <agente> <job> <script>
#   operacao/lib/pslock.sh status
#   operacao/lib/pslock.sh release <agente>
set -u
source "$(dirname "${BASH_SOURCE[0]}")/mkroot.sh"
LOCK="$MK_ROOT/operacao/.ps.lock"
INFO="$LOCK/owner"

case "${1:-}" in
  acquire)
    agente="${2:?agente}"; job="${3:?job}"; script="${4:?script}"
    if ! mkdir "$LOCK" 2>/dev/null; then
      printf 'RECUSADO — lock já detido:\n' >&2
      [ -f "$INFO" ] && sed 's/^/  /' "$INFO" >&2
      printf '\nLock expirado NÃO é removido automaticamente. Confira o PID,\n' >&2
      printf 'fale com o operador e registre o handoff antes de liberar.\n' >&2
      exit 2
    fi
    { printf 'agente=%s\n' "$agente"; printf 'pid=%s\n' "$$"
      printf 'inicio=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
      printf 'job=%s\n' "$job"; printf 'script=%s\n' "$script"
      printf 'raiz=%s\n' "$MK_ROOT"
      printf 'nonce=%s\n' "$(od -An -N8 -tx1 /dev/urandom | tr -d ' \n')"
    } > "$INFO"
    printf 'ADQUIRIDO por %s — job=%s\n' "$agente" "$job"
    ;;
  status)
    if [ -d "$LOCK" ]; then printf 'OCUPADO\n'; cat "$INFO" 2>/dev/null
      # O PID é do shell que adquiriu, não do trabalho no Photoshop: cada
      # comando do agente é um processo novo. Idade é o sinal confiável.
      ini=$(awk -F= '/^inicio=/{print $2}' "$INFO" 2>/dev/null)
      if [ -n "${ini:-}" ]; then
        # TZ=UTC: o carimbo é gravado em UTC; sem isso date -j assume local.
        t0=$(TZ=UTC date -j -f '%Y-%m-%dT%H:%M:%SZ' "$ini" +%s 2>/dev/null || echo 0)
        if [ "$t0" -gt 0 ]; then
          idade=$(( ($(date -u +%s) - t0) / 60 ))
          printf '\nidade do lock: %s min\n' "$idade"
          [ "$idade" -gt 90 ] && printf 'ATENÇÃO: acima de 90 min. Confirme com o operador\nantes de liberar; nunca libere automaticamente.\n'
        fi
      fi
    else printf 'LIVRE\n'; fi
    ;;
  release)
    agente="${2:?agente}"
    [ -d "$LOCK" ] || { printf 'já estava livre\n'; exit 0; }
    dono=$(awk -F= '/^agente=/{print $2}' "$INFO" 2>/dev/null)
    if [ "$dono" != "$agente" ]; then
      printf 'RECUSADO — lock é de "%s", não de "%s".\n' "$dono" "$agente" >&2; exit 2
    fi
    rm -rf "$LOCK"; printf 'LIBERADO por %s\n' "$agente"
    ;;
  *) printf 'uso: pslock.sh {acquire <agente> <job> <script>|status|release <agente>}\n' >&2; exit 64 ;;
esac
