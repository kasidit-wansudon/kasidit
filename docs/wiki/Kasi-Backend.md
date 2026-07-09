# /kasi-backend

> Multi-mode backend mission router — counterpart to `/kasi-ui` for the server side. Auto-detects Laravel / Node stack.

## Usage

```
/kasi-backend fix <issue>
/kasi-backend audit <scope>
/kasi-backend scaffold <module>
/kasi-backend design <feature>
/kasi-backend perf <endpoint>
/kasi-backend security <scope>
```

## What it does

- Routes to one of six sub-modes: `fix` / `audit` / `scaffold` / `design` / `perf` / `security`.
- Auto-detects stack: `composer.json` + `laravel/framework` → Laravel; `package.json` + Express/Fastify/Hono/NestJS/Koa → Node; both → asks user; neither → stack-agnostic API checklist.
- For `audit`/`perf`: builds or refreshes the function call graph first ([[Kasi-Graph]]) and offers to scope the specialist to a subgraph instead of the whole repo.
- Dispatches the matching specialist with a full dispatch brief and synthesizes the result with confidence labels.

## Flow

1. Confirm sub-mode + scope in one line — refuse vague scope, list the six sub-modes.
2. Detect stack, print `[stack=laravel|node|both|agnostic] [files=<n>]`.
3. (`audit`/`perf` only) Run `/kasi-graph build`, show top-10 hotspots, let user pick a subgraph.
4. Load the matching checklist(s): `backend-laravel.md`, `backend-node.md`, or `backend-api-design.md`.
5. Dispatch specialist with a full brief (`MISSION / INPUTS / CONSTRAINTS / EXPECTED OUTPUT`).
6. Synthesize output into a confidence-labeled report.
7. Ask: apply fix? open follow-up mission? commit?

## Sub-mode → specialist map

| Sub | Specialist |
|---|---|
| `fix` | `bug-hunter` |
| `audit` | `audit-specialist --focus=quality` |
| `scaffold` | `architect-planner` then writer |
| `design` | `architect-planner` (no code) |
| `perf` | `audit-specialist --focus=perf` |
| `security` | `audit-specialist --focus=security` |

## When to use

- Any backend controller/service/route/DB work where you know which of the six sub-modes fits.
- `perf`/`audit` on a large backend — the call-graph subgraph scoping avoids reviewing the whole repo.

## When NOT to use

- Frontend/UI work — use [[Kasi-Ui]].
- DB schema changes directly — this escalates to `migration-specialist`, it doesn't touch schema itself.
- Deploy — use [[Kasi-Deploy]] / [[Kasi-Review-Deploy]], not this command.

## Tier behavior

- **Haiku** — only `fix` and `audit`. Refuses `scaffold`/`design` (architecture decisions). `perf`/`security` allowed only if the subgraph is ≤5 functions.
- **Sonnet** — all sub-modes, mandatory verifier pass on `audit` + `security`.
- **Opus** — all sub-modes, may reason cross-file.

## Anti-patterns

- ❌ Run `audit` without a subgraph or explicit scope — "all backend" is too vague.
- ❌ Run `scaffold` without confirming endpoint shape with the user first.
- ❌ Touch DB schema directly — escalate to `migration-specialist`.
- ❌ Add validation/middleware "while I'm here" during `fix`.
- ❌ Trust ORM/router doc memory — fetch version-matched docs via [[Kasi-Docs]].

## Since

Introduced in [[v0.11.0]].

## See also

- [[Commands]] (aggregate)
- [[Kasi-Graph]] — call-graph scoping used by `audit`/`perf`
- [[Kasi-Struc]] — structural state this command reads from
- [[Kasi-Ui]] — the frontend counterpart
- [[Checklists]]
