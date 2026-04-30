# /kasi-cascade

> Tier cascade orchestration — Opus plans, Sonnet writes, Haiku greps. For missions too large for a single tier.

## Usage

```
/kasi-cascade "<mission>"
./orchestration/tier_cascade.sh "<mission>"
python orchestration/python/orchestrator.py "<mission>"
```

## What it does

- Decomposes a mission into subtasks at the Opus tier (plan phase).
- Routes each subtask to the cheapest tier that can handle it: grep/read → Haiku, work → Sonnet, nested plan → Opus.
- Verifies outputs at Opus before merge.
- Produces a plan JSON, per-subtask outputs, final git diff, and a verifier verdict.

## Flow

1. Opus decomposes the mission into typed subtasks (plan JSON, no prose).
2. Dispatch workers by type: grep → Haiku, read → Haiku, work → Sonnet, nested plan → Opus.
3. Opus verifies every worker output.
4. Verifier emits verdict JSON: PASS / FAIL / UNSURE.
5. Main merges (PASS) or escalates (FAIL / UNSURE).

## When to use

- Mission spans more than 3 files.
- Mission has more than 5 distinct subtasks.
- Cross-file refactor.
- Multi-module bug fix.

## When NOT to use

- Single-file edit — use [[Kasi-Fix]].
- One-line change.
- Trivial task — cascade overhead outweighs savings.

## Execution paths

- **A. In Claude Code (simulated)** — Opus explains the cascade plan; user runs subtasks manually via `claude --model X`.
- **B. Bash orchestrator** — `./orchestration/tier_cascade.sh "mission"`.
- **C. Python API** — `python orchestration/python/orchestrator.py "mission"` (needs `ANTHROPIC_API_KEY`).

## Cost (Path B/C)

- Typical mission: $0.20–0.50.
- All-Opus comparison: 5–10× more expensive for equivalent output.

## Exit codes

- `0` — PASS, merge recommended.
- `2` — FAIL, review + retry.
- `3` — UNSURE, user review required.

## Anti-patterns

- ❌ Planner producing prose instead of valid JSON — workers cannot route.
- ❌ Workers exceeding their tier budget (Haiku running a nested plan).
- ❌ Skipping the verifier to save cost — verifier is the last gate.
- ❌ Using cascade for a one-line fix.

## Since

Introduced in [[v0.8.0]].

## See also

- [[Commands]] (aggregate)
- [[Multi-Agent-Orchestration]]
- [[Kasi-Multi]]
- [[Model-Tiers]]
