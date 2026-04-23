# Commands

All `/kasi-*` commands shipped with the plugin. Invoke with `/` from Claude Code.

## Mission commands

### `/kasi-review`

Launch a code review mission with full Kasidit discipline: narrow scope → load or generate CHECKLISTS → dispatch per-file agents → synthesize findings with confidence labels + Top 5 priority.

Tier behavior: on Haiku, 1 file per agent + mandatory verifier pass.

### `/kasi-security`

Security audit variant of review. Runs through `CHECKLISTS/security-<stack>.md`. Flags injection, auth, file handling, output, session, crypto issues. Confidence-labeled.

### `/kasi-fix`

Bug-fix mission with conservative discipline. Runs mandatory `git log --grep=<term>` and `git log -S <symbol>` before any fix (Rule 2.6). Minimal-change fix with regression test.

### `/kasi-ui`

UI/CSS mission in UI Override Mode. Requires visual target (screenshot / CSS values / Claude Design mockup). One change per round. Cache-aware.

### `/kasi-cascade`

Tier Cascade orchestration ([[v0.8.0]]): Opus plans → Sonnet writes → Haiku greps. Invoke for missions large enough to benefit from multi-tier routing.

## Project commands

### `/kasi-init`

Bootstrap a new or existing project. Chains:

```
/kasi-scaffold → /kasi-pull (stack defaults) → /kasi-docs →
.kasidit/MISSION.md seed → optional /kasi-review →
register SessionStart hook in .claude/settings.local.json → CLAUDE.md pointer
```

Skip flags: `skip docs`, `skip review`, `no auto-invoke`, `dry-run`.

Haiku: skips the review step during init unless user insists.

### `/kasi-scaffold`

Build `.kasidit/` structure: INDEX, RELATIONS, MEMORY, PATTERNS, CHECKLISTS, knowledge. Detects stack from `composer.json` / `package.json` / etc. Asks to confirm detection before generating.

### `/kasi-docs`

Fetch version-matched official documentation for the detected stack. Caches to `.kasidit/knowledge/<stack>-<version>-<topic>.md`. Follows the Trust Hierarchy from [[v0.2.1]].

### `/kasi-status`

Show current mission state, failure counter, context usage. Quick health check.

## Gravity commands

### `/kasi-promote`

```
/kasi-promote <type> <name>
```

Lift item from `.kasidit/` into `~/.claude/skills/kasidit/center/`. Types:

| Type | Source | Target |
|---|---|---|
| `pattern` | `.kasidit/PATTERNS.md` section | append to `center/patterns.jsonl` |
| `checklist` | `.kasidit/CHECKLISTS/<name>.md` | copy to `center/checklists/<name>.md` |
| `knowledge` | `.kasidit/knowledge/<file>.md` | copy to `center/knowledge/<file>.md` |
| `rule` | free text | append to `center/rules.md` |
| `mission` | `.kasidit/MISSION.md` | append summary to `center/missions.jsonl` |

Always asks confirmation. Never auto-promotes. See [[Gravity Pattern]].

### `/kasi-pull`

```
/kasi-pull <type> <name>
/kasi-pull all-for <stack>
```

Fetch item from Centerlite into project `.kasidit/`. Diffs before overwrite; `(o)verwrite / (m)erge-append / (s)kip` on conflict. See [[Gravity Pattern]].

### `/kasi-sync`

```
/kasi-sync              # everything
/kasi-sync checklists   # one type
/kasi-sync <name>       # one item
```

Audit drift between dcenterlite and centerlite. Read-only. Prints per-item status: `up-to-date / local ahead / center ahead / conflict / local only / center only` with suggested command.

### `/kasi-search`

```
/kasi-search "<query>"
```

Semantic search over `.kasidit/knowledge/` via local embeddings ([[v0.8.0]]). Returns top-k snippets with file path, line range, similarity score. No network calls.

## Design commands ([[v0.9.0]])

### `design <what>`

Route to Claude Design for visual work. Asks audience / platform / brand constraints, pre-fills the Claude Design brief.

### `mockup <screen>`

Shortcut for `design mockup <screen>`.

### `extract-system`

Claude Design reads codebase CSS and component files, produces a draft `.kasidit/DESIGN_SYSTEM.md`.

### `parity <mockup-id>`

Compare current UI screenshot vs saved `.kasidit/prototypes/<mockup-id>-after.png`. Report `[parity high | medium | low]` with per-token diffs.

### `report visual`

Export last findings as a one-pager via Claude Design. Useful for non-technical audiences.

## Meta commands

### `/kasi-wiki-sync`

```
/kasi-wiki-sync          # dry-run (default)
/kasi-wiki-sync apply    # actually push
/kasi-wiki-sync <page>   # one page only
```

Push `docs/wiki/*.md` into `github.com/kasidit-wansudon/kasidit.wiki.git`. Manual — not wired to commit hooks. Requires auth to the wiki repo.

## Steering shorthand (informal, not slash commands)

Useful phrases recognized by the skill:

- `task status` — summary of mission, counter, pending items
- `clear` — reset working context, keep สารบัญ and MEMORY.md
- `remember <fact>` — save to `.kasidit/MEMORY.md`
- `forget that` — drop last failed attempt
- `wave 2` — force escalation
- `tier opus | sonnet | haiku` — override tier auto-detect
- `verify` — run verification pass on last findings
- `build index` — generate `.kasidit/INDEX.md` from structure
- `build checklist <domain>` — scaffold a stack-specific checklist

## See also

- [[Getting Started]]
- [[Gravity Pattern]]
- [[Model Tiers]]
