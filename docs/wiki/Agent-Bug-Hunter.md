# Agent: bug-hunter

> Root-cause a failing symptom and return the smallest fix that makes runtime green.

## When to invoke

- Test breaks, CI red
- Endpoint returns wrong data / wrong status
- Stack trace or uncaught exception
- User asks "why does X fail" or "why is this broken"
- Regression after a recent deploy
- Handoff from [[Agent-Perf-Profiler]] when a bottleneck is actually a bug

## What it does

- Reproduces the failure before hypothesizing
- Runs `git log --grep=<keyword>` and `git log -S <symbol>` as mandatory first pass
- Reads the failing code path top-down, no skipping
- States hypothesis with confidence label `[high|medium|low|unsure]` before editing
- Makes minimal change — one file if possible, no surrounding cleanup
- Re-runs repro; runtime green = done, still red = revert + re-hypothesize

## What it will NOT do

- Refactor while fixing (cleanup is a separate mission)
- Suppress errors (no `try/except pass`, `@`, `// eslint-disable`) to hide the symptom
- Speculate ("probably", "likely", "should work")
- Add features or tests — tests go to [[Agent-Test-Writer]]

## Inputs expected

- Symptom: exact error message, failing test name, wrong output, or stack trace
- Repro steps (if known)
- Relevant files (optional — agent can locate)

## Outputs

Structured report:

```
SYMPTOM / REPRO / ROOT CAUSE (file:line) / CONFIDENCE / FIX / VERIFICATION / SCOPE
```

Confidence `low` or `unsure` → stops, presents options, user picks.

## Tier behavior

Runs on Sonnet by default. Bumped to Opus when root cause spans >2 files or involves framework internals.

## Anti-patterns

- ❌ "This might fix it — try and see"
- ❌ Drive-by refactor in the same diff
- ❌ Catch-and-ignore to make CI green
- ❌ Skipping `git log` archaeology

## Since

Introduced in [[v0.9.1]].

## See also

- [[Master-Orchestrator]]
- [[Multi-Agent-Orchestration]]
- [[Kasi-Fix]]
- [[Agent-Test-Writer]]
- [[Agent-Audit-Specialist]] — for `--focus=perf` after a fix exposes a bottleneck (deprecated `[[Agent-Perf-Profiler]]` stub still works)
