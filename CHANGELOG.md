# Changelog

All notable changes to Kasidit are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.9.0] — 2026-04-20

### Added
- **Claude Design Integration** section in SKILL.md. Routing protocol for mockup/wireframe/deck/one-pager work.
- **Design / Visual Mode** in Domain Detection. Triggers: `mockup`, `prototype`, `wireframe`, `pitch deck`, `slide`, `one-pager`, `landing page`.
- **`.kasidit/prototypes/`** storage for Claude Design exports.
- **`DESIGN_SYSTEM.md`** — visual counterpart to `PATTERNS.md` (colors, spacing, typography, components).
- **Mockup-to-code handoff flow** — save mockup, extract components, parity check per round.
- **UI Override Rule 8** — mockup-to-code token-level parity check.
- **New commands**: `design <what>`, `mockup <screen>`, `extract-system`, `parity <id>`, `report visual`.
- **Haiku rule**: never hand-code mockups. Always route to Claude Design.

### Changed
- **Rule 3 (Design before code)** — now offers Claude Design prototype for UI-touching missions.
- **UI Override Rule 1** — visual target options now include Claude Design mockup as a third path.
- **Review Mode step 8** — optional visual report via Claude Design for non-technical audiences.
- **Workflow diagram** updated to reflect design-mode routing and prototype saves.

### Fixed
- Anti-patterns list expanded with 3 Claude Design-specific items.

## [0.8.0] — 2026-04-15

### Added
- **Tier Cascade orchestration** — Opus plans, Sonnet works, Haiku greps.
- **Local embedding layer** — sentence-transformers scoped to `.kasidit/knowledge/`.

## [0.7.4] — 2026-04-10

### Added
- **Rule 2.3** — no fake metrics. Banned "analytical / theoretical / expected / projected" labels. Must measure before claiming numbers.
- **Rule 2.4** — number all options when asking user (1/2/3).
- **Rule 2.5** — native language reply (Thai user → Thai).
- **Rule 2.6** — mandatory `git log --grep` and `git log -S` before fixing bugs.

### Validated
- SWE-bench Lite sequential sample: 56/300 tasks. PASS strict 60.7% (34/56), valid rate 87.5% (49/56).
- 15 curated tasks: PASS 53% (8/15), valid 100% (15/15), 0 FAIL.
- 7 curated Opus tasks: PASS 86% (6/7), valid 100%.

## [0.3.0] — 2026-03-XX

### Added
- **Model tier adaptation** — Haiku / Sonnet / Opus rules.
- **Confidence labels** — `[high | medium | low | unsure]` on every non-trivial finding.
- **CHECKLISTS/** — pre-built audit lists (security, performance, framework-specific).
- **PATTERNS.md** — project-specific patterns AI copies, not reinvents.
- **Multi-agent orchestration** — subagents for parallel file/module review.
- **Verifier pass** — second agent removes false positives (mandatory on Haiku).
- **Vague mission detection** — refuse to start without narrowing.
- **CSS width audit protocol** — grep-before-fix for UI.
- **Review Mode** — checklist-driven audit flow.

## [0.2.1] — 2026-02-XX

### Added
- **Documentation retrieval protocol** — trust hierarchy, version matching, knowledge caching at `.kasidit/knowledge/<stack>-<version>-<topic>.md`.

## [0.2.0] — 2026-02-XX

### Added
- **UI Override Mode** — scoped class + `!important`, cache-aware, one-change-per-round.
- **Cache protocol** — version query bump + hard refresh verification.
- **Domain detection** — backend / UI / review routing.
- **Override-first strategy** — for legacy CSS, override beats audit.

## [0.1.0] — 2026-01-XX

### Added
- **Core principles** — mission-driven, minimal, design-before-code, docs-first, env-check, step-by-step, focused, terse, runtime-judged, data-before-UI.
- **Mission counter** — retry budget + Wave 1 / Wave 2 escalation.
- **สารบัญ system** — INDEX.md / RELATIONS.md / MEMORY.md for project-level knowledge.

[0.9.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.9.0
[0.8.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.8.0
[0.7.4]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.7.4
[0.3.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.3.0
[0.2.1]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.2.1
[0.2.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.2.0
[0.1.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.1.0
