# PHP Code Review Checklist

Use during `/kasi-review` on PHP modules. Focus: readability, correctness, PSR alignment.

## Structure
- [ ] File follows PSR-4 autoload path matches namespace?
- [ ] Class single responsibility — one reason to change?
- [ ] Function length < 40 lines? No deep nesting (> 3 levels)?
- [ ] Magic numbers replaced with named constants?

## Correctness
- [ ] Nullable returns handled at every call site (`?->`, `??`, explicit null check)?
- [ ] Strict comparisons (`===` / `!==`) unless loose intentional?
- [ ] Array access on possibly missing key guarded (`isset` / `array_key_exists`)?
- [ ] Loop index mutation does not skip / double-count?

## API / Data
- [ ] Request validation before use (FormRequest / manual validator)?
- [ ] DTO / typed object instead of raw array for cross-layer data?
- [ ] Repository / query object isolates SQL — no raw queries in controllers?

## Errors / Logging
- [ ] Exceptions typed (not bare `\Exception`) where caller needs to distinguish?
- [ ] `try/catch` does not swallow the error silently?
- [ ] Log context includes request id / user id — no PII in plain logs?

## Tests
- [ ] New branch covered by at least one test?
- [ ] Test name describes behaviour, not implementation?
- [ ] No `sleep()` / real clock in unit tests?

## Dependencies
- [ ] No new composer package for a 5-line utility?
- [ ] Package actively maintained (last release < 2 years)?
