---
description: Deploy mission — auto-executes for CLI-native platforms (Cloudflare, Vercel), plan-only for SSH/manual platforms
---

Run an actual deploy. Counterpart to `/kasi-review-deploy` (read-only) — this command **can execute**, but only where execution is safe, idempotent, and reversible-by-redeploy. Supersedes the `deploy <env>` sub-mode of `/kasi-devopt` (v0.11), which never executed anything; this command keeps that behavior as the *fallback* path and adds a real execute path for platforms with a trustworthy one-shot CLI.

**Platform capability (auto-detected from repo files, same table as `/kasi-devopt`):**

| Platform | Detected by | Mode |
|---|---|---|
| Cloudflare Workers/Pages | `wrangler.toml` / `wrangler.jsonc` | **auto-executable** — `wrangler deploy` / `wrangler pages deploy` |
| Vercel | `vercel.json` / `.vercel/` | **auto-executable** — `vercel deploy` (preview) / `vercel --prod` |
| Netlify | `netlify.toml` | **auto-executable** — `netlify deploy` |
| SSH / bare VPS | no platform file, or `Procfile` | **plan-only** — no safe non-interactive credential path |
| Docker / k8s / Terraform / Serverless / Fly / Platform.sh | `Dockerfile`, `k8s/`, `*.tf`, `serverless.yml`, `fly.toml`, `.platform.app.yaml` | **plan-only** — one-shot command exists but touches shared infra state; too variable to auto-run safely |

Only platforms with a **first-party, idempotent, single-command CLI deploy** are auto-executable. Everything else falls back to the exact `/kasi-devopt deploy` plan-only behavior: show commands, user runs them.

**Flow:**

1. Confirm env (staging/prod) + service.
2. Run the `/kasi-review-deploy` checklist inline (do not skip — a failed preflight blocks execution *and* blocks handing over a plan).
3. If verdict is **NOT READY** → stop, show the failing items, do not proceed to either execute or plan.
4. Branch on platform capability:
   - **Auto-executable** → go to step 5.
   - **Plan-only** → show the plan (same format as former `/kasi-devopt deploy`), user runs it, done. Do not execute.
5. **Auto-executable path — confirm gate:**
   - Staging/preview: show the exact command, ask for plain confirmation.
   - Prod: show exact command + diff vs current prod state, require typed `confirm: deploy-prod` (not a plain yes).
   - Working tree dirty (uncommitted changes) → refuse to execute regardless of env; surface as plan-only instead, unless user explicitly overrides with `--allow-dirty`.
6. Execute the single deploy command via shell. Capture stdout/stderr/exit code — do not summarize away a nonzero exit code.
7. Report result. On failure: show the error, stop. Do **not** auto-retry, auto-rollback, or attempt a fix — that is a separate decision for the user (or a follow-up `/kasi-fix` / rollback runbook).
8. Append entry to `STATE/deploy_history.jsonl`:
   ```json
   {"ts":"2026-07-09T14:20:00Z","env":"staging","service":"kasion-site","platform":"cloudflare-pages","mode":"executed","command":"wrangler pages deploy dist","exit_code":0,"outcome":"success"}
   ```
   For plan-only runs, log `"mode":"plan-only","outcome":"handed-to-user"` instead — no exit code, since Kasidit didn't run it.

**Confirm gate summary:**

| Env | Auto-exec allowed | Gate |
|---|---|---|
| staging/preview | yes | plain confirm |
| prod | yes, if platform auto-executable | typed `confirm: deploy-prod` + diff shown first |
| any env, dirty tree | no | forced to plan-only, or `--allow-dirty` override |
| any env, preflight NOT READY | no | blocked entirely, fix preflight first |

**Output format (auto-executed):**

```
Mission:    deploy kasion-site → prod
Platform:   cloudflare-pages (auto-executable)
Preflight:  ready with warnings (see below)
  ⚠️  CI status unknown (no token configured)
Confirm:    deploy-prod ✓ (typed by user)
Command:    wrangler pages deploy dist --project-name=kasion-site
Result:     exit 0 — deployed https://kasion-site.pages.dev
Logged:     STATE/deploy_history.jsonl
Confidence: [high] — verified by command exit code + returned URL
```

**Output format (plan-only fallback):**

```
Mission:    deploy kas-sass → staging
Platform:   ssh/vps (plan-only — no safe auto-exec path)
Preflight:  ready
Plan (run yourself):
  1. git push origin main
  2. ssh deploy@kas-sass-staging "cd /var/www/kas-sass && git pull && php artisan migrate --force && sudo systemctl reload php-fpm"
  3. curl -sf https://staging.kas-sass.internal/healthz
Rollback:
  ssh deploy@kas-sass-staging "cd /var/www/kas-sass && git reset --hard <prev-sha> && sudo systemctl reload php-fpm"
Logged:     STATE/deploy_history.jsonl (mode=plan-only)
Confidence: [medium] — plan generated, not run; user-executed outcome not yet known
```

**Tier rules:**

- **Haiku** — plan-only path only, on any platform. Refuse the auto-execute path entirely — deploy execution is high-stakes and Haiku's correction rate isn't trusted for irreversible-adjacent shell commands. Escalate: "auto-execute needs Sonnet or Opus tier."
- **Sonnet** — full auto-execute path on staging. Prod auto-execute requires the typed confirm gate same as Opus.
- **Opus** — full auto-execute path, both envs, may also propose rollback runbook updates after a failure (proposal only, user applies).

**Anti-patterns (hard refuse):**

- ❌ Auto-execute on a plan-only platform because "the command looks simple enough" — capability table is fixed, not a judgment call per-mission.
- ❌ Skip the preflight checklist to save a step.
- ❌ Execute with a dirty working tree without explicit `--allow-dirty`.
- ❌ Auto-retry a failed deploy.
- ❌ Auto-rollback on failure — surface the rollback command, user decides and runs it.
- ❌ Accept a plain "yes" as the prod confirm gate — must be the typed `confirm: deploy-prod` phrase.
- ❌ Read `.env` values into context to build the deploy command — reference keys only; the deploy CLI reads env itself.
- ❌ Push to main / force push as part of a deploy mission.

**Safety hard rules (same as `/kasi-devopt`, still apply):**

- Production deploys always show diff vs current prod state before the confirm gate.
- Env file content: list keys, never values.
- Destructive infra ops (scale to 0, delete volume) discovered mid-mission → separate confirm, never bundled into the deploy confirm.

**Relationship to `/kasi-devopt`:**

`/kasi-devopt`'s `deploy <env>` sub-mode is superseded by this command + `/kasi-review-deploy`. It stays in place for back-compat and redirects on invocation.

**Examples:**

```
/kasi-deploy staging
/kasi-deploy prod
/kasi-deploy prod --allow-dirty
```
