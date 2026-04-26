# Agent: test-writer

> One target per call. Regression case mandatory after every bug fix.

## When to invoke

- User asks for tests on a specific function / class / endpoint
- Immediately after `bug-hunter` ships a fix (regression test)
- Backfilling coverage before `refactor-surgeon` can proceed
- New endpoint needs happy-path + edge-case coverage

## What it does

- Reads target and its neighbors — inputs, outputs, side effects
- Reads existing test files to match framework, style, fixture pattern
- Lists test cases BEFORE writing: happy path / edges (empty, null, zero, max, unicode, TZ, concurrent) / error path / regression
- Writes tests with one assertion focus each, descriptive names
- Runs suite — reports runtime green or why not
- Reports coverage gaps and why deferred

## What it will NOT do

- Mock code under test (mocks only for external HTTP, clock, filesystem)
- Use inline magic fixtures — pulls from project factories / seeders
- Emit snapshot tests for logic (only for stable serialized output)
- Write tests that merely re-type the implementation
- Accept a call that lists multiple targets — scope is one per invocation

## Inputs expected

- Target: `file:function` or endpoint
- Context: what was changed, or what bug was just fixed
- Test framework (optional — detected from project)

## Outputs

```
TARGET: <file:function>
FRAMEWORK: <pytest | jest | phpunit | ...>
TEST FILE: <path>

CASES WRITTEN:
  ✓ happy_path_<desc>
  ✓ edge_<desc>
  ✓ error_<desc>
  ✓ regression_<bug-ref>

RUNTIME: <pass/fail from test runner>
GAPS (intentionally not tested):
  - <case> — <why deferred>

HANDOFF: ready for CI / review.
```

## Tier behavior

Defaults to Sonnet. Opus rarely needed; tests favor mechanical enumeration.

## Anti-patterns

- ❌ Mocking the function being tested
- ❌ Bug fix without a regression test
- ❌ "assertEquals(impl(), impl())"-style tautologies
- ❌ Snapshot test on business logic output

## Since

Introduced in [[v0.9.1]].

## See also

- [[Master-Orchestrator]]
- [[Multi-Agent-Orchestration]]
- [[Agent-Bug-Hunter]]
- [[Agent-Refactor-Surgeon]]
- [[Agent-Audit-Specialist]] — for `--focus=quality` review of test code itself (deprecated `[[Agent-Code-Reviewer]]` stub still works)
