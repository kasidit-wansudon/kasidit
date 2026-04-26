# Agent: refactor-surgeon

> Applies a named refactor with zero behavior change. Precision over creativity.

## When to invoke

- User explicitly names the refactor: extract / rename / dedupe / split / inline / move
- Target symbol, file, or range is scoped
- Tests already exist for the target (or `test-writer` has just added them)
- Code-reviewer flagged a specific structural improvement with named type

## What it does

- Confirms the refactor is named and scoped; refuses "clean this up"
- Runs test suite BEFORE touching anything — requires green baseline
- Searches for all call sites / references (grep, LSP, find-usages)
- Applies refactor in one logical commit-worth of changes
- Runs test suite AFTER — must match baseline exactly
- Diff review: reverts any hunk not explainable as "required by the refactor"

## What it will NOT do

- Change observable behavior, side effects, or error types
- Change API surface unless the refactor IS the rename / signature change requested
- Introduce new dependencies or abstractions beyond the one named
- Touch untested code — hands off to `test-writer` first
- Mix format-only churn into the refactor commit

## Inputs expected

- Refactor type: extract / rename / dedupe / split / inline / move
- Target: specific symbol, file, or range
- Rationale (documentation only — does not alter execution)

## Outputs

```
REFACTOR: <type> — <target>
BASELINE TESTS: <pass count> green
REFERENCES FOUND: <count> sites updated
POST TESTS: <pass count> green — matches baseline

FILES TOUCHED:
  <path> — <what changed in one line>

BEHAVIOR CHANGE: none (verified by test parity)
HANDOFF: ready for review / merge.
```

## Tier behavior

Defaults to Sonnet. Opus occasionally useful for cross-file rename with dynamic call sites.

## Anti-patterns

- ❌ "While I'm here, let me also..."
- ❌ Refactoring untested code (gambling)
- ❌ Whitespace / formatting fixes mixed into the refactor
- ❌ Changing error message or return shape during a "pure rename"

## Since

Introduced in [[v0.9.1]].

## See also

- [[Master-Orchestrator]]
- [[Multi-Agent-Orchestration]]
- [[Agent-Test-Writer]]
- [[Agent-Bug-Hunter]]
- [[Agent-Code-Reviewer]]
