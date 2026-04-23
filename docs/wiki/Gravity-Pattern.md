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
├── logs/              # prompt log from UserPromptSubmit hook
├── patterns.jsonl     # validated cross-project patterns
├── checklists/        # master checklist library
├── knowledge/         # shared doc snippets (version-matched)
├── missions.jsonl     # mission history (ts, project, tier, outcome)
└── rules.md           # accumulated user rules
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

**No auto-promote.** No auto-pull. The hub only grows by deliberate action. Noise is the enemy.

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

v0.9.2 intentionally keeps promote/pull manual. Post-v0.9.2 may add:

- Auto-scan aggregation — "pattern seen in 3 projects → suggest promote"
- Shared Centerlite across devices (git-backed, opt-in, PII-filtered)
- Team-scale Centerlite with access controls

## See also

- [[v0.9.2]] — the release that introduced Gravity
- [[Commands]]
