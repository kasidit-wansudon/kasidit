# Agent: code-reviewer

> ⚠️ **Deprecated in v0.10.** Merged into [[Agent-Audit-Specialist]]. Invoke as `audit-specialist --focus=quality <target>` instead. This file kept for name resolution only; removed in v0.11. No automatic mapping — invoke explicitly.

---

> Multi-dimensional code review with quality gates — correctness, readability, architecture, security, performance.

## When to invoke

- PR / diff / commit range ready for review
- Pre-merge gate on shared branches
- After [[Agent-Refactor-Surgeon]] or [[Agent-Bug-Hunter]] produces a change
- Spot-check on a specific file or module

## What it does

- Detects domain (backend / frontend / data / infra) and loads matching [[Checklists]]
- Reviews across 5 dimensions: correctness, readability, architecture, security, performance
- Checks for scope creep and deviation from existing codebase patterns (PATTERNS.md)
- Flags genuine bugs with `file:line` references
- Emits verdict: APPROVE with comments / REQUEST CHANGES / NEEDS DISCUSSION

## What it will NOT do

- Suggest rewrites outside PR scope
- Insist on personal style preferences
- Flag stylistic nits as blockers
- Replace a dedicated [[Agent-Security-Auditor]] sweep for security-critical code

## Inputs expected

- Diff / PR / commit range
- Scope: specific files or modules
- Domain hint (optional — auto-detected otherwise)

## Outputs

Verdict block with issues grouped by severity:

```
APPROVE — [critical] / [minor] with file:line
REQUEST CHANGES — blockers with file:line
NEEDS DISCUSSION — non-obvious trade-offs
```

## Tier behavior

Sonnet default. Opus recommended when reviewing cross-module architecture changes.

## Anti-patterns

- ❌ "Rewrite this whole file using <pattern>" when PR scope is narrow
- ❌ Blocking merge on preference-level naming
- ❌ Approving without reading existing conventions
- ❌ Treating every lint warning as a blocker

## Since

Introduced pre-[[v0.9.1]] (early release).

## See also

- [[Master-Orchestrator]]
- [[Multi-Agent-Orchestration]]
- [[Agent-Security-Auditor]]
- [[Checklists]]
- [[Agent-Refactor-Surgeon]]
