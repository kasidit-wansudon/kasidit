---
description: Initialize Kasidit on first install — 1-question prompt, scaffold, wire hooks, seed Gravity hub. One-shot.
---

One-shot bootstrap. Runs once per machine (global) and once per project (local). Wires everything so subsequent sessions work out of the box.

**Chain executed (in order):**

1. **First-run question** (skip if `~/.claude/skills/kasidit/center/config.json` already exists):
   ```
   Q. Kasidit default mode? Type 1, 2, or 3 (default: 1)
     1. router    — thin classifier, ~20 line load. Routes each message. (recommended)
     2. lite      — always Rule 1 + Rule 11. Light discipline baseline.
     3. full      — always full framework. Audit / refactor / security projects.
   ```
   Save to `~/.claude/skills/kasidit/center/config.json`. `1 → router`, `2 → lite`, `3 → full`. If the user replies with anything that is not 1/2/3 (blank, word, etc.), treat as `1`. `ultra` opt-in only via `/kasi ultra`.

2. **Run the installer** (user-scope, one-time per machine — idempotent, re-runnable):
   ```
   bash "$CLAUDE_PLUGIN_ROOT/install.sh"
   ```
   If `CLAUDE_PLUGIN_ROOT` is not exported (manual invocation), pass the plugin path directly:
   ```
   bash ~/.claude/plugins/marketplaces/kasidit-wansudon/plugins/kasidit/install.sh
   ```
   Use `--dry-run` first if you want to preview. The installer:
   - copies `hooks/kasidit-*.{py,sh}` → `~/.claude/hooks/` (chmod +x),
   - seeds `~/.claude/skills/kasidit/center/` (5 JSONL + checklists + knowledge templates),
   - writes `.last_sync` + `.last_update_check` stamps.

   Verify the printed summary matches the "After init, report" block below. If the row `hooks` shows 0 scripts or the `gravity hub` row lists 0 checklists, abort and investigate before proceeding.

3. **Settings wiring** is performed by `install.sh` step 2:
   - Backs up `~/.claude/settings.json` → `settings.json.kasidit-backup-<YYYYMMDDHHMMSS>` before touching it.
   - Merges 6 hook registrations into `SessionStart` / `UserPromptSubmit` / `PostToolUse` / `Stop` arrays.
   - Skips any entry whose exact `command` string already exists (no double-registration).
   - Uses `jq` when available; falls back to `python3` stdlib. If neither present, the installer prints a warning and leaves `settings.json` untouched — install `jq` and re-run.

   Target shape after merge:
   ```json
   {
     "hooks": {
       "SessionStart": [
         {"hooks": [{"type": "command", "command": "bash ~/.claude/hooks/kasidit-update-check.sh"}]},
         {"hooks": [{"type": "command", "command": "bash ~/.claude/hooks/kasidit-drift-check.sh"}]}
       ],
       "UserPromptSubmit": [
         {"hooks": [{"type": "command", "command": "python3 ~/.claude/hooks/kasidit-route.py"}]}
       ],
       "PostToolUse": [
         {"hooks": [{"type": "command", "command": "python3 ~/.claude/hooks/kasidit-verify.py"}]}
       ],
       "Stop": [
         {"hooks": [{"type": "command", "command": "python3 ~/.claude/hooks/kasidit-verify.py"}]},
         {"hooks": [{"type": "command", "command": "python3 ~/.claude/hooks/kasidit-record.py"}]}
       ]
     }
   }
   ```
   To skip settings edits (hooks-only install for debugging), export `KASIDIT_SKIP_SETTINGS=1` before running `install.sh`.

