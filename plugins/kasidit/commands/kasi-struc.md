---
description: Project structure index — file paths, module relations, function call graph, auto-bridged so AI doesn't rescan every time
---

Build and serve the project's structural knowledge: directory layout, module relations, function call graph, and config map. Acts as an **auto-bridge** — when any kasi-* command needs structure info, it pulls from cached state instead of re-scanning. Updates incrementally on file change.

**Sub-modes (first arg):**

| Sub | What it does |
|-----|--------------|
| `build` | Full scan, write `.kasidit/STATE/structure.json` + sub-files. First-time use. |
| `refresh` | Incremental — only re-scan files changed since `last_sync`. |
| `show` | Print summary (top dirs, module count, fn count, last sync). |
| `tree` | Print directory tree (depth limit 3). |
| `module <name>` | Show module info — files, exports, callers. |
| `path <file>` | Show one file's role — defines, imports, called by. |
| `bridge` | Print which kasi-* commands consume which STATE files. |
| `verify` | Sanity check — walk repo, flag stale entries. |

If no sub-mode → run `build` (first time) or `show` (subsequent).

**State directory:**

```
.kasidit/STATE/
├── structure.json          # top-level — dirs, files, languages, sizes
├── modules.jsonl           # one module per line — name, files, exports
├── relations.jsonl         # module-to-module deps (imports/requires)
├── functions.jsonl         # symlink/copy of FUNCTIONS.jsonl from /kasi-graph
├── routes.jsonl            # HTTP routes — method, path, handler, middleware
├── config.json             # detected configs — laravel/node/python/etc
├── changelog.jsonl         # append-only log of state changes
└── last_sync               # timestamp + git ref of last build
```

**The bridge (auto-load contract):**

When a kasi-* command needs structural info, it MUST:

1. Check `.kasidit/STATE/last_sync` exists.
2. Compare with current `git rev-parse HEAD` (or mtime of repo root if no git).
3. If state newer than last user-edit → use cached state directly (no re-scan).
4. If stale → refresh incrementally (only changed files), update changelog, then use.
5. If state missing → tell user `run /kasi-struc build first`, then proceed with degraded scope.

This avoids re-scanning the repo every audit/fix/review.

**changelog.jsonl shape:**

```json
{"ts":"2026-04-30T11:23:01Z","op":"add","kind":"file","path":"app/Services/RefundService.php","by":"refresh"}
{"ts":"2026-04-30T11:23:02Z","op":"modify","kind":"function","sig":"SaleController::store","line":42,"prev_line":40,"by":"refresh"}
{"ts":"2026-04-30T12:01:33Z","op":"delete","kind":"file","path":"app/Helpers/OldHelper.php","by":"refresh"}
```

Each kasi-* command, before reasoning, may print:

```
[bridge] state ok (last sync 11:23, 2 files changed since git HEAD)
```

Or:

```
[bridge] state stale (47 files changed) — running incremental refresh...
```

**Sub-mode detail:**

### `build`

1. Walk repo (skip `vendor/`, `node_modules/`, `dist/`, `build/`, `.git/`, `tests/` unless flag).
2. For each file: language, size, exported symbols (functions/classes/types).
3. Build module tree (group by directory + entry file).
4. Detect routes (Laravel `routes/*.php`, Express `app.use`, Fastify `register`, NestJS controllers, Hono `app.get`).
5. Detect configs (`composer.json`, `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `.env.example`).
6. Call `/kasi-graph build` to populate `functions.jsonl`.
7. Write all STATE files.
8. Stamp `last_sync` with timestamp + git HEAD.

### `refresh`

1. Diff: `git diff --name-only <last_sync_ref> HEAD` + uncommitted changes.
2. For each changed file: re-extract symbols, update `modules.jsonl` + `relations.jsonl`.
3. Append entries to `changelog.jsonl`.
4. Update `last_sync`.
5. If git unavailable → fall back to mtime newer than `last_sync` timestamp.

### `module <name>`

```
Module: app/Services/StockService
Files:    1 (StockService.php)
Exports:  StockService::deduct, StockService::add, StockService::reserve
Imports:  Stock (model), Log, Cache
Callers:  SaleController::store, TransferController::execute, ReturnController::process
Routes:   none direct
```

### `path <file>`

```
File:     app/Http/Controllers/SaleController.php
Lang:     php
Lines:    412
Class:    SaleController
Methods:  index, show, store, update, destroy, refund (6)
Imports:  Sale, StockService, Log, Validator, Auth
Routes:   GET /api/sales, POST /api/sales, ...
Called by: routes/api.php, tests/Feature/SaleTest.php
```

### `bridge`

Lists which commands read which STATE files:

```
/kasi-backend audit  → STATE/functions.jsonl, modules.jsonl, routes.jsonl
/kasi-backend perf   → STATE/functions.jsonl, routes.jsonl
/kasi-fix            → STATE/functions.jsonl (impact check)
/kasi-graph          → STATE/functions.jsonl (writes)
/kasi-devopt         → STATE/config.json, routes.jsonl, deploy_history
/kasi-review         → STATE/modules.jsonl, relations.jsonl
```

**Tier rules:**

- **Haiku** — `build`, `refresh`, `show`, `path`, `module`, `tree` allowed. Mechanical only.
- **Sonnet/Opus** — all sub-modes including `verify`.

**Limits + caveats:**

- Refresh assumes git. If no git → mtime fallback (slower, less precise).
- Symbol extraction same brittleness as `/kasi-graph` (regex unless ast-grep present).
- Routes detection per-framework — covers common ones, may miss DSL routes.
- STATE/ is gitignored by default (project artifact).

**Why this exists:**

> AI re-scanning the repo every command = slow + context bloat + forgets across turns.
> Structure changes rarely; reason: build once, refresh incrementally, serve from cache.
> Changelog = audit trail. If something looks wrong, last known-good state visible.

**Anti-patterns:**

- ❌ Force `build` every command — use `refresh`.
- ❌ Edit STATE files by hand — they are derived; will be overwritten.
- ❌ Trust state across branch switch without `refresh`.
- ❌ Commit STATE/ to git — add `.kasidit/STATE/` to `.gitignore`.

**Examples:**

```
/kasi-struc build
/kasi-struc refresh
/kasi-struc show
/kasi-struc tree
/kasi-struc module Services/StockService
/kasi-struc path app/Http/Controllers/SaleController.php
/kasi-struc bridge
/kasi-struc verify
```
