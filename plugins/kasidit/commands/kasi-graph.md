---
description: Function call graph — build/show/extract subgraph for scoped audit
---

Build and query a function-level call graph of the project. Used by `/kasi-backend audit|perf` to scope specialists to a subgraph instead of the whole repo.

**Sub-modes (first arg):**

| Sub | What it does |
|-----|--------------|
| `build` | parse project, write `.kasidit/FUNCTIONS.jsonl` + `.kasidit/HOTSPOTS.md` |
| `show` | print HOTSPOTS.md (no rebuild) |
| `extract <fn>` | extract subgraph around fn, write `.kasidit/subgraph-<id>.md` |
| `impact <fn>` | show all callers transitively (who breaks if I change fn?) |
| `trace <fn>` | show full call chain from fn down |
| `cycles` | list detected cycles |
| `dead` | list functions with 0 callers (potential dead code) |

If no sub-mode → run `build` then `show`.

**Storage:**

```
.kasidit/
├── FUNCTIONS.jsonl       # one fn per line — {file, fn, calls, called_by, lang, line}
├── HOTSPOTS.md           # human-readable summary
└── subgraph-<id>.md      # extracted subgraph for current mission
```

**Record shape (FUNCTIONS.jsonl):**

```json
{"file":"app/Http/Controllers/SaleController.php","fn":"store","class":"SaleController","line":42,"lang":"php","calls":["validate","Sale::create","StockService::deduct","Log::info"],"called_by":["routes/api.php:apiResource"]}
```

**HOTSPOTS.md sections:**

```
## Top hubs (called the most)
1. SaleController::store — 47 callers
2. StockService::deduct — 31 callers
...

## Top callers (call the most)
1. Migrate::run — calls 89 fns
...

## Cycles
- A → B → C → A

## Isolated (no caller, no callee)
- OldHelper::deprecated_x

## Dead (defined but never called)
- HelperUnused::doStuff
```

**Build pipeline:**

1. Detect language(s) by file extension + project files (composer.json / package.json).
2. Try ast-grep if installed → exact AST extraction.
3. Else fallback: grep-based regex parser (PHP/JS/TS) — fast, ~95% accurate, brittle on edge cases.
4. Two passes:
   - **Pass 1**: extract all fn definitions (file, name, class, line).
   - **Pass 2**: for each definition body, extract callsites; resolve to known definitions by name match.
5. Write JSONL.
6. Compute hotspots → write HOTSPOTS.md.

**Run script:**

```
~/.claude/skills/kasidit/scripts/build_graph.sh <project-root>
```

If ast-grep missing → script auto-falls back to Python regex parser. Reports which path used in stdout.

**Extract subgraph:**

```
/kasi-graph extract SaleController::store
/kasi-graph extract SaleController.*       ← glob all methods of SaleController
```

Writes `.kasidit/subgraph-<id>.md`:

```
# Subgraph: SaleController::store

## Center
SaleController::store @ app/Http/Controllers/SaleController.php:42

## Callees (depth=2)
SaleController::store
├── validate (Laravel framework)
├── Sale::create
│   └── Sale::boot::saving (Eloquent hook)
├── StockService::deduct
│   ├── Stock::query
│   └── Stock::save
└── Log::info

## Callers (depth=2)
routes/api.php:apiResource
└── (route group: middleware [AuthSanctum, ThrottleApi])

## Files in subgraph
- app/Http/Controllers/SaleController.php
- app/Models/Sale.php
- app/Services/StockService.php
- app/Models/Stock.php
- routes/api.php
```

**Tier rules:**

- **Haiku** — `build` allowed (mechanical), `extract` allowed. `impact`/`trace` analytical → Sonnet/Opus only.
- **Sonnet** — all modes.
- **Opus** — all modes, may infer indirect dynamic calls.

**Limits + caveats:**

- Static analysis only. Misses: dynamic dispatch (`call_user_func`, `$obj->{$method}()`), magic methods (`__call`), reflection, Eloquent hooks via name convention.
- Resolution by name match only. If two classes have method `save`, both get linked — overcounts.
- Confidence per edge: `[high]` if class+method both resolve, `[medium]` if name-only match, `[low]` if string-call.
- Skip `vendor/`, `node_modules/`, `dist/`, `build/`, `.git/`, `tests/` (unless `--include-tests`).

**Defaults:**

- subgraph depth = 2 (callers 2 hops up + callees 2 hops down).
- top-N for hotspots = 10.
- file size limit = 1MB per file (skip larger).

**Anti-patterns:**

- ❌ Build graph during a fix mission — adds noise, slows iteration.
- ❌ Run audit on full graph when subgraph would do.
- ❌ Trust [low] edges — flag for user review, don't reason on them.

**Examples:**

```
/kasi-graph build
/kasi-graph show
/kasi-graph extract SaleController::store
/kasi-graph impact StockService::deduct
/kasi-graph trace Migrate::run
/kasi-graph cycles
/kasi-graph dead
```
