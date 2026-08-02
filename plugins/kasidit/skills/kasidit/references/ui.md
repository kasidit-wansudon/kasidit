# Kasidit — UI Override + Claude Design

> Visual/UI work routing. Referenced from ../SKILL.md.

---

## UI Override Mode

> Visual is truth. Cascade is noise.

### Why override, not audit

Legacy codebases have:
- Multiple CSS sources (Bootstrap mod + custom + inline).
- Version pinning and caching layers.
- Specificity wars between old and new rules.
- Dead code that still loads.

Auditing cascade is expensive and often wrong. When you can see the bug, override to win.

### Rules

**1. Refuse vague missions — demand a target.**

If user says "ดูดี / สวย / เหมาะสม / ปรับ / เพี้ยน" without criteria, ask:
- Screenshot of current state.
- **Visual target (choose one):**
  - Screenshot or wireframe of desired state, OR
  - Specific CSS values (width: 1200px, margin: 0 auto), OR
  - **Claude Design mockup** (offer this when user has no reference — "ขอให้ผมสร้าง mockup ใน Claude Design ก่อนไหม ?").

Do not guess. Visual target is non-negotiable.

**2. Cache is part of runtime.**

Every CSS/JS change:
- Bump version query (`?v=1.0.X`).
- Tell user: "Clear cache + hard refresh (Cmd+Shift+R / Ctrl+Shift+R)".
- Ask user to confirm via DevTools that new version loaded.
- Only then evaluate fix.

If user still sees old behavior after a change, **suspect cache first**, not the fix.

**3. Override with scoped class + !important.**

When screenshot shows visual mismatch and user has pointed at element:

```css
.kasidit-fix-<mission-id> <selector> {
  property: value !important;
}
```

- Unique wrapper class prefixed `kasidit-fix-`.
- `!important` without guilt — documented exception.
- Do not refactor legacy CSS unless user asks.

**4. One change per round.**

UI work: change exactly one thing per round:
- One property.
- One selector.
- Bump version.
- Wait for screenshot.

Multiple simultaneous changes make it impossible to tell what worked.

**5. UI counter is tighter.**

- **Round 2 fail**: Stop guessing. Ask user to paste DevTools "Computed" panel.
- **Round 3 (Haiku) / Round 4 (Opus) fail**: Hand back to user.

**6. Source-of-truth pattern copy.**

When one element looks right and another does not, copy the exact CSS pattern from the good one. Do not invent new values.

**7. Width/spacing audit protocol (v3).**

When "element แคบ/กว้าง/เตี้ย" — before fix:
```bash
grep -rn "max-width\|min-width\|width:" <css-files>
grep -rn "style=.*width" <view-files>
```

List ALL constraints affecting the element, including:
- Selectors by class/ID.
- Parent containers.
- Inline styles.
- Media queries.

Do not assume a selector named `#datatable` is "scoped elsewhere". Verify via DOM chain.

**8. Mockup-to-code parity check (v0.9).**

If mission started with a Claude Design mockup in `.kasidit/prototypes/<mission-id>-after.png`:
- After each CSS change, compare user screenshot vs mockup side-by-side.
- Parity criteria: spacing (px-level), color (hex), typography (family + weight + size), component placement.
- Report: `[parity high | medium | low]` per round.
- Mission done only when parity = high AND user confirms.

---

## Claude Design Integration (v0.9)

> Hand-coded HTML mockups are a waste of senior engineer time.
> Claude Design does visuals. Kasidit does code. Know which is which.

### Why this section exists

Before v0.9, Kasidit defaulted to hand-coding UI targets, wireframes, and stakeholder artifacts. That is:
- Slow (HTML/CSS takes 10x longer than prompting a visual tool).
- Wrong tool (mockups do not need to be production code).
- Hallucination-prone (AI invents layouts instead of iterating on a visible artifact).

**Claude Design (Anthropic Labs, launched 2026-04-17)** handles visuals; Kasidit handles the code that implements the visual.

### When to route to Claude Design

Route to Claude Design **before writing any markup/CSS** when the mission is any of:

| Trigger | Use Claude Design to produce |
|---|---|
| `mockup`, `wireframe`, `ร่าง UI` | Screen mockup (PNG or live URL) |
| `pitch deck`, `slide`, `deck` | PPTX or Canva-exportable deck |
| `one-pager`, `landing page` | One-page HTML / PDF |
| `pre-code sketch`, `ยังไม่ code` | Low-fi wireframe |
| `design system extract`, `visual pattern` | DESIGN_SYSTEM.md draft |
| `stakeholder review` | Prototype URL for PM/client to click |
| `audit visual report` | One-pager summary of findings |

