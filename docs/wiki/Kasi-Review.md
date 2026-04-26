# /kasi-review

> Launch a code review mission with full Kasidit discipline: narrow scope, checklist-driven scan, confidence-labeled findings.

## Usage

```
/kasi-review <module-or-file>
/kasi-review <commit-sha>
/kasi-review <path> --domain=security|performance|ui|backend
```

## What it does

- Forces scope narrowing before any scan — no "review the whole repo".
- Detects domain (backend / UI / security / performance) and loads the matching checklist from `.kasidit/CHECKLISTS/`.
- Fans out per-file (Haiku) or per-module (Opus / Sonnet) subagents, each running the checklist mechanically.
- Main synthesizes findings with `[high | medium | low | unsure]` confidence labels.
- Emits HIGH / MED / LOW severity buckets plus a Top-5 actionable list.

## Flow

1. Ask user which module / file / commits — refuse vague scope.
2. Detect domain → load matching `CHECKLISTS/*.md`.
3. Spawn subagents: 1 per file on Haiku, 1 per module on Opus / Sonnet.
4. Each subagent scans mechanically against the checklist.
5. Main aggregates + deduplicates + labels confidence.
6. Output severity-bucketed findings + Top-5 priority.
7. If counter hits 4 (Opus) / 2 (Haiku), escalate or hand back.

## When to use

- PR review before merge.
- Pre-release sanity pass on a changed module.
- Periodic checklist audit on a legacy area.

## When NOT to use

- You want a fix, not findings — use [[Kasi-Fix]].
- You need a security audit specifically — use [[Kasi-Security]] (different checklist set).
- Scope is "everything" — the command will refuse.

## Tier behavior

- **Opus** — 1 subagent per module, counter cap 4.
- **Sonnet** — same as Opus, default workhorse.
- **Haiku** — 1 subagent per file (cheaper context), counter cap 2, mandatory verifier pass.

## Anti-patterns

- ❌ Accepting "review all code" — always narrow.
- ❌ Declaring victory without runtime evidence (tests, traces, or user confirmation).
- ❌ Silently guessing `[unsure]` findings — list them separately.
- ❌ Skipping the checklist because "this file is small".

## Since

Introduced in [[v0.1.0]].

## See also

- [[Commands]] (aggregate)
- [[Checklists]]
- [[Confidence-Labels]]
- [[Kasi-Security]]
