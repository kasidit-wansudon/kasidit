# Backend Hooks (v0.10)

> Runtime-enforced layer. 5 scripts wired into Claude Code's event system via `install.sh`. Stdlib-only — no extra dependencies.

Until v0.10 Kasidit was 100% prompt convention — the framework lived in `SKILL.md` and depended on the AI reading and obeying it. v0.10 adds a **real backend** that runs outside the LLM context: Python/bash scripts that fire on Claude Code events and can inject context, detect violations, and persist memory without the AI's cooperation.

## The 5 hooks

Located at `plugins/kasidit/hooks/` in the repo; installed to `~/.claude/hooks/` by `install.sh`.

| Hook | Claude Code event | Purpose | Enforced? |
|---|---|---|---|
| `kasidit-route.py` | `UserPromptSubmit` | Classify prompt, query route-memory, inject 1-line recommendation | ✅ runtime |
| `kasidit-verify.py` | `PostToolUse` + `Stop` | Cross-check `[high]` confidence labels vs actual tool calls; flag orchestrator violations | ✅ runtime (warning only, not blocking) |
| `kasidit-record.py` | `Stop` / `SubagentStop` | Parse `[kasidit-log\|pattern\|memory\|rule]` emit lines → JSONL backend | ✅ runtime |
| `kasidit-update-check.sh` | `SessionStart` (1×/UTC day) | GitHub Release tag check, soft-notify on update | ✅ runtime |
| `kasidit-drift-check.sh` | `SessionStart` | Centerlite stale-sync reminder (>7 days) | ✅ runtime |
| `kasidit-log.sh` + `kasidit-log.py` | `UserPromptSubmit` (opt-in) | Capture every prompt to JSONL log for `/kasi-search` | ✅ runtime (off by default) |

## 1. `kasidit-route.py` — Router / Classifier

**Event:** `UserPromptSubmit`
**Stdin:** `{"prompt": "<message>", "session_id": "...", "cwd": "..."}`
**Stdout:** One line injected into turn context (or silent on unclassified):

```
[kasidit] kind=<kind> mode=<mode> history=<n_pass>/<n_total> avg_turns=<x>
```

or (no history yet):

```
[kasidit] kind=<kind> mode=<mode> [low-history]
```

### Classification logic

1. Lower-case the prompt.
2. Iterate `KEYWORDS` dict (insert-ordered, first hit wins).
3. Word-boundary match: `re.search(r'\b' + kw + r'\b', msg)`.
4. Map to `(kind, default_mode)`.
5. If unmatched → return silent (no output, no token cost).

### KEYWORDS table

See [[Kasi-Mode]] for the full mapping. Source of truth: `plugins/kasidit/hooks/kasidit-route.py:KEYWORDS`.

### Memory query

When a kind matches:

1. Load `~/.claude/skills/kasidit/center/route-memory.jsonl` (env: `KASIDIT_CENTER`).
2. Filter records where `kind == <classified-kind>` and `outcome == "pass"`.
3. Group by `mode_used`.
4. Compute `avg_turns` per mode.
5. Rank by `(avg_turns ascending, n_pass descending)`.
6. If top mode has `n_pass >= 3`, recommend it with history stats.
7. Otherwise recommend the keyword-table default with `[low-history]`.

This is the learning loop: over months the router gets sharper. If `bug-fix` kind has 10 pass records all in `lite` mode averaging 2 turns, every new `bug-fix` prompt gets `mode=lite history=10/10 avg_turns=2.0`.

## 2. `kasidit-verify.py` — Confidence Label + Orchestrator Check

**Event:** `PostToolUse` + `Stop`
**Stdin:** `{"assistant_text": "...", "tool_uses": [...]}` (or `text` / `tool_events` — hook is defensive about key names)
**Stdout:** One line per violation, or silent on clean pass.

### Check 1: confidence label verification

- Regex extracts `[high|medium|low|unsure]` labels from assistant text with a `(?:^|\s)` anchor (avoids matching inside quoted example blocks) and MULTILINE flag (works inside bullet lists).
- For each `[high]` claim, extract the target (`file:line` or `file`).
- Build `touched` set from the turn's tool calls:
  - `Read` / `Edit` / `Write` → target file path + basename.
  - `Bash` → every `\w+\.\w+` token in the command.
  - `Grep` / `Glob` → pattern or path arg.
