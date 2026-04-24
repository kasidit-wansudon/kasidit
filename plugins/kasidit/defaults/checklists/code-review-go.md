# Go Code Review Checklist

For each package / PR, check:

## Error handling
- [ ] Unchecked error return (`_ = json.Unmarshal(...)`, ignored `err`)?
- [ ] `panic` used inside library code (should return `error`)?
- [ ] Test coverage on error paths, not just happy path?

## Concurrency
- [ ] Goroutine leak: missing `ctx.Done()` / `sync.WaitGroup` / channel close?
- [ ] `defer` inside a loop (stacks until function return)?
- [ ] `sync.Mutex` / `sync.WaitGroup` copied by value (must be pointer)?
- [ ] Context cancellation ignored in long-running calls?
- [ ] `sync.Map` used where plain `map` + `RWMutex` would be clearer/faster?

## API design
- [ ] Accept interfaces, return structs — violated?
- [ ] Exported type / func missing doc comment?
- [ ] Over-broad `interface{}` / `any` where concrete type fits?
- [ ] `new(T)` used where `&T{...}` literal is clearer?

## Project hygiene
- [ ] `go vet` / `staticcheck` / `golangci-lint` wired into CI?
- [ ] Circular import between packages?
- [ ] `time.Now()` used without `.UTC()` for stored / serialized timestamps?
