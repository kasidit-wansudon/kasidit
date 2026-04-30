---
description: Backend mission — multi-mode (fix/audit/scaffold/design/perf) for API/controller/service/route/DB work
---

Run a backend-focused Kasidit mission. Counterpart to `/kasi-ui` for the server side.

**Sub-modes (first arg):**

| Sub | What it does | Specialist |
|-----|--------------|------------|
| `fix <issue>` | conservative bug fix in controller/service/route | `bug-hunter` |
| `audit <scope>` | checklist-driven review of backend files | `audit-specialist --focus=quality` |
| `scaffold <module>` | design → confirm → code a new endpoint/module | `architect-planner` then writer |
| `design <feature>` | architecture + relation diagram only, no code | `architect-planner` |
| `perf <endpoint>` | find slowness, N+1, missing index | `audit-specialist --focus=perf` |
| `security <scope>` | OWASP checklist on backend files | `audit-specialist --focus=security` |

If no sub-mode given → ask user to pick one of the six.

**Stack auto-detect (in order):**

1. `composer.json` + `"laravel/framework"` → Laravel mode → load `CHECKLISTS/backend-laravel.md`
2. `package.json` + (`express`/`fastify`/`hono`/`@nestjs/core`/`koa`) → Node mode → load `CHECKLISTS/backend-node.md`
3. Both → ask user which surface
4. Neither → agnostic mode, load `CHECKLISTS/backend-api-design.md` only

**Pre-mission step (mandatory for `audit` and `perf`):**

Before specialist runs, build / refresh function call graph:

```
/kasi-graph build
```

Then ask user:
> "Audit ทั้งหมด, หรือเลือก subgraph จาก HOTSPOTS.md?"

If user picks subgraph → specialist receives `subgraph-<id>.md` as scope, not full repo.

**Flow:**

1. Confirm sub-mode + scope (1 line). If vague → refuse, list 6 sub-modes.
2. Detect stack. Print: `[stack=laravel|node|both|agnostic] [files=<n>]`.
3. (audit/perf only) Run `/kasi-graph build` → show top 10 hotspots → user picks.
4. Load matching checklist(s) from `CHECKLISTS/`.
5. Dispatch specialist with brief: `MISSION / INPUTS / CONSTRAINTS / EXPECTED OUTPUT`.
6. Synthesize specialist output → produce report with confidence labels.
7. Ask user: apply fix? open follow-up mission? commit?

**Tier rules:**

- **Haiku** — only `fix` and `audit`. Refuse `scaffold`/`design` (architecture decisions). `perf`/`security` allowed only if subgraph ≤ 5 fns.
- **Sonnet** — all sub-modes. Verifier pass mandatory on `audit` + `security`.
- **Opus** — all sub-modes, may reason cross-file.

**Output format (audit/security/perf):**

```
Stack:     <laravel|node|agnostic>
Scope:     <files / subgraph-id>
Findings:
  🔴 HIGH (n)
    [high] file.php:LINE — <type> — <one-line>
  🟡 MED (n)
    [medium] file.php:LINE — <type> — <one-line>
  ❓ UNSURE (n)
    [unsure] file.php:LINE — <reason need user review>

Top-5 actionable:
  1. <fix-hint> — file:line
  ...

Counter: <round>/<max>
Next:    <propose>
```

**Output format (fix):**

```
Mission:       <one-line>
Stack:         <laravel|node>
Hypothesis:    <root cause + file:line>
Fix:           <diff>
Blast radius:  <n files / m lines>
Confidence:    [high|medium|low|unsure]
Verify:        <curl / test / log>
```

**Output format (scaffold/design):**

```
Mission:       <one-line>
Endpoint:      <method + path>
Request:       <shape>
Response:      <shape>
Flow:          Request → Controller → Service → Repository → DB
Files to add:  <list>
Files to edit: <list>
Open Qs:       <list>  ← user answers before code
```

**Anti-patterns (refuse):**

- ❌ Run `audit` without subgraph or explicit scope (`all backend` is too vague).
- ❌ Run `scaffold` without confirming endpoint shape with user.
- ❌ Touch DB schema directly — escalate to `migration-specialist`.
- ❌ Add validation/middleware "while I'm here" during `fix`.
- ❌ Trust ORM/router doc memory — fetch version-matched docs via `/kasi-docs`.

**Examples:**

```
/kasi-backend fix "store endpoint return 500 on duplicate sku"
/kasi-backend audit app/Http/Controllers/SaleController.php
/kasi-backend audit subgraph-saleflow
/kasi-backend perf api/sales/index
/kasi-backend scaffold "POST /api/transfers — warehouse-to-warehouse stock move"
/kasi-backend design "background job for daily inventory snapshot"
/kasi-backend security routes/api.php
```
