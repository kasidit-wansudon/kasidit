# Installation

Install the Kasidit plugin for Claude Code, install the global prompt-log hook, and initialize a project.

## 1. Install the plugin

### Via Claude Code marketplace

```
/plugin marketplace add kasidit-wansudon/kasidit
/plugin install kasidit
```

Restart Claude Code (or reload the session). Verify:

```
/kasi-status
```

### Manual clone (for development)

```bash
git clone https://github.com/kasidit-wansudon/kasidit.git ~/path/to/kasidit-marketplace
```

Register as a custom marketplace source in `~/.claude/settings.json` under `extraKnownMarketplaces`.

## 2. Install the prompt-log hook (v0.9.2)

The hook captures every user prompt to `~/.claude/skills/kasidit/center/logs/YYYY-MM-DD.jsonl`. Prompts longer than 200 lines are trimmed to head + tail with a marker.

### Copy the hook scripts

```bash
mkdir -p ~/.claude/hooks ~/.claude/skills/kasidit/center/logs
cp ~/path/to/kasidit-marketplace/plugins/kasidit/hooks/kasidit-log.sh ~/.claude/hooks/
cp ~/path/to/kasidit-marketplace/plugins/kasidit/hooks/kasidit-log.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/kasidit-log.sh ~/.claude/hooks/kasidit-log.py
```

### Register in `~/.claude/settings.json`

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

Expect a JSONL record with `ts`, `session`, `cwd`, `lines`, `chars`, `trimmed`, `prompt`.

### Customize

- **Log location:** export `KASIDIT_LOG_DIR=/path/to/elsewhere` before Claude Code starts
- **Trim thresholds:** edit `MAX_LINES`, `HEAD_LINES`, `TAIL_LINES` in `~/.claude/hooks/kasidit-log.py`

### Opt out

Remove the `UserPromptSubmit` block from `~/.claude/settings.json`.

### Privacy

Logs contain whatever you type, including prompts to multiple models. **Never commit `~/.claude/skills/kasidit/center/logs/`** to any repo.

## 3. Add default allow-list entries (optional but recommended)

To reduce permission prompts during `kasi-*` missions, add to `~/.claude/settings.json` under `permissions.allow`:

```json
"Bash(bash /Users/<you>/.claude/hooks/kasidit-*:*)",
"Read(//Users/<you>/.claude/skills/kasidit/**)",
"Read(//Users/<you>/.claude/plugins/marketplaces/kasidit/**)",
"Read(//**/.kasidit/**)",
"Write(//**/.kasidit/**)",
"Write(//Users/<you>/.claude/skills/kasidit/center/logs/**)",
"Bash(grep:*)",
"Bash(rg:*)",
"Bash(find:*)",
"Bash(git log:*)",
"Bash(git status:*)",
"Bash(git diff:*)",
"Bash(git blame:*)",
"Bash(git show:*)",
"Bash(php -v)",
"Bash(node -v)",
"Bash(python3 --version)",
"Bash(composer show:*)",
"Bash(npm ls:*)",
"Bash(pip show:*)"
```

Replace `<you>` with your user name.

## 4. Initialize a project

In any project directory, run:

```
/kasi-init
```

This chains: `/kasi-scaffold` → `/kasi-pull all-for <stack>` → `/kasi-docs` → `MISSION.md` seed → optional `/kasi-review` → project-level auto-invoke registration.

Skip flags if you want a lighter init:

- `skip docs` — no web fetch
- `skip review` — no light review
- `no auto-invoke` — skip SessionStart hook for this project
- `dry-run` — print plan, do not write files

## 5. (Optional) Push wiki content

If you want the GitHub wiki to reflect `docs/wiki/`:

```
/kasi-wiki-sync apply
```

Requires auth to `github.com/kasidit-wansudon/kasidit.wiki.git`.

## Uninstall

1. `/plugin uninstall kasidit`
2. Remove the `UserPromptSubmit` block from `~/.claude/settings.json`
3. (Optional) `rm -rf ~/.claude/skills/kasidit/center/` to drop Centerlite data
4. (Optional) `rm -rf .kasidit/` in each project to drop per-project data

## Troubleshooting

- **Hook not firing:** check `settings.json` is valid JSON (`python3 -m json.tool ~/.claude/settings.json > /dev/null`).
- **Log file empty:** check `~/.claude/hooks/kasidit-log.sh` is executable and python3 is on PATH.
- **`/kasi-init` refuses:** you may already have a `.kasidit/`; pick merge or skip.
- **Permission prompt for hook:** add the allow-list entries above.

## See also

- [[Getting Started]]
- [[Commands]]
- [[v0.9.2]] — what the hook is for
