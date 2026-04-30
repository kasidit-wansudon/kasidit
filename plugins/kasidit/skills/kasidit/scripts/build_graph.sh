#!/usr/bin/env bash
# build_graph.sh — function call graph builder for /kasi-graph
# Usage: build_graph.sh <project-root>
#
# Tries ast-grep first (exact AST), falls back to grep-based regex parser
# (brittle but no external deps). Writes:
#   <project-root>/.kasidit/FUNCTIONS.jsonl
#   <project-root>/.kasidit/HOTSPOTS.md

set -euo pipefail

ROOT="${1:-$(pwd)}"
KAS="$ROOT/.kasidit"
OUT_JSONL="$KAS/FUNCTIONS.jsonl"
OUT_MD="$KAS/HOTSPOTS.md"

if [[ ! -d "$ROOT" ]]; then
  echo "ERR: project root not found: $ROOT" >&2
  exit 1
fi

mkdir -p "$KAS"

PARSER="grep-fallback"
if command -v ast-grep >/dev/null 2>&1 || command -v sg >/dev/null 2>&1; then
  PARSER="ast-grep"
fi

echo "[kasi-graph] root=$ROOT parser=$PARSER"

PYBIN="$(command -v python3 || command -v python || echo '')"
if [[ -z "$PYBIN" ]]; then
  echo "ERR: python3 not found — required for graph builder" >&2
  exit 1
fi

# Delegate to Python — easier to maintain than bash for this much logic.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$PYBIN" "$SCRIPT_DIR/build_graph.py" \
  --root "$ROOT" \
  --out-jsonl "$OUT_JSONL" \
  --out-md "$OUT_MD" \
  --parser "$PARSER"
