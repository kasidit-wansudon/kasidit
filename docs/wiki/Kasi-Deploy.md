# /kasi-deploy

> Deploy mission with a real execute path. The first Kasidit command permitted to run a deploy command itself — and only under a fixed platform capability table.

## Usage

```
/kasi-deploy staging
/kasi-deploy prod
/kasi-deploy prod --allow-dirty
```

Supersedes `/kasi-devopt deploy <env>` ([[v0.16.0]]), which never executed anything. Counterpart to [[Kasi-Review-Deploy]] (read-only) — this command **can execute**, but only where execution is safe, idempotent, and reversible-by-redeploy.

## Platform capability (fixed, not a per-mission judgment call)

| Platform | Detected by | Mode |
|---|---|---|
| Cloudflare Workers/Pages | `wrangler.toml` / `wrangler.jsonc` | **auto-executable** — `wrangler deploy` / `wrangler pages deploy` |
| Vercel | `vercel.json` / `.vercel/` | **auto-executable** — `vercel deploy` / `vercel --prod` |
| Netlify | `netlify.toml` | **auto-executable** — `netlify deploy` |
| SSH / bare VPS | no platform file, or `Procfile` | **plan-only** — no safe non-interactive credential path |
| Docker / k8s / Terraform / Serverless / Fly / Platform.sh | `Dockerfile`, `k8s/`, `*.tf`, `serverless.yml`, `fly.toml`, `.platform.app.yaml` | **plan-only** — one-shot command exists but touches shared infra state |

Only platforms with a first-party, idempotent, single-command CLI deploy are auto-executable. Everything else gets the exact plan-only behavior the old `/kasi-devopt deploy` always had.

## What it does

- Runs the [[Kasi-Review-Deploy]] preflight checklist inline, every time — never skipped.
- NOT READY verdict → stops. Neither executes nor hands over a plan until preflight passes.
- Branches on platform capability: auto-executes, or falls back to a plan-only command list.
- Confirm gate: staging/preview needs a plain confirm; **prod requires the typed phrase `confirm: deploy-prod`** — a plain "yes" is rejected.
- Dirty working tree → forced to plan-only regardless of env, unless `--allow-dirty`.
- On execute: captures stdout/stderr/exit code. A nonzero exit is reported, never summarized away.
- On failure: reports the error, stops. **No auto-retry, no auto-rollback** — that's a separate decision for the user.
- Logs every attempt to `STATE/deploy_history.jsonl` — `mode: executed` (with exit code) or `mode: plan-only` (`outcome: handed-to-user`).

## Flow

1. Confirm env (staging/prod) + service.
2. Run preflight ([[Kasi-Review-Deploy]] checklist).
3. NOT READY → stop, show failing items.
4. Auto-executable platform → confirm gate → execute → report + log.
5. Plan-only platform → show commands (same format as old `/kasi-devopt deploy`), user runs them, log `mode: plan-only`.

## Confirm gate summary

| Env | Auto-exec allowed | Gate |
|---|---|---|
| staging/preview | yes | plain confirm |
| prod | yes, if platform auto-executable | typed `confirm: deploy-prod` + diff shown first |
| any env, dirty tree | no | forced plan-only, or `--allow-dirty` |
| any env, preflight NOT READY | no | blocked entirely |

## When to use

- A deploy on Cloudflare/Vercel/Netlify where you want it actually run, not just planned.
- Any deploy where you want the preflight discipline even if the platform is plan-only.

## When NOT to use

- You never want Kasidit to execute anything — use [[Kasi-Review-Deploy]] instead, permanently read-only regardless of platform.
- Rollback after a failure — this command reports the error and stops; rolling back is a separate, deliberate user action.

## Tier behavior

- **Haiku** — plan-only path only, on any platform. Auto-execute is refused: "auto-execute needs Sonnet or Opus tier."
- **Sonnet** — full auto-execute path on staging; prod requires the same typed confirm gate as Opus.
- **Opus** — full auto-execute path on both envs, may also propose rollback runbook updates after a failure (proposal only — user applies).

## Anti-patterns

- ❌ Auto-execute on a plan-only platform because "the command looks simple enough" — the capability table is fixed.
- ❌ Skip the preflight checklist to save a step.
- ❌ Execute with a dirty working tree without explicit `--allow-dirty`.
- ❌ Auto-retry a failed deploy, or auto-rollback on failure.
- ❌ Accept a plain "yes" as the prod confirm — must be the typed `confirm: deploy-prod` phrase.
- ❌ Read `.env` values into context to build the deploy command — keys only; the deploy CLI reads env itself.

## Since

Introduced in [[v0.16.0]]. Supersedes `/kasi-devopt deploy`.

## See also

- [[Commands]] (aggregate)
- [[Kasi-Review-Deploy]] — the read-only counterpart, run internally as this command's preflight
- [[Kasi-Devopt]] — the superseded original, other sub-modes unchanged
- [[Model Tiers]] — deploy execution tier gating
