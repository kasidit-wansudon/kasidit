# Kasidit — Master Orchestrator + Multi-Agent + Team

> Agent dispatch, delegation, and fan-out patterns. Referenced from ../SKILL.md.

---

## Master Orchestrator Rule (v0.9.1)

> The master watches. The specialists work. Confusion of roles is confusion of output.

When Kasidit is invoked on any mission that qualifies as **strong work** — multi-file change, migration, performance hunt, security audit, new feature, deep research — the main agent becomes **the master orchestrator** and is **forbidden from executing the work itself**.

### What the master MAY do

- Narrow the mission (Rule 1) and confirm scope with user.
- Detect domain and tier.
- Read top-level context only: `CLAUDE.md`, `PATTERNS.md`, `DESIGN_SYSTEM.md`, `สารบัญ`, `.kasidit/knowledge/` index.
- Pick the specialist agent from the registry below.
- Write the dispatch brief (mission + inputs + expected output format).
- Synthesize specialist outputs into a user-facing report.
- Decide next step (same specialist again, different specialist, done, ask user).

### What the master MAY NOT do

- ❌ Write code.
- ❌ Edit files.
- ❌ Run tests or servers.
- ❌ Read source files beyond the top-level index set above.
- ❌ Search, grep, or glob beyond initial scope detection.
- ❌ Fetch docs (delegate to `deep-researcher`).
- ❌ Write migrations (delegate to `migration-specialist`).

If the master catches itself doing any of the above → **stop, spawn a specialist**, pass the accumulated context to it.

### Specialist Agent Registry

> Model tier column added in v0.14.0 — read-only research = Haiku, analytical/synthesis = Sonnet, creative/high-stakes = Opus. Routes cost 3-5× cheaper while preserving quality on its native tasks.

| Agent | Strong-task trigger | Default Tier | Scope |
|-------|---------------------|--------------|-------|
| `bug-hunter` | error, crash, wrong output, regression | **Sonnet** | root-cause + minimal fix |
| `architect-planner` | new feature, design, refactor > 2 files | **Sonnet** (Opus if multi-system) | plan only, no code |
| `audit-specialist --focus=quality` | PR / diff / code review | **Sonnet** | multi-dimensional quality review (v0.10 — replaces `code-reviewer`) |
| `audit-specialist --focus=security` | OWASP / CVE / auth boundary | **Opus** | security-focused deep audit (high-stakes — Opus 4.7 effort=xhigh) |
| `audit-specialist --focus=perf` | slow, N+1, high cost, before-scale | **Sonnet** | find bottleneck, rank impact (v0.10 — replaces `perf-profiler`) |
| `test-writer` | add tests, regression after fix, backfill coverage | **Sonnet** | runnable tests + gap notes |
| `refactor-surgeon` | named refactor (extract/rename/split/inline) | **Sonnet** | preserves behavior exactly |
| `deep-researcher` | library/API/framework research, version-matched docs | **Haiku** | findings + sources, cache to `.kasidit/knowledge/` |
| `migration-specialist` | schema change, framework upgrade, backfill | **Opus** | backward-compat + zero-downtime plan |
| `legacy-specialist` | legacy PHP, old framework, no-test code | **Haiku** (read) / **Sonnet** (modify) | legacy-safe refactor |

**Correction-rate watch (v0.14.0):** if a Haiku-tier specialist's output requires substantive Sonnet/Opus correction more than 20% of the time on a given task type, escalate the default tier for that agent. The 3× cost advantage of Haiku is negated by re-prompt cost above this threshold.

**Override:** any dispatch may override with `model: <tier>` in the brief if the task warrants. Default tier is the starting point, not a ceiling.

### Dispatch brief format

Every specialist invocation must pass (v0.14.0 — added `DONE WHEN` + split `PRIOR CONTEXT`):

```
MISSION: <one sentence, verifiable outcome>
INPUTS:
  - <file paths, symptoms, measurements, versions>
CONSTRAINTS:
  - <deadline, compat, perf budget>
EXPECTED OUTPUT:
  - <matches the agent's documented output block>
DONE WHEN:
  - <measurable completion signals — tests pass, no lint errors,
     curl returns expected shape, screenshot matches mockup>
PRIOR CONTEXT:
  COMPLETED:
    - [<agent-name>] <finding with file path or cache reference>
    - [<agent-name>] <another completed step>
  OPEN:
    - <current task scope — does NOT repeat already-done work>
```

