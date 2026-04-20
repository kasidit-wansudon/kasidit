---
description: UI/CSS fix mission with Override Mode
---

Fix UI/CSS issues using Kasidit Override Mode.

**Philosophy:** Visual is truth. Cascade is noise.

**Flow:**
1. Demand screenshot — no guessing from text alone
2. Demand specific target — which element, what property?
3. Before any fix, grep ALL width/margin/padding/z-index affecting element
4. Check parent containers + inline styles + media queries
5. Apply override with scoped class + !important:
   ```css
   .kasidit-fix-<mission-id> <selector> {
     property: value !important;
   }
   ```
6. Bump cache version in HTML/template
7. Tell user to clear cache + Cmd+Shift+R
8. Wait for screenshot confirmation

**One change per round.** Multiple simultaneous changes = impossible to diagnose.

**Counter:**
- Round 2 fail → demand DevTools Computed panel from user
- Round 3 (Haiku) / 4 (Opus) → hand back to user

**Cache is runtime:**
- If user sees no change, suspect cache FIRST
- Version query: `?v=1.0.X` bumped every change
- Verify via DevTools Network tab before concluding fix failed

**Source-of-truth pattern copy:**
When one element looks right, copy its exact CSS to the broken one.
Do not invent values. Do not refactor legacy cascade.
