# /kasi-promote

> Lift a validated item from project `.kasidit/` (dcenterlite) up into the global Centerlite hub. Confirmed, append-only, never automatic.

## Usage

```
/kasi-promote <type> <path-or-id>
```

## Types

| Type | Source | Target |
|------|--------|--------|
| `pattern`   | `.kasidit/PATTERNS.md` section | append to `center/patterns.jsonl` |
| `checklist` | `.kasidit/CHECKLISTS/<name>.md` | copy to `center/checklists/<name>.md` (suffix `_v2` on conflict) |
| `knowledge` | `.kasidit/knowledge/<file>.md` | copy to `center/knowledge/<file>.md` (ask on conflict) |
| `rule`      | free-form text or memory note | append to `center/rules.md` |
| `mission`   | `.kasidit/MISSION.md` (completed) | append record to `center/missions.jsonl` |

## What it does

- Reads the source item and previews what will be promoted.
- Checks Centerlite for name or near-duplicate conflicts.
- Asks user to confirm (diff shown on patterns / rules).
- Appends or copies to the Centerlite path.
- Logs the promotion event to `center/missions.jsonl` with timestamp, source project, and reason.

## Flow

1. Read source item. Print preview.
2. Check for conflict in Centerlite.
3. Ask to confirm. Show diff for text-type items.
4. Append or copy.
5. Log promotion event.

## When to use

- A pattern or checklist has proven useful across more than one mission in this project.
- A rule discovered locally should become a default for new projects.
- A completed mission is worth recording as a reusable template.

## When NOT to use

- First time seeing a pattern — wait for repeated usefulness.
- Project-specific names (table names, route names, internal vars) — those stay in dcenterlite.
- Prompts / logs — they flow into `center/logs/` automatically via the global hook.

## Anti-patterns

- Auto-promoting — user must confirm each item; prevents noise climbing the hub.
- Rewriting `.jsonl` history — append-only.
- Overwriting an existing checklist without a version suffix.
- Promoting from a path matching `client/` or `confidential/` without explicit `--force`.

## Since

Introduced in [[v0.9.2]].

## See also

- [[Commands]] (aggregate)
- [[Gravity-Pattern]]
- [[Kasi-Pull]]
- [[Kasi-Sync]]
