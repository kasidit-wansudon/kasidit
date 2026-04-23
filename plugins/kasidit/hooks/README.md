# Kasidit Hooks

Hook scripts bundled with the plugin. They are **reference copies**; Claude Code does not auto-register them from the plugin. Install at user scope.

## `kasidit-log.sh` + `kasidit-log.py`

Captures every user prompt to `~/.claude/skills/kasidit/center/logs/YYYY-MM-DD.jsonl`. Trims prompts > 200 lines to head (40) + tail (20) + `[trimmed N lines] ...` marker.

### Install

```bash
mkdir -p ~/.claude/hooks ~/.claude/skills/kasidit/logs
cp kasidit-log.sh kasidit-log.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/kasidit-log.sh ~/.claude/hooks/kasidit-log.py
```

### Register (edit `~/.claude/settings.json`)

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
