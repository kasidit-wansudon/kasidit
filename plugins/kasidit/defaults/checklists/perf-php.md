# PHP Performance Checklist

Use during `/kasi-review perf` on suspected hot paths. Measure before you change.

## Database
- [ ] N+1: loop that calls a model query per iteration — eager load / join?
- [ ] `SELECT *` where only 2-3 columns used — narrow the projection?
- [ ] Missing index on filter / join column — check `EXPLAIN`?
- [ ] Pagination uses `LIMIT/OFFSET` on very deep pages — switch to keyset?
- [ ] Write inside a loop without batch / transaction?

## Caching
- [ ] Expensive pure computation repeated per request — memoize (request-scope)?
- [ ] External API call on hot path without cache or circuit breaker?
- [ ] Cache key stable across deploys — not tied to auto-increment ids that churn?

## PHP runtime
- [ ] OPcache enabled in production config?
- [ ] Large array built then only one item used — build lazily / generator?
- [ ] JSON encode/decode of same blob multiple times per request?
- [ ] Regex in tight loop — precompile / simpler string op possible?

## HTTP / IO
- [ ] Response not gzipped / no ETag on cacheable content?
- [ ] Asset not served via CDN / static handler?
- [ ] Synchronous outbound request on user-facing path — move to queue?