- If a `[high]` target has no match in `touched` → **downgrade**:

```
[kasidit-verify] downgraded 1 [high] → [medium] — no matching Read/Bash call: login.php:42
```

Log written to `~/.claude/skills/kasidit/center/verify.log` for audit.

### Check 2: master orchestrator violation

Detects the pattern of "claiming to delegate but then doing the work":

- Regex: `(delegat(e|ing)|delegation|dispatch(ing)?|spawn(ing)?|handoff|invocation)\s+(to\s+)?(the\s+)?(specialist|agent|sub-?agent|bug-hunter|architect|audit-specialist|migration-specialist|refactor-surgeon)`.
- If the claim fires AND the same turn has direct `Edit` / `Write` / destructive `Bash` calls → warn:

```
[kasidit-verify] master violation — claimed delegation but performed 3 direct Edit/Write/Bash call(s). Master should spawn, not execute.
```

**Warning only, not blocking.** The user sees it and can redirect the model.

## 3. `kasidit-record.py` — Incremental JSONL Backend

**Event:** `Stop` / `SubagentStop` (also safe on `PostToolUse`)
**Stdin:** `{"assistant_text": "..."}`
**Stdout:** `[kasidit-record] +<N> backend entries saved` when records parsed, silent otherwise.

AI emits tiny structured lines at mission end or pattern discovery (~20-50 tokens each):

```
[kasidit-log] kind=bug-fix mode=lite turns=2 outcome=pass
[kasidit-pattern] name=sanctum-bearer-auth file=app/Middleware/ApiAuth.php note="v3 trust hierarchy"
[kasidit-memory] fact="mex_canteen uses PHP 7.4 + Laravel 8"
[kasidit-rule] scope=project rule="no composer update without lock diff"
[kasidit-rule] scope=global rule="always run migrations with --pretend first"
```

### Parse contract

- `EMIT_RE` matches `\[kasidit-(log|pattern|memory|rule)\]\s+(.+?)$` per line (MULTILINE).
- `KV_RE` extracts `key=value` pairs. Values in double quotes preserve spaces. Unquoted values stop at whitespace.
- Trailing `.,;:` (sentence punctuation) is stripped from unquoted values — so `outcome=pass.` stores as `"pass"`.
- `)` and `]` are **not** stripped — so `note=foo[bar]` stores as `foo[bar]` intact.
- `NUMERIC_KEYS = {"turns", "tokens", "rounds", "n"}` are coerced to `int`/`float`.
- `mode` is renamed to `mode_used` on write (matches the route.py reader).

### Storage map

| Emit tag | Target store | Consumer |
|---|---|---|
| `[kasidit-log]` | `~/.claude/skills/kasidit/center/route-memory.jsonl` | router recommendations |
| `[kasidit-pattern]` | `~/.claude/skills/kasidit/center/patterns.jsonl` | `/kasi-pull pattern`, PATTERNS.md seed |
| `[kasidit-memory]` | `~/.claude/skills/kasidit/center/memory.jsonl` | cross-session fact recall |
| `[kasidit-rule] scope=project` | `<project>/.kasidit/rules.jsonl` | project-local rules |
| `[kasidit-rule] scope=global` | `~/.claude/skills/kasidit/center/rules.jsonl` | user-wide rules |

All writes append a UTC timestamp: `{"ts":"2026-04-24T05:12:34Z", ...}`.

### Cost model

- AI pays ~20-50 tokens per mission end to emit 1-3 lines.
- No context cost on read — the hook output is not injected back.
- Storage: JSONL, cheap, local.
- **Return:** router saves far more tokens on future similar missions by skipping escalation when history shows a lighter mode succeeded.

## 4. `kasidit-update-check.sh` — Release Notifier

**Event:** `SessionStart` (throttled 1× per UTC day)
**Stamp file:** `~/.claude/skills/kasidit/center/.last_update_check`

Logic:

