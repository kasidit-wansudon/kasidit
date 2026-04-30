# Tier-aware

> Opus reasons. Sonnet works. Haiku greps. Rules diverge by model.

Kasidit adapts its behavior to the model tier running the session. Weaker reasoning triggers tighter rules; stronger reasoning unlocks creative latitude. This is the operational intent behind the framework's tier awareness.

The full technical spec of what changes per tier lives on [[Model-Tiers]]. This page is the short summary.

## The core idea

> When reasoning is weak, scaffolding is strong.

A senior engineer carries a mental model of the system. AI pattern-matches surface similarity. The gap is largest on Haiku-class models; smallest on Opus-class. Kasidit closes that gap with **external scaffolding** — checklists, confidence labels, patterns, and hub knowledge — that lets a smaller model execute reliably without needing bigger reasoning.

## What changes by tier

| Behavior | Opus | Sonnet | Haiku |
|---|---|---|---|
| Architecture decisions | ok | ok | refuse — requires Opus/Sonnet or user |
| Creative refactor | ok | ok | copy established patterns only |
| Per-agent scope | 1 module | 1 module | 1 file |
| Confidence labels | recommended | recommended | **mandatory** on every finding |
| Verifier pass on review | optional | recommended on security | **mandatory** |
| Hand-coded UI mockups | small ok | avoid | **never** — always Claude Design |
| Memory-based library coding | ok for trivial | cite docs | **never** — must fetch or cite cache |
| Counter before Wave 1 | 4 rounds | 3 rounds | 2 rounds |
| Fan-out N cap (`/kasi-multi`) | no cap | prefer 4 | **cap at 4** |

## Tier detection

The skill detects the tier from session context. When ambiguous, it assumes Haiku rules — it costs nothing to be more disciplined on Opus.

Force override in any session:

```
tier opus
tier sonnet
tier haiku
```

## Why Haiku rules are harder

Haiku does not have weaker reasoning *in general* — it has weaker **ungrounded** reasoning. Given a checklist it executes faithfully. Given an open question it confabulates.

Kasidit converts as many open questions as possible into checklist execution:

- Security audit → [[Checklists]] (`security-<stack>.md`)
- Project patterns → `PATTERNS.md`
- Version-matched knowledge → `.kasidit/knowledge/`
- Hub scaffolding → Centerlite ([[Gravity-Pattern]])

With those files in place, Haiku performs on many tasks comparably to Sonnet at a fraction of the cost. Without them, Haiku hallucinates.

## Subsystems that take tier into account

- [[Master-Orchestrator]] — fan-out cap at N=4 on Haiku; synthesis collapses above that
- [[Multi-Agent-Orchestration]] — 1 file per agent on Haiku, 1 module on Opus/Sonnet; verifier pass mandatory on Haiku
- [[Gravity-Pattern]] — Haiku pulls aggressively during `/kasi-init`; promotes rarely
- [[UI-Override-Mode]] — Haiku counter caps at 2 rounds; Opus at 4
- [[Claude-Design-Integration]] — Haiku must route visual work; Opus may hand-code small sketches

## Tier Cascade

Introduced in [[v0.8.0]]. Route sub-tasks across tiers within a single mission:

```
Opus: plan
  ↓
Sonnet: implement
  ↓
Haiku: audit by checklist
  ↓
Opus: synthesize
```

Invoked via [[Kasi-Cascade]] when the mission is large enough to benefit from multi-tier routing.

## v0.10 — Mode gate × Tier

Mode (`/kasi off|router|lite|full|ultra`) and Tier (Opus / Sonnet / Haiku) are orthogonal. Combined behavior:

| Mode | Opus | Sonnet | Haiku |
|------|------|--------|-------|
| `off`    | minimal | minimal | minimal |
| `router` | classifier only | classifier only | classifier only — but stricter escalation thresholds |
| `lite`   | Rule 1 + Rule 11 | same | same + checklist auto-load on review/audit |
| `full`   | full framework | full framework | full + verifier pass mandatory + 1-file-per-agent + N≤4 fan-out cap |
| `ultra`  | full + master self-check | same | same — but prefer escalating tier rather than running ultra on Haiku |

**Recommendation per tier:**

- Opus → default `router`, escalate to `full` for audits and refactors
- Sonnet → default `router`, escalate to `lite` for routine work, `full` for cross-file
- Haiku → default `lite` (always-on Rule 1 + Rule 11), escalate to `full` for any audit. Avoid `ultra` — prefer Sonnet/Opus for high-stakes work.

See [[Kasi-Mode]] for switching and [[Backend-Hooks]] for runtime enforcement.

## See also

- [[Model-Tiers]] — full technical spec
- [[Master-Orchestrator]] — what the master rule does differently per tier
- [[Kasi-Mode]] — mode toggle (v0.10)
- [[Backend-Hooks]] — runtime hooks (v0.10)
- [[Checklists]] — why checklists are Haiku's single biggest enabler
- [[v0.3.0]] — when tier adaptation was introduced
- [[v0.8.0]] — Tier Cascade orchestration
- [[v0.10.0]] — Mode gate adds another axis on top of tier
