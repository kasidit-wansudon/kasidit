---
description: Pull item from Centerlite hub into local project .kasidit/ (dcenterlite)
---

Copy a shared item from **Centerlite** (`~/.claude/skills/kasidit/center/`) into the current project's **dcenterlite** (`.kasidit/`). Part of the **Gravity Pattern** — reuse proven assets without reinventing.

**Usage:**

```
/kasi-pull <type> <name>
```

Types:

| Type | Source | Target |
|------|--------|--------|
| `checklist` | `center/checklists/<name>.md` | `.kasidit/CHECKLISTS/<name>.md` |
| `knowledge` | `center/knowledge/<name>.md` | `.kasidit/knowledge/<name>.md` |
| `rule`      | selected line from `center/rules.md` | append to project `.kasidit/MEMORY.md` |
| `pattern`   | filter `center/patterns.jsonl` by tag | append to `.kasidit/PATTERNS.md` |
| `all-for <stack>` | everything in center tagged for stack (php / node / go / ...) | seed entire `.kasidit/` bootstrap |

**Flow:**

1. List matching items from Centerlite (glob, tag filter, or exact name).
2. Show what would be pulled + target paths.
3. Diff against existing local file (if present).
4. Ask user to confirm (overwrite / merge / skip per item).
5. Copy or merge. Local file becomes the customizable copy — upstream changes do not auto-flow.

**Rules:**

- **Never auto-pull.** `/kasi-init` invokes pull for stack-matched defaults during scaffold, but confirms once for the batch.
- Pulled file is **detached** from upstream — edits in project do not push back (use `/kasi-promote` for that).
- If local file exists, ask: `(o)verwrite / (m)erge-append / (s)kip`.
- Record pull event to `.kasidit/MEMORY.md` as `pulled <type> <name> from center on <date>` for traceability.

**Anti-patterns:**

- ❌ Pulling entire hub — that defeats "lightweight".
- ❌ Silent overwrite of project-customized files.
- ❌ Pulling stack-mismatched checklist (php checklist into node project).

**See also:** `/kasi-promote` (reverse direction), `/kasi-sync` (audit diffs).