1. If today's date matches stamp → exit silently (already checked today).
2. Parse installed version from `~/.claude/plugins/marketplaces/kasidit/.claude-plugin/marketplace.json`:
   - Prefer `jq .plugins[] | select(.name=="kasidit") | .version` (correct plugin-scoped lookup).
   - Fall back to `jq .metadata.version`.
   - Fall back to `grep -o '"version":...'` if jq absent.
3. Get latest release tag via:
   - `gh api repos/kasidit-wansudon/kasidit/releases/latest --jq .tag_name`, or
   - `curl -s -m 3 api.github.com/repos/.../releases/latest` + grep.
4. Semver-compare (`sort -V`). If remote > local, print:

```
[kasidit] update available: v0.10.0 → v0.11.0 — run: /plugin marketplace update kasidit
```

Silent on: match, offline, missing `gh` + `curl`, already checked today. Writes today's date to stamp regardless — prevents repeated checks on partial failures.

## 5. `kasidit-drift-check.sh` — Gravity Sync Reminder

**Event:** `SessionStart`
**Stamp file:** `~/.claude/skills/kasidit/center/.last_sync`
**Env var:** `${KASIDIT_CENTER:-${KASIDIT_CENTER_DIR:-$HOME/.claude/skills/kasidit/center}}` (accepts both new and legacy names)

1. If `.last_sync` missing → create silently (first run, no nag).
2. If age < 7 days → exit silently.
3. Otherwise print one line to stderr:

```
[kasidit] Centerlite last synced 12d ago. Run /kasi-sync to check drift.
```

**Reminder only, not a block.** User continues session normally.

## Bonus: `kasidit-log.sh` + `kasidit-log.py` — Prompt Log (opt-in)

**Event:** `UserPromptSubmit`
**Opt-in:** `export KASIDIT_LOG_ENABLED=1` in shell rc
**Output:** `~/.claude/skills/kasidit/center/logs/YYYY-MM-DD.jsonl`

Captures every user prompt with:

- Timestamp, session id, cwd, line count, char count.
- Full prompt text, trimmed if >200 lines (first 40 + last 20 with a `[trimmed N lines]` marker).

**Not wired automatically by `install.sh`.** The hook script is installed but the `UserPromptSubmit` registration is left to the user (or a future opt-in flow). Set `KASIDIT_LOG_ENABLED=1` and add the hook registration manually — see `plugins/kasidit/hooks/README.md`.

**Privacy:** logs contain whatever the user typed, including PII. Never commit. `.gitignore` guidance in `/kasi-init` covers `~/.claude/skills/kasidit/center/logs/`.

## Backend integrity

The hooks maintain an integration contract. Violations = silent data loss.

### Contract table

| Producer → Channel → Consumer | Fields written | Fields read | Status |
|---|---|---|---|
| AI emit → `[kasidit-log]` line | `kind, mode, turns, outcome` | record.py parses | integrity preserved post-v0.10 punctuation fix |
| record.py → `route-memory.jsonl` | `ts, kind, mode_used, turns (int), outcome` | route.py reads | integrity preserved |
| route.py → stdout | `kind, mode, history, avg_turns` | Claude Code injects to context | ✅ |
| Claude Code → verify.py stdin | `assistant_text \| text, tool_uses \| tool_events` | verify.py accepts both key names | defensively safe |
| install.sh → settings.json | 6 hook registrations (SessionStart×2, UserPromptSubmit, PostToolUse, Stop×2) | Claude Code reads on load | idempotent, no duplicates |

## Install flow

```bash
git clone https://github.com/kasidit-wansudon/kasidit.git
cd kasidit
bash plugins/kasidit/install.sh
```

What happens:

1. Plugin root detected via `CLAUDE_PLUGIN_ROOT` or `realpath "$0"` fallback.
2. Hooks copied to `~/.claude/hooks/` (chmod +x).
3. `~/.claude/settings.json` backed up to `.kasidit-backup-<ts>` (3 most recent kept).
4. 6 hook entries merged into `settings.json`:
   - `SessionStart` → `kasidit-update-check.sh`, `kasidit-drift-check.sh`
   - `UserPromptSubmit` → `kasidit-route.py`
   - `PostToolUse` → `kasidit-verify.py`
   - `Stop` → `kasidit-verify.py`, `kasidit-record.py`
