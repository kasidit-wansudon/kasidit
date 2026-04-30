# /kasi-status

> Show the current Kasidit session state — mission, counter, tier, `.kasidit/` summary, last action, next step.

## Usage

```
/kasi-status
```

## What it does

- Prints the current mission (what / scope).
- Shows the mission counter (rounds failed) against the tier limit.
- Shows detected domain (backend / UI / review / audit).
- Shows current tier (Opus / Sonnet / Haiku) and mode (interactive / batch).
- Summarizes `.kasidit/` contents (INDEX presence, checklist count, MEMORY lines, cached docs).
- Lists pending items and blockers.
- Shows the last action and the suggested next step.

## Output format

```
Mission: <narrow goal>
Domain: <detected>
Tier: <model>
Mode: interactive | batch
Counter: N/4 (N/2 Haiku)

.kasidit/ status:
  - INDEX.md: exists | missing
  - CHECKLISTS/: N files
  - MEMORY.md: N lines
  - knowledge/: N cached docs

Last: <last action>
Next: <suggested>
Blocker: <if any>
```

## When to use

- Long session, lost track of the mission.
- Switching contexts between projects or tasks.
- Before `/clear` to snapshot state.
- Debugging why Kasidit behavior seems off (wrong tier, wrong domain).

## When NOT to use

- Mid-diff — run after the edit, not during.
- As a stand-in for a real progress report to stakeholders.

## Anti-patterns

- Treating `kasi-status` output as user-facing progress — it is an internal snapshot.
- Running it repeatedly in a loop instead of fixing the blocker it already surfaced.

## Since

Introduced in [[v0.1.0]].

## See also

- [[Commands]] (aggregate)
- [[Model-Tiers]]
- [[Kasi-Mode]] — current Mode is part of `/kasi-status` output
- [[v0.1.0]] — where the mission counter was introduced
