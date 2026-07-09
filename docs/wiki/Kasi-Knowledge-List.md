# /kasi-knowledge-list

> Browse runbooks and knowledge entries captured by [[Kasi-Acknowledge]]. Pick one by number or slug to replay it step-by-step.

## Usage

```
/kasi-knowledge-list
/kasi-knowledge-list show <n|slug>
/kasi-knowledge-list recent [n]
/kasi-knowledge-list tag <tag>
/kasi-knowledge-list kind <kind>
/kasi-knowledge-list search <query>
/kasi-knowledge-list replay <slug>
/kasi-knowledge-list stats
/kasi-knowledge-list stale
```

If no sub-mode is given, runs `list`.

## What it does

- Scans three sources in order: project-local runbooks (`.kasidit/knowledge/runbooks/`), the global hub (`~/.claude/skills/kasidit/center/knowledge/runbooks/`, marked `[hub]`), and non-runbook knowledge docs (`.kasidit/knowledge/*.md`, marked `[doc]`).
- `list` prints a numbered index grouped by kind, with last-run date, run count, and tags.
- `replay <slug>` walks the steps interactively — prints one step, waits for the user to confirm before showing the next.
- `stale` surfaces runbooks not run in >90 days, as candidates for re-verification or archival.

## Replay is display-only

Kasidit **never executes commands during replay** — it prints and waits. The user runs each command themselves, matching the same discipline [[Kasi-Devopt]] and [[Kasi-Deploy]] apply to deploy commands. If a step requires sudo or production access, an extra confirmation banner appears. A `[low]`/`[unsure]` confidence runbook gets a warning at the start of replay.

## `list` output shape

```
Runbooks (12 local + 4 hub)

DEPLOY (4)
  1. deploy-kas-sass-staging          last 2026-04-30 · runs 3 · staging,laravel,ssh
  ...
[stale: 2 runbooks not run >90d — see /kasi-knowledge-list stale]
```

## When to use

- Before repeating a known procedure — check `list`/`search` first instead of re-deriving steps.
- After a deploy attempt — `/kasi-devopt deploy` (and now [[Kasi-Deploy]]) checks for a matching runbook automatically and offers to replay it.
- Periodic hygiene — `stale` to find runbooks that might no longer match reality.

## Tier behavior

- **Haiku** — `list`, `show`, `recent`, `tag`, `kind`, `stats`, `stale`, `archive`, `delete`. No `search` (semantic ranking needs Sonnet+).
- **Sonnet** — all sub-modes including the `replay` walkthrough.
- **Opus** — same, plus can suggest merging similar runbooks or flag drift between hub and local versions.

## Anti-patterns

- ❌ Print every runbook in full on `list` — only the index.
- ❌ Execute `replay` commands automatically.
- ❌ Hide `[hub]` entries from the list — always mark the source.
- ❌ Use a stale runbook without warning the user first.
- ❌ Reveal redacted secrets in list/show output.

## Since

Introduced in [[v0.11.0]].

## See also

- [[Commands]] (aggregate)
- [[Kasi-Acknowledge]] — writes what this command reads
- [[Kasi-Devopt]] · [[Kasi-Deploy]] — check for a matching runbook before deploying
- [[Kasi-Promote]] — lifts a local runbook to the hub
