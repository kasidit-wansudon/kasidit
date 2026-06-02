---
description: Team mode — HYBRID panel brainstorm + user decision gate + parallel dispatch + QA synthesis. Assembles a CORE team (lead, qa) plus DYNAMIC specialists for the mission. Use when you want structured options before implementation, not just parallel execution.
---

Assemble a dev team around the current mission. Main orchestrates a small **panel** of role-agents that each propose an approach from their own perspective; Main **synthesizes** their input into a few options with trade-offs and asks the **user to choose**. After the user picks, Main **dispatches** implementation specialists in parallel (reusing `/kasi-multi` fan-out), runs a **QA pass**, and synthesizes one final report.

The one-line difference from `/kasi-multi` and `sudo`: they dispatch specialists to **execute** a known approach in parallel; `/kasi-team` first runs a panel to **propose** approaches, then has the user **decide**, then executes. Structured decision before implementation.

## Usage

```
/kasi-team                      # default: panel N=3, surface 2-3 options
/kasi-team 2                    # constrain to 2 brainstorm options
/kasi-team <mission>            # explicit mission (skip Rule 1 narrowing)
/kasi-team --fast               # skip the refinement round; pick after first synthesis. Panel stays N=3. QA pass NOT skipped.
```

## Phase 1 — Brainstorm panel

Main spawns a small **panel** in parallel (one message, parallel tool calls — per `/kasi-multi` dispatch rule). Default 3 roles:

- **Lead** — `architect-planner`. Proposes an architecture + top 3 architectural risks.
- **Domain lens** — picked by mission: `audit-specialist --focus=security` (auth / data / crypto), `migration-specialist` (schema / framework change), `perf` lens via `audit-specialist --focus=perf` (hot path). Skipped if the mission has no matching concern — Main narrates the skip.
- **Pragmatist** — `general-purpose`, brief scoped to "the fastest safe path" + top 3 pragmatic risks (complexity / maintenance).

Each panel agent gets a dispatch brief (`MISSION / INPUTS / CONSTRAINTS / EXPECTED OUTPUT = "one proposed approach + top 3 risks from your perspective" / DONE WHEN = "approach described in plain text, no code written"`). Panel agents **do not write code** — they propose.

Panel failures (an agent returns no coherent approach) do **not** count against the Mission Counter — Main replaces that output with a placeholder row.

## Phase 2 — Synthesis + user decision gate

Main merges the panel outputs into an options table and presents it:

```
Option 1 — <name>   | <1-line approach> | key risk: <…> | est. dispatch: <N> agents
Option 2 — <name>   | <1-line approach> | key risk: <…> | est. dispatch: <N> agents
```

Then asks: **"Which option? (number, or `refine` for one more round)"**

The decision gate is **mandatory** — Main never auto-picks (except under `--fast`, which picks after the first synthesis without offering refinement).

**Refinement Counter cap = 1 round** for this phase (tighter than the framework default of 3 — more than one "what if" round produces option proliferation, not clarity). If the user requests a second round, Main surfaces:

> Refinement cap reached (max 1 round). Final options below — choose a number, or `/kasi-team --fast` to take Option 1 and proceed.

Confidence-halt still applies: if refined options are same-or-lower confidence than the first synthesis, Main halts and re-presents the originals.

## Phase 3 — Dispatch + QA

After the user picks, Main writes dispatch briefs and sends the implementation specialists. **This phase reuses `/kasi-multi` mechanics** — N selection rules, dispatch brief format (with `DONE WHEN` + `PRIOR CONTEXT` `COMPLETED:`/`OPEN:` split), Haiku cap N=4, parallel-not-serial, synthesize-do-not-forward. See `kasi-multi.md` for the full spec; do not reinvent it here.

`PRIOR CONTEXT COMPLETED:` carries the panel outputs + chosen option so specialists don't re-derive the approach.

When all specialists return, Main dispatches **`audit-specialist --focus=quality`** as a dedicated **QA pass** (mandatory, always last). This is separate from any audit slot in `/kasi-multi`'s default roster — it reviews the combined result of the chosen approach.

Main then synthesizes one user-facing report: approach taken, files changed, QA findings (HIGH / MED / LOW + confidence labels), suggested next step.

## Team composition

| Role | Phase | Agent | Default tier | Notes |
|---|---|---|---|---|
| **Lead** (core) | 1 | `architect-planner` | Sonnet (Opus if multi-system) | proposes approach + risks |
| Domain lens (dynamic) | 1 | `audit-specialist --focus=security\|perf` / `migration-specialist` | per registry (Opus for security/migration) | only if mission matches |
| Pragmatist (dynamic) | 1 | `general-purpose` | Sonnet | "fastest safe path" perspective |
| Implementation specialists (dynamic) | 3 | from Specialist Agent Registry | per-agent default | picks = chosen option's needs |
| **QA reviewer** (core) | 3 | `audit-specialist --focus=quality` | Sonnet | mandatory, always last |

