# /kasi-wiki-sync

> Push `docs/wiki/*.md` to `github.com/kasidit-wansudon/kasidit.wiki.git`. Dry-run by default, manual-only.

## Usage

```
/kasi-wiki-sync              # dry-run by default: shows what would change
/kasi-wiki-sync apply        # actually push
/kasi-wiki-sync <page>       # single page only
```

## What it does

- Verifies `docs/wiki/` exists and contains `*.md` pages.
- Clones `git@github.com:kasidit-wansudon/kasidit.wiki.git` into a tmp dir on first run, or fetches and checks out.
- Diffs `docs/wiki/*.md` against the wiki repo, prints file-by-file diff.
- On `apply`: copies changed files in, commits `docs(wiki): sync from main @ <short-sha>`, pushes.
- On dry-run: prints the diff plan and exits.
- Never deletes wiki pages automatically — prints orphan list, user decides.

## Why manual

GitHub wiki is a separate git repo. Syncing on every commit adds noise, breaks atomic PR review, and risks auth failures interrupting normal work. Manual invocation keeps the wiki intentional.

## Flow

1. Verify `docs/wiki/` exists with `.md` pages.
2. Clone or fetch the wiki repo into a tmp dir. `git pull` first to avoid push conflicts.
3. Diff `docs/wiki/*.md` vs wiki repo contents.
4. If `apply`, copy changed files, commit with the source sha in the message, push.
5. If dry-run, print the diff plan and exit.

## File name mapping

| Source | Wiki page |
|--------|-----------|
| `docs/wiki/Home.md` | `Home.md` (wiki landing) |
| `docs/wiki/Version-History.md` | `Version-History.md` |
| `docs/wiki/v0.9.2.md` | `v0.9.2.md` |
| `docs/wiki/_Sidebar.md` | `_Sidebar.md` (wiki nav) |
| `docs/wiki/_Footer.md` | `_Footer.md` |

GitHub wiki files must live at the root of the wiki repo — flat structure only.

## Auth prereq

- SSH: `git@github.com:kasidit-wansudon/kasidit.wiki.git` with a working key.
- HTTPS: token with `repo` scope.
- If auth fails, the command prints the git commands and the user runs them manually.

## When to use

- Publishing a release's wiki changes alongside the version tag.
- Correcting a wiki page after merging a docs PR in the main repo.
- Promoting a freshly written page from `docs/wiki/` to the public wiki.

## When NOT to use

- Automated post-commit hooks — wiki stays manual by design.
- Force-pushing over wiki history — never rewrite.
- Pushing nested folders — wiki is flat; nested structure silently flattens.

## Anti-patterns

- Auto-run on post-commit hook.
- `--force` push on the wiki repo.
- Rendering markdown client-side before push — GitHub wiki renders; ship raw `.md`.
- Nested folders in `docs/wiki/` — silently loses structure on push.

## Future

If user opts in, wrap this in a GitHub Action on `push: main` gated by a flag file (`docs/wiki/SYNC_ON_PUSH`). Not in [[v0.9.2]] scope.

## Since

Introduced in [[v0.9.2]].

## See also

- [[Commands]] (aggregate)
- [[Version-History]]
- [[Home]]
