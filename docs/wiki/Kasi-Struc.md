# /kasi-struc

> Project structure index + auto-bridge cache. `kasi-*` commands read cached state instead of rescanning the repo every invocation.

## Usage

```
/kasi-struc build
/kasi-struc refresh
/kasi-struc show
/kasi-struc tree
/kasi-struc module <name>
/kasi-struc path <file>
/kasi-struc bridge
/kasi-struc verify
```

If no sub-mode is given, runs `build` on first use or `show` on subsequent calls.

## What it does

- Builds and serves structural knowledge — directory layout, module relations, function call graph (delegates to [[Kasi-Graph]]), HTTP routes, and config map.
- Acts as an **auto-bridge**: when any `kasi-*` command needs structural info, it pulls from cached state at `.kasidit/STATE/` instead of re-scanning.
- Updates incrementally on file change via `refresh` (diffs against `git diff --name-only <last_sync_ref> HEAD` + uncommitted changes) rather than re-walking the whole repo.

## The bridge contract

Any `kasi-*` command that needs structural info must:

1. Check `.kasidit/STATE/last_sync` exists.
2. Compare with current `git rev-parse HEAD` (or repo-root mtime if no git).
3. If state is newer than the last user edit → use cached state directly.
4. If stale → refresh incrementally (only changed files), update the changelog, then use.
5. If state is missing → tell the user to run `/kasi-struc build` first, then proceed with degraded scope.

## State directory

```
.kasidit/STATE/
├── structure.json          # top-level — dirs, files, languages, sizes
├── modules.jsonl           # module-level: files, exports
├── relations.jsonl         # module-to-module deps (imports/requires)
├── functions.jsonl         # mirrors FUNCTIONS.jsonl from /kasi-graph
├── routes.jsonl            # HTTP routes — method, path, handler, middleware
├── config.json             # detected configs — laravel/node/python/etc
├── changelog.jsonl         # append-only log of state changes
└── last_sync               # timestamp + git ref of last build
```

## When to use

- Any time you'd otherwise want the AI to "look around the repo first" — build once, then every subsequent command reads cache.
- `module <name>` / `path <file>` for a quick structural summary of one area without a full audit.
- `bridge` to see which commands consume which STATE files.

## When NOT to use

- Force a full `build` every command — use `refresh`, it's incremental and cheaper.
- Hand-edit STATE files — they're derived and get overwritten on the next refresh.

## Tier behavior

- **Haiku** — `build`, `refresh`, `show`, `path`, `module`, `tree` allowed (all mechanical).
- **Sonnet/Opus** — all sub-modes, including `verify`.

## Limits + caveats

- `refresh` assumes git; without it, falls back to slower/less-precise mtime comparison.
- Symbol extraction has the same brittleness as [[Kasi-Graph]] (regex unless `ast-grep` is present).
- Route detection covers common frameworks — may miss DSL-style routes.
- `.kasidit/STATE/` is gitignored by default — it's a derived project artifact, not source of truth.

## Anti-patterns

- ❌ Force `build` every command — use `refresh`.
- ❌ Edit STATE files by hand.
- ❌ Trust cached state across a branch switch without `refresh`.
- ❌ Commit `STATE/` to git.

## Since

Introduced in [[v0.11.0]].

## See also

- [[Commands]] (aggregate)
- [[Kasi-Graph]] — call graph, the piece `/kasi-struc build` calls into
- [[Kasi-Backend]] — primary consumer of `STATE/functions.jsonl` + `routes.jsonl`
- [[Kasi-Devopt]] — consumes `STATE/config.json` + `routes.jsonl`
