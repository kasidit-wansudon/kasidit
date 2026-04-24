# Go Performance Checklist

For each hot path / service, check:

## Allocations
- [ ] String concat in loop with `+` (use `strings.Builder`)?
- [ ] Heavy per-request allocs without `sync.Pool` buffer reuse?
- [ ] `fmt.Sprintf` in hot path for simple int/string (use `strconv`)?
- [ ] Map created without size hint (`make(map[K]V, n)`) when size known?
- [ ] Slice `append` without preallocated cap (`make([]T, 0, n)`)?
- [ ] Large struct passed by value through hot path (pass pointer)?

## Serialization
- [ ] `json.Marshal` / `Unmarshal` in hot path (consider `easyjson` / codegen)?
- [ ] Reflection (`reflect.*`) used per call where codegen would win?

## Concurrency
- [ ] Channel unbuffered where buffered would remove sender block?
- [ ] Goroutine fan-out unbounded (use worker pool / semaphore)?

## I/O
- [ ] DB N+1: per-row query inside a `range` loop (batch / JOIN)?
- [ ] `regexp.MustCompile` called per request (precompile as package var)?
- [ ] `http.Client` created per call (reuse one client for conn pooling)?
- [ ] `io.ReadAll` on response body without `io.LimitReader` bound?

## Observability
- [ ] `net/http/pprof` / `runtime/pprof` hook missing in service?
