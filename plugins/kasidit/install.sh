#!/usr/bin/env bash
# Kasidit installer — idempotent, re-runnable.
# Copies hooks, merges settings.json, seeds Gravity hub.
#
# Usage:
#   install.sh              # install / update
#   install.sh --dry-run    # print plan, no writes
#   install.sh --mode=<router|lite|full>  # set initial mode (default: router)
#   install.sh --help
#
# Honours:
#   CLAUDE_PLUGIN_ROOT       — set by Claude Code; falls back to script dir.
#   HOME                     — target user home; fake HOME for tests works.
#   KASIDIT_SKIP_SETTINGS=1  — copy hooks but do not touch settings.json.
#   KASIDIT_INITIAL_MODE     — router|lite|full (overridden by --mode flag).

set -eu
set -o pipefail

# -------- args --------
DRY_RUN=0
INITIAL_MODE="${KASIDIT_INITIAL_MODE:-router}"
for a in "$@"; do
  case "$a" in
    --dry-run) DRY_RUN=1 ;;
    --mode=*)  INITIAL_MODE="${a#--mode=}" ;;
    --help|-h)
      sed -n '2,16p' "$0"
      exit 0
      ;;
    *) echo "unknown arg: $a" >&2; exit 2 ;;
  esac
done
case "$INITIAL_MODE" in
  router|lite|full) ;;
  *) echo "[install] ERROR: invalid --mode value '$INITIAL_MODE'. Must be router|lite|full." >&2; exit 2 ;;
esac

# -------- locate plugin root --------
SCRIPT_PATH="$0"
# realpath fallback for macOS default bash
if command -v realpath >/dev/null 2>&1; then
  SCRIPT_PATH="$(realpath "$0")"
