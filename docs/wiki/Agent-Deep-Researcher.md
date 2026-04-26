# Agent: deep-researcher

> Gather evidence from trusted sources, cache it, and return a findings digest. Never writes production code.

## When to invoke

- Need version-matched docs for a library / API / framework question
- Competitor or alternative library comparison
- Codebase survey before a design decision
- Migration planning needs "what changed between v9 and v10"
- [[Agent-Architect-Planner]] flagged an OPEN QUESTION that requires external evidence

## What it does

- Applies trust hierarchy: project source → official docs (pinned version) → latest docs → framework source at release tag → changelogs → (keyword hints only) SO/blogs
- Cross-checks every load-bearing claim against ≥2 sources
- Flags version mismatches aggressively ("works in v10" ≠ "works in v8")
- Caches findings to `.kasidit/knowledge/<stack>-<version>-<topic>.md` with source URL + fetched-at date
- Returns 5–10 bullet digest, each tagged with confidence + source URL

## What it will NOT do

- Synthesize version-specific syntax from model memory (assumed wrong until doc-verified)
- Emit claims without a source URL
- Write final production code — hands off to [[Agent-Architect-Planner]] or main
- Stop at one source for load-bearing claims

## Inputs expected

- Question: scoped, answerable ("how does Laravel 8 handle X")
- Constraints: version pins, license, perf, ecosystem fit
- Decision the research supports (keeps scope tight)

## Outputs

```
QUESTION / VERSION CONTEXT / FINDINGS (confidence + URL + fetched-at) /
CONTRADICTIONS (+ resolution) / CACHED TO / HANDOFF
```

Cache path: `.kasidit/knowledge/<stack>-<version>-<topic>.md`

## Tier behavior

Sonnet default. WebFetch + WebSearch tools required.

## Anti-patterns

- ❌ "Based on my training data..." for version-specific APIs
- ❌ Single-source claim flagged `[high]`
- ❌ Stack Overflow cited as primary source
- ❌ Writing the fix instead of handing off

## Since

Introduced in [[v0.9.1]].

## See also

- [[Master-Orchestrator]]
- [[Multi-Agent-Orchestration]]
- [[Kasi-Docs]]
- [[Agent-Architect-Planner]]
- [[Agent-Migration-Specialist]]
