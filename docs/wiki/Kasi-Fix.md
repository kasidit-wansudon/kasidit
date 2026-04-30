# /kasi-fix

> Bug-fix mission with conservative discipline — mandatory `git log --grep` / `-S` recon, literal fix, runtime verification.

## Usage

```
/kasi-fix <bug-description>
/kasi-fix <issue-id>
/kasi-fix <file:line> <expected-vs-actual>
```

## What it does

- Forces a narrowed mission statement: exact bug, expected vs actual.
- Runs mandatory `git log --grep=<term>` and `git log -S <symbol>` to surface prior fixes on the same area (Rule 2.6).
- Designs before coding — shows hypothesis + fix location before editing.
- Applies the smallest change that satisfies the literal issue — no "while I'm here" refactors.
- Verifies at runtime (test, curl, screenshot, or user confirmation) before declaring done.

## Flow

1. Narrow mission — what is broken, what should happen?
2. Run `git log --grep` and `git log -S` over the symbol / file. Read matching commits.
3. Show hypothesis + fix location. Wait for signal.
4. Rule A — literal fix first, only what the issue states.
5. Rule B — match existing pattern in the same file.
6. Rule C — modify existing code over creating new files.
7. Rule D — smallest blast radius (fewest files, fewest lines).
8. Runtime verify + emit confidence label.

## Output format

```
Mission: <one-line statement>
Design: <hypothesis + location>
Fix: <diff with file:line>
Confidence: [high|medium|low|unsure]
Blast radius: N files, M lines
Next: <how to verify>
```

## When to use

- Specific, reproducible bug with a clear expected behavior.
- Regression surfaced in a PR.
- Follow-up fix after a [[Kasi-Review]] or [[Kasi-Security]] finding.

## When NOT to use

- You do not know what is wrong — diagnose first, do not fix.
- Bug is UI / CSS — use [[Kasi-Ui]] with Override Mode.
- Fix requires cross-file refactor — route through [[Kasi-Cascade]] or [[Kasi-Multi]].

## Tier behavior

- **Opus** — counter max 4 before Wave 1 escalation.
- **Sonnet** — counter max 3.
- **Haiku** — counter max 2; design step is mandatory, not optional.

## Anti-patterns

- ❌ Skipping `git log --grep` / `-S` — you repeat fixes that were already tried and reverted.
- ❌ "While I'm here" refactors that expand blast radius.
- ❌ Declaring done with no runtime evidence.
- ❌ Merging `[unsure]` into `[high]` to look confident.

## Since

Introduced in [[v0.7.4]].

## See also

- [[Commands]] (aggregate)
- [[Confidence-Labels]]
- [[Kasi-Review]]
- [[Kasi-Ui]]