**Core** = Lead + QA reviewer (always present). **Dynamic** = domain/pragmatist lenses + implementation specialists (picked per mission). Main narrates which dynamic roles activated and why.

No new agent files: Lead and QA are dispatch personas over existing registry agents (`architect-planner`, `audit-specialist`).

## Panel size selection

| Panel N | When |
|---|------|
| 2 | Single-concern mission (Lead + Pragmatist) |
| **3 (default)** | Most missions — Lead + one domain lens + Pragmatist |
| 4 | Cross-cutting mission (e.g. schema + security + perf) |

Panel N is **not** dispatch N. Dispatch N follows `/kasi-multi` rules (2–10).

## Tier behavior

- **Opus** — panel up to N=4, Lead may run on Opus for multi-system missions, full fan-out dispatch.
- **Sonnet** (default) — panel N=3, 1 refinement round, dispatch caps per `/kasi-multi` Sonnet rules.
- **Haiku** — panel **N=2** (Lead + Pragmatist only; skip domain lenses — Haiku synthesis is weak), **0 refinement rounds** (skip to dispatch on first synthesis), dispatch cap N=4. Warn on entry:
  > [kasidit] Haiku tier: panel reduced to N=2, refinement skipped, dispatch cap=4. `--fast` is implicit.
  If the mission needs a security or migration lens, **refuse** on Haiku:
  > This mission needs a security/migration lens — Haiku can't reliably synthesize it. Use Sonnet/Opus, or narrow the scope.

## Counter interaction

- **Refinement Counter** (SKILL.md) — capped at **1** for the brainstorm phase. Halt on same-or-lower confidence.
- **Mission Counter** (SKILL.md) — applies normally to the dispatch phase. Panel-phase agent failures do not increment it.

## Rules

- **Brief format is non-negotiable** — every panel and dispatch agent gets a full dispatch brief.
- **Panel agents may not write code** — they propose approaches and list risks only (`DONE WHEN` enforces this).
- **User decision is required before dispatch** — never auto-pick (except explicit `--fast`).
- **Dispatch is parallel**, not serial — all implementation specialists in one message.
- **QA pass is mandatory** — never skip to save tokens; `--fast` skips refinement only.
- **Core roles (Lead + QA) are always present** regardless of `--fast`.
- **Master Orchestrator Rule applies** — Main synthesizes, never executes; no source edits beyond the top-level index set.

## Anti-patterns

- ❌ Running `/kasi-team` on a one-line fix — overhead exceeds benefit. Use `/kasi-fix` or `/kasi-multi 2`.
- ❌ Skipping the decision gate and auto-picking Option 1 (unless `--fast` is explicit).
- ❌ More than 1 refinement round without the user explicitly asking — the option-proliferation trap.
- ❌ Spawning Opus-tier panel agents on every mission — Lead defaults to Sonnet; escalate only for multi-system.
- ❌ Panel agents that write code — approach + risks only.
- ❌ Confusing `/kasi-team` with `sudo` / `/kasi-multi` — those execute a known approach; this decides the approach first.
- ❌ On Haiku, running a 4-role panel — synthesis collapses. Cap at 2.

## Examples

### Design + build a feature

```
/kasi-team build /kasi-search as semantic search over .kasidit/knowledge/
```

→ Panel N=3: `architect-planner` (vector-embed approach), `general-purpose` pragmatist (BM25 + cache), security lens skipped (no auth boundary). Main surfaces 2 options. User picks Option 2 (BM25 + cache). Dispatch: `general-purpose` (indexer) + `general-purpose` (query) + `test-writer`, parallel. QA: `audit-specialist --focus=quality`. Report = files changed + QA findings + next step.

### Cross-cutting mission

```
/kasi-team add multi-tenant row-level security to kas-sass on MySQL 8
```

→ Panel N=4: `architect-planner` (Lead), `audit-specialist --focus=security` + `migration-specialist` (domain lenses, mission touches auth + schema), `general-purpose` (pragmatist). 2 options surface. User picks. Dispatch includes `migration-specialist` + `audit-specialist --focus=security` in the implementation phase. QA pass last.

## See also

- `/kasi-multi` — fan-out mechanics reused in Phase 3 (dispatch)
- `/kasi-cascade` — tier-routed alternative when the approach is known and you want Opus to plan + Sonnet to work
- Master Orchestrator Rule, Specialist Agent Registry, dispatch brief format, Refinement Counter — all in SKILL.md
