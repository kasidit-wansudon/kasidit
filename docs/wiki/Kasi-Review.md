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
- Auto-escalates Mode `router` → `full` for the duration; reverts on completion (v0.10).
- Dispatches `audit-specialist --focus=quality` (v0.10 — replaces standalone `code-reviewer`) per file (Haiku) or per module (Opus / Sonnet).
- Main synthesizes findings with `[high | medium | low | unsure]` confidence labels.
- Emits HIGH / MED / LOW severity buckets plus a Top-5 actionable list.

## Flow

1. Ask user which module / file / commits — refuse vague scope.
2. Detect domain → load matching `CHECKLISTS/*.md`.
3. Auto-escalate Mode → `full` (v0.10).
4. Dispatch `audit-specialist --focus=quality`: 1 per file on Haiku, 1 per module on Opus / Sonnet.
5. Each agent scans mechanically against the checklist.
6. Main aggregates + deduplicates + labels confidence.
7. Output severity-bucketed findings + Top-5 priority.
8. Emit `[kasidit-log] kind=review-<stack> mode=full turns=N outcome=...` for router memory.
9. If counter hits 4 (Opus) / 2 (Haiku), escalate or hand back.
10. Revert to prior Mode.

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
- [[Agent-Audit-Specialist]] — the agent dispatched (`--focus=quality`)
- [[Kasi-Mode]] — auto-escalation contract
- [[Kasi-Security]]
