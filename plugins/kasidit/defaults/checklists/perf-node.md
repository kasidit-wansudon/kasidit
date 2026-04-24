# Node.js Performance Checklist

Use during `/kasi-review` when latency / throughput matters. Focus: event loop, I/O, memory.

## Event loop
- [ ] `fs.readFileSync` / `fs.writeFileSync` in request handler — use async variants
- [ ] `JSON.parse` on large payload on hot path — stream-parse (`stream-json`) or cap size
- [ ] Heavy crypto (`pbkdf2`, `bcrypt`, big hashes) sync in handler — use async version / worker thread
- [ ] `console.log` / sync logger in request path — switch to async logger (`pino`) with transport

## Async shape
- [ ] Sequential `await` where calls are independent — parallelise with `Promise.all`
- [ ] Unnecessary `await` on non-promise value — drop it
- [ ] Loop of `await repo.findOne(id)` (N+1) — batch with `findByIds` / DataLoader

## Data / DB
- [ ] DB driver connection pool configured (size > 1, < provider limit)?
- [ ] ORM lazy-loading relations inside a map — use `include` / `join` once
- [ ] Response missing `Content-Encoding: gzip` — add `compression` middleware
- [ ] Repeated pure computation uncached — add in-memory / Redis cache with TTL

## Imports / bundle
- [ ] `import _ from 'lodash'` in hot path — use `lodash/get` or `lodash-es` tree-shakable
- [ ] `moment` in hot path — swap for `dayjs` / `date-fns`

## Memory / leaks
- [ ] Unbounded array / map growing per request (cache without eviction) — add LRU
- [ ] `EventEmitter` listener added per request without `removeListener` — `MaxListenersExceededWarning`
- [ ] Closure retains large object (req/res) past handler return — null the ref

## Streams / regex
- [ ] Stream piped without backpressure respect (`pipe` ok, manual `data` events need `pause`)?
- [ ] Regex with nested quantifiers (`(a+)+`) on user input — simplify or bound input length
