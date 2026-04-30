# /kasi-pull

> Copy a shared item from Centerlite into the current project's `.kasidit/` (dcenterlite). Diff-aware, confirmed, detached after copy.

## Usage

```
/kasi-pull <type> <name>
/kasi-pull all-for <stack>     # bootstrap seed, used by /kasi-init
```

## Types

| Type | Source | Target |
|------|--------|--------|
| `checklist` | `center/checklists/<name>.md` | `.kasidit/CHECKLISTS/<name>.md` |
| `knowledge` | `center/knowledge/<name>.md` | `.kasidit/knowledge/<name>.md` |
| `rule`      | selected line from `center/rules.md` | append to `.kasidit/MEMORY.md` |
| `pattern`   | filter `center/patterns.jsonl` by tag | append to `.kasidit/PATTERNS.md` |
| `all-for <stack>` | everything tagged for stack | seed entire `.kasidit/` |

## What it does

- Lists matching items from Centerlite (glob, tag filter, or exact name).
- Shows preview and target paths.
- Diffs against any existing local file.
- Asks to confirm: `(o)verwrite / (m)erge-append / (s)kip`.
- Copies or merges into `.kasidit/`.
- Records the pull event in `MEMORY.md` for traceability.

## Flow

1. Match Centerlite items by name, glob, or tag.
2. Print plan with target paths.
3. Diff against any existing local file.
4. Ask per-item confirmation on conflict.
5. Copy or merge.
6. Append `pulled <type> <name> from center on <date>` to `.kasidit/MEMORY.md`.

## When to use

- Bootstrapping a new project — `/kasi-init` runs `all-for <stack>` as one batch.
- Reusing a proven checklist from another project.
- Importing a shared rule into a new `.kasidit/MEMORY.md`.

## When NOT to use

- Pulling the entire hub — defeats "lightweight per-project".
- Pulling stack-mismatched assets (PHP checklist into a Node project).
- Silent overwrite of a project-customized file.

## Anti-patterns

- Auto-pulling — always confirm (except the single-batch confirm inside `/kasi-init`).
- Treating a pulled file as upstream-tracked — it is detached after copy; use [[Kasi-Promote]] to push back.
- Pulling a mismatched stack checklist.

## Since

Introduced in [[v0.9.2]].

## See also

- [[Commands]] (aggregate)
- [[Gravity-Pattern]]
- [[Kasi-Promote]]
- [[Kasi-Sync]]
