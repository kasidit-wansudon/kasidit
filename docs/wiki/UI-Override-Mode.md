# UI Override Mode

Introduced in [[v0.2.0]], extended in [[v0.9.0]] with Claude Design mockup support.

> Visual is truth. Cascade is noise. Override with scope, not elegance.

## When to use

Triggered automatically when the domain is UI / CSS / layout. Triggers include: `styling`, `spacing`, `alignment`, `color`, `font`, `layout`, `เพี้ยน`, `ดูดี`, `ไม่ตรง`, `shift`, `overflow`, `responsive`. Screenshot attached with visual complaint also enters this mode.

## The eight rules

### Rule 1 — Refuse vague missions

Require a visual target (choose one):

1. Screenshot or wireframe of desired state
2. Specific CSS values (width / margin / color / font)
3. Claude Design mockup — the agent can offer to draft one (added in [[v0.9.0]])

Do not guess. Visual target is non-negotiable.

### Rule 2 — Cache is part of runtime

Every CSS / JS change:

- Bump version query (`?v=1.0.X`)
- Tell user: "Clear cache + hard refresh (Cmd+Shift+R / Ctrl+Shift+R)"
- Confirm via DevTools that the new version loaded
- Only then evaluate the fix

If user still sees old behavior after a change, **suspect cache first**, not the fix.

### Rule 3 — Override with scoped class + `!important`

```css
.kasidit-fix-<mission-id> <selector> {
  property: value !important;
}
```

Documented exception — do not refactor legacy CSS unless user asks.

### Rule 4 — One change per round

One property, one selector, bump version, wait for screenshot. Multiple simultaneous changes make it impossible to tell what worked.

### Rule 5 — UI counter is tighter

| Tier | Rounds before handback |
|---|---|
| Opus | 4 |
| Sonnet | 3 |
| Haiku | 2 |

Round 2 fail: ask user for DevTools "Computed" panel contents.

### Rule 6 — Source-of-truth pattern copy

When one element looks right and another does not, copy the exact CSS pattern from the good one. Do not invent new values.

### Rule 7 — Width / spacing audit protocol

Before fixing "too narrow / too wide / too short":

```bash
grep -rn "max-width\|min-width\|width:" <css-files>
grep -rn "style=.*width" <view-files>
```

List **all** constraints: class / ID, parent containers, inline styles, media queries. Do not assume scope.

### Rule 8 — Mockup-to-code parity check ([[v0.9.0]])

If mission started with a mockup in `.kasidit/prototypes/<mission-id>-after.png`:

- After each CSS change, compare user screenshot vs mockup side-by-side
- Parity criteria: spacing (px-level), color (hex), typography (family + weight + size), placement
- Report `[parity high | medium | low]` per round
- Mission done only when parity = high **and** user confirms

## Anti-patterns

- ❌ Audit entire cascade before a simple visual fix
- ❌ Multiple simultaneous changes in one round
- ❌ Trust that "the CSS is right" without a screenshot
- ❌ Parity check by vibes — token-level comparison required
- ❌ Invent width values — copy from source-of-truth

## See also

- [[v0.2.0]] — introduction
- [[v0.9.0]] — Claude Design integration + Rule 8
- [[Claude Design Integration]]
