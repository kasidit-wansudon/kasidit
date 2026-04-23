# Model Tiers

Kasidit adapts behavior to the current model. Rules diverge by tier — because reasoning capacity diverges by tier.

> When reasoning is weak, scaffolding is strong.

## Detection

The skill detects the current tier from session context. When ambiguous, assume Haiku rules — it costs nothing to be more disciplined on Opus.

| Tier | Representative models |
|---|---|
| **Opus-class** | Opus 4.x, GPT-5, Gemini Ultra |
| **Sonnet-class** | Sonnet 4.x, mid-tier |
| **Haiku-class** | Haiku 4.x, Flash, Mini |

Force override: `tier opus | sonnet | haiku`.

## Rules by tier

### Opus-class

- Full framework enabled
- Architecture suggestions OK
- Creative problem solving OK
- May reason across files
- Counter max 4 rounds before Wave 1

### Sonnet-class

- Full framework enabled
- Verification pass recommended for security-critical work
- Cross-file reasoning OK — state assumptions explicitly
- Counter max 3 rounds before Wave 1

### Haiku-class — harder rules

- **No architecture decisions** — output "requires Opus/Sonnet or user decision"
- **No creative refactor** — only follow established patterns in codebase
- **Scope narrower** — 1 file per agent call, not 1 module
- **Checklist-driven** — use explicit rule files, not reasoning
- **Confidence scoring mandatory** — every finding tagged `high | medium | low | unsure`
- **Refuse uncertainty** — `unsure` → defer to user, do not guess
- **Verification pass mandatory** — second pass removes false positives after review
- **No speculation** — "this might cause X" → forbidden; prove X or do not mention
- **No hand-coded mockups** — always route visual work to Claude Design
- **Counter max 2 rounds** before Wave 1 — Haiku compounds errors faster

## Tier behavior across subsystems

### Review / Audit

- Opus: 1 module per agent; verifier optional
- Sonnet: 1 module per agent; verifier recommended on security
- Haiku: 1 file per agent; verifier **mandatory**

### UI Override

- Counter: Opus 4 / Sonnet 3 / Haiku 2 rounds before handback
- Mockups: Opus may hand-code small sketches; Sonnet defaults to Claude Design; Haiku always Claude Design

### Gravity

- Opus: may suggest promotions; user confirms
- Sonnet: default — pulls during init, promotes after 2+ occurrences
- Haiku: pulls aggressively during init; promotes rarely

### Docs fetching

- Opus/Sonnet: fetch when version-sensitive or unknown
- Haiku: **must** fetch or cite existing `.kasidit/knowledge/` entry before writing library code. No memory-based coding on libraries, ever.

### Tier Cascade ([[v0.8.0]])

- Opus: plan step
- Sonnet: work step
- Haiku: grep / scan / checklist step
- Opus: synthesize step

## Why Haiku rules are harder

Haiku does not have weaker reasoning *in general* — it has weaker **ungrounded** reasoning. Given a checklist, it executes faithfully. Given an open question ("should we refactor UserService?"), it confabulates.

Kasidit converts as many open questions as possible into checklist execution:

- Security audit → `CHECKLISTS/security-<stack>.md`
- Project patterns → `PATTERNS.md`
- Knowledge → `.kasidit/knowledge/`
- Hub scaffolding → Centerlite ([[Gravity Pattern]])

With those files in place, Haiku performs on many tasks comparably to Sonnet at a fraction of the cost. Without them, Haiku hallucinates. The framework is the difference.

## See also

- [[v0.3.0]] — tier adaptation was introduced
- [[Gravity Pattern]]
- [[Multi Agent Orchestration]]
