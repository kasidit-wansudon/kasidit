# /kasi-graph

> Function-level call graph — build, query, and extract scoped subgraphs. The primitive `/kasi-backend audit|perf` uses to avoid scanning the whole repo.

## Usage

```
/kasi-graph build
/kasi-graph show
/kasi-graph extract <fn>
/kasi-graph impact <fn>
/kasi-graph trace <fn>
/kasi-graph cycles
/kasi-graph dead
```

If no sub-mode is given, runs `build` then `show`.

## What it does

- Parses the project into a function-level call graph: who calls whom, across files.
- Writes `.kasidit/FUNCTIONS.jsonl` (one record per function: file, name, class, calls, called_by) and `.kasidit/HOTSPOTS.md` (human-readable summary — top hubs, top callers, cycles, dead code).
- Extracts a scoped subgraph around a specific function so a specialist can be handed a narrow slice instead of the full repo.
- `impact <fn>` answers "who breaks if I change this?" via transitive callers; `trace <fn>` shows the full call chain downward from a function.

## Build pipeline

1. Detect language(s) by extension + project files.
2. Try `ast-grep` if installed → exact AST extraction.
3. Else fall back to a grep-based regex parser (PHP/JS/TS) — fast, ~95% accurate, brittle on edge cases.
4. Two passes: extract all function definitions, then resolve callsites by name match.
5. Write `FUNCTIONS.jsonl`, compute hotspots, write `HOTSPOTS.md`.

Run script: `~/.claude/skills/kasidit/scripts/build_graph.sh <project-root>` — auto-falls back to the Python regex parser if `ast-grep` is missing, and reports which path it used.

## When to use

- Before `/kasi-backend audit|perf` on anything larger than a handful of files.
- "What breaks if I change this function" (`impact`) before a risky refactor.
- Finding dead code (`dead`) or circular dependencies (`cycles`) as a periodic health check.

## When NOT to use

- During a fix mission — building the graph mid-fix adds noise and slows iteration; build it before, not during.
- When you already have a subgraph cached and nothing's changed — use `show`, not `build`.

## Tier behavior

- **Haiku** — `build` (mechanical) and `extract` allowed. `impact`/`trace` are analytical — Sonnet/Opus only.
- **Sonnet** — all sub-modes.
- **Opus** — all sub-modes, may infer indirect dynamic calls.

## Limits + caveats

- Static analysis only — misses dynamic dispatch (`call_user_func`, `$obj->{$method}()`), magic methods (`__call`), reflection, and Eloquent hooks via naming convention.
- Resolution is by name match only — two classes with a method named `save` both get linked, which overcounts edges.
- Per-edge confidence: `[high]` if class+method both resolve, `[medium]` if name-only match, `[low]` if string-call.
- Skips `vendor/`, `node_modules/`, `dist/`, `build/`, `.git/`, `tests/` unless `--include-tests` is passed.

## Anti-patterns

- ❌ Build the graph during a fix mission.
- ❌ Run an audit on the full graph when a subgraph would do.
- ❌ Trust `[low]`-confidence edges without flagging for user review.

## Since

Introduced in [[v0.11.0]].

## See also

- [[Commands]] (aggregate)
- [[Kasi-Backend]] — primary consumer (`audit`/`perf` subgraph scoping)
- [[Kasi-Struc]] — broader structural state that includes this graph
