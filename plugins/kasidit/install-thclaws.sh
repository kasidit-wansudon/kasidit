#!/usr/bin/env bash
# Kasidit installer for thClaws — idempotent, re-runnable.
#
# Installs Kasidit framework files under thClaws's directory layout
# (~/.config/thclaws/) and registers the supported hooks
# (session_start, post_tool_use, session_end).
#
# Hooks NOT supported on thClaws (no equivalent event):
#   - kasi-route.py    (was: UserPromptSubmit)
#   - kasi-log.sh      (was: UserPromptSubmit)
# These run only on Claude Code. thClaws users get the rest of the
# framework — discipline rules, commands, agents, checklists, scripts —
# without runtime prompt routing.
#
# Usage:
#   install-thclaws.sh              # install / update
#   install-thclaws.sh --dry-run    # print plan, no writes
#   install-thclaws.sh --mode=<router|lite|full>
#   install-thclaws.sh --help

set -eu
set -o pipefail

# -------- args --------
DRY_RUN=0
INITIAL_MODE="${KASIDIT_INITIAL_MODE:-router}"
for a in "$@"; do
  case "$a" in
    --dry-run) DRY_RUN=1 ;;
    --mode=*)  INITIAL_MODE="${a#--mode=}" ;;
    --help|-h) sed -n '2,21p' "$0"; exit 0 ;;
    *) echo "unknown arg: $a" >&2; exit 2 ;;
  esac
done
case "$INITIAL_MODE" in
  router|lite|full) ;;
  *) echo "[install-thclaws] ERROR: invalid --mode '$INITIAL_MODE'" >&2; exit 2 ;;
esac

# -------- locate plugin root --------
SCRIPT_PATH="$0"
if command -v realpath >/dev/null 2>&1; then
  SCRIPT_PATH="$(realpath "$0")"