else
  # portable-ish
  case "$0" in
    /*) SCRIPT_PATH="$0" ;;
    *)  SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")" ;;
  esac
fi
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$SCRIPT_PATH")}"

if [ ! -d "$PLUGIN_ROOT/hooks" ]; then
  echo "[install] ERROR: $PLUGIN_ROOT/hooks not found." >&2
  echo "[install] Set CLAUDE_PLUGIN_ROOT to the kasidit plugin directory and re-run." >&2
  exit 1
fi

# -------- targets --------
CLAUDE_HOME="${HOME}/.claude"
HOOKS_DIR="${CLAUDE_HOME}/hooks"
SCRIPTS_DIR="${CLAUDE_HOME}/skills/kasidit/scripts"
SETTINGS="${CLAUDE_HOME}/settings.json"
CENTER="${CLAUDE_HOME}/skills/kasidit/center"
CHECKLISTS="${CENTER}/checklists"
KNOWLEDGE="${CENTER}/knowledge"
LOGS_DIR="${CENTER}/logs"
STAMP_SYNC="${CENTER}/.last_sync"
STAMP_UPD="${CENTER}/.last_update_check"
TS_UTC="$(date -u +%Y%m%dT%H%M%SZ)"
TS_FILE="$(date -u +%Y%m%d%H%M%S)"

log() { printf '[install] %s\n' "$*"; }
run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    printf '[dry-run] %s\n' "$*"
  else
    "$@"
  fi
}

# -------- track summary --------
HOOKS_COUNT=0
HOOKS_COPIED=0
HOOKS_REGISTERED=0
CONFIG_CREATED=0
CHECKLISTS_SEEDED=0

# -------- 1. dirs --------
log "plugin root: $PLUGIN_ROOT"
log "claude home: $CLAUDE_HOME"
run mkdir -p "$HOOKS_DIR" "$CENTER" "$CHECKLISTS" "$KNOWLEDGE" "$LOGS_DIR"

# -------- 2. copy hooks --------
log "copying hooks → $HOOKS_DIR"
for f in "$PLUGIN_ROOT"/hooks/kasidit-*.py "$PLUGIN_ROOT"/hooks/kasidit-*.sh; do
  [ -e "$f" ] || continue
  base="$(basename "$f")"
  dst="$HOOKS_DIR/$base"
  # copy only if different (idempotent)
  if [ -f "$dst" ] && cmp -s "$f" "$dst"; then
    :
  else
    run cp "$f" "$dst"
    HOOKS_COPIED=$((HOOKS_COPIED + 1))
  fi
  run chmod +x "$dst"
  HOOKS_COUNT=$((HOOKS_COUNT + 1))
done
log "hooks copied: $HOOKS_COUNT"

# -------- 3. seed Gravity hub JSONL files --------
for jf in route-memory.jsonl patterns.jsonl memory.jsonl rules.jsonl missions.jsonl; do
  if [ ! -e "$CENTER/$jf" ]; then
    run touch "$CENTER/$jf"
  fi
done

# -------- 4. seed default checklists --------
DEFAULTS_CL="$PLUGIN_ROOT/defaults/checklists"
if [ -d "$DEFAULTS_CL" ]; then
  for f in "$DEFAULTS_CL"/*.md; do
    [ -e "$f" ] || continue
    base="$(basename "$f")"
    dst="$CHECKLISTS/$base"
    if [ ! -f "$dst" ]; then
      run cp "$f" "$dst"
      CHECKLISTS_SEEDED=$((CHECKLISTS_SEEDED + 1))
    fi
  done
fi
log "checklists seeded (new): $CHECKLISTS_SEEDED"

# -------- 5. seed knowledge templates (non-destructive) --------
INC="$PLUGIN_ROOT/skills/kasidit/includes"
if [ -d "$INC" ]; then
  for f in "$INC"/patterns-template.md "$INC"/design-system-template.md; do
    [ -e "$f" ] || continue
    base="$(basename "$f")"
    dst="$KNOWLEDGE/$base"
    if [ ! -f "$dst" ]; then
      run cp "$f" "$dst"
    fi
  done
fi

# -------- 5b. seed scripts (build_graph, build_struc) — overwrite OK, source of truth is plugin --------
SCRIPTS_SRC="$PLUGIN_ROOT/skills/kasidit/scripts"
if [ -d "$SCRIPTS_SRC" ]; then
  run mkdir -p "$SCRIPTS_DIR"
  for f in "$SCRIPTS_SRC"/*.sh "$SCRIPTS_SRC"/*.py; do
    [ -e "$f" ] || continue
    base="$(basename "$f")"
    run cp "$f" "$SCRIPTS_DIR/$base"
    run chmod +x "$SCRIPTS_DIR/$base"
  done
fi

# -------- 6. config.json (mode) --------
CONFIG_JSON="$CENTER/config.json"
if [ ! -f "$CONFIG_JSON" ]; then
  if [ "$DRY_RUN" -eq 1 ]; then
    printf '[dry-run] write default config.json (mode=%s)\n' "$INITIAL_MODE"
  else
    printf '{"mode":"%s","created":"%s"}\n' "$INITIAL_MODE" "$TS_UTC" > "$CONFIG_JSON"
  fi
  CONFIG_CREATED=1
fi

# -------- 7. stamps --------
if [ "$DRY_RUN" -eq 1 ]; then
  printf '[dry-run] write %s and %s\n' "$STAMP_SYNC" "$STAMP_UPD"
else
  date -u +%Y-%m-%dT%H:%M:%SZ > "$STAMP_SYNC"
  date -u +%Y-%m-%d > "$STAMP_UPD"
fi

# -------- 8. settings.json merge --------
if [ "${KASIDIT_SKIP_SETTINGS:-0}" = "1" ]; then
  log "KASIDIT_SKIP_SETTINGS=1 → skipping settings.json merge"
else
  if [ -f "$SETTINGS" ]; then
    BACKUP="${SETTINGS}.kasidit-backup-${TS_FILE}"
    log "backing up settings.json → $BACKUP"
    run cp "$SETTINGS" "$BACKUP"
    # keep only 3 most recent backups
    if [ "$DRY_RUN" -eq 1 ]; then
      printf '[dry-run] prune old backups (keep 3)\n'
    else
      ls -1t "${SETTINGS}".kasidit-backup-* 2>/dev/null | tail -n +4 | xargs -I{} rm -f {}
    fi
  fi

  # Prefer jq, fall back to python3
  MERGER=""
  if command -v jq >/dev/null 2>&1; then
    MERGER="jq"
  elif command -v python3 >/dev/null 2>&1; then
    MERGER="python3"
  else
    log "WARN: neither jq nor python3 available — cannot merge settings.json."
    log "      install jq (brew install jq) or python3, then re-run."
    MERGER="none"
  fi
  log "settings merger: $MERGER"

  # Hook registrations to ensure
  # format: EVENT|COMMAND
  ENTRIES="
SessionStart|bash ~/.claude/hooks/kasi-update-check.sh
SessionStart|bash ~/.claude/hooks/kasi-drift-check.sh
UserPromptSubmit|python3 ~/.claude/hooks/kasi-route.py
PostToolUse|python3 ~/.claude/hooks/kasi-verify.py
Stop|python3 ~/.claude/hooks/kasi-verify.py
Stop|python3 ~/.claude/hooks/kasi-record.py
"

  if [ "$MERGER" = "jq" ]; then
    # initialize file if missing
    if [ ! -f "$SETTINGS" ]; then
      if [ "$DRY_RUN" -eq 1 ]; then
        printf '[dry-run] create empty settings.json\n'
      else
        printf '{}\n' > "$SETTINGS"
      fi
    fi
    # validate JSON before touching it
    if [ "$DRY_RUN" -eq 0 ]; then
      jq empty "$SETTINGS" 2>/dev/null || {
        printf '[install] ERROR: settings.json not valid JSON — aborting merge\n' >&2
        exit 3
      }
    fi
    # Use a temp file + while loop in the current shell (not subshell) so
    # HOOKS_REGISTERED updates survive.
    TMPENTRIES="$(mktemp)"
    printf '%s\n' "$ENTRIES" > "$TMPENTRIES"
    while IFS='|' read -r EVT CMD; do
      [ -z "$EVT" ] && continue
      if [ "$DRY_RUN" -eq 1 ]; then
        printf '[dry-run] register %s → %s\n' "$EVT" "$CMD"
      else
        # Skip if already registered (so counter reflects truly-new adds).
        if jq -e --arg evt "$EVT" --arg cmd "$CMD" \
             '([.hooks[$evt][]?.hooks[]?.command] | index($cmd)) != null' \
             "$SETTINGS" >/dev/null 2>&1; then
          :
        else
          TMP="$(mktemp)"
          jq --arg evt "$EVT" --arg cmd "$CMD" '
            .hooks = (.hooks // {}) |
            .hooks[$evt] = (.hooks[$evt] // []) |
            .hooks[$evt] += [{"hooks":[{"type":"command","command":$cmd}]}]
          ' "$SETTINGS" > "$TMP" && mv "$TMP" "$SETTINGS"
          HOOKS_REGISTERED=$((HOOKS_REGISTERED + 1))
        fi
      fi
    done < "$TMPENTRIES"
    rm -f "$TMPENTRIES"
  elif [ "$MERGER" = "python3" ]; then
    if [ "$DRY_RUN" -eq 1 ]; then
      echo "$ENTRIES" | while IFS='|' read -r EVT CMD; do
        [ -z "$EVT" ] && continue
        printf '[dry-run] register %s → %s\n' "$EVT" "$CMD"
      done
    else
      _PY_OUT="$(python3 - "$SETTINGS" <<'PYEOF'
import json, os, sys
path = sys.argv[1]
entries = [
    ("SessionStart", "bash ~/.claude/hooks/kasi-update-check.sh"),
    ("SessionStart", "bash ~/.claude/hooks/kasi-drift-check.sh"),
    ("UserPromptSubmit", "python3 ~/.claude/hooks/kasi-route.py"),
    ("PostToolUse", "python3 ~/.claude/hooks/kasi-verify.py"),
    ("Stop", "python3 ~/.claude/hooks/kasi-verify.py"),
    ("Stop", "python3 ~/.claude/hooks/kasi-record.py"),
]
try:
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("settings.json root is not an object")
except (FileNotFoundError, ValueError):
    data = {}
except json.JSONDecodeError as e:
    print(f"[install] ERROR: settings.json not valid JSON ({e}). Aborting merge.", file=sys.stderr)
    sys.exit(3)

hooks = data.setdefault("hooks", {})
added = 0
for evt, cmd in entries:
    arr = hooks.setdefault(evt, [])
    already = False
    for item in arr:
        for h in (item.get("hooks") or []):
            if h.get("command") == cmd:
                already = True
                break
        if already:
            break
    if not already:
        arr.append({"hooks": [{"type": "command", "command": cmd}]})
        added += 1

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
print(f"[install] settings.json merged; {added} new entries.")
print(f"KASIDIT_ADDED={added}")
PYEOF
      )"
      printf '%s\n' "$_PY_OUT"
      HOOKS_REGISTERED="$(printf '%s\n' "$_PY_OUT" | grep -o 'KASIDIT_ADDED=[0-9]*' | cut -d= -f2 || true)"
      HOOKS_REGISTERED="${HOOKS_REGISTERED:-0}"
      HOOKS_REGISTERED="${HOOKS_REGISTERED:-0}"
    fi
  fi
fi

# -------- final summary --------
NOTE=""
[ "$DRY_RUN" -eq 1 ] && NOTE=" (dry-run — no files written)"

printf '\n'
printf 'Kasidit install summary%s\n' "$NOTE"
printf '%s\n' "-----------------------------------------"
if [ "$CONFIG_CREATED" -eq 1 ]; then CFG_STATE="new"; else CFG_STATE="ok"; fi
printf 'config          %s mode=%s (%s)\n' "$CFG_STATE" "$INITIAL_MODE" "$CONFIG_JSON"
HOOKS_UNCHANGED=$((HOOKS_COUNT - HOOKS_COPIED))
printf 'hooks           %d present (copied=%d unchanged=%d) in %s\n' "$HOOKS_COUNT" "$HOOKS_COPIED" "$HOOKS_UNCHANGED" "$HOOKS_DIR"
printf 'registrations   %d wired in %s (SessionStart x2, UserPromptSubmit, PostToolUse, Stop x2)\n' "$HOOKS_REGISTERED" "$SETTINGS"
printf 'gravity hub     %s (JSONLx5, checklists=%d seeded, knowledge templates)\n' "$CENTER" "$CHECKLISTS_SEEDED"
printf 'stamps          %s, %s\n' "$STAMP_SYNC" "$STAMP_UPD"
printf '\n'
printf 'Next: run /kasi-scaffold in a project, or state a mission.\n'
