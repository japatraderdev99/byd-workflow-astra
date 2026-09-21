#!/bin/bash
# mkroot.sh — resolução de raiz para shell.
#   source "$(dirname "${BASH_SOURCE[0]}")/../lib/mkroot.sh"
#   echo "$MK_ROOT"
mk_root() {
  local dir; dir="$(cd "$(dirname "${BASH_SOURCE[1]:-$0}")" && pwd)"
  while [ "$dir" != "/" ]; do
    [ -f "$dir/.mkroot" ] && { printf '%s\n' "$dir"; return 0; }
    dir="$(dirname "$dir")"
  done
  printf 'MKROOT_NOT_FOUND\n' >&2; return 1
}
MK_ROOT="$(mk_root)" || exit 1
export MK_ROOT
