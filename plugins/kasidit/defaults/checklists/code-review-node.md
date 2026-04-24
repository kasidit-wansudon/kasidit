# Node.js Code Review Checklist

Use during `/kasi-review` on Node / TypeScript modules. Focus: correctness, readability, async hygiene.

## Async / Promises
- [ ] `await` inside `forEach` / `.map` without `Promise.all` — switch to `for..of` or `Promise.all(map)`
- [ ] Promise created but not returned / not awaited — unhandled rejection risk, add `return` or `await`
- [ ] Mixed callback + promise on the same function — pick one style
- [ ] Error-first callback: `err` branch actually handled, not just logged and continued?

## Correctness
- [ ] Null / undefined guard before `.prop` access (`?.`, `??`, explicit check)?
- [ ] Loose equality `==` / `!=` used where `===` would be safer — replace unless intentional
- [ ] `let` used where value never reassigned — switch to `const`
- [ ] Magic numbers / strings replaced with named constants?

## Structure
- [ ] Function length < 40 lines, nesting ≤ 3 levels?
- [ ] Module import triggers side effects (network, fs, mutable singleton at import) — move into init function
- [ ] Stateful singleton module — is the shared state intentional and documented?
- [ ] Cyclic dependency between modules (`require`/`import` loop) — break with interface or DI
- [ ] Dead code / commented-out blocks — delete, rely on git history

## Tests
- [ ] New branch covered by at least one test?
- [ ] Mock boundary at the right layer (HTTP / DB adapter) — not deep internals?
- [ ] Test name describes behaviour, not implementation?
