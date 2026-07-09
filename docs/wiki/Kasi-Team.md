# /kasi-team

> HYBRID panel brainstorm + mandatory user decision gate + parallel dispatch + QA synthesis. Decides the approach before executing it.

## Usage

```
/kasi-team                      # default: panel N=3, surface 2-3 options
/kasi-team 2                    # constrain to 2 brainstorm options
/kasi-team <mission>            # explicit mission (skip Rule 1 narrowing)
/kasi-team --fast               # skip the refinement round; QA pass NOT skipped
```

The one-line difference from `/kasi-multi` / `sudo`: those dispatch specialists to **execute** a known approach in parallel. `/kasi-team` runs a panel to **propose** approaches first, has the **user decide**, then executes.

## What it does

- Spawns a small brainstorm panel (parallel, one message) — Lead (`architect-planner`) + a domain lens picked by mission (security/perf/migration) + a Pragmatist (`general-purpose`, "fastest safe path").
- Panel agents propose only — they do not write code.
- Synthesizes panel output into 2-3 options with trade-offs, presents an options table.
- **Mandatory user decision gate** — never auto-picks, except under `--fast`.
- After the pick: dispatches implementation specialists in parallel, reusing `/kasi-multi` fan-out mechanics (same dispatch brief format, same tier caps).
- Runs a mandatory QA pass (`audit-specialist --focus=quality`) — always last, never skipped.

## Flow

1. **Phase 1 — Brainstorm panel.** Default N=3: Lead + domain lens (skipped if mission has no matching concern) + Pragmatist. Each gets a dispatch brief with `EXPECTED OUTPUT: one proposed approach + top 3 risks` and `DONE WHEN: approach described in plain text, no code written`.
2. **Phase 2 — Synthesis + decision gate.** Main merges panel outputs into an options table (name / 1-line approach / key risk / est. dispatch size). Asks: "Which option? (number, or `refine` for one more round)."
3. **Refinement cap = 1 round** for this phase (tighter than the framework default of 3 — prevents option proliferation). Confidence-halt still applies: same-or-lower confidence on refine → halt, re-present originals.
4. **Phase 3 — Dispatch + QA.** After the pick, Main writes dispatch briefs and sends implementation specialists in parallel (reuses `/kasi-multi` N-selection, Haiku cap N=4). `PRIOR CONTEXT COMPLETED:` carries the panel outputs + chosen option. `audit-specialist --focus=quality` runs last as a dedicated QA pass, separate from any audit slot in `/kasi-multi`'s roster.
5. Main synthesizes one final report: approach taken, files changed, QA findings, suggested next step.

## Team composition

| Role | Phase | Agent | Default tier | Notes |
|---|---|---|---|---|
| **Lead** (core) | 1 | `architect-planner` | Sonnet (Opus if multi-system) | proposes approach + risks |
| Domain lens (dynamic) | 1 | `audit-specialist --focus=security\|perf` / `migration-specialist` | per registry | only if mission matches |
| Pragmatist (dynamic) | 1 | `general-purpose` | Sonnet | "fastest safe path" perspective |
| Implementation specialists (dynamic) | 3 | from Specialist Agent Registry | per-agent default | picked by chosen option's needs |
| **QA reviewer** (core) | 3 | `audit-specialist --focus=quality` | Sonnet | mandatory, always last |

**Core** = Lead + QA (always present). **Dynamic** = domain/pragmatist lenses + implementation specialists (picked per mission). No new agent files — Lead and QA are dispatch personas over the existing registry.

## Panel size selection

| Panel N | When |
|---|---|
| 2 | Single-concern mission (Lead + Pragmatist) |
| **3 (default)** | Most missions |
| 4 | Cross-cutting mission (e.g. schema + security + perf) |

Panel N is **not** dispatch N — dispatch N follows `/kasi-multi` rules (2-10).

## When to use

- The mission has real uncertainty about *which approach* to take — architecture choices, migration strategy, build-vs-buy.
- You want structured trade-off comparison and a decision checkpoint before implementation starts.

## When NOT to use

- A one-line fix — overhead exceeds benefit. Use [[Kasi-Fix]] or `/kasi-multi 2`.
- The approach is already known — use `/kasi-multi` or `sudo` to execute it directly.

## Tier behavior

- **Opus** — panel up to N=4, Lead may run on Opus for multi-system missions, full fan-out dispatch.
- **Sonnet** (default) — panel N=3, 1 refinement round, dispatch per `/kasi-multi` Sonnet rules.
- **Haiku** — panel **N=2** (Lead + Pragmatist only, domain lenses skipped), **0 refinement rounds**, dispatch cap N=4. **Refuses** missions needing a security/migration lens — directs to Sonnet/Opus.

## Anti-patterns

- ❌ Running `/kasi-team` on a one-line fix.
- ❌ Skipping the decision gate and auto-picking Option 1 (unless `--fast` is explicit).
- ❌ More than 1 refinement round without the user explicitly asking.
- ❌ Panel agents that write code — approach + risks only.
- ❌ Confusing this with `sudo` / `/kasi-multi` — those execute a known approach; this decides it first.

## Since

Introduced in [[v0.15.0]].

## See also

- [[Commands]] (aggregate)
- [[Kasi-Multi]] — fan-out mechanics reused in Phase 3
- [[Kasi-Cascade]] — tier-routed alternative when the approach is already known
- [[Dispatch-Brief]]
- [[Master-Orchestrator]]