4. **Verify Gravity hub** (`~/.claude/skills/kasidit/center/`) — the installer in step 2 already:
   - created `logs/`, `checklists/`, `knowledge/`,
   - touched empty JSONL: `route-memory.jsonl`, `patterns.jsonl`, `memory.jsonl`, `rules.jsonl`, `missions.jsonl`,
   - wrote `.last_sync` + `.last_update_check` stamps,
   - copied starter checklists from `$CLAUDE_PLUGIN_ROOT/defaults/checklists/*.md` → `center/checklists/`,
   - copied pattern + design-system templates from `$CLAUDE_PLUGIN_ROOT/skills/kasidit/includes/` → `center/knowledge/`.

   This step is a non-destructive check: confirm all 5 JSONL files and at least one checklist exist. If any are missing, re-run `install.sh` (idempotent).

5. **Prompt log opt-in** — ask once:
   ```
   Enable global prompt log? Logs every prompt to center/logs/ for /kasi-search. Contains PII. (y/N)
   ```
   Default N. If y → append `export KASIDIT_LOG_ENABLED=1` to shell rc.

6. **`/kasi-scaffold`** — build `.kasidit/` structure in current project.

7. **Gravity pull** — if `center/checklists/` has items matching detected stack → seed `.kasidit/CHECKLISTS/` + `.kasidit/knowledge/`. One batch confirm.

8. **`/kasi-docs`** — fetch version-matched official docs for detected stack. Cache to `.kasidit/knowledge/`.

9. Create `.kasidit/MISSION.md` — blank template.

10. Create `.kasidit/config.json` — project-level mode override (empty by default, inherits global).

11. **`.gitignore` privacy guard**:
    ```
    .kasidit/knowledge/*.private.md
    .kasidit/config.json
    # Do NOT commit ~/.claude/skills/kasidit/center/logs/ anywhere — contains prompts.
    ```
    Append if not already present. Create `.gitignore` if missing.

12. Append to project `CLAUDE.md` (create if missing):
    ```md
    ## Kasidit

    Framework active. Router mode default — auto-classifies each message.
    Heavy missions → `/kasi-*` commands. Mode override → `/kasi full` this session.
    See `.kasidit/INDEX.md` for project knowledge map.
    ```

**Flow rules:**

- Confirm each step with the user before running — `/kasi-init` is multi-command.
- If `.kasidit/` already exists → ask: (1) skip scaffold, (2) merge non-destructively, (3) abort.
- If `~/.claude/settings.json` hooks already registered → detect + skip step 3 with `[exists]` note.
- Detect stack from `composer.json` / `package.json` / `requirements.txt` / `go.mod` / `Cargo.toml`. If ambiguous → ask.
- Tier = current session tier. On Haiku → skip step 6 review unless user insists.

**After init, report:**

```
config          new   mode=router (~/.claude/skills/kasidit/center/config.json)
hooks           7 script(s) in ~/.claude/hooks/  (present=copied+unchanged)
registrations   6 wired in ~/.claude/settings.json  (SessionStart x2, UserPromptSubmit, PostToolUse, Stop x2)
gravity hub     ~/.claude/skills/kasidit/center/  (JSONLx5, 12 checklists, knowledge templates)
stamps          .last_sync, .last_update_check
.kasidit/       INDEX/RELATIONS/MEMORY/PATTERNS + CHECKLISTS/ + knowledge/  (from /kasi-scaffold, step 6)
log hook        off   (enable with: export KASIDIT_LOG_ENABLED=1 — requires manual settings.json edit, not yet wired automatically)
.gitignore      privacy guard appended  (step 11)

Next: state a mission, or run /kasi-review <module>
```

**Anti-patterns:**

- ❌ Silent overwrite of `~/.claude/settings.json`.
- ❌ Silent overwrite of existing `.kasidit/`.
- ❌ Registering hooks twice (check each hook array for existing entry before push).
- ❌ Injecting auto-invoke into shared / production repos without asking.
- ❌ Skipping stack detection and assuming Laravel / React / whatever.

**User commands during init:**

- `skip docs` — omit step 8.
- `skip scaffold` — omit step 6 (hooks + hub only).
- `skip hooks` — omit step 2+3 (skill-only install, advanced).
- `dry-run` — print plan, do not write files.
- `reinstall` — run full chain even if `center/config.json` exists.
