---
description: Audit diffs between project .kasidit/ (dcenterlite) and global Centerlite hub
---

Compare every named item in local **dcenterlite** against the matching item in **Centerlite**, report drift. Part of the **Gravity Pattern** — surface divergence; user decides whether to promote, pull, or keep both.

**Usage:**

```
/kasi-sync              # compare everything
/kasi-sync checklists   # one type only
/kasi-sync <name>       # one item
```

**Report format:**

```
Gravity sync — <project>

CHECKLISTS
  security-php.md     [local ahead]   5 lines added locally  →  /kasi-promote checklist security-php
  css-audit.md        [up-to-date]
  perf-sql.md         [center ahead]  3 lines added upstream →  /kasi-pull checklist perf-sql
  laravel8-custom.md  [local only]    no upstream            →  consider /kasi-promote
  node-xss.md         [center only]   not in project         →  consider /kasi-pull

KNOWLEDGE
  laravel-8-eloquent.md  [up-to-date]
  php-7.4-types.md       [conflict]   both sides edited      →  resolve manually

PATTERNS (in PATTERNS.md)
  2 local patterns not in center     →  /kasi-promote pattern …
  1 center pattern not in project    →  /kasi-pull pattern …

RULES (MEMORY.md vs center/rules.md)
  0 drift
```

**Flow:**

1. Walk `.kasidit/CHECKLISTS/`, `.kasidit/knowledge/`, parse `PATTERNS.md`, `MEMORY.md`.
2. Match each item to Centerlite counterpart (by filename / pattern hash).
3. Diff. Tag each pair: `up-to-date | local ahead | center ahead | conflict | local only | center only`.
4. Print report with suggested command per item.
5. **Does not apply changes.** User decides via `/kasi-promote` or `/kasi-pull`.

**Rules:**

- Read-only. Never mutates either side.
- Hash-based match for patterns (line-normalized sha256).
- `conflict` = both sides diverged after last shared state → flag, do not guess winner.
- Logs (`center/logs/`) ignored — one-way flow only.
- Fast on small sets; on large dcenterlite, use `/kasi-sync <type>` to scope.

**Anti-patterns:**

- ❌ Auto-resolving conflicts.
- ❌ Treating "local only" as stale (it may be project-specific — that is the point).
- ❌ Running `/kasi-sync` outside a project dir — needs `.kasidit/` present.

**See also:** `/kasi-promote`, `/kasi-pull`.
