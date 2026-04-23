---
description: Sync docs/wiki/ content to github wiki repo (github.com/kasidit-wansudon/kasidit.wiki.git)
---

Push the repo-tracked wiki source (`docs/wiki/`) up to the GitHub wiki. Manual command — runs only on invocation, not automatic on commit.

**Usage:**

```
/kasi-wiki-sync              # dry-run by default: shows what would change
/kasi-wiki-sync apply        # actually push
/kasi-wiki-sync <page>       # single page only
```

**Why manual:**

GitHub wiki is a separate git repo (`kasidit.wiki.git`). Syncing on every commit adds noise, breaks atomic PR review, and risks auth failures interrupting normal work. Manual invocation keeps the wiki **intentional**.

**Flow:**

1. Verify `docs/wiki/` exists in repo and has `*.md` pages.
2. Clone `git@github.com:kasidit-wansudon/kasidit.wiki.git` into tmp dir (first run) or fetch + checkout.
3. Diff `docs/wiki/*.md` vs wiki repo. Print file-by-file diff.
4. If `apply`:
   - Copy changed files into wiki clone.
   - Commit: `docs(wiki): sync from main @ <short-sha>`
   - Push. Report result.
5. If dry-run: list changes, exit. No push.

**File name mapping:**

| Source | Wiki page |
|--------|-----------|
| `docs/wiki/Home.md` | `Home.md` (wiki landing) |
| `docs/wiki/Version-History.md` | `Version-History.md` |
| `docs/wiki/v0.9.2.md` | `v0.9.2.md` |
| `docs/wiki/_Sidebar.md` | `_Sidebar.md` (wiki nav) |
| `docs/wiki/_Footer.md` | `_Footer.md` |

GitHub wiki files must live at root of the wiki repo — flat structure only.

**Auth prereq:**

- SSH: `git@github.com:kasidit-wansudon/kasidit.wiki.git` with working key.
- HTTPS: token with `repo` scope.
- If auth fails → print command, user runs manually.

**Rules:**

- Dry-run by default. Never push without explicit `apply`.
- Never delete wiki pages automatically — print list of orphans, user decides.
- Each sync commit message includes source sha for traceability.
- If wiki clone dir already exists, `git pull` first to avoid push conflicts.

**Anti-patterns:**

- ❌ Auto-run on post-commit hook (user said: manual).
- ❌ Rewriting wiki history (`--force` push).
- ❌ Rendering markdown client-side — GitHub wiki renders; just ship raw `.md`.
- ❌ Nested folders in `docs/wiki/` — flattened on push, silently loses structure.

**Future:**

If user opts in, wrap this in a GitHub Action on `push: main` with a flag file (`docs/wiki/SYNC_ON_PUSH`). Not v0.9.2 scope.