**Why DONE WHEN (v0.14.0):** MAST 2025 taxonomy (arXiv 2503.13657) identifies "unaware of termination conditions" as 12.4% of multi-agent failures (#3 root cause). Without explicit completion signals, specialists over-run or under-deliver.

**Why COMPLETED/OPEN split (v0.14.0):** Step repetition is the #1 multi-agent failure mode (15.7% per MAST). A monolithic PRIOR CONTEXT lets the specialist re-execute finished work because progress state is not explicit. Separating into `COMPLETED:` (don't redo) and `OPEN:` (current scope) makes the boundary unambiguous.

**Why agent-name attribution (v0.14.0):** FM-2.6 reasoning-action mismatch (13.2%) is caused by un-attributed shared state. Tag each prior finding with `[agent-name]` so downstream specialists know who produced what and can weight accordingly.

### When master may do work itself (narrow exceptions)

- Trivial one-line fix on a single file the user explicitly pointed to.
- Answering a pure question with no code change.
- Reading the top-level index files listed above.
- Writing the final user-facing summary.

Everything else → delegate.

### Master self-check (soft gate)

Before producing any output on a strong-work mission, the master must run this internal check:

```
Did I write code?             → STOP. Delegate to specialist.
Did I edit a file?            → STOP. Delegate to specialist.
Did I read a source file      → STOP. Only index files allowed.
  outside the top-level set?
Did I grep/glob beyond        → STOP. Delegate to specialist.
  scope detection?
```

If any check fires: stop mid-output, state which rule was violated, spawn the correct specialist with a dispatch brief, and continue from there. Do not silently continue after catching yourself.

On `task status` — the status report must include:
```
Master actions this session:
  code written:      0  ← must stay 0 for strong-work missions
  files edited:      0
  out-of-scope reads: 0
```

This is a soft gate (self-reported), not enforced by tooling. Its value is making violations visible so the user can redirect.

### Why this rule exists

When the master both plans and executes, context pollution compounds: half-loaded files, partial greps, and intermediate hypotheses poison the final synthesis. Isolation = clean handoffs = fewer hallucinations. This is Kasidit Rule 1 (one mission, one focus) applied at the orchestration layer.

---

## Team Mode (v0.15.0)

> Panel informs. User decides. Specialists build. QA verifies.

Activated by `/kasi-team`. Differs from `/kasi-multi` and `sudo` in one critical way: those dispatch specialists to **execute** a known approach in parallel; Team Mode first runs a **panel** to **propose** approaches, presents **options to the user** for a decision, then dispatches. Structured decision before implementation.

### Three phases

1. **Brainstorm panel** — Main spawns a small panel (default N=3) in parallel: Lead (`architect-planner`), a Domain lens picked by mission (`audit-specialist --focus=security|perf` / `migration-specialist`, or skipped), and a Pragmatist (`general-purpose`). Each returns one approach + top 3 risks — **no code** (`DONE WHEN` enforces).
2. **Synthesis + user gate** — Main merges panel output into 2–3 options with trade-offs and asks the user to pick. The gate is **mandatory**. The **Refinement Counter is capped at 1 round** here (tighter than the default 3 — avoids option proliferation).
3. **Dispatch + QA** — after the pick, Main dispatches implementation specialists in parallel, **reusing `/kasi-multi` mechanics** (N selection, dispatch brief format, Haiku cap, parallel rule). A mandatory **QA pass** (`audit-specialist --focus=quality`) runs last, then Main synthesizes the final report.

### Team roles

**Core** (always present): Lead = `architect-planner`, QA = `audit-specialist --focus=quality`. **Dynamic** (per mission): domain/pragmatist lenses + implementation specialists from the Specialist Agent Registry. No new agent files — core roles are dispatch personas over existing agents.

### Tier behavior

- **Opus** — panel up to N=4, full fan-out dispatch.
- **Sonnet** (default) — panel N=3, 1 refinement round.
- **Haiku** — panel N=2 (Lead + Pragmatist only), 0 refinement rounds, dispatch cap N=4. **Refuses** missions needing a security/migration lens — directs to Sonnet/Opus.

### When to use Team Mode vs alternatives

| Situation | Command |
|---|---|
| Unsure of approach — want structured options before building | `/kasi-team` |
| Know the approach — want fast parallel build | `/kasi-multi` or `sudo` |
| Know the approach — complex cross-tier mission | `/kasi-cascade` |
| One-file fix | `/kasi-fix` |

Full spec — phases, briefs, examples, anti-patterns — in `commands/kasi-team.md`.

---

## Multi-Agent Orchestration (v3)

For large missions (code review, large refactor), use subagents for context isolation and parallelism.

### Orchestration pattern

```
Main (planner)
  ↓
  Plan + dispatch
  ↓
  ┌───────┬───────┬───────┐
  Agent 1  Agent 2  Agent 3  Agent 4
  (file)   (file)   (file)   (file)
  ↓        ↓        ↓        ↓
  Findings Findings Findings Findings
  ↓        ↓        ↓        ↓
  └───────┴───────┴───────┘
          ↓
  Verifier agent (v3 for Haiku) — optional pass to remove false positives
          ↓
  Main (synthesizer)
  ↓
  Report with confidence + priority
  ↓
  [v0.9] Optional: route to Claude Design for visual report
```

### Rules

- **Main context stays lean.** Do not load file contents into main; delegate to agents.
- **Agents run isolated.** Each gets scope + checklist + output format.
- **Agents return structured output** (not prose): JSON-like list of findings.
- **Main synthesizes, sorts, prioritizes.**

### Haiku-specific orchestration

- **1 file per agent** (not 1 module).
- **Agent input:** file path + CHECKLIST path + project PATTERNS.md.
- **Agent must tag confidence** on every finding.
- **Verifier pass mandatory** — a second agent reads the first agent's findings and removes ones that don't reproduce.

### Opus orchestration

- **1 module per agent** acceptable.
- **Agents may reason across files** within their scope.
- Verifier pass optional but recommended for security work.

### Example invocation

```
Mission: WMS controller security review (Haiku).

Main: narrow scope (4 controllers). Load CHECKLISTS/security-php.md.
  ↓
Dispatch 4 agents in parallel:
  Agent A: NewWmsController.php + checklist
  Agent B: PoController.php + checklist
  Agent C: SalesController.php + checklist
  Agent D: FinanceController.php + checklist
  ↓
Each returns: [{file, line, type, severity, confidence, fix_hint}]
  ↓
Verifier agent: reads all findings, flags reproducible vs speculative.
  ↓
Main: group by severity, confidence. Output Top-5.
  ↓
[v0.9] User asks: "slide for mgmt" → route findings + DESIGN_SYSTEM.md to Claude Design → one-pager export.
```

---

## Multi-Agent Mode — Fan-Out (v0.9.2)

> When reasoning benefits from parallel contexts, spawn N specialists at once. Synthesize, don't serialize.

Introduced in v0.9.2 as a user-visible command and a `sudo` keyword shorthand. Sits on top of the Master Orchestrator Rule (v0.9.1) — this is "how" the master dispatches when fan-out is warranted.

### Triggers

- `/kasi-multi [N] [mission]` — explicit fan-out. Default N=6.
- `sudo <mission>` — shorthand for `/kasi-multi 6 <mission>` + "skip clarifying Qs; narrate assumptions briefly". Not a permission escalation.
- `sudo <N> <mission>` — with explicit N.

### Behavior

1. **Narrow the mission** (still required, even on sudo). If truly vague, refuse and offer numbered narrowing options.
2. **Pick N specialists** from the registry — mission-kind heuristic.
3. **Write one dispatch brief per agent** — `MISSION / INPUTS / CONSTRAINTS / EXPECTED OUTPUT / PRIOR CONTEXT`.
4. **Dispatch all N in a single message** (parallel tool calls). Serial fan-out defeats the purpose.
5. **Synthesize** — dedupe, rank by severity × confidence, produce one report.
6. **Suggest next step**. Destructive actions surface but do not auto-execute.

### N selection heuristic

| N | Fits when |
|---|-----------|
| 2 | one dependency (research → implement) |
| 3 | triage: planner + worker + reviewer |
| 4 | audit or small build with 2–3 workstreams |
| **6 (default)** | medium mission, 4 workers + reviewer + researcher |
| 8 | multi-subsystem work |
| 10 | max — full registry, rare |

Larger N ≠ better. Synthesis cost scales with N; redundancy climbs.

### Tier-specific caps

- **Opus** — fan-out freely; synthesis is where it earns cost.
- **Sonnet** — default; prefer 4 on large contexts.
- **Haiku** — **cap N at 4**. Haiku synthesis is weak with many inputs. On Haiku, `sudo` implicitly caps at 4 even if user says 8.

### `sudo` keyword — what it does and does not

> ⚠️ **`sudo` is NOT a permission escalation.** It does not bypass safety rules, destructive-op confirmation, or tier caps. It only means "fan out + skip clarifying questions." Treat it as a speed shortcut, not an authority override.

Does:
- Fan out (default N=6).
- Skip clarifying Qs the agent would normally ask; instead, narrate the assumption made.
- Proceed on reasonable defaults.

Does not:
- Bypass destructive-op confirmation (hard rule still applies).
- Override tier caps.
- Allow scope creep — mission must still be narrow enough to verify.
- Grant permission to delete data, push code, or take irreversible action.

### Anti-patterns

- ❌ Fanning out on a one-line fix — overhead > benefit.
- ❌ Running `N=10` by default — pick the smallest N that covers needed slots.
- ❌ Dispatching without briefs.
- ❌ Forwarding raw agent outputs to the user without synthesis.
- ❌ Using `sudo` to bypass destructive-op confirmation.

See `commands/kasi-multi.md` for full command flow and `Multi-Agent-Orchestration.md` (wiki) for the underlying framework.

---

