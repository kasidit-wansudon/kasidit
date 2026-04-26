# /kasi-docs

> Fetch version-matched official documentation and cache a concise snippet under `.kasidit/knowledge/`.

## Usage

```
/kasi-docs <topic>             # fetch docs for a topic / function
```

## What it does

- Detects stack version from `composer.json`, `package.json`, `requirements.txt`, `pyproject.toml`, or `go.mod`, plus CLI checks (`artisan --version`, `php -v`, `node -v`).
- Fetches in priority order: project source → official docs at exact version → GitHub source at matching release tag.
- Extracts the specific snippet needed, not the full page.
- Caches to `.kasidit/knowledge/<stack>-<version>-<topic>.md`.
- Outputs a concise answer with source URL and cached path.

## Trust hierarchy

1. Project source (local, actual) — `grep -r "functionName" vendor/ node_modules/`
2. Official docs at the project's pinned version
3. Official docs at latest (only if version is current)
4. GitHub source at the matching release tag
5. Stack Overflow — keywords only, never copy code
6. AI memory for version-specific syntax — never trust

## Flow

1. Detect stack version.
2. User names a topic or function.
3. Walk the trust hierarchy top-down.
4. Extract the minimal snippet.
5. Cache under `.kasidit/knowledge/<stack>-<version>-<topic>.md`.
6. If a cached file already matches, read cache first.

## When to use

- Before writing framework-specific code on an unfamiliar version.
- When model's pretrained syntax might mismatch the project's pinned version.
- Building up `.kasidit/knowledge/` during [[Kasi-Init]].

## When NOT to use

- Project uses latest on a current framework and the snippet is trivial.
- No network and cache is empty — offer to defer.

## Anti-patterns

- Fetching latest docs for an old project version — confident wrong code.
- Caching whole pages instead of the needed snippet.
- Skipping the cache check and re-fetching on every invocation.

## Since

Introduced in [[v0.2.1]].

## See also

- [[Commands]] (aggregate)
- [[Kasi-Init]]
- [[Kasi-Search]]
