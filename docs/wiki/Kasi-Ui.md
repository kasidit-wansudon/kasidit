# /kasi-ui

> UI / CSS mission in Override Mode. Visual is truth, cascade is noise. One change per round, cache-aware.

## Usage

```
/kasi-ui <element> <property>
/kasi-ui <screenshot-path> <target>
```

## What it does

- Demands a screenshot — no guessing from text alone.
- Demands a specific target (which element, which property).
- Greps every width / margin / padding / z-index touching the target before editing.
- Checks parent containers, inline styles, and media queries.
- Applies a scoped override with `!important` under a mission-tagged class.
- Bumps cache version on the HTML / template and tells the user to hard-reload.

## Flow

1. Require screenshot of the broken state.
2. Require specific target — element + property.
3. Grep all rules affecting the element across CSS / inline / media queries.
4. Apply scoped override:
   ```css
   .kasidit-fix-<mission-id> <selector> {
     property: value !important;
   }
   ```
5. Bump cache version (`?v=1.0.X`) on the loader.
6. Tell user to clear cache + `Cmd+Shift+R`.
7. Wait for screenshot confirmation before next change.

## When to use

- UI change that is not sticking (cache or specificity war).
- Legacy CSS where refactoring is out of scope.
- One specific visual target the user can point at.

## When NOT to use

- You want to rewrite the design system — use `extract-system` + Claude Design, not Override Mode.
- Multi-element redesign — Override Mode is for surgical fixes, not layouts.
- You have no screenshot — refuse until you get one.

## Counter

- Round 2 fail → demand DevTools Computed panel from user.
- Round 3 (Haiku) / Round 4 (Opus) → hand back to user with findings.

## Cache is runtime

- If user sees no change, suspect cache **first**.
- Verify via DevTools Network tab before concluding the fix failed.

## Source-of-truth pattern copy

- When one element looks right, copy its exact CSS to the broken one.
- Do not invent values. Do not refactor legacy cascade.

## Anti-patterns

- ❌ Multiple simultaneous changes in one round — impossible to diagnose.
- ❌ Editing CSS without grepping all rules hitting the element.
- ❌ Forgetting the cache bump — "my change isn't working" is almost always cache.
- ❌ Inventing CSS values instead of copying from a working sibling.

## Since

Introduced in [[v0.2.0]].

## See also

- [[Commands]] (aggregate)
- [[UI-Override-Mode]]
- [[Kasi-Fix]]
