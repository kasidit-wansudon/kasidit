# /kasi-review-deploy

> Deploy readiness review — inspect and report only. Zero execution, zero file writes, on any platform, at any tier. Permanently.

## Usage

```
/kasi-review-deploy staging
/kasi-review-deploy prod diff
/kasi-review-deploy prod secrets
```

Counterpart to [[Kasi-Deploy]] — this command has **no execute path at all**. It's the strict extraction of the preflight checklist that used to live inside `/kasi-devopt deploy <env>`, pulled out so the "never runs anything" guarantee is an unconditional property of the command itself, not a soft rule embedded in a multi-mode one.

## What it does

- Runs a full preflight checklist for the given env: env vars vs template, pending migrations, CI status (read-only — never triggers a run), uncommitted changes, debug statements left in the diff, rollback plan present, secrets diff.
- Scores each item ✅ / ⚠️ / ❌ / ❓.
- Outputs one of three verdicts: **ready** / **ready with warnings** / **not ready**.
- Answers "is it safe to deploy" — never "how do I deploy." It does not propose deploy commands; that framing belongs to [[Kasi-Deploy]].

## Flow

1. Confirm env + service.
2. Refresh structural state if stale ([[Kasi-Struc]], read-only bridge check).
3. Read `STATE/config.json` + `STATE/deploy_history.jsonl` — never write to either.
4. Detect platform from repo files (same detection table as [[Kasi-Deploy]] / [[Kasi-Devopt]]).
5. Run the checklist, score each item.
6. Print the report + verdict. Stop.

## Output shape

```
Mission:    review-deploy kas-sass → staging
Platform:   <detected>
Branch:     <git ref>
Preflight:
  ✅ env vars match template
  ✅ no pending migrations
  ⚠️  CI status unknown (no token configured)
  ❌ uncommitted changes present (3 files)
Verdict:    NOT READY — resolve ❌ item(s) first
Confidence: [high] — every item read from source, none inferred
```

## When to use

- Any time before a deploy window, whether or not you're about to run [[Kasi-Deploy]] right after.
- You want the safety check with an absolute guarantee nothing gets touched — e.g. reviewing readiness hours before an actual deploy, or on a platform you don't fully trust Kasidit to touch.

## When NOT to use

- You actually want the deploy to happen — this command stops after reporting. Use [[Kasi-Deploy]] to execute or get a plan.

## Tier behavior

**No tier restriction, at all.** Haiku, Sonnet, and Opus run this identically — a mechanical checklist scan carries zero execution risk regardless of which model runs it. This is the one deploy-adjacent command where tier gating doesn't apply.

## Anti-patterns (hard refuse, no tier exception)

- ❌ Run any command beyond local read — including "safe"-seeming ones like a `curl` health check against prod, or a dry-run flag on a deploy CLI. Anything that shells out beyond local read belongs to [[Kasi-Deploy]], not here.
- ❌ Write to `STATE/deploy_history.jsonl` — that file is written by [[Kasi-Deploy]] on actual attempts, never by this command.
- ❌ Modify any file, including `.env*`, config, or runbooks — flag issues, never fix them.
- ❌ Suggest exact deploy commands as if to run next — that framing belongs to [[Kasi-Deploy]]'s plan-only fallback.
- ❌ Read `.env` file contents into context — list keys only.

## Since

Introduced in [[v0.16.0]]. Extracted from `/kasi-devopt deploy`'s inline preflight.

## See also

- [[Commands]] (aggregate)
- [[Kasi-Deploy]] — the execute-capable counterpart, runs this checklist internally first
- [[Kasi-Devopt]] — the superseded original
- [[Model Tiers]]
