---
description: Initialize project for Kasidit — chains scaffold + docs + review + registers auto-invoke
---

One-shot bootstrap for a new or existing project. Chains the essential Kasidit commands and wires the project so future sessions auto-apply the framework.

**Chain executed (in order):**

1. `/kasi-scaffold` — build `.kasidit/` structure (INDEX / RELATIONS / MEMORY / PATTERNS / CHECKLISTS / knowledge).
2. **Gravity pull** — if `~/.claude/skills/kasidit/center/checklists/` has items matching detected stack, invoke `/kasi-pull all-for <stack>` to seed `.kasidit/CHECKLISTS/` and `.kasidit/knowledge/` from Centerlite. One batch confirm.
3. `/kasi-docs` — fetch version-matched official docs for detected stack, cache to `.kasidit/knowledge/`.
4. Create `.kasidit/MISSION.md` — blank mission template (mission / tier / counter / success criteria).
5. `/kasi-review` (light pass) — quick top-level sanity review on one module picked by user. Skippable on request.
6. **`.gitignore` privacy guard** — append `.kasidit/knowledge/*.private.md` and a comment noting Centerlite logs live at `~/.claude/skills/kasidit/center/logs/` and must never be committed anywhere. If project has no `.gitignore`, create one. Skipped on `dry-run`.
7. Register project auto-invoke:
   - If `.claude/settings.local.json` missing → create.
   - Add `SessionStart` hook that prints `"/kasidit framework active for this project"` into context, so every new session starts grounded.
   - Append guidance block to project `CLAUDE.md` (or create if missing) pointing at `.kasidit/INDEX.md`.

**Flow rules:**

- Confirm each step with the user before running — `/kasi-init` is multi-command; narrate, do not surprise.
- If `.kasidit/` already exists → ask whether to (1) skip scaffold, (2) merge non-destructively, (3) abort.
- Detect stack first from `composer.json` / `package.json` / `requirements.txt` / `go.mod` / `Cargo.toml`. If ambiguous → ask.
- Tier = current session tier (Opus / Sonnet / Haiku). On Haiku → skip step 4 (review) unless user insists; Haiku review without checklists is weak.
- Global user log hook (`UserPromptSubmit → kasidit-log.sh`) already captures prompts at user scope; `/kasi-init` does **not** re-register it per project.

**After init, report:**

```
.kasidit/ ✓
  ├ INDEX.md        (N files indexed)
  ├ RELATIONS.md    (M modules)
  ├ PATTERNS.md     (K detected patterns)
  ├ CHECKLISTS/     (copied for <stack>)
  └ knowledge/      (D doc snippets cached)
Auto-invoke     ✓ registered in .claude/settings.local.json
Log hook        ✓ global (~/.claude/skills/kasidit/logs/)
Next mission    → suggest /kasi-review <module> or state your own mission
```

**Anti-patterns:**

- ❌ Silent overwrite of existing `.kasidit/`.
- ❌ Registering global log hook again (already at user scope).
- ❌ Injecting auto-invoke hook into shared / production repos without asking.
- ❌ Running full `/kasi-review` on Haiku during init — heavy, use a small module or defer.
- ❌ Skipping stack detection and assuming Laravel / React / whatever.

**User commands during init:**

- `skip docs` — omit step 2 (use when offline or docs already cached).
- `skip review` — omit step 4.
- `no auto-invoke` — omit step 5 (scaffold only).
- `dry-run` — print plan, do not write files.
