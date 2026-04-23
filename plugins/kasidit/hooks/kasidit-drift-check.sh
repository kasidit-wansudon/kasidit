#!/bin/bash
# SessionStart hook — remind user when Centerlite has not been synced in >7 days.
# Never blocks. Fails silently.

set -u

CENTER="${KASIDIT_CENTER_DIR:-$HOME/.claude/skills/kasidit/center}"
LAST_SYNC="$CENTER/.last_sync"
THRESHOLD_DAYS=7

if [[ ! -f "$LAST_SYNC" ]]; then
    # First run — create file silently, no reminder.
    mkdir -p "$CENTER" 2>/dev/null
    date +%s > "$LAST_SYNC" 2>/dev/null
    exit 0
fi

last=$(cat "$LAST_SYNC" 2>/dev/null | tr -d '[:space:]')
now=$(date +%s)

if [[ -z "$last" ]] || ! [[ "$last" =~ ^[0-9]+$ ]]; then
    exit 0
fi

age_days=$(( (now - last) / 86400 ))

if (( age_days >= THRESHOLD_DAYS )); then
    echo "[kasidit] Centerlite last synced ${age_days}d ago. Run /kasi-sync to check drift." >&2
fi

exit 0
