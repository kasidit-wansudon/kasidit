# Gravity Pattern

> Center has mass. Local has autonomy. Things fall in when proven.

The **Gravity Pattern** is Kasidit's two-tier knowledge system, introduced in [[v0.9.2]]. Knowledge splits into:

- **Centerlite** — global hub at `~/.claude/skills/kasidit/center/`. Shared. Lightweight. Stable.
- **Dcenterlite** — project-local at `<project>/.kasidit/`. Full fidelity. Authoritative for the project.

Nothing moves between them automatically. Users promote proven items inward; users pull shared items outward; sync reports drift.

## Why

Every project re-derives the same patterns without a hub. The cost:

- **Opus:** wasteful — re-reasons things it already reasoned about
- **Sonnet:** slower — re-fetches knowledge it already cached somewhere else
- **Haiku:** broken — cannot cross-project reason, so it guesses

Gravity gives every tier a canonical base to cite and a disciplined way to grow that base.

## Layout

### Centerlite — `~/.claude/skills/kasidit/center/`

```
center/
├── config.json         # Mode + version + last_changed (v0.10)
├── logs/               # prompt log from UserPromptSubmit hook
├── checklists/         # master checklist library (12 default seeded by install.sh in v0.10)
├── knowledge/          # shared doc snippets (version-matched) + templates
├── patterns.jsonl      # validated cross-project patterns (promote target)
├── missions.jsonl      # mission history (ts, project, tier, outcome)
├── route-memory.jsonl  # router learnings — kind/mode/turns/outcome (v0.10)
├── memory.jsonl        # cross-session facts emitted by [kasidit-memory] (v0.10)
├── rules.jsonl         # global user rules emitted by [kasidit-rule] scope=global (v0.10)
├── rules.md            # legacy rules markdown (kept for backward-compat)
├── .last_sync          # timestamp of last /kasi-sync (read by drift-check hook)
└── .last_update_check  # timestamp of last update poll
```

**Discipline:**

- Lightweight — facts, pointers, small snippets, < 1 MB per file
- Append-only for `*.jsonl` — history is load-bearing
- Never project-specific — no table names, client names, internal vars
- Promotions require user confirmation

### Dcenterlite — `<project>/.kasidit/`

```
.kasidit/
├── INDEX.md RELATIONS.md MEMORY.md PATTERNS.md
├── DESIGN_SYSTEM.md MISSION.md
├── CHECKLISTS/    # pulled copies, customizable
├── knowledge/     # version-matched docs for this project
└── prototypes/    # Claude Design exports
```

**Discipline:**

- Source of truth for the project
- Pulled items are detached — local edits do not auto-push back
- Customize freely — `.kasidit/` is yours

## Sync logic

| Operation | Direction | Trigger | Automatic? |
|---|---|---|---|
| **Read** | dcenter → center fallback | missing local → check hub → copy down | yes |
| **Write** | local only | every mission writes to `.kasidit/` | yes |
| **Promote** | dcenter → center | `/kasi-promote <type> <name>` | **no — user confirm** |
| **Pull** | center → dcenter | `/kasi-pull <type> <name>` | **no — user confirm** |
| **Sync audit** | both, read-only | `/kasi-sync` | on invocation |
| **Prompt log** | prompt → `center/logs/` | `UserPromptSubmit` hook | yes, user scope |
| **Backend save** (v0.10) | AI emit → `center/*.jsonl` | `Stop` hook → `kasidit-record.py` parses `[kasidit-log\|pattern\|memory\|rule]` lines | yes, user scope |
| **Drift check** (v0.10) | read `.last_sync` | `SessionStart` → `kasidit-drift-check.sh` | yes, prints reminder if > 7 days |
| **Update check** (v0.10) | read `marketplace.json` vs GitHub Releases | `SessionStart` (1×/UTC day) → `kasidit-update-check.sh` | yes, silent if up-to-date |

**No auto-promote.** No auto-pull. The hub only grows by deliberate action. Noise is the enemy.

## v0.10 incremental backend save ("ออม")

AI emits tiny structured lines at mission end. `kasidit-record.py` (Stop hook) parses and appends:

```
[kasidit-log] kind=bug-fix-single-file mode=lite turns=2 outcome=pass
[kasidit-pattern] name=sanctum-bearer-auth file=app/Middleware/ApiAuth.php note="..."
[kasidit-memory] fact="project uses PHP 7.4 + Laravel 8 with custom Auth facade"
[kasidit-rule] scope=project rule="no composer update without lock diff"
[kasidit-rule] scope=global rule="never bypass --no-verify on commit hooks"
```

| Emit tag | Target store | Read by |
|---|---|---|
| `[kasidit-log]` | `center/route-memory.jsonl` | router classifier — picks shortest successful mode per kind |
| `[kasidit-pattern]` | `center/patterns.jsonl` | `/kasi-pull pattern`, `PATTERNS.md` seed |
| `[kasidit-memory]` | `center/memory.jsonl` | cross-session fact recall |
| `[kasidit-rule] scope=project` | `<project>/.kasidit/rules.jsonl` | project-local rules |
| `[kasidit-rule] scope=global` | `center/rules.jsonl` | user-wide rules across projects |

**Cost model:** AI pays ~20-50 extra tokens per mission to emit 1-3 lines. Router compounds savings over months by skipping unnecessary escalation.

**Privacy:** these stores hold metrics + facts, not prompt text. Safe to keep local. Logs of full prompts live separately under `center/logs/` and **must not be committed**.

## Commands

- [[Commands#kasi-promote|/kasi-promote]] — lift item to hub
- [[Commands#kasi-pull|/kasi-pull]] — fetch item to project
- [[Commands#kasi-sync|/kasi-sync]] — audit drift

See [[Commands]] for full syntax.

## Per-tier usage

**Opus** — suggests promotions after missions; never promotes without confirm.

**Sonnet** — default. Pulls during `/kasi-init`, promotes after a pattern appears in 2+ projects.

**Haiku** — pull aggressively during init (Centerlite = scaffold). Promote rarely.

## Privacy

Centerlite is local filesystem. Nothing uploads. `center/logs/` contains verbatim prompts — **do not sync Centerlite into shared storage** without reviewing PII. `/kasi-init` adds this to `.gitignore` automatically.

## Anti-patterns

- ❌ Auto-promoting every pattern — pollutes the hub
- ❌ Editing Centerlite when the edit belongs to one project
- ❌ Pulling the entire hub into every project
- ❌ Silent overwrite on pull when local is customized
- ❌ Committing `center/logs/` anywhere

## Future

v0.9.2 introduced manual promote/pull. v0.10 added incremental backend save (above). Still pending:

- **Auto-scan aggregation** — "pattern seen in 3 projects → suggest promote" (router would consume this; not shipped in v0.10)
- **`/kasi-memory` subcommand** — inspect / forget / export `route-memory.jsonl` records
- **Shared Centerlite across devices** — git-backed, opt-in, PII-filtered
- **Team-scale Centerlite** — access controls

## See also

- [[v0.9.2]] — the release that introduced Gravity (manual promote/pull/sync)
- [[v0.10.0]] — runtime hooks add automatic backend save layer
- [[Backend-Hooks]] — payload contract for `kasidit-record.py`
- [[Kasi-Mode]] — how `route-memory.jsonl` feeds the router
- [[Commands]]
