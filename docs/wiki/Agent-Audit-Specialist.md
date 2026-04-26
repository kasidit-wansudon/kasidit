# Agent: audit-specialist

> Multi-focus audit agent (v0.10) — review code **quality**, **security**, or **performance** depending on `--focus` flag. Replaces `code-reviewer`, `security-auditor`, and `perf-profiler` (kept as name-resolution stubs; removed in v0.11).

## Why merged

The three prior agents overlapped heavily — same file reads, same checklist mechanics, different focus areas. One entry point with a `--focus` flag is cleaner: router picks the lens, not the agent.

## When to invoke

| Trigger | Focus |
|---|---|
| PR / diff / code review | `quality` |
| OWASP / CVE / auth boundary / session handling | `security` |
| Slow page, N+1, high bill, before-scale | `perf` |
| Pre-merge full sweep | `all` (runs all three lenses sequentially) |

## Invocation

```
audit-specialist --focus=quality <target>
audit-specialist --focus=security <target>
audit-specialist --focus=perf <target>
audit-specialist --focus=all <target>
```

`<target>` = file path, module path, or diff range.

**No automatic name-mapping** — users (or the master orchestrator) must specify `--focus` explicitly. The old agent names (`code-reviewer`, `security-auditor`, `perf-profiler`) exist only as name-resolution stubs so references do not raise a missing-agent error.

## What each focus does

### `--focus=quality`

Checklist: `CHECKLISTS/code-review-<stack>.md` (PHP / Node / Python / Go seeded by default; see [[Checklists]]).

Scan dimensions:

1. **Correctness** — logic bugs, off-by-one, null handling, boundary conditions.
2. **Readability** — naming, function size, nesting depth, comment quality.
3. **Architecture** — single responsibility, coupling, dead code, duplicated logic.
4. **Testability** — hardcoded deps, side effects, mockability.
5. **Error handling** — swallowed errors, overly broad `catch`, error types.

Report format: `[confidence] file:line — finding — fix hint`.

### `--focus=security`

Checklist: `CHECKLISTS/security-<stack>.md`.

OWASP-aligned scan:

1. Injection (SQL / command / template / LDAP).
2. Broken auth — session management, password storage, MFA, JWT claims.
3. Data exposure — PII logging, error-message leakage, DB dumps.
4. XXE / SSRF / SSTI.
5. Access control — missing authz, IDOR, privilege escalation.
6. Crypto — weak algos, hardcoded keys, missing HTTPS.
7. Deserialization, upload handling, path traversal.
8. Dependency CVEs (`composer audit` / `npm audit` / `pip-audit`).

**Mandatory on Haiku**: verifier pass — second scan removes speculative findings.

### `--focus=perf`

Scan dimensions:

1. Query patterns — N+1, missing index, `SELECT *`, OFFSET on large tables.
2. Loops — O(n²) nested iteration, repeated DB calls inside loop.
3. Memory — large string concat, unbounded caches, leaked closures.
4. Rendering (UI) — unnecessary re-renders, large bundle imports, sync-blocking.
5. Cost proxies — external API calls per request, cold-start heavy work.

**Do not optimize** unless explicitly asked. Report + rank by `impact × confidence`, Top 5.

### `--focus=all`

Runs `quality` → `security` → `perf` sequentially. Separate report per lens. Synthesizes Top-5 actionable across all three at the end.

## What it will NOT do

- Apply fixes (delegate to `bug-hunter` or `refactor-surgeon` with explicit scope).
- Rewrite legacy code (delegate to `legacy-specialist`).
- Narrate the review as prose — output is structured with confidence labels.
- Run `--focus=all` on a full codebase without narrowed scope.

## Inputs expected

- **Target** — file path, module path, or diff range.
- **Focus** — `quality` | `security` | `perf` | `all`.
- **Checklist file** (optional) — override path to `.kasidit/CHECKLISTS/<name>.md`. Default: auto-pick by focus + stack.
- **Scope limit** — file / module / project.

## Outputs

```
Target: <target>
Focus:  <focus>
Tier:   <tier>

🔴 HIGH — verified
  [high] file:line — finding — fix hint

🟡 MEDIUM — pattern match
  [medium] file:line — finding

🟢 LOW — inferred
  [low] file:line — finding

❓ UNSURE — needs user review
  [unsure] file:line — question
```

At mission end, emit a [kasidit-log] line for the backend router memory:

```
[kasidit-log] kind=audit-<focus>-<stack> mode=full turns=N outcome=pass
```

See [[Global-Prompt-Log]] and `kasidit-record.py` for how this feeds `route-memory.jsonl`.

## Tier behavior

- **Opus** — full fan-out allowed. Module-scoped scans OK. `--focus=all` acceptable.
- **Sonnet** — default. Module-scoped OK, prefer `--focus=all` only on small codebases.
- **Haiku** — 1 file per call maximum. Checklist-driven only, no reasoning. Verifier pass mandatory.

## Anti-patterns

- ❌ `--focus=all` on a huge codebase without narrowing scope.
- ❌ Reporting findings without confidence labels.
- ❌ Marking speculative findings as `[high]` — downgrade or drop.
- ❌ Mixing lenses within a single finding (state focus per finding).
- ❌ Suggesting fixes the user did not ask for — audit is read-only.
- ❌ Auditing the three deprecated-stub files — they are empty shells; look at the real code.

## Deprecated predecessors (v0.10)

These three pages describe the agents that were merged into `audit-specialist`. They remain for historical context; the invocation sections in each should redirect here.

- [[Agent-Code-Reviewer]] → `audit-specialist --focus=quality`
- [[Agent-Security-Auditor]] → `audit-specialist --focus=security`
- [[Agent-Perf-Profiler]] → `audit-specialist --focus=perf`

## Since

v0.10.0 — introduced; consolidates three prior agents.

## See also

- [[Master-Orchestrator]]
- [[Multi-Agent-Orchestration]]
- [[Checklists]]
- [[Agent-Bug-Hunter]] (for fixes after audit)
- [[Agent-Refactor-Surgeon]] (for cleanup after audit)
- [[v0.10]] (release notes — pending)
