---
description: DevOps mission — deploy flow, infra, CI/CD, env vars, data structure connections, runbooks
---

Run a DevOps-focused Kasidit mission. Counterpart to `/kasi-backend` for the deploy + infra + ops surface. Reads from `.kasidit/STATE/` (the bridge) instead of rescanning every time.

**Sub-modes (first arg):**

| Sub | What it does | Specialist |
|-----|--------------|------------|
| `deploy <env>` | walk through deploy flow for env, dry-run preflight | `architect-planner` |
| `pipeline <name>` | inspect/edit CI pipeline (GH Actions / GitLab CI / etc) | `migration-specialist` |
| `env diff` | diff env vars across `.env.example` / `.env.staging` / prod | `audit-specialist --focus=quality` |
| `infra <kind>` | review infra-as-code (Terraform / wrangler / docker / k8s) | `audit-specialist` |
| `data <action>` | data flow — connections, ETL, backup, retention | `migration-specialist` |
| `runbook <topic>` | generate or update runbook in `.kasidit/runbooks/` | `architect-planner` |
| `health <env>` | check `/healthz`, queue depth, error rate, deploy state | `bug-hunter` |
| `secrets audit` | find hardcoded secrets, rotate plan | `audit-specialist --focus=security` |
| `connect <a> <b>` | document/verify connection between two services | `architect-planner` |

If no sub-mode → ask user to pick one.

**Detected platforms (auto from STATE/config.json + repo files):**

| File / pattern | Platform |
|---|---|
| `.github/workflows/*.yml` | GitHub Actions |
| `.gitlab-ci.yml` | GitLab CI |
| `wrangler.toml` / `wrangler.jsonc` | Cloudflare Workers/Pages |
| `vercel.json` | Vercel |
| `netlify.toml` | Netlify |
| `Dockerfile` / `docker-compose.yml` | Docker |
| `*.tf` | Terraform |
| `k8s/` / `helm/` | Kubernetes |
| `Procfile` | Heroku-style |
| `fly.toml` | Fly.io |
| `serverless.yml` | Serverless Framework |
| `.platform.app.yaml` | Platform.sh |

**Data connection map:**

`data` sub-mode builds and reads `.kasidit/STATE/data_flow.json`:

```json
{
  "services": [
    {"id":"kasion-site","kind":"frontend","platform":"cloudflare-pages"},
    {"id":"kas-sass","kind":"backend","platform":"vps","db":["mysql8"]},
    {"id":"ai-router","kind":"node-worker","platform":"cloudflare-workers"}
  ],
  "edges": [
    {"from":"kasion-site","to":"kas-sass","via":"https","auth":"sanctum-token"},
    {"from":"kasion-site","to":"ai-router","via":"https","auth":"jwt"},
    {"from":"kas-sass","to":"mysql8","via":"tcp:3306","auth":"db_user"}
  ],
  "secrets": ["KAS_API_KEY","AI_ROUTER_TOKEN","DB_PASSWORD"]
}
```

Used to answer: "what connects to what, with what credential, on what protocol?"

**Pre-mission step (mandatory for `deploy` and `health`):**

Run state bridge check first:

```
/kasi-struc refresh
```

If recent deploy_history exists in STATE — read it before proposing new deploy.

**Flow (deploy <env>):**

1. Confirm env (staging/prod) + service.
2. Read `STATE/config.json` + `STATE/deploy_history.jsonl`.
3. Preflight checklist:
   - Env vars match template? (`/kasi-devopt env diff`)
   - Migrations pending? (check `database/migrations` + last migrated)
   - Tests passing on target branch? (read CI status if available)
   - No `console.log`/`dd()`/debug left in diff?
   - Rollback plan documented?
4. Show deploy plan to user — commands to run, in order.
5. User confirms → user runs commands themselves (Kasidit does NOT execute deploy).
6. User reports outcome → write entry to `STATE/deploy_history.jsonl`.

**Flow (env diff):**

1. Read all `.env*` files + `.env.example`.
2. Build matrix: var × env.
3. Report:
   - Missing in env A but in B.
   - Different value for key (without leaking value).
   - In template but not in any env.
   - In env but not in template.

**Flow (data action):**

| Action | What |
|---|---|
| `map` | regenerate `data_flow.json` from repo + user input |
| `connect <a> <b>` | document a new connection between two services |
| `verify` | sanity check — every secret in `data_flow.json` exists in env |
| `backup` | review backup config (frequency, retention, restore tested?) |
| `retention` | review data retention rules vs compliance |
| `etl <name>` | review/scaffold an ETL job |

**Tier rules:**

- **Haiku** — `env diff`, `secrets audit` (mechanical scan), `health`, `runbook` (template only). Refuse `infra` design or `pipeline` redesign.
- **Sonnet** — all sub-modes. Verifier pass on `infra` and `pipeline`.
- **Opus** — all sub-modes, may suggest cross-service architecture changes.

**Output format (deploy):**

```
Mission:    deploy kas-sass to staging
Platform:   <ssh / docker / k8s / cf-workers>
Branch:     <git ref>
Preflight:
  ✅ env vars match template
  ✅ no pending migrations
  ⚠️  CI status unknown (no token)
  ✅ no debug code in diff
  ❓ rollback plan — needs runbook
Plan (run yourself):
  1. <command>
  2. <command>
  3. <verify command>
Rollback:
  <commands>
Confidence: [medium] — preflight item missing
```

**Output format (env diff):**

```
Env diff:
  staging vs prod:
    only in staging: KAS_DEBUG, FAKE_SMTP_HOST
    only in prod:    SENTRY_DSN, RELEASE_TAG
    different:       LOG_LEVEL (staging=debug, prod=info)
    in template, missing both:  NEW_FEATURE_FLAG
```

**Anti-patterns (refuse):**

- ❌ Run `deploy` command yourself — output the plan, user runs it.
- ❌ Auto-rotate secrets — propose plan, user executes.
- ❌ Modify production config without explicit user confirmation per file.
- ❌ Push to main / force push during deploy mission.
- ❌ Trust env values — never read `.env` directly into model context, list keys only.
- ❌ Skip rollback plan on deploy.

**Safety hard rules:**

- Destructive ops (drop table, force push, delete volume, scale to 0) → require explicit `confirm: yes-i-understand` from user.
- Production deploys: always show diff vs current prod state first.
- Env file content: list keys, never values.

**Examples:**

```
/kasi-devopt deploy staging
/kasi-devopt env diff
/kasi-devopt data map
/kasi-devopt data connect kasion-site ai-router
/kasi-devopt secrets audit
/kasi-devopt pipeline ci.yml
/kasi-devopt runbook "rollback kas-sass"
/kasi-devopt health prod
```
