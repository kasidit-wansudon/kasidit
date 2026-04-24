---
description: Fan-out mode — dispatch N specialist agents in parallel for the current mission. `/kasi-multi` default N=6; `sudo` shorthand uses min 2 for speed. Max per tier cap.
---

Fan out the current mission across **N parallel specialist agents**. Each agent gets an isolated context and a narrow dispatch brief. Main synthesizes the N reports into one user-facing answer.

## Usage

```
/kasi-multi                       # default: N=6, auto-selected roster
/kasi-multi 4                     # 4 agents
/kasi-multi 6 <mission>           # 6 agents + explicit mission
sudo <mission>                    # session-only speed mode — min 2 parallel, skip clarifying Qs
sudo 6 <mission>                  # sudo with explicit N
/kasi-multi --fast                # synonym for sudo flag on this invocation only
```

## `sudo` keyword — session-only speed shortcut

Typing `sudo <mission>` at the start of a message means:

1. **Spawn min 2 specialists in parallel** — never serial on sudo. Default N=2 unless number follows.
2. **Skip clarifying questions** — proceed on reasonable assumptions; narrate them briefly.
3. **Session-only pacing** — does not persist. Next session reverts to config defaults.
4. **Stay inside safety rails** — no destructive ops without confirm (hard rule applies).

`sudo` is **not** a permission escalation. It is a pacing signal: "trust defaults, go fast, use parallel."

Mnemonic: think `sudo` = "speed mode, 2 up" — a signal to the orchestrator, not a security claim.

## `--fast` flag

Functionally identical to `sudo` but passed as an explicit flag — useful when scripting or when `sudo` at the start of a line is awkward.

```
/kasi-multi 4 --fast review AuthController.php
```

## Flow

1. **Narrow the mission** (one line) — even in sudo mode, the mission must be verifiable. If the request is truly vague, refuse and ask for a number from a short list.
2. **Select N specialists** — pick from the registry based on mission kind:
   - Review / audit → `audit-specialist --focus=quality`, `audit-specialist --focus=security`, plus per-file workers
   - Build / feature → `architect-planner`, `general-purpose` workers, `test-writer`, `audit-specialist --focus=quality`
   - Research → `deep-researcher` (possibly multiple on different sources)
   - Bug hunt → `bug-hunter`, `deep-researcher`, `test-writer`
   - Perf → `audit-specialist --focus=perf`, per-module workers
3. **Write one dispatch brief per agent** — `MISSION / INPUTS / CONSTRAINTS / EXPECTED OUTPUT / PRIOR CONTEXT`. No brief → no dispatch.
4. **Dispatch all N in a single message** (parallel tool calls) — no serial waits.
5. **Synthesize** — merge findings, deduplicate, rank by severity × confidence. Produce one user-facing report.
6. **Suggest next step** — not auto-execute destructive things surfaced in the synthesis.

## Default agent mix (N = 6)

When no mission-specific signal is given, the default roster is:

| Slot | Agent | Job |
|---|---|---|
| 1 | `architect-planner` / `deep-researcher` | scope + research |
| 2 | `general-purpose` | scaffolding / build step |
| 3 | `general-purpose` | secondary build step (parallel work surface) |
| 4 | `general-purpose` | extract / data / glue |
| 5 | `test-writer` / `general-purpose` | verification slot |
| 6 | `audit-specialist --focus=quality` | review slot |

The mix is a heuristic; the master may swap in `bug-hunter`, `audit-specialist --focus=perf|security`, `refactor-surgeon`, `migration-specialist`, `legacy-specialist` as the mission demands.

## N selection rules

| N | When |
|---|------|
| 2 | Small mission with one clear dependency (researcher → implementer) |
| 3 | Triage — planner + worker + reviewer |
| 4 | Audit with 2–3 workstreams + reviewer |
| **6 (default)** | Medium mission, 4 workers + reviewer + researcher |
| 8 | Large mission with multiple subsystems |
| 10 | Max — entire specialist registry (rare) |

Higher N is not always better. More agents = more synthesis cost + more redundancy. Default 6 has best cost/quality trade-off in observed runs.

## Tier behavior

- **Opus** — full fan-out allowed. Synthesis step is where Opus earns its cost.
- **Sonnet** — default. Can fan out to 6, prefers 4 on large contexts.
- **Haiku** — cap N at 4. Haiku synthesis is weak; prefer fewer-but-focused dispatches. Always include `audit-specialist --focus=quality` or `verifier` in the roster. On Haiku, `sudo` implicitly caps at N=4 even if user says N=8.

## Rules

- **Context isolation is the point.** Never share file contents between agents via main context — let each agent read its own inputs.
- **Brief format is non-negotiable.** Ad-hoc prompts produce ad-hoc output.
- **Parallel, not serial.** All N dispatches in one message. Serial fan-out defeats the purpose.
- **Synthesize, do not forward.** Raw agent outputs are not user-facing. Main merges.
- **Destructive actions stay behind user confirmation.** Fan-out may discover risky fixes; it does not apply them without confirm.

## Anti-patterns

- ❌ Fanning out on a one-line fix — overhead exceeds benefit.
- ❌ Running `N=10` out of habit — pick the smallest N that covers the slots.
- ❌ Dispatching agents without briefs.
- ❌ Forwarding raw agent outputs to the user without synthesis.
- ❌ Using `sudo` to bypass destructive-op confirmation — it does not do that.
- ❌ On Haiku, fanning out to large N — synthesis collapses.

## Examples

### Review a PR fast

```
sudo review PR #42 in /Users/me/repo
```

→ N=6 default, roster: `audit-specialist --focus=quality` (overall), 2× `audit-specialist --focus=quality` (per-file), `audit-specialist --focus=security`, `audit-specialist --focus=perf`, `test-writer`. Parallel dispatch. Synthesis = ranked findings + go/no-go.

### Build a feature fast

```
sudo 4 build /kasi-search as a mini semantic search over .kasidit/knowledge/
```

→ N=4, roster: `architect-planner`, `general-purpose` (scaffold), `general-purpose` (indexer), `test-writer`. Parallel dispatch. Synthesis = integrated PR plan with file list.

### Migrate a schema

```
/kasi-multi 3 migrate users.email to citext in Laravel 8
```

→ N=3, roster: `migration-specialist`, `deep-researcher` (docs + prior migrations), `test-writer`. Parallel dispatch. Synthesis = expand-contract plan + rollback per phase.

## See also

- [[Multi-Agent-Orchestration]] — the underlying framework
- `/kasi-cascade` — tier-routed orchestration (Opus plans → Sonnet works → Haiku greps) as an alternative to fan-out
- Dispatch brief format in SKILL.md