### When NOT to route (stay in Kasidit)

- User has already provided a target (screenshot / CSS values / reference element).
- Mission is a tiny spacing/color/alignment fix on existing UI.
- Backend / data / logic / infra work — unrelated to visuals.
- User explicitly says "skip mockup, go code".

### Routing protocol

When a Design Mode trigger fires:

```
1. Confirm the mission in one line.
2. State: "routing to Claude Design for the visual."
3. Ask for:
   - Target audience (PM / client / dev handoff / self-reference)
   - Rough dimensions or platform (web / mobile / print / slide)
   - Existing brand constraints (link to DESIGN_SYSTEM.md if present)
4. Hand off prompt to Claude Design (open claude.ai/design with pre-filled brief).
5. Wait for user to return with:
   - Exported PNG/PDF/PPTX/URL, OR
   - "done, here's the result"
6. Save export to `.kasidit/prototypes/<mission-id>-<stage>.{png,url,pptx}`.
7. Resume Kasidit for coding/implementation if mission requires it.
```

**Haiku rule:** if mission starts in Design Mode and user has no reference, DO NOT attempt to generate a mockup as HTML. Refuse and route to Claude Design. Haiku hand-coded mockups are consistently wrong.

### Mockup → Code handoff

When user brings back a Claude Design mockup and wants to implement:

```
1. Save mockup to .kasidit/prototypes/<mission-id>-after.png
2. Read mockup + DESIGN_SYSTEM.md (if exists).
3. Extract:
   - Component list (nav, cards, table, buttons, ...)
   - Spacing values (px)
   - Color tokens (match DESIGN_SYSTEM.md or flag new)
   - Typography (family/weight/size)
4. Produce a text plan:
   - "Components to build: [list]"
   - "New tokens needed: [list]"  ← user confirms before adding
   - "Existing components reused: [list]"
5. Wait for user confirmation.
6. Enter UI Override / standard implementation flow.
7. Each round, parity check vs mockup (see UI Override Rule 8).
```

### Design System extraction

`build design-system` command:

```
1. Claude Design reads codebase:
   - CSS files (token values, classes)
   - Component files (Vue/React/Blade templates)
   - Existing screens (screenshots if available)
2. Generates draft DESIGN_SYSTEM.md with:
   - Extracted colors (hex + usage count)
   - Spacing scale detected
   - Typography stack
   - Components cataloged
3. User reviews and edits.
4. Save to .kasidit/DESIGN_SYSTEM.md.
5. Future Claude Design work for this project auto-applies this system.
```

This is the v0.9 equivalent of PATTERNS.md for visual work.

### Cost/benefit rules

- **Opus:** may skip Claude Design for internal-only, self-reference sketches (fast-path).
- **Sonnet:** default to Claude Design for any stakeholder-facing artifact.
- **Haiku:** always route visual work to Claude Design. No hand-coded mockups. Ever.

### Fallback when Claude Design is unavailable

Claude Design requires `claude.ai` access. In API-only, Cursor, or offline contexts it may not be reachable. Detect by asking user or by the absence of a `design` slash command.

**Fallback behavior by tier:**

| Tier | Claude Design available | Claude Design unavailable |
|------|------------------------|--------------------------|
| Opus | Route to Claude Design | Hand-code allowed — demand visual target (screenshot / CSS values / reference element) before starting |
| Sonnet | Route to Claude Design | Demand visual target; no speculative mockup; produce text wireframe only |
| Haiku | Route to Claude Design | **Refuse to produce mockup.** Output: "Visual target required — provide screenshot, CSS values, or reference element. No speculative mockup on Haiku." |

**Detection prompt (when unsure):**

```
Is claude.ai/design accessible in your current environment? (y/n)
If no: please provide a visual target — screenshot, CSS spec, or reference element.
```

Never assume availability. If the user has not confirmed Claude Design access this session, ask once.

### Anti-patterns for this section

- ❌ Hand-coding a mockup in HTML when Claude Design is available.
- ❌ Producing a "pitch deck" in markdown when user said deck/slides.
- ❌ Generating a mockup without asking audience + platform.
- ❌ Implementing code from a mockup without saving the mockup to `.kasidit/prototypes/`.
- ❌ Skipping DESIGN_SYSTEM.md check when mockup introduces new colors/spacing.
- ❌ Parity check by vibes — must be per-token comparison.

---

