# /kasi-sync

> Audit drift between project `.kasidit/` (dcenterlite) and global Centerlite. Read-only; prints per-item status with suggested command.

## Usage

```
/kasi-sync                 # compare everything
/kasi-sync checklists      # one type only
/kasi-sync <name>          # one item
```

## What it does

- Walks `.kasidit/CHECKLISTS/`, `.kasidit/knowledge/`, parses `PATTERNS.md` and `MEMORY.md`.
- Matches each item to its Centerlite counterpart by filename or pattern hash.
- Tags each pair: `up-to-date | local ahead | center ahead | conflict | local only | center only`.
- Prints report with a suggested command per item.
- Never mutates either side — user decides via [[Kasi-Promote]] or [[Kasi-Pull]].

## Report format

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

## Flow

1. Walk project `.kasidit/` and parse pattern / memory files.
2. Match each item to Centerlite counterpart (filename or line-normalized sha256 for patterns).
3. Diff and tag status.
4. Print report with suggested per-item command.
5. Exit — user applies fixes via [[Kasi-Promote]] or [[Kasi-Pull]].

## When to use

- Periodic drift check across a project.
- Before a release or project handover — surface promote candidates.
- After a long stretch of local edits, to check what should climb the hub.

## When NOT to use

- Outside a project directory — needs `.kasidit/` present.
- To auto-apply resolutions — this command is read-only by design.

## Anti-patterns

- Auto-resolving conflicts — always flag, never guess a winner.
- Treating "local only" as stale — it may be project-specific (that is the point).
- Running on a large dcenterlite without scoping — use `/kasi-sync <type>` to narrow.

## Since

Introduced in [[v0.9.2]].

## See also

- [[Commands]] (aggregate)
- [[Gravity-Pattern]]
- [[Kasi-Promote]]
- [[Kasi-Pull]]