else
  case "$0" in
    /*) SCRIPT_PATH="$0" ;;
    *)  SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")" ;;
  esac
fi
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-${THCLAWS_PLUGIN_ROOT:-$(dirname "$SCRIPT_PATH")}}"

if [ ! -d "$PLUGIN_ROOT/hooks" ]; then
  echo "[install-thclaws] ERROR: $PLUGIN_ROOT/hooks not found." >&2
  exit 1
fi

# -------- targets (thClaws layout) --------
THCLAWS_HOME="${HOME}/.config/thclaws"
HOOKS_DIR="${THCLAWS_HOME}/hooks"
SCRIPTS_DIR="${THCLAWS_HOME}/skills/kasidit/scripts"
SETTINGS="${THCLAWS_HOME}/settings.json"
CENTER="${THCLAWS_HOME}/skills/kasidit/center"
CHECKLISTS="${CENTER}/checklists"
KNOWLEDGE="${CENTER}/knowledge"
LOGS_DIR="${CENTER}/logs"
STAMP_SYNC="${CENTER}/.last_sync"
STAMP_UPD="${CENTER}/.last_update_check"
TS_UTC="$(date -u +%Y%m%dT%H%M%SZ)"
TS_FILE="$(date -u +%Y%m%d%H%M%S)"

log() { printf '[install-thclaws] %s\n' "$*"; }
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

# -------- 0. detect runtime --------
if [ ! -d "$THCLAWS_HOME" ] && [ -d "$HOME/.claude" ]; then
  log "WARN: ~/.config/thclaws not found, but ~/.claude exists."
  log "      You may want to run install.sh (Claude Code) instead."
  log "      Continuing with thClaws install — will create $THCLAWS_HOME"
fi

# -------- 1. dirs --------
log "plugin root: $PLUGIN_ROOT"
log "thclaws home: $THCLAWS_HOME"
run mkdir -p "$HOOKS_DIR" "$CENTER" "$CHECKLISTS" "$KNOWLEDGE" "$LOGS_DIR"

# -------- 2. copy hooks (thClaws-supported events only) --------
log "copying hooks → $HOOKS_DIR"
# Supported on thClaws: session_start, post_tool_use, session_end
# kasi-update-check.sh    → session_start
# kasi-drift-check.sh     → session_start
# kasi-verify.py          → post_tool_use (per-tool, no per-turn aggregation)
# kasi-record.py          → session_end (per-session, not per-turn)
# kasi-route.py           → SKIPPED (no UserPromptSubmit equivalent)
# kasi-log.sh / kasi-log.py → SKIPPED (no UserPromptSubmit equivalent)
THCLAWS_HOOKS="kasi-update-check.sh kasi-drift-check.sh kasi-verify.py kasi-record.py"
for name in $THCLAWS_HOOKS; do
  src="$PLUGIN_ROOT/hooks/$name"
  [ -e "$src" ] || continue
  dst="$HOOKS_DIR/$name"
  if [ -f "$dst" ] && cmp -s "$src" "$dst"; then
    :
  else
    run cp "$src" "$dst"
    HOOKS_COPIED=$((HOOKS_COPIED + 1))
  fi
  run chmod +x "$dst"
  HOOKS_COUNT=$((HOOKS_COUNT + 1))
done
log "hooks copied: $HOOKS_COUNT (thClaws-compatible subset)"
log "skipped (Claude Code only): kasi-route.py, kasi-log.{sh,py}"

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

# -------- 5. seed knowledge templates --------
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

# -------- 5b. seed scripts --------
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
    printf '{"mode":"%s","created":"%s","runtime":"thclaws"}\n' "$INITIAL_MODE" "$TS_UTC" > "$CONFIG_JSON"
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

# -------- 8. settings.json merge (thClaws format) --------
# thClaws hook config: {"hooks": {"event_name": "shell command"}}
# Different from Claude Code's array-of-objects format
if [ "${KASIDIT_SKIP_SETTINGS:-0}" = "1" ]; then
  log "KASIDIT_SKIP_SETTINGS=1 → skipping settings.json merge"
else
  if [ -f "$SETTINGS" ]; then
    BACKUP="${SETTINGS}.kasidit-backup-${TS_FILE}"
    log "backing up settings.json → $BACKUP"
    run cp "$SETTINGS" "$BACKUP"
    if [ "$DRY_RUN" -eq 1 ]; then
      printf '[dry-run] prune old backups (keep 3)\n'
    else
      ls -1t "${SETTINGS}".kasidit-backup-* 2>/dev/null | tail -n +4 | xargs -I{} rm -f {}
    fi
  fi

  if ! command -v python3 >/dev/null 2>&1; then
    log "WARN: python3 not found — cannot merge settings.json."
    log "      install python3, then re-run."
  else
    if [ "$DRY_RUN" -eq 1 ]; then
      printf '[dry-run] register thClaws hooks (session_start, post_tool_use, session_end)\n'
    else
      _PY_OUT="$(python3 - "$SETTINGS" <<'PYEOF'
import json, os, sys

path = sys.argv[1]
home = os.path.expanduser("~")
hooks_dir = f"{home}/.config/thclaws/hooks"

# thClaws supports: pre_tool_use, post_tool_use, post_tool_use_failure,
# permission_denied, session_start, session_end, pre_compact, post_compact.
# We register only the subset Kasidit cares about.
new_hooks = {
    "session_start": (
        f"bash {hooks_dir}/kasi-update-check.sh ; "
        f"bash {hooks_dir}/kasi-drift-check.sh"
    ),
    "post_tool_use": f"python3 {hooks_dir}/kasi-verify.py",
    "session_end":   f"python3 {hooks_dir}/kasi-record.py",
}

try:
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("settings.json root is not an object")
except (FileNotFoundError, ValueError):
    data = {}
except json.JSONDecodeError as e:
    print(f"[install-thclaws] ERROR: settings.json invalid ({e}); aborting merge.", file=sys.stderr)
    sys.exit(3)

hooks = data.setdefault("hooks", {})
added = 0
for evt, cmd in new_hooks.items():
    if hooks.get(evt) != cmd:
        # Preserve any user-existing snippet by chaining with `;`
        if evt in hooks and hooks[evt] and cmd not in hooks[evt]:
            hooks[evt] = f"{hooks[evt]} ; {cmd}"
        else:
            hooks[evt] = cmd
        added += 1

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
print(f"[install-thclaws] settings.json merged; {added} new entries.")
print(f"KASIDIT_ADDED={added}")
PYEOF
      )"
      printf '%s\n' "$_PY_OUT"
      HOOKS_REGISTERED="$(printf '%s\n' "$_PY_OUT" | grep -o 'KASIDIT_ADDED=[0-9]*' | cut -d= -f2 || true)"
      HOOKS_REGISTERED="${HOOKS_REGISTERED:-0}"
    fi
  fi
fi

# -------- final summary --------
NOTE=""
[ "$DRY_RUN" -eq 1 ] && NOTE=" (dry-run — no files written)"

printf '\n'
printf 'Kasidit install summary (thClaws)%s\n' "$NOTE"
printf '%s\n' "-----------------------------------------"
if [ "$CONFIG_CREATED" -eq 1 ]; then CFG_STATE="new"; else CFG_STATE="ok"; fi
printf 'config          %s mode=%s runtime=thclaws (%s)\n' "$CFG_STATE" "$INITIAL_MODE" "$CONFIG_JSON"
HOOKS_UNCHANGED=$((HOOKS_COUNT - HOOKS_COPIED))
printf 'hooks           %d present (copied=%d unchanged=%d) in %s\n' "$HOOKS_COUNT" "$HOOKS_COPIED" "$HOOKS_UNCHANGED" "$HOOKS_DIR"
printf 'registrations   %s wired in %s (session_start, post_tool_use, session_end)\n' "$HOOKS_REGISTERED" "$SETTINGS"
printf 'gravity hub     %s (JSONLx5, checklists=%d seeded, knowledge templates)\n' "$CENTER" "$CHECKLISTS_SEEDED"
printf 'stamps          %s, %s\n' "$STAMP_SYNC" "$STAMP_UPD"
printf '\n'
printf 'NOTE: Kasidit on thClaws runs in degraded mode — kasi-route.py + kasi-log.sh\n'
printf '      have no thClaws hook equivalent (no UserPromptSubmit event). The framework\n'
printf '      still applies via SKILL.md + 21 commands + 8 agents + 15 checklists.\n'
printf '      For full runtime enforcement, use Claude Code.\n'
printf '\n'
printf 'Next: launch thClaws, run /help to see Kasidit commands.\n'
