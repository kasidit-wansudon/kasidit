# Multi-Agent Orchestration

Introduced in [[v0.3.0]], formalized in [[v0.9.1]] as the Master Orchestrator Rule.

> When the master both plans and executes, context pollution compounds. Isolation = clean handoffs = fewer hallucinations.

**See also:** [[Master-Orchestrator]] for the master rule · [[Dispatch-Brief]] for the brief format

## The rule

For any **strong-work mission** — multi-file change, migration, perf hunt, security audit, new feature, deep research — the main agent becomes an **orchestrator only**. It narrows, dispatches, synthesizes. It does not execute.

### Master MAY

- Narrow mission and confirm scope with user
- Detect domain and tier
- Read top-level index only: `CLAUDE.md`, `PATTERNS.md`, `DESIGN_SYSTEM.md`, `สารบัญ`, `.kasidit/knowledge/` index
- Pick the specialist from the registry
- Write the dispatch brief
- Synthesize outputs into a user-facing report
- Decide next step

### Master MAY NOT

- ❌ Write code
- ❌ Edit files
- ❌ Run tests or servers
- ❌ Read source files beyond the top-level index set
- ❌ Search / grep / glob beyond initial scope detection
- ❌ Fetch docs (delegate to `deep-researcher`)
- ❌ Write migrations (delegate to `migration-specialist`)

If the master catches itself doing any of the above → stop, spawn a specialist, pass the accumulated context.

### Exceptions (master may act directly)

- Trivial one-line fix on a single file the user explicitly pointed to
- Answering a pure question with no code change
- Reading the top-level index files
- Writing the final user-facing summary

## Specialist registry

| Agent | Trigger | Scope |
|---|---|---|
| `bug-hunter` | error / crash / wrong output / regression | root-cause + minimal fix; mandatory `git log --grep` / `-S` |
| `architect-planner` | new feature / refactor > 2 files | plan only; trade-offs + open questions |
| `perf-profiler` | slow / N+1 / high cost / pre-scale | measure first; top 5 by impact × confidence |
| `test-writer` | add tests / regression / coverage | one target per call; regression after bug fix |
| `refactor-surgeon` | named refactor | zero behavior change; test-parity |
| `deep-researcher` | library / API / framework research | trust hierarchy; caches to `.kasidit/knowledge/` |
| `migration-specialist` | schema / framework upgrade / backfill | expand-contract phases; rollback per phase |
| `code-reviewer` | PR / diff / audit | multi-dimensional |
| `security-auditor` | OWASP / CVE / auth boundary | security-focused deep audit |
| `legacy-specialist` | legacy PHP / old framework / no-test | legacy-safe refactor |

## Dispatch brief format

Every specialist invocation:

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

No brief → no dispatch.

## Sub-agent pattern for reviews

Heavy missions split across multiple agents:

```
Main (planner)
  ↓
Dispatch per file/module
  ↓
Agent 1    Agent 2    Agent 3    Agent 4
(file)     (file)     (file)     (file)
  ↓          ↓          ↓          ↓
Findings   Findings   Findings   Findings
  ↓          ↓          ↓          ↓
  └──────────┴──────────┴──────────┘
              ↓
Verifier agent (Haiku: mandatory)
  ↓
Main (synthesizer) → report with confidence + priority
```

- 1 file per agent on Haiku
- 1 module per agent on Opus/Sonnet
- Main context stays lean — delegates all file reads
- Each agent returns structured output, not prose
- Verifier pass removes false positives (Haiku mandatory, Sonnet recommended for security)

## Fan-Out Mode (`/kasi-multi`, [[v0.9.2]])

When user wants parallel execution over dependency-chained execution, fan out.

```
/kasi-multi [N] [mission]       # explicit
sudo <mission>                   # shorthand for N=6 + skip clarifying Qs
sudo <N> <mission>               # shorthand with N
```

**Default N=6 roster** (heuristic, swappable by mission kind):

| Slot | Agent |
|---|---|
| 1 | `architect-planner` or `deep-researcher` |
| 2 | `general-purpose` (build step) |
| 3 | `general-purpose` (secondary workstream) |
| 4 | `general-purpose` (extract / glue) |
| 5 | `test-writer` or `general-purpose` (verification) |
| 6 | `code-reviewer` |

**Tier caps:**

- Opus — full fan-out
- Sonnet — default, prefer 4 on large contexts
- Haiku — cap at N=4 (synthesis collapses with more)

**`sudo` is a pacing signal, not a permission escalation.** It still respects the destructive-op confirmation rule.

See [[Commands#kasi-multi|/kasi-multi]] for full flow.

## Tier-specific orchestration ([[v0.8.0]] Tier Cascade)

```
Opus: plan
  ↓
Sonnet: implement
  ↓
Haiku: audit by checklist
  ↓
Opus: synthesize
```

Invoke via `/kasi-cascade`.

## Anti-patterns

- ❌ Master writing code on a strong-work mission
- ❌ Master reading source files beyond the top-level index
- ❌ Invoking a specialist without a dispatch brief
- ❌ Specialist working outside its documented scope
- ❌ Main agent loading file contents "just to check" — delegate
- ❌ Running Haiku review without a verifier pass

## See also

- [[v0.3.0]] — multi-agent orchestration introduced
- [[v0.8.0]] — tier cascade
- [[v0.9.1]] — master orchestrator rule formalized
- [[Model Tiers]]
