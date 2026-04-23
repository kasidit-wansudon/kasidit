#!/bin/bash
# UserPromptSubmit hook — capture user prompts to global kasidit log.
# Trims prompts >200 lines to head+tail with [trimmed N lines] marker.
# Never blocks the prompt. All errors swallowed.

set -u

LOG_DIR="${KASIDIT_LOG_DIR:-$HOME/.claude/skills/kasidit/center/logs}"
mkdir -p "$LOG_DIR" 2>/dev/null || exit 0

LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).jsonl"

# Pipe stdin JSON → python; python writes to LOG_FILE.
python3 "$HOME/.claude/hooks/kasidit-log.py" "$LOG_FILE" 2>/dev/null || true
exit 0
