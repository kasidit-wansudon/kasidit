# Kasidit Hooks

Hook scripts bundled with the plugin. Claude Code does not auto-register them from the plugin repo; they have to be copied to `~/.claude/hooks/` and referenced from `~/.claude/settings.json`.

## Canonical install (preferred)

Use the bundled installer at the plugin root:

```bash
bash "$CLAUDE_PLUGIN_ROOT/install.sh"          # normal
bash "$CLAUDE_PLUGIN_ROOT/install.sh" --dry-run # preview only
```

If `CLAUDE_PLUGIN_ROOT` is not set (e.g. you are running from a shell outside Claude Code), invoke the script directly:

```bash
bash ~/.claude/plugins/marketplaces/kasidit-wansudon/plugins/kasidit/install.sh
```

`install.sh`:

- copies every `kasidit-*.{py,sh}` in this directory to `~/.claude/hooks/` (chmod +x),
- backs up `~/.claude/settings.json` to `settings.json.kasidit-backup-<ts>` before editing,
- merges hook registrations idempotently (re-run is safe; duplicate commands are skipped),
- seeds the Gravity hub under `~/.claude/skills/kasidit/center/` (JSONL files, checklists, knowledge templates),
- writes `.last_sync` and `.last_update_check` stamps.

Flags / env:

- `--dry-run` — print the plan, touch nothing.
- `KASIDIT_SKIP_SETTINGS=1` — copy hooks but do not modify `settings.json`.

Requires `jq` or `python3` for the settings merge. macOS ships `python3` via the Command Line Tools; `jq` is optional (`brew install jq`).

## Manual install (debug / skip-automation fallback)

If `install.sh` cannot run (e.g. locked-down environment, auditing every step) use the manual procedure below. This is the same work the installer does, but as discrete commands.

### `kasidit-log.sh` + `kasidit-log.py`

Captures every user prompt to `~/.claude/skills/kasidit/center/logs/YYYY-MM-DD.jsonl`. Trims prompts > 200 lines to head (40) + tail (20) + `[trimmed N lines] ...` marker.

```bash
mkdir -p ~/.claude/hooks ~/.claude/skills/kasidit/center/logs
cp kasidit-log.sh kasidit-log.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/kasidit-log.sh ~/.claude/hooks/kasidit-log.py
```

### Register manually (edit `~/.claude/settings.json`)

Add under the `hooks` object:

```json
"UserPromptSubmit": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "bash /Users/<you>/.claude/hooks/kasidit-log.sh"
      }
    ]
  }
]
```

### Verify

```bash
echo '{"prompt":"hi","session_id":"x","cwd":"/tmp"}' | bash ~/.claude/hooks/kasidit-log.sh
ls ~/.claude/skills/kasidit/center/logs/
tail -1 ~/.claude/skills/kasidit/center/logs/*.jsonl
```

### Customize

- **Log location:** export `KASIDIT_LOG_DIR=/path/to/elsewhere` before Claude Code starts.
- **Trim threshold:** edit `MAX_LINES`, `HEAD_LINES`, `TAIL_LINES` in `kasidit-log.py`.
- **Opt out:** remove the `UserPromptSubmit` block from `settings.json`.

### Privacy note

Logs contain whatever the user typed. Do **not** commit `~/.claude/skills/kasidit/center/logs/`. Add to `.gitignore` or keep outside version control entirely.
