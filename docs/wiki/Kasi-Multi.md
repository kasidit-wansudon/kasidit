# /kasi-multi

> Fan-out mode — dispatch N specialist agents in parallel, each with isolated context and a dispatch brief. Main synthesizes the N reports into one answer.

## Usage

```
/kasi-multi                       # default: 6 agents, auto-selected
/kasi-multi 4                     # 4 agents
/kasi-multi 6 <mission>           # 6 agents + explicit mission
sudo <mission>                    # shorthand: /kasi-multi 6 <mission>, skip clarifying Qs
sudo 8 <mission>                  # shorthand + custom N
```

## What it does

- Fans the current mission out across N parallel specialist agents in a single dispatch message.
- Gives each agent an isolated context window — they do not see each other's inputs.
- Writes one dispatch brief per agent (`MISSION / INPUTS / CONSTRAINTS / EXPECTED OUTPUT / PRIOR CONTEXT`).
- Synthesizes the N reports into one user-facing answer, ranked by severity × confidence.
- Suggests next steps but does not auto-execute destructive ones.

## `sudo` keyword

At the start of a message, `sudo` means:

1. **Fan out by default** — enter `/kasi-multi` with N=6 unless a number follows.
2. **Skip clarifying questions** — proceed on reasonable assumptions; narrate briefly.
3. **Stay inside safety rails** — destructive ops still require confirmation (hard rule #1).

`sudo` is a pacing signal, not a permission escalation.

## Flow

1. Narrow the mission to one line. Even in sudo mode, refuse truly vague requests.
2. Select N specialists from the registry based on mission kind.
3. Write one dispatch brief per agent — no brief, no dispatch.
4. Dispatch all N in a single message (parallel tool calls, no serial waits).
5. Synthesize — merge, deduplicate, rank by severity × confidence.
6. Suggest next step; do not auto-apply destructive findings.

## Default roster at N=6 (v0.10)

| Slot | Agent | Job |
|---|---|---|
| 1 | `architect-planner` / `deep-researcher` | scope + research |
| 2 | `general-purpose` | scaffolding / build step |
| 3 | `general-purpose` | secondary build step |
| 4 | `general-purpose` | extract / data / glue |
| 5 | `test-writer` / `general-purpose` | verification |
| 6 | `audit-specialist --focus=quality` | review slot (v0.10 — was standalone `code-reviewer` pre-v0.10) |

Main swaps in `bug-hunter`, `audit-specialist --focus=security`, `audit-specialist --focus=perf`, `refactor-surgeon`, `migration-specialist`, `legacy-specialist` based on mission kind.

> Note: `code-reviewer`, `security-auditor`, `perf-profiler` are kept as **name-resolution stubs** in v0.10 — invoking them logs a deprecation notice. Use `audit-specialist --focus=quality|security|perf|all` going forward. Stubs disappear in v0.11.

## N selection

| N | When |
|---|------|
| 2 | Small mission, one dependency (researcher → implementer) |
| 3 | Triage — planner + worker + reviewer |
| 4 | Audit, 2–3 workstreams + reviewer |
| **6 (default)** | Medium mission — 4 workers + reviewer + researcher |
| 8 | Large mission, multiple subsystems |
| 10 | Max — entire registry, rare |

Higher N is not always better. Default 6 has best cost / quality trade-off in observed runs.

## When to use

- Audit or review with multiple workstreams (security + perf + tests + overall).
- Feature build decomposable into parallel chunks.
- Research needing multiple independent sources.
- Bug hunt where hypotheses are cheap to generate but expensive to verify.

## When NOT to use

- One-line fix — fan-out overhead eats the savings.
- Hard sequential dependency chain — fan-out collapses to serial anyway.
- Haiku + large N — synthesis breaks down.

## Tier behavior

- **Opus** — full fan-out allowed. Synthesis is where Opus earns its cost.
- **Sonnet** — default workhorse. Fans out to 6, prefers 4 on large contexts.
- **Haiku** — cap N at 4. Always include `audit-specialist --focus=quality` (verifier slot) — pre-v0.10 this was a standalone `code-reviewer`; now invoked via the `--focus=` flag. `sudo` implicitly caps at 4 even if user says 8.

## Anti-patterns

- ❌ Fanning out on a one-line fix.
- ❌ Running `N=10` out of habit.
- ❌ Dispatching agents without briefs.
- ❌ Forwarding raw agent outputs to the user without synthesis.
- ❌ Using `sudo` to bypass destructive-op confirmation — it does not do that.
- ❌ Large N on Haiku — synthesis collapses.

## Examples

Review a PR fast:

```
sudo review PR #42 in /Users/me/repo
```

N=6, roster: `audit-specialist --focus=quality` (overall) + 2× `audit-specialist --focus=quality` (per-file) + `audit-specialist --focus=security` + `audit-specialist --focus=perf` + `test-writer`. Synthesis = ranked findings + go/no-go. (Pre-v0.10 invoked separate `code-reviewer` / `security-auditor` / `perf-profiler` agents — those are now `--focus=` flags on `audit-specialist`.)

Build a feature fast:

```
sudo 4 build /kasi-search as a mini semantic search over .kasidit/knowledge/
```

N=4, roster: `architect-planner` + `general-purpose` (scaffold) + `general-purpose` (indexer) + `test-writer`. Synthesis = integrated PR plan + file list.

Migrate a schema:

```
/kasi-multi 3 migrate users.email to citext in Laravel 8
```

N=3, roster: `migration-specialist` + `deep-researcher` + `test-writer`. Synthesis = expand-contract plan + rollback per phase.

## Since

Introduced in [[v0.9.2]].

## See also

- [[Commands]] (aggregate)
- [[Master-Orchestrator]]
- [[Multi-Agent-Orchestration]]
- [[Kasi-Cascade]]
