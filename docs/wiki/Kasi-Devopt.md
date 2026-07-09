# /kasi-devopt

> DevOps mission — infra, CI/CD, env vars, data-flow connections, runbooks. Counterpart to [[Kasi-Backend]] for the deploy + infra + ops surface.

## Usage

```
/kasi-devopt env diff
/kasi-devopt data <action>
/kasi-devopt infra <kind>
/kasi-devopt secrets audit
/kasi-devopt runbook <topic>
/kasi-devopt health <env>
/kasi-devopt connect <a> <b>
```

> **`deploy <env>` is superseded** ([[v0.16.0]]) by [[Kasi-Deploy]] (execute-capable) and [[Kasi-Review-Deploy]] (permanently read-only). Invoking `/kasi-devopt deploy <env>` now redirects to those two commands instead of running the old flow.

## What it does

- Reads from `.kasidit/STATE/` (the bridge, see [[Kasi-Struc]]) instead of rescanning every time.
- `env diff` — diffs env vars across `.env.example` / `.env.staging` / prod, reporting missing/different/orphaned keys. Never reads values into context — keys only.
- `data <action>` — builds and maintains a service data-flow map (`STATE/data_flow.json`): services, edges (with auth method), and the secrets each edge depends on.
- `infra <kind>` — reviews infra-as-code (Terraform / wrangler / docker / k8s).
- `secrets audit` — finds hardcoded secrets, proposes a rotation plan.
- `runbook <topic>` — generates or updates a runbook in `.kasidit/knowledge/runbooks/` (see [[Kasi-Acknowledge]]).
- `health <env>` — checks `/healthz`, queue depth, error rate, deploy state.
- `connect <a> <b>` — documents/verifies a connection between two services.

## Sub-mode → specialist map

| Sub | Specialist |
|---|---|
| `pipeline` | `migration-specialist` |
| `env diff` | `audit-specialist --focus=quality` |
| `infra` | `audit-specialist --focus=security` |
| `data` | `migration-specialist` |
| `runbook` | `architect-planner` |
| `health` | `bug-hunter` |
| `secrets audit` | `audit-specialist --focus=security` |
| `connect` | `architect-planner` |

## Data connection map

`data map` regenerates `.kasidit/STATE/data_flow.json` — services, edges (`from`/`to`/`via`/`auth`), and a flat `secrets` list. Answers "what connects to what, with what credential, on what protocol?"

## When to use

- Env var drift between staging and prod.
- Mapping how services connect before a migration or an incident postmortem.
- Secrets audit before a security review.
- Deploy readiness or execution — but use [[Kasi-Review-Deploy]] or [[Kasi-Deploy]] directly, not this command's old sub-mode.

## When NOT to use

- Deploying — use [[Kasi-Deploy]] (executes) or [[Kasi-Review-Deploy]] (read-only preflight).
- Backend code fixes — use [[Kasi-Backend]].

## Tier behavior

- **Haiku** — `env diff`, `secrets audit` (mechanical scan), `health`, `runbook` (template only). Refuses `infra` design or `pipeline` redesign.
- **Sonnet** — all sub-modes, verifier pass on `infra` and `pipeline`.
- **Opus** — all sub-modes, may suggest cross-service architecture changes.

## Anti-patterns

- ❌ Auto-rotate secrets — propose a plan, user executes.
- ❌ Modify production config without explicit per-file user confirmation.
- ❌ Push to main / force push during a devopt mission.
- ❌ Read `.env` values into model context — list keys only.
- ❌ Use this command's old `deploy` flow for a new mission — use [[Kasi-Deploy]] / [[Kasi-Review-Deploy]] instead.

## Since

Introduced in [[v0.11.0]]. `deploy` sub-mode superseded in [[v0.16.0]].

## See also

- [[Commands]] (aggregate)
- [[Kasi-Deploy]] · [[Kasi-Review-Deploy]] — supersede the old `deploy` sub-mode
- [[Kasi-Struc]] — structural state this command reads
- [[Kasi-Acknowledge]] — runbook capture used by `runbook`
