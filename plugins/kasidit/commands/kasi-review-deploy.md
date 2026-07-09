---
description: Deploy readiness review — inspect and report only, never executes anything or touches files
---

Read-only preflight review before a deploy. Counterpart to `/kasi-deploy` — this command has **zero side effects**: no shell command execution, no file writes, no state mutation beyond the review report itself. Extracted from `/kasi-devopt deploy <env>` (v0.11) as its own command so the "never runs anything" guarantee is explicit and unconditional, not just a soft rule inside a multi-mode command.

**Sub-modes (first arg):**

| Sub | What it does | Specialist |
|-----|--------------|------------|
| `<env>` | full preflight checklist for env, no exceptions | `audit-specialist --focus=quality` |
| `<env> diff` | preflight + diff vs currently deployed prod state | `audit-specialist --focus=quality` |
| `<env> secrets` | preflight + secrets-in-diff scan (no values, keys only) | `audit-specialist --focus=security` |

If no arg → ask user which env (staging/prod) + which service.

**Flow:**

1. Confirm env + service.
2. `/kasi-struc refresh` if state stale (read-only bridge check).
3. Read `STATE/config.json` + `STATE/deploy_history.jsonl` — never write to either.
4. Detect platform from repo files (same detection table as `/kasi-devopt`).
5. Preflight checklist:
   - Env vars match template? (`/kasi-devopt env diff`, read-only)
   - Migrations pending? (check `database/migrations` vs last-migrated marker)
   - Tests passing on target branch? (read CI status if token available — never trigger a run)
   - Uncommitted changes in working tree? (`git status --short`, read-only)
   - No `console.log` / `dd()` / debug statements left in diff?
   - Rollback plan documented in `.kasidit/runbooks/`?
   - Secrets diff — any new/changed keys not in template?
6. Score each item ✅ / ⚠️ / ❌ / ❓.
7. Output report + one-line verdict: **ready** / **ready with warnings** / **not ready**.
8. Stop. Do not propose commands to run, do not offer to run anything, do not write history.

**Output format:**

```
Mission:    review-deploy kas-sass → staging
Platform:   <detected>  (read-only detection, not confirmed by execution)
Branch:     <git ref>
Preflight:
  ✅ env vars match template
  ✅ no pending migrations
  ⚠️  CI status unknown (no token configured)
  ✅ no debug code in diff
  ❌ uncommitted changes present (3 files)
  ❓ rollback plan — not found in .kasidit/runbooks/
Verdict:    NOT READY — resolve ❌ item(s) first
Confidence: [high] — every item read from source, none inferred
```

**Tier rules:**

- **Haiku** — full mode. Mechanical checklist scan is exactly what Haiku is for; no execution risk exists at any tier.
- **Sonnet** — same, adds narrative on ⚠️/❓ items.
- **Opus** — same, may flag structural deploy-process risks beyond the checklist (e.g. "this env has no CI gate at all").

**Anti-patterns (hard refuse, no tier exception):**

- ❌ Run any command — including "safe" ones like `git status` outside a read-only wrapper, `curl` health checks that hit prod, or a dry-run flag on a deploy CLI. If it touches the network or shells out beyond local read, it doesn't belong here — that's `/kasi-deploy`'s job.
- ❌ Write to `STATE/deploy_history.jsonl` — that file is written by `/kasi-deploy` on actual attempts, never by this command.
- ❌ Modify any file, including `.env*`, config, or runbooks — flag issues, never fix them.
- ❌ Suggest exact deploy commands as if to be run next — that framing belongs to `/kasi-deploy`'s plan-only fallback, not here. This command answers "is it safe to deploy", not "how do I deploy".
- ❌ Read `.env` file contents into context — list keys only, per `/kasi-devopt` safety rule.

**Relationship to other commands:**

- `/kasi-review-deploy <env>` → read report → user decides → `/kasi-deploy <env>` (executes or hands plan, depending on platform).
- Running `/kasi-deploy` always runs this checklist internally first — but this standalone command exists so a user can review without triggering `/kasi-deploy`'s execute path, e.g. hours before an actual deploy window.

**Examples:**

```
/kasi-review-deploy staging
/kasi-review-deploy prod diff
/kasi-review-deploy prod secrets
```
