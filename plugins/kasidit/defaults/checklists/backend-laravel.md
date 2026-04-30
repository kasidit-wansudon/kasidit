# Backend — Laravel Checklist

Mechanical scan list for Laravel controllers, services, routes, and Eloquent models. Used by `/kasi-backend audit` and `audit-specialist --focus=quality|security`.

Tag every finding with `[high]` / `[medium]` / `[low]` / `[unsure]` and `severity` (HIGH/MED/LOW).

## A. Routing + Controller surface

- [ ] Route file (`routes/api.php`, `routes/web.php`) — every route has a controller method or closure (no orphan).
- [ ] Route names unique and consistent (`resource.action` pattern).
- [ ] Middleware stack documented per route group (auth, throttle, locale).
- [ ] No business logic in route closures — must live in controller/service.
- [ ] `Route::resource` / `apiResource` used consistently — no manual duplicate of CRUD.
- [ ] Public-facing routes use rate limiting (`throttle:`).
- [ ] Admin routes gated by middleware, not just by frontend hiding.

## B. Validation

- [ ] FormRequest class used (not inline `$request->validate()` for non-trivial input).
- [ ] Every input field has a rule — no implicit pass-through.
- [ ] `unique:`, `exists:` rules use the correct table + connection.
- [ ] File uploads validate `mimes`, `max`, and store outside webroot.
- [ ] Authorization (`authorize()` in FormRequest) returns true intentionally — not as a stub.
- [ ] Custom rules tested.

## C. Auth + Authorization

- [ ] `auth` middleware on every protected route.
- [ ] Sanctum/Passport tokens scoped (abilities/scopes set, not blank).
- [ ] Policy classes used (`$this->authorize('update', $model)`) — not raw user-id checks.
- [ ] Gate definitions in `AuthServiceProvider` — not scattered.
- [ ] Password hashing uses `Hash::make` — never raw bcrypt or md5.
- [ ] Session config `same_site=lax` minimum, `secure=true` in prod.

## D. Eloquent + Query

- [ ] N+1: every loop over a collection that calls `$item->relation` has eager load (`with()`).
- [ ] `whereIn` not in a loop (replace with single `whereIn` outside loop).
- [ ] `chunk()` / `chunkById()` for large datasets — not `all()`.
- [ ] Mass assignment guarded — `$fillable` or `$guarded` set explicitly.
- [ ] No `DB::raw()` with concatenated user input — use bindings.
- [ ] Transactions wrap multi-statement writes (`DB::transaction(...)`).
- [ ] Soft deletes documented per model — global scope visible.
- [ ] Indexes match `where`/`orderBy`/`join` columns — check migrations.

## E. SQL injection — high priority

- [ ] No `DB::select("... $var ...")` with concatenated input.
- [ ] No `whereRaw(...)` / `havingRaw(...)` with concatenated input.
- [ ] No `orderByRaw(...)` with user input — whitelist column names instead.
- [ ] No `\DB::statement(...)` with user input.

## F. Mass assignment + IDOR

- [ ] `Model::create($request->all())` — only acceptable if `$fillable` is strict.
- [ ] `Model::find($request->input('id'))->update($request->all())` — must check ownership first.
- [ ] Route-bound `{user}` in admin route — confirm policy gates it.
- [ ] Numeric IDs in URLs — confirm authorization, do not rely on uuid for security.

## G. File handling

- [ ] No `$_FILES` direct read — use `$request->file('x')`.
- [ ] No `move_uploaded_file($_FILES['x']['tmp_name'], $userPath)` — path traversal.
- [ ] Disk used (`Storage::disk('s3')` or `local`) — no raw `fopen`.
- [ ] Filename sanitized — never trust `$file->getClientOriginalName()` for storage path.
- [ ] Download routes — content-disposition + mime-type controlled.

## H. Service / Repository layer

- [ ] Controller is thin — fat controllers flagged.
- [ ] Business logic in services, not models (model = data + relationships).
- [ ] Service classes constructor-injected, not facade-resolved (testability).
- [ ] Side effects logged (`Log::info` with structured context).

## I. Queue + Jobs

- [ ] Long-running work dispatched (`dispatch(new Job)`) — not run inline.
- [ ] Jobs idempotent — safe to retry.
- [ ] `failed_jobs` monitored.
- [ ] Queue worker config matches deployment (`supervisor` / systemd).
- [ ] Sensitive data not in serialized job payload.

## J. API response

- [ ] API Resource class used for response shape — not raw model JSON.
- [ ] Pagination consistent — `paginate()` or cursor.
- [ ] HTTP status codes correct (201 on create, 204 on delete-no-body, 422 on validation).
- [ ] Error response shape standard — `{message, errors: {...}}`.
- [ ] No leaked stack traces in prod (`APP_DEBUG=false`).

## K. Config + secrets

- [ ] No hardcoded API keys / passwords — `config()` + `.env`.
- [ ] `.env` not committed.
- [ ] `config:cache` works (no closures in config files).
- [ ] Per-env config (`config/services.php`) — not in code.

## L. Logging + observability

- [ ] Sensitive data redacted before log (PII, tokens).
- [ ] Log channel separated (errors, audits, requests).
- [ ] Structured log (key/value), not free-form `Log::info("user $id did $thing")`.

## M. Testing surface (notes only)

- [ ] Critical endpoints have feature test.
- [ ] Service classes have unit test.
- [ ] Auth + authorization scenarios tested (positive + negative).
- [ ] Migration tested via `RefreshDatabase` or `DatabaseTransactions`.

## Severity guide

| Type | Default severity |
|------|------------------|
| SQL injection (E) | HIGH |
| Mass assignment / IDOR (F) | HIGH |
| Path traversal / file (G) | HIGH |
| Auth missing (C) | HIGH |
| Validation missing (B) | MED |
| N+1 (D) | MED |
| Mass assignment risk (F) | MED |
| Logging PII (L) | MED |
| Magic numbers / structure (H, J) | LOW |
| Test gap (M) | LOW |

## Output format

```
🔴 HIGH (n)
  [high] app/Http/Controllers/SaleController.php:317 — SQL injection — whereRaw($sku) concat
  [high] app/Http/Controllers/UserController.php:88 — Auth missing — public route /admin/users

🟡 MED (n)
  [medium] app/Http/Controllers/PoController.php:113 — N+1 — loop $po->items->each($item->stock)

❓ UNSURE
  [unsure] app/Services/Refund.php:45 — possible race — concurrent refund context unclear
```
