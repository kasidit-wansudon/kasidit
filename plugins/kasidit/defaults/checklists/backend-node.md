# Backend — Node Checklist

Mechanical scan list for Node backends (Express / Fastify / Hono / NestJS / Koa). Used by `/kasi-backend audit` and `audit-specialist`.

Tag every finding `[high|medium|low|unsure]` + severity HIGH/MED/LOW.

## A. Framework + Routing

- [ ] Single router entry — no router defined in random files.
- [ ] Route handler is `async` if any await inside — no unhandled promise.
- [ ] No business logic in route handler — service layer required.
- [ ] CORS config explicit (`origin`, `credentials`) — no `*` with credentials.
- [ ] Rate limit middleware on public routes (`express-rate-limit` / `@fastify/rate-limit`).
- [ ] Body parser limit set (`json({ limit: '1mb' })`) — no unbounded.

## B. Validation

- [ ] Every input validated with schema lib (`zod`/`joi`/`yup`/`@hapi/joi`/`class-validator`).
- [ ] Schemas live with route or in `schemas/` — not inline mixed with logic.
- [ ] `parse` (throws) vs `safeParse` (returns) chosen intentionally.
- [ ] Query params validated (numbers parsed, booleans coerced).
- [ ] File uploads validated (mime, size, count).

## C. Auth + Authorization

- [ ] JWT verify uses public key / shared secret loaded from env, not hardcoded.
- [ ] Token expiry checked — `<` vs `<=` correct (off-by-one).
- [ ] Refresh-token endpoint rate-limited.
- [ ] Authorization done per-resource (RBAC/ABAC), not just "is logged in".
- [ ] `passport` strategy or middleware applied to every protected route.
- [ ] Cookie auth: `httpOnly`, `secure`, `sameSite` set.

## D. Database — ORM/Query

- [ ] N+1: every `findAll` followed by per-row query — flagged.
- [ ] `include`/`with` used for relations (Sequelize / Prisma / TypeORM).
- [ ] No template-string SQL (`db.query(\`SELECT * FROM users WHERE id=${id}\`)`).
- [ ] Parameterized queries always (`db.query('SELECT * FROM users WHERE id=$1', [id])`).
- [ ] Transactions wrap multi-statement writes.
- [ ] Connection pool size set appropriate to deployment.
- [ ] Indexes match query patterns (verify via migration).

## E. SQL/NoSQL injection — HIGH

- [ ] No string concatenation into raw SQL.
- [ ] Mongo: no `$where` with user input. No `find(req.body)` blindly (allow operator injection).
- [ ] Whitelist sortable columns (no `ORDER BY ${userInput}`).
- [ ] Whitelist filterable fields.

## F. NoSQL operator injection / mass assignment

- [ ] `find({ ...req.body })` — sanitize / pick allowed keys first.
- [ ] `update({ ...req.body })` — same.
- [ ] Mongoose `strict: true` (default in 6+).

## G. File handling

- [ ] `multer` / `fastify-multipart` config — destination, limits, fileFilter.
- [ ] Filename sanitized — no path traversal (no `../`).
- [ ] Storage outside repo / web root.
- [ ] Mime type checked server-side, not just `Content-Type` header.

## H. Service layer

- [ ] Service has clear input/output type — not `any`.
- [ ] Errors thrown with class hierarchy (`AppError extends Error`) — no string throw.
- [ ] DI used for testability (constructor injection or container).
- [ ] No `console.log` in service — use logger (winston/pino).

## I. Async + concurrency

- [ ] Every `await` inside try-catch or `.catch()` chain.
- [ ] No `Promise.all` followed by partial await — race conditions.
- [ ] Long-running tasks moved to queue (BullMQ / RabbitMQ) — not blocking event loop.
- [ ] No `for-await-of` over huge stream without backpressure.

## J. HTTP client + outgoing

- [ ] Outgoing requests timeout-bounded (`axios timeout`, `fetch AbortController`).
- [ ] Retries explicit with backoff — not silent infinite retry.
- [ ] No SSRF: validate URL host/scheme before fetch (block internal IPs unless intended).
- [ ] Outgoing secrets in headers, not URL params.

## K. Logging + observability

- [ ] Structured logger (`pino`/`winston`) — JSON output.
- [ ] Sensitive fields redacted in log middleware.
- [ ] Request ID propagated (`X-Request-ID`).
- [ ] Errors logged with stack — not just message.

## L. Config + secrets

- [ ] `.env` loaded via `dotenv` or platform env, not committed.
- [ ] `process.env` reads validated (zod schema for env).
- [ ] No secrets in `package.json` / Docker image layers.

## M. Error handling

- [ ] Global error middleware — all uncaught errors land here.
- [ ] HTTP status codes correct (4xx vs 5xx).
- [ ] Error response sanitized in prod — no stack traces leaked.
- [ ] Validation errors return 400/422 with field map.

## N. Dependencies

- [ ] No deprecated packages (`npm outdated`).
- [ ] No CVE in `npm audit` (HIGH/CRITICAL).
- [ ] `package-lock.json` committed.
- [ ] No `node_modules` committed.

## Severity guide

| Type | Default severity |
|------|------------------|
| SQL/NoSQL injection (E, F) | HIGH |
| Auth missing / token bug (C) | HIGH |
| Path traversal (G) | HIGH |
| SSRF (J) | HIGH |
| Async unhandled (I) | MED |
| N+1 (D) | MED |
| Validation missing (B) | MED |
| Logging PII (K) | MED |
| Config/structure | LOW |

## Output format

Same shape as Laravel checklist — group by severity, tag confidence, list Top-5 actionable.
