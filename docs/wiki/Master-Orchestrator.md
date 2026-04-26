# Master Orchestrator

> The main agent plans and delegates. Specialists execute.

Formalized in [[v0.9.1]]. The Master Orchestrator is not a new agent — it is a **role the main agent is locked into** the moment a mission qualifies as strong work (multi-file change, migration, perf hunt, security audit, new feature, deep research).

## Why this rule exists

When the master both plans and executes, context pollution compounds. The agent loads a dozen files "just to check", forms hypotheses from half-loaded fragments, then implements on top of polluted reasoning. Half-loaded files + partial greps + intermediate hypotheses → hallucination.

Isolation = clean handoffs = fewer hallucinations. This is Kasidit Rule 1 (*one mission, one focus*) applied at the orchestration layer. See [[v0.9.1]] for the full rationale and release notes.

## What the master MAY do

- Narrow the mission to one verifiable outcome; confirm scope with user
- Detect domain (backend / UI / review / design) and tier (Opus / Sonnet / Haiku)
- Read the **top-level index set only**: `CLAUDE.md`, `PATTERNS.md`, `DESIGN_SYSTEM.md`, `สารบัญ`, `.kasidit/knowledge/` index
- Pick the specialist from the [Specialist Registry](#specialist-registry)
- Write the [dispatch brief](#dispatch-brief-format)
- Synthesize specialist outputs into a user-facing report (dedupe, rank by severity × confidence)
- Decide next step: same specialist again, different specialist, done, or ask user

## What the master MAY NOT do

- ❌ Write code
- ❌ Edit files
- ❌ Run tests or servers
- ❌ Read source files beyond the top-level index set above
- ❌ Search, grep, or glob beyond initial scope detection
- ❌ Fetch docs — delegate to `deep-researcher`
- ❌ Write migrations — delegate to `migration-specialist`

If the master catches itself doing any of the above → **stop, spawn a specialist**, pass the accumulated context to it.

## Exceptions — master may act directly

Narrow, documented exceptions only:

- Trivial one-line fix on a single file the user explicitly pointed to
- Answering a pure question with no code change
- Reading the top-level index files listed above
- Writing the final user-facing summary

Everything else → delegate.

## Specialist Registry

**8 active + 3 deprecated stubs (v0.10).** Each agent has its own page (link below) for input shape, output block, and examples.

| Agent | Trigger | Scope |
|---|---|---|
| [[Agent-Architect-Planner]] | new feature / refactor > 2 files | plan only; no code; trade-offs + open questions |
| [[Agent-Audit-Specialist]] (v0.10) | PR / OWASP / CVE / N+1 / pre-merge / pre-scale | unified audit via `--focus=quality\|security\|perf\|all` — replaces 3 prior agents |
| [[Agent-Bug-Hunter]] | error / crash / wrong output / regression | root-cause + minimal fix; mandatory `git log --grep` / `git log -S` before patching |
| [[Agent-Deep-Researcher]] | library / API / framework research | trust hierarchy source→docs→notes→blogs; caches to `.kasidit/knowledge/` |
| [[Agent-Legacy-Specialist]] | legacy PHP / old framework / no-test code | legacy-safe refactor |
| [[Agent-Migration-Specialist]] | schema change / framework upgrade / backfill | expand-contract phases; rollback per phase; GREEN/YELLOW/RED risk class |
| [[Agent-Refactor-Surgeon]] | extract / rename / split / inline | zero behavior change; test-parity verified |
| [[Agent-Test-Writer]] | add tests / regression after fix / coverage gap | one target per call; regression case mandatory after bug fix |

**Deprecated stubs** (kept for name resolution only — removed in v0.11):

| Stub | Use this instead |
|---|---|
| [[Agent-Code-Reviewer]] | `audit-specialist --focus=quality` |
| [[Agent-Security-Auditor]] | `audit-specialist --focus=security` |
| [[Agent-Perf-Profiler]] | `audit-specialist --focus=perf` |

## Dispatch brief format

Every specialist invocation must pass a structured brief. No brief → no dispatch.

```
MISSION: <one sentence, verifiable outcome>
INPUTS:
  - <file paths, symptoms, measurements, versions>
CONSTRAINTS:
  - <deadline, compat, perf budget>
EXPECTED OUTPUT:
  - <matches the agent's documented output block>
PRIOR CONTEXT:
  - <findings from earlier specialists, if any>
```

Rules:

- `MISSION` must be a **verifiable outcome**, not a directive. "Fix SQL injection in SalesController::exportCancelIMEI" — not "look at sales code".
- `INPUTS` is literal: file paths, error messages, measured numbers, version strings. No prose hand-waving.
- `EXPECTED OUTPUT` must match the agent's documented output block on its individual `Agent-*` wiki page (e.g. [[Agent-Bug-Hunter]], [[Agent-Audit-Specialist]]).
- `PRIOR CONTEXT` carries forward findings from earlier specialists in the same mission — the master is the only source of this continuity.

"Do stuff" prompts reaching a specialist with ambiguous scope is a v0.9.1 anti-pattern. See [[Dispatch-Brief]] for the full template and per-agent variations.

## Fan-Out Mode

When the mission benefits from parallel contexts instead of a dependency chain, the master fans out — dispatching N specialists in a single message. Introduced in [[v0.9.2]].

```
/kasi-multi [N] [mission]       # explicit
sudo <mission>                    # shorthand for N=6 + skip clarifying Qs
sudo <N> <mission>                # shorthand with N
```

`sudo` is a **pacing signal, not a permission escalation**. It skips clarifying questions the master would normally ask and narrates assumptions instead. It does **not** bypass the destructive-op confirmation rule and does **not** override tier caps.

Default N=6 roster: planner/researcher, 3 workers, verifier, reviewer. Swappable by mission kind.

Full flow, roster details, and synthesis rules are in [[Multi-Agent-Orchestration]] and [[Kasi-Multi]].

## Per-tier caps

Synthesis cost scales with N. Larger N is not better.

| Tier | Fan-out behavior |
|---|---|
| Opus | Full fan-out. Synthesis is where Opus earns its cost. Fan out freely when the mission justifies it. |
| Sonnet | Default. Prefer N=4 on large contexts. N=6 on medium. |
| Haiku | **Cap N ≤ 4.** Haiku synthesis collapses with more than 4 inputs. On Haiku, `sudo` implicitly caps at 4 even if the user requests 8. |

Haiku also requires a **mandatory verifier pass** on review-style fan-outs — a second agent reads the first set's findings and removes non-reproducible items.

## Anti-patterns

- ❌ Master writing code on a strong-work mission — delegate to the specialist
- ❌ Master reading source files beyond the top-level index — delegate
- ❌ Invoking a specialist without a dispatch brief
- ❌ Specialist working outside its documented scope — refuse, return to master
- ❌ Main agent loading file contents "just to check" — delegate
- ❌ Running Haiku fan-out review without a verifier pass
- ❌ Fanning out on a one-line fix — overhead > benefit
- ❌ Forwarding raw agent outputs to the user without synthesis
- ❌ Using `sudo` to bypass destructive-op confirmation

## Mode-gated activation (v0.10)

The Master Orchestrator rule applies fully under `/kasi full` and `/kasi ultra`. Lower modes relax it:

| Mode | Master Orchestrator rule |
|------|--------------------------|
| `off`    | Inactive. Master may execute directly. |
| `router` | Inactive for routine tasks; auto-escalates to `full` when message matches heavy-work keywords. |
| `lite`   | Soft — master tries to delegate but may execute trivial single-file edits directly. |
| `full`   | **Hard — full rule applies.** Strong-work missions must delegate. |
| `ultra`  | **Hardest** — master self-checks every turn; specialist call requires complete dispatch brief. |

See [[Kasi-Mode]] for switching modes and [[Backend-Hooks#kasidit-verify]] for runtime detection of master orchestrator violations (a `[high]` claim paired with direct `Edit` / `Write` / `Bash` triggers a downgrade notice in v0.10).

## v0.10 agent registry update

The audit roles consolidated:

| Old agent (deprecated) | New invocation |
|---|---|
| `code-reviewer` | `audit-specialist --focus=quality` |
| `security-auditor` | `audit-specialist --focus=security` |
| `perf-profiler` | `audit-specialist --focus=perf` |

Specialist registry is now **8 active + 3 stubs** (stubs delegate to `audit-specialist` and disappear in v0.11). Stubs exist only for name-resolution; **no automatic mapping** — master must invoke `audit-specialist --focus=<lens>` explicitly. See [[Agent-Audit-Specialist]].

## See also

- [[Multi-Agent-Orchestration]] — how specialists run under the hood, sub-agent pattern, tier-specific rules
- [[Dispatch-Brief]] — full template + per-agent variations
- [[v0.9.1]] — release notes, why the rule exists, migration
- [[v0.10.0]] — Mode gate + audit-specialist consolidation + runtime verifier hook
- [[Kasi-Mode]] — `/kasi off|router|lite|full|ultra` toggle
- [[Backend-Hooks]] — `kasidit-verify` runtime check for master orchestrator violations
- [[Gravity-Pattern]] — Centerlite + Dcenterlite knowledge sync that specialists read from
- [[Checklists]] — mechanical audit lists specialists run instead of reasoning
- [[Kasi-Multi]] — `/kasi-multi` and `sudo` command flow