5. Entries already present (by command-string match) are skipped. Re-running is safe.
6. `~/.claude/skills/kasidit/center/` seeded:
   - `logs/`, `checklists/`, `knowledge/` directories.
   - Empty JSONL: `route-memory.jsonl`, `patterns.jsonl`, `memory.jsonl`, `rules.jsonl`, `missions.jsonl`.
   - 12 default checklists copied from `defaults/checklists/`.
   - `patterns-template.md` + `design-system-template.md` → `knowledge/`.
   - `.last_sync` + `.last_update_check` stamps.
7. `config.json` written with chosen `--mode` (default `router`).

Merger: `jq` primary, `python3` stdlib fallback. If neither present, prints warning and leaves settings untouched — install jq (`brew install jq`) or python3 and re-run.

### Flags

| Flag | Effect |
|---|---|
| `--dry-run` | Print plan only, write nothing. |
| `--mode=router\|lite\|full` | Initial mode saved to `config.json`. Default `router`. |
| `--help` | Show usage. |
| `KASIDIT_SKIP_SETTINGS=1` | Copy hooks but do not merge `settings.json`. Hook-only install for debugging. |

## Testing

`plugins/kasidit/hooks/test_hooks.py` — 10 isolated snapshot tests. Each test creates its own `KASIDIT_CENTER` tempdir + cleanup closure. No shared state, no ordering dependency.

```bash
python3 plugins/kasidit/hooks/test_hooks.py
python3 plugins/kasidit/hooks/test_hooks.py --verbose
```

Coverage:

- route.py: security keyword / bug keyword / unclassified silent / history recommendation
- verify.py: unverified `[high]` downgrade / verified `[high]` silent / master violation
- record.py: log emit append / pattern emit persist / mode→mode_used normalization / int turns coercion
- e2e: record 4 runs → route reads history and recommends from JSONL

Verified under Python 3.9.19 (pyenv) and default interpreter — all 10 pass on both.

## What is runtime-enforced vs. convention

Honest split:

### Enforced at runtime (by these hooks)

- Prompt classification + recommendation injection.
- `[high]` confidence label cross-check → automatic downgrade notice.
- Master orchestrator "claim-delegation-but-edit" detection → warning line.
- Incremental JSONL persistence of emit lines.
- Daily update-check + Gravity sync reminder.
- Settings merge idempotency.

### Prompt-level convention (not harness-enforced)

- Rule 1 (mission-driven narrowing) — AI decides.
- All 11 core rules except the two above (2 and 11) — AI applies.
- Mode gating — AI respects the "router only" / "full loaded" distinction best-effort.
- State precedence resolution — AI reads config files and applies.
- Agent auto-mapping — does **not** exist. Users must invoke `audit-specialist --focus=<lens>` explicitly.

## Anti-patterns

- ❌ Editing hook scripts directly in `~/.claude/hooks/` and expecting `install.sh` re-run to preserve — it won't, will overwrite.
- ❌ Committing `route-memory.jsonl` or `logs/*.jsonl` to a repo — contains PII + project state.
- ❌ Relying on `kasidit-verify.py` to block the model from editing — it only **warns**, does not stop.
- ❌ Assuming the recommendation line in context is authoritative — it is a suggestion. User override always wins.
- ❌ Double-registering a hook by manual edit of `settings.json` — `install.sh` will detect and skip, but manual registrations can create duplicates.

## Debugging

Hook output visible via:

```bash
# 1. Smoke test a hook manually with a fake payload
printf '{"prompt":"fix auth bug"}' | python3 ~/.claude/hooks/kasidit-route.py

# 2. Check where memory lives
ls -la ~/.claude/skills/kasidit/center/
cat ~/.claude/skills/kasidit/center/route-memory.jsonl

# 3. View settings.json registrations
jq '.hooks' ~/.claude/settings.json

# 4. Run test suite
python3 ~/.claude/plugins/marketplaces/kasidit/plugins/kasidit/hooks/test_hooks.py
```

## Since

v0.10.0 — introduced.

## See also

- [[Kasi-Mode]]
- [[Agent-Audit-Specialist]]
- [[Gravity Pattern]]
- [[Master-Orchestrator]]
- [[Checklists]]
- [[v0.10]]
