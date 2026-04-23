---
description: Promote fact / pattern / knowledge from project .kasidit/ (dcenterlite) into global Centerlite hub
---

Push a validated item from **dcenterlite** (`<project>/.kasidit/`) up into **Centerlite** (`~/.claude/skills/kasidit/center/`). Part of the **Gravity Pattern** — only promote what has proven useful; local is source of truth by default.

**Usage:**

```
/kasi-promote <type> <path-or-id>
```

Types:

| Type | Source | Target |
|------|--------|--------|
| `pattern`  | `.kasidit/PATTERNS.md` section | append to `center/patterns.jsonl` |
| `checklist` | `.kasidit/CHECKLISTS/<name>.md` | copy to `center/checklists/<name>.md` (suffix `_v2` if exists) |
| `knowledge` | `.kasidit/knowledge/<file>.md` | copy to `center/knowledge/<file>.md` (ask on conflict) |
| `rule`     | free-form text or memory note | append to `center/rules.md` |
| `mission`  | `.kasidit/MISSION.md` (completed) | append summary record to `center/missions.jsonl` |

**Flow:**

1. Read source item. Show what will be promoted.
2. Check Centerlite for conflict (same name / near-duplicate).
3. Ask user to confirm (preview diff if pattern / rule).
4. Append or copy to Centerlite path.
5. Log promotion event to `center/missions.jsonl` with ts + source project + reason.

**Rules:**

- **Never auto-promote.** User must confirm each one — prevents noise climbing the hub.
- Promotion is **append-only** for `.jsonl`. Do not rewrite history.
- For file-type (checklist / knowledge), version-suffix on conflict (`_v2`, `_v3`).
- Prompts/logs (`center/logs/`) are **not** promote targets — they flow in via hook automatically.
- Cross-project leak guard: if source path contains `client/` or `confidential/`, require explicit `--force`.

**Anti-patterns:**

- ❌ Promoting every pattern the first time you see it — promotion is for *repeated* usefulness.
- ❌ Overwriting existing checklist without suffix.
- ❌ Promoting project-specific names (tables, routes, internal vars) — those stay in dcenterlite.

**See also:** `/kasi-pull` (reverse direction), `/kasi-sync` (audit).
