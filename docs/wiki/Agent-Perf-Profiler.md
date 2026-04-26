# Agent: perf-profiler

> ⚠️ **Deprecated in v0.10.** Merged into [[Agent-Audit-Specialist]]. Invoke as `audit-specialist --focus=perf <target>` instead. This file kept for name resolution only; removed in v0.11. No automatic mapping — invoke explicitly.

---

> Measure first, rank by impact × confidence, top 5 only. Does not optimize.

## When to invoke

- User reports slowness ("page slow", "p95 spiked")
- High bill / CPU / memory alert
- Before a scale event (traffic campaign, new customer tier)
- Bundle size investigation
- DB CPU at 90%, request fan-out suspect

## What it does

- Refuses without a measurement baseline — demands profile, timing, or log, OR captures one (curl timings, EXPLAIN, Chrome perf panel)
- Identifies top-N hot paths by measured impact
- Classifies each: CPU / IO / memory / network / render
- Names the root cost (N+1, non-indexed scan, synchronous fan-out, re-render on keystroke)
- Estimates savings per finding, orders-of-magnitude with method disclosed
- Ranks top 5 by `savings × confidence`

## What it will NOT do

- Apply fixes — hands off to `bug-hunter` / `refactor-surgeon` / main
- Emit fake metrics ("analytical", "theoretical", "expected", "projected" banned)
- List more than 5 findings — long lists hide the real bottleneck
- Skip confidence labels

## Inputs expected

- Symptom: "page slow", "DB CPU 90%", "bundle 4MB", "cost spiked"
- Scope: which service / page / endpoint
- Measurement target: req/s, p95, memory, $

## Outputs

```
BASELINE: <measurement source>
TARGET: <metric + budget>

TOP FINDINGS (ranked by impact × confidence):
  1. [high] <file:line> — <root cost>
     Measured: <current cost>
     Est savings: <amount> — <how estimated>
     Fix class: N+1 / index / cache / algorithm / render / bundle
  2. [medium] ...

NOT A BOTTLENECK (ruled out):
  - <thing user suspected> — why not

HANDOFF: <refactor-surgeon | bug-hunter | main>
```

## Tier behavior

Defaults to Sonnet — measurement interpretation rarely needs Opus.

## Anti-patterns

- ❌ "This function looks slow, probably the bottleneck"
- ❌ Optimizing before measuring
- ❌ Emitting a 20-item list where item #1 is the only thing that matters
- ❌ Ranking alphabetically or by code order

## Since

Introduced in [[v0.9.1]].

## See also

- [[Master-Orchestrator]]
- [[Multi-Agent-Orchestration]]
- [[Agent-Bug-Hunter]]
- [[Agent-Refactor-Surgeon]]
- [[Agent-Migration-Specialist]]
