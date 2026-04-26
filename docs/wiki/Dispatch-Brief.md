# Dispatch Brief

> No brief, no dispatch.

The structured payload the [[Master-Orchestrator]] passes to every specialist agent. Introduced in [[v0.9.1]] as part of the Master Orchestrator Rule; used by [[Kasi-Multi]] for fan-out dispatch in [[v0.9.2]].

## Format

Every specialist invocation must pass all five fields:

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

Ad-hoc prompts produce ad-hoc output. The brief is the contract between master and specialist.

## Field-by-field

### MISSION

One sentence. Verifiable. Present-tense imperative.

- ✓ "Find the root cause of the 500 error on GET /api/sales after 2026-04-20 deploy"
- ✓ "Add regression test for the timezone offset bug fixed in commit abc123"
- ❌ "Look into the sales API" — not verifiable
- ❌ "Improve performance" — not scoped

If you cannot write the mission in one sentence, the scope is wrong. Narrow first.

### INPUTS

Concrete. File paths, line numbers, symptoms, measurements, versions. Never "the codebase".

- File paths: `app/Http/Controllers/SalesController.php:3708`
- Symptoms: user report quoted verbatim; stack traces with line numbers
- Measurements: `p95 latency 2.3s`, `query count 47 per request`
- Versions: `Laravel 8.83 / PHP 7.4 / MySQL 5.7`

### CONSTRAINTS

What the specialist must respect.

- Deadlines: `ship before 2026-05-01 release`
- Compatibility: `must support Laravel 5.x → 8.x`
- Performance budgets: `< 200ms p95`, `< 50MB bundle`
- Scope limits: `touch only app/Models/`, `do not refactor related controllers`

If no real constraints exist, write "none" — do not fabricate.

### EXPECTED OUTPUT

What the specialist returns. Must match the agent's documented output block.

- `bug-hunter` returns: root cause + minimal fix + regression test plan
- `architect-planner` returns: file list + step sequence + trade-offs + open questions (no code)
- `perf-profiler` returns: top 5 findings ranked by impact × confidence (does not optimize)
- `test-writer` returns: runnable test file + gap notes

Wrong shape = rejected output, re-dispatch.

### PRIOR CONTEXT

Findings from earlier specialists in the same mission.

- "architect-planner produced plan X (attached summary)"
- "deep-researcher cached Laravel 8 upsert docs at `.kasidit/knowledge/laravel-8-upsert.md`"
- "initial bug-hunter pass found path but not root cause"

Empty on first dispatch. Never empty on follow-up within the same mission.

## Example — real dispatch

```
MISSION: Audit SalesController.php for SQL injection, HIGH severity only

INPUTS:
  - File: app/Http/Controllers/SalesController.php (lines 1-9806)
  - Stack: Laravel 8.83, PHP 7.4, MySQL 5.7
  - Checklist: .kasidit/CHECKLISTS/security-php.md
  - Patterns: .kasidit/PATTERNS.md (error handling, DB query conventions)

CONSTRAINTS:
  - Confidence labels mandatory (Haiku session)
  - [unsure] items listed separately
  - No speculation — prove exploitability or do not mention

EXPECTED OUTPUT:
  - JSON-like list: [{ file, line, type, severity, confidence, fix_hint }]
  - Only severity = HIGH (ignore MED / LOW this pass)
  - Separate [unsure] section for user decision

PRIOR CONTEXT:
  - none (first dispatch in mission)
```

## When to use

- Every invocation from master → specialist
- Every `/kasi-multi` fan-out (all N specialists get their own brief)
- Every follow-up dispatch within the same mission (carry prior findings in PRIOR CONTEXT)

## When the brief is too heavy

Trivial exceptions the master may handle itself without a brief:

- One-line fix on a single file the user explicitly pointed to
- Pure question with no code change
- Reading top-level index (`CLAUDE.md`, `PATTERNS.md`, `INDEX.md`, `RELATIONS.md`)
- Final user-facing summary

Everything else → dispatch with a brief.

## Anti-patterns

- ❌ "Do stuff" prompts to specialists — no mission, no output shape
- ❌ Skipping INPUTS because "the agent can figure it out"
- ❌ CONSTRAINTS omitted — leads to out-of-scope work
- ❌ EXPECTED OUTPUT as prose — "write some tests" instead of "runnable test file + gap notes"
- ❌ PRIOR CONTEXT forgotten on follow-up — specialist re-does earlier work
- ❌ Brief longer than the work itself — scope is wrong, narrow first

## v0.10 — invoking `audit-specialist`

`audit-specialist` is the only audit agent in v0.10 (replaces `code-reviewer` / `security-auditor` / `perf-profiler`). Briefs must include the `--focus` flag:

```
MISSION: Pre-merge security gate on AuthService.php — only HIGH severity findings.
INPUTS:
  - app/Services/AuthService.php
  - .kasidit/CHECKLISTS/security-php.md (or default seeded)
CONSTRAINTS:
  - HIGH severity only
  - confidence labels mandatory
EXPECTED OUTPUT:
  - audit-specialist --focus=security <target>
  - findings array: [{file, line, type, severity, confidence, fix_hint}]
  - verifier pass note (which findings reproduced, which deferred to user)
PRIOR CONTEXT:
  - last audit found 2 SQL injection points in v1.4.x; patched in PR #1182
```

`--focus=quality` for code review, `--focus=perf` for profiling, `--focus=all` for the pre-merge full sweep.

## See also

- [[Master-Orchestrator]] — the rule that requires briefs
- [[Multi-Agent-Orchestration]] — fan-out dispatch mechanics
- [[Agent-Audit-Specialist]] — single-entry audit agent (v0.10)
- [[Kasi-Multi]] — the command that dispatches N briefs in parallel
- [[Kasi-Cascade]] — tier-cascaded briefs (Opus → Sonnet → Haiku)
- [[v0.9.1]] — introduction
- [[v0.9.2]] — fan-out extension
- [[v0.10.0]] — `--focus` flag for audit-specialist briefs
