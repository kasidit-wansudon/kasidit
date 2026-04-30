#!/usr/bin/env bash
# build_struc.sh — project structure index for /kasi-struc
# Usage: build_struc.sh <project-root> [build|refresh]
#
# Writes .kasidit/STATE/{structure.json,modules.jsonl,routes.jsonl,config.json,last_sync}
# Appends to .kasidit/STATE/changelog.jsonl on refresh.

set -euo pipefail

ROOT="${1:-$(pwd)}"
MODE="${2:-build}"

if [[ ! -d "$ROOT" ]]; then
  echo "ERR: project root not found: $ROOT" >&2
  exit 1
fi

PYBIN="$(command -v python3 || command -v python || echo '')"
if [[ -z "$PYBIN" ]]; then
  echo "ERR: python3 not found — required for struc builder" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$PYBIN" "$SCRIPT_DIR/build_struc.py" --root "$ROOT" --mode "$MODE"
