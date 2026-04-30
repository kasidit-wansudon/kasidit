# Getting Started

Your first Kasidit mission in under five minutes.

## Prerequisites

- Claude Code installed
- The plugin installed — see [[Installation]]

## 1. Init a project

In any git repo (or plain directory):

```
/kasi-init
```

Answer the prompts. The agent detects your stack (Laravel / Vue / Go / Python / etc.), scaffolds `.kasidit/`, pulls stack-matched defaults from Centerlite if any, and offers a light review.

The init flow asks **one Mode question** (v0.10) — pick `1` (router, default), `2` (lite), or `3` (full). Anything else falls back to router. See [[Kasi-Mode]] for what each level loads.

## 1b. (Optional) Switch Mode later

```
/kasi router    # default — thin classifier, escalates only when needed
/kasi lite      # always-on Rule 1 (mission narrowing) + Rule 11 (confidence labels)
/kasi full      # full framework — for audits, refactors, new features
/kasi save      # persist current Mode to .kasidit/config.json
```

Heavy commands (`/kasi-review`, `/kasi-security`, `/kasi-fix`, `/kasi-ui`, `/kasi-multi`, `/kasi-cascade`) auto-escalate to `full` for the duration of the mission, then revert. Casual chat stays in `router`.

## 2. State a mission

Kasidit missions are **narrow and verifiable**. Compare:

- ❌ "check my backend"
- ❌ "make the dashboard better"
- ✓ "audit `SalesController.php` for SQL injection — only HIGH severity"
- ✓ "fix the N+1 on `GET /api/sales` — first page load must drop below 300ms"

If you say the first, the agent will refuse and give you numbered options to narrow. If you say the second, it begins.

## 3. Watch the flow

For any strong-work mission, the **master agent does not write code**. It narrows, dispatches a specialist, and synthesizes. You will see agent hand-offs — that is intentional (see [[v0.9.1]]).

You will also see:

- **Confidence labels** `[high / medium / low / unsure]` on non-trivial findings
- **File:line references** instead of prose
- **Runtime verification** — the agent asks you to confirm the fix works, not just that the code compiles

## 4. Common shapes of missions

### Bug fix

```
/kasi-fix
```

Mandatory `git log --grep` and `git log -S` before any fix (Rule 2.6). Minimal-change fix with regression test.

### Review / audit

```
/kasi-review
/kasi-security
```

Checklist-driven. Top 5 findings with confidence + priority.

### UI fix

```
/kasi-ui
```

Requires visual target (screenshot / CSS values / Claude Design mockup). One change per round. Cache-aware — you will be asked to hard-refresh and confirm the new version loaded.

### Deep research

Say "research <topic>" or name a library. The `deep-researcher` specialist fetches official docs (Trust Hierarchy: source → official docs → release notes → blogs), caches snippets to `.kasidit/knowledge/`.

### Bootstrap a new project

```
/kasi-init
```

### Share learnings across projects

```
/kasi-promote pattern <name>     # lift to Centerlite
/kasi-pull checklist <name>      # fetch from Centerlite
/kasi-sync                       # audit drift
```

See [[Gravity Pattern]].

## 5. When things get stuck

The **mission counter** tracks failures. Each failure = runtime did not pass.

- **1–4 rounds:** agent retries with different hypotheses
- **Round 4 (Opus) / 3 (Sonnet) / 2 (Haiku):** Wave 1 — agent asks you for bullet points on expected outcome
- **Round 8:** Wave 2 — agent stops, outputs full state, hands back to you

You can also say:

- `task status` — show counter + pending items
- `wave 2` — force escalation now
- `forget that` — drop the last failed attempt

## 6. What the agent writes down

Every non-trivial fact goes into:

- `.kasidit/MEMORY.md` — project facts
- `.kasidit/PATTERNS.md` — project patterns to copy
- `.kasidit/knowledge/<stack>-<version>-<topic>.md` — cached doc snippets
- `.kasidit/MISSION.md` — current mission state

Across projects, the global hub (Centerlite) accumulates:

- `~/.claude/skills/kasidit/center/rules.jsonl` — accumulated user rules (v0.10 — emit-driven)
- `~/.claude/skills/kasidit/center/patterns.jsonl` — cross-project patterns
- `~/.claude/skills/kasidit/center/route-memory.jsonl` — router learnings (v0.10)
- `~/.claude/skills/kasidit/center/memory.jsonl` — cross-session facts (v0.10)
- `~/.claude/skills/kasidit/center/logs/*.jsonl` — every prompt you have typed (PII — keep local)

`kasidit-record.py` (Stop hook) parses the AI's emit lines (`[kasidit-log]`, `[kasidit-pattern]`, `[kasidit-memory]`, `[kasidit-rule]`) and appends to the matching store. See [[Backend-Hooks]] for the contract.

## 7. Next reads

- [[Commands]] — full reference
- [[Kasi-Mode]] — Mode levels (off / router / lite / full / ultra)
- [[Backend-Hooks]] — runtime hooks (v0.10)
- [[Model Tiers]] — what changes on Opus vs Sonnet vs Haiku
- [[Gravity Pattern]] — the hub-and-orbit knowledge system
- [[FAQ]]
