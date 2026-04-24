#!/usr/bin/env bash
# kasidit-update-check.sh — SessionStart hook, runs once per UTC day.
#
# Compares local installed version (from plugin.json) against the latest
# GitHub tag via `gh api`. Prints a 1-line notice if newer version exists.
# Silent if up-to-date, offline, gh missing, or already checked today.
#
# Notice shape:
#   [kasidit] update available: v0.9.3 → v0.10.0 — /plugin marketplace update kasidit

set -eu

CENTER="${KASIDIT_CENTER:-$HOME/.claude/skills/kasidit/center}"
STAMP="$CENTER/.last_update_check"
REPO="kasidit-wansudon/kasidit"
PLUGIN_JSON="$HOME/.claude/plugins/marketplaces/kasidit/.claude-plugin/marketplace.json"

mkdir -p "$CENTER" 2>/dev/null || exit 0

# once per UTC day
today=$(date -u +%Y-%m-%d)
if [ -f "$STAMP" ] && [ "$(cat "$STAMP" 2>/dev/null)" = "$today" ]; then
  exit 0
fi

# locally installed version
if [ ! -f "$PLUGIN_JSON" ]; then
  echo "$today" > "$STAMP"
  exit 0
fi
if command -v jq >/dev/null 2>&1; then
  local_ver=$(jq -r '.plugins[] | select(.name=="kasidit") | .version' "$PLUGIN_JSON" 2>/dev/null | head -1) || true
  [ -z "${local_ver:-}" ] && local_ver=$(jq -r '.metadata.version // empty' "$PLUGIN_JSON" 2>/dev/null) || true
fi
if [ -z "${local_ver:-}" ]; then
  local_ver=$(grep -o '"version":[[:space:]]*"[^"]*"' "$PLUGIN_JSON" 2>/dev/null \
    | head -1 | sed -E 's/.*"([^"]+)"$/\1/') || true
fi
[ -z "${local_ver:-}" ] && { echo "$today" > "$STAMP"; exit 0; }

# latest remote tag — gh first, fallback curl
remote_ver=""
if command -v gh >/dev/null 2>&1; then
  remote_ver=$(gh api "repos/$REPO/releases/latest" --jq '.tag_name' 2>/dev/null \
    | sed 's/^v//') || true
fi
if [ -z "$remote_ver" ] && command -v curl >/dev/null 2>&1; then
  remote_ver=$(curl -s -m 3 "https://api.github.com/repos/$REPO/releases/latest" 2>/dev/null \
    | grep -o '"tag_name":[[:space:]]*"[^"]*"' \
    | head -1 | sed -E 's/.*"v?([^"]+)"$/\1/') || true
fi

echo "$today" > "$STAMP"

[ -z "$remote_ver" ] && exit 0
[ "$local_ver" = "$remote_ver" ] && exit 0

# crude semver compare: if sort -V puts local last, local is newer (=up-to-date)
newest=$(printf '%s\n%s\n' "$local_ver" "$remote_ver" | sort -V | tail -1)
[ "$newest" = "$local_ver" ] && exit 0

echo "[kasidit] update available: v$local_ver → v$remote_ver — run: /plugin marketplace update kasidit"
