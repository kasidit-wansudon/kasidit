# Backend — API Design Checklist

Stack-agnostic rules for designing or reviewing a REST/RPC API surface. Loaded by `/kasi-backend design|scaffold` and as fallback when stack auto-detect returns "agnostic".

## A. Resource modeling

- [ ] Nouns, not verbs — `/sales` not `/getSales`.
- [ ] Plural collection — `/sales`, item via id `/sales/:id`.
- [ ] Nested resources max 2 levels — `/warehouses/:id/stocks` OK, deeper → flatten with query param.
- [ ] Sub-actions on item only when not CRUD — `/sales/:id/refund`.
- [ ] No mixed singular/plural.

## B. HTTP method semantics

- [ ] `GET` — read only, idempotent, safe.
- [ ] `POST` — create or non-idempotent action.
- [ ] `PUT` — replace whole resource, idempotent.
- [ ] `PATCH` — partial update.
- [ ] `DELETE` — remove, idempotent.
- [ ] No state change on `GET`.

## C. Status codes

- [ ] `200 OK` — success with body.
- [ ] `201 Created` — POST returning new resource (include `Location` header or body with id).
- [ ] `204 No Content` — DELETE / PUT with no body.
- [ ] `400 Bad Request` — malformed payload (parse fail).
- [ ] `401 Unauthorized` — no/invalid auth.
- [ ] `403 Forbidden` — auth ok, not allowed.
- [ ] `404 Not Found` — resource missing or hidden by auth (latter to avoid leak).
- [ ] `409 Conflict` — uniqueness / version mismatch.
- [ ] `422 Unprocessable Entity` — validation fail with field map.
- [ ] `429 Too Many Requests` — rate limit.
- [ ] `5xx` — server side, never leak stack.

## D. Request shape

- [ ] JSON request body for POST/PUT/PATCH (or multipart for file upload).
- [ ] Query string for filter/sort/pagination, not body for GET.
- [ ] Pagination scheme picked — offset (`page`/`per_page`) or cursor (`cursor`/`limit`).
- [ ] Sort param whitelisted — `?sort=created_at,-name` parsed into allowed fields.
- [ ] Filter param flat or namespaced — `?status=open&customer_id=42`.
- [ ] No deep query nesting parsed via `qs` lib unless explicit.

## E. Response shape

- [ ] Consistent envelope across endpoints (e.g. `{data, meta, links}` or flat resource — pick one).
- [ ] Error envelope consistent — `{message, errors: {field: [msg]}, code}`.
- [ ] Field naming consistent (snake_case OR camelCase project-wide).
- [ ] Timestamps ISO-8601 UTC always.
- [ ] Money as integer minor unit + currency code, not float.
- [ ] Booleans not strings.

## F. Versioning

- [ ] Strategy chosen — URL prefix (`/v1/sales`) or header (`Accept: application/vnd.x.v1+json`).
- [ ] Breaking change → new version, never silent.
- [ ] Deprecation window documented (date + replacement endpoint).
- [ ] Old version response includes `Sunset` / `Deprecation` header.

## G. Auth

- [ ] Bearer token in `Authorization` header, not query param.
- [ ] Token type stated (JWT / opaque).
- [ ] Refresh flow documented.
- [ ] Per-endpoint scope/role required listed.
- [ ] Idempotency-Key header supported on POST that creates/charges (`Idempotency-Key`).

## H. Rate limiting + quotas

- [ ] Public endpoints rate-limited.
- [ ] Limits returned via headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`).
- [ ] Per-user vs per-IP scope chosen.

## I. Caching

- [ ] `Cache-Control` set on GET — `no-store` for sensitive, `private, max-age=N` for personal.
- [ ] `ETag` + `If-None-Match` for revalidation if collection is large.
- [ ] No caching on auth/billing endpoints.

## J. Idempotency + concurrency

- [ ] Side-effecting POST supports `Idempotency-Key`.
- [ ] PUT/PATCH supports optimistic concurrency via `If-Match: "<etag>"` or version field in body.
- [ ] Server returns `409 Conflict` on version mismatch.

## K. Documentation

- [ ] OpenAPI / spec file exists or planned.
- [ ] Each endpoint: method, path, auth, request, response, error, status codes, example.
- [ ] Spec generated from code (decorators / annotations) — not hand-drift.

## L. Edge cases (per endpoint)

- [ ] Empty list response shape — `{data: []}`, not `null`.
- [ ] Big payload — pagination forced if collection > threshold.
- [ ] Concurrent create — uniqueness handled (DB constraint + 409).
- [ ] Cascading delete documented.
- [ ] Soft delete vs hard delete chosen explicitly.

## M. Security cross-cutting

- [ ] HTTPS only (HSTS).
- [ ] CORS allowlist — no wildcard with credentials.
- [ ] CSRF: cookie-auth APIs need CSRF token; bearer-token APIs do not.
- [ ] Output not reflected with HTML — JSON content-type fixed.
- [ ] Input length bounded.

## Output format (design mode)

```
Endpoint:    POST /api/transfers
Auth:        Bearer (scope: warehouse.write)
Request:     { from_warehouse_id, to_warehouse_id, items: [{ sku, qty }], idempotency_key }
Response:    201 { data: { transfer_id, status, items: [...] } }
Errors:      400 (parse), 401, 403, 422 (validation), 409 (insufficient stock), 429
Concurrency: idempotency_key required; server uses unique constraint on (key, requester_id)
Flow:        Request → TransferController::store → TransferService::execute → DB tx (Stock::deduct + Stock::add) → Response
Open Qs:
  - background notification on transfer create? (queue or sync?)
  - partial transfer allowed if stock insufficient on some lines?
```
