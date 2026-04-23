# Changelog

All notable changes to Kasidit are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.9.2] — 2026-04-23

### Added

- **Gravity Pattern** — canonical name for Kasidit's two-tier knowledge system.
  - **Centerlite** (global hub): `~/.claude/skills/kasidit/center/` — shared patterns, checklists, knowledge, rules, mission history, prompt logs. Lightweight, append-only, user scope.
  - **Dcenterlite** (project orbit): `<project>/.kasidit/` — full-fidelity project knowledge. Source of truth for each project.
  - **Sync logic:** read = local with Centerlite fallback. Write = local only. Promote and pull are explicit user actions; nothing moves automatically. Logs flow one-way (prompt → Centerlite).
  - Documented in new **Gravity Pattern** section of `SKILL.md`.

- **Four new commands** (Gravity + workflow):
  - `/kasi-promote <type> <name>` — lift pattern / checklist / knowledge / rule from `.kasidit/` into Centerlite. Always asks confirmation.
  - `/kasi-pull <type> <name>` — fetch a shared item from Centerlite into current `.kasidit/`. Always diffs before overwrite.
  - `/kasi-sync` — audit drift between local and hub. Read-only; prints per-item suggestions but does not mutate.
  - `/kasi-wiki-sync` — push `docs/wiki/*.md` into the GitHub wiki repo (`kasidit.wiki.git`). Dry-run by default; `apply` flag required to push. Manual only — not wired to commit hooks.

- **`/kasi-init`** — one-shot project bootstrap. Chains `/kasi-scaffold` → `/kasi-docs` → `.kasidit/MISSION.md` seed → optional `/kasi-review` → registers project-level auto-invoke (SessionStart hook in `.claude/settings.local.json` + pointer in project `CLAUDE.md`). Skip flags: `skip docs`, `skip review`, `no auto-invoke`, `dry-run`.

- **Global prompt log** — new `UserPromptSubmit` hook (`~/.claude/hooks/kasidit-log.sh` + `kasidit-log.py`) writes every user prompt to `~/.claude/skills/kasidit/center/logs/YYYY-MM-DD.jsonl`. Prompts > 200 lines are trimmed to first 40 + last 20 lines with a `[trimmed N lines] ...` marker. Shared across all projects (user scope). Never blocks prompt; errors swallowed. Hook script + `README.md` bundled under `plugins/kasidit/hooks/` for install reference.

- **Default allow-list** for Kasidit workflows — adds `Bash(kasidit-*:*)`, `Read/Write(.kasidit/**)`, `Read(~/.claude/skills/kasidit/**)`, `Read(~/.claude/plugins/marketplaces/kasidit/**)`, and common read-only patterns (`grep`, `rg`, `find`, `git log/status/diff/blame/show`, version checks) so `kasi-*` missions run with fewer permission prompts.

- **Wiki source tree** — `docs/wiki/` with detailed per-version pages describing every release from `v0.1.0` to `v0.9.2` and the major subsystems (Gravity, Model Tiers, Multi-Agent Orchestration, Claude Design Integration, UI Override, Commands, FAQ). Intended to be pushed to the GitHub wiki via `/kasi-wiki-sync`.

### Changed

- `SKILL.md` — new sections **Gravity Pattern (v0.9.2)**, **Global Prompt Log (v0.9.2)**, **Project Init (v0.9.2)** inserted before User Commands. User Commands list gains five v0.9.2 entries (`/kasi-init`, `/kasi-promote`, `/kasi-pull`, `/kasi-sync`, `/kasi-wiki-sync`).
- `~/.claude/skills/kasidit/logs/` path canonicalized under Centerlite (`center/logs/`). Old path kept as a symlink for backward compat.
- `plugins/kasidit/hooks/kasidit-log.sh` default `LOG_DIR` points at the new Centerlite path.

### Fixed

- Haiku guidance on `/kasi-init`: skip the light review step during init unless user insists — Haiku needs checklists that scaffold has not finished producing yet.
- Promote / pull flows explicitly refuse silent overwrite; conflict path surfaces a diff instead of guessing a winner.

## [0.9.1] — 2026-04-22

### Added
- **Master Orchestrator Rule** in SKILL.md. Master agent delegates strong work to specialists; never executes code, edits, tests, or searches beyond top-level index.
- **Specialist Agent Registry** — 10 agents total (3 existing + 7 new).
- **Dispatch brief format** — every specialist invocation requires mission + inputs + constraints + expected output + prior context.
- 7 new specialist agents:
  - `bug-hunter` — root-cause debugging, minimal-change fix, mandatory `git log --grep` / `git log -S`.
  - `architect-planner` — plan only, no code; trade-offs + open questions + step sequence.
  - `perf-profiler` — measure first, rank by impact × confidence, top 5 only, does not optimize.
  - `test-writer` — one target per invocation, regression case mandatory after bug fix.
  - `refactor-surgeon` — named refactor only, zero behavior change, test-parity verified.
  - `deep-researcher` — trust hierarchy (source > official docs > release notes > blogs), cache to `.kasidit/knowledge/`.
  - `migration-specialist` — expand-contract phases, rollback per phase, risk classification GREEN/YELLOW/RED.

### Changed
- Anti-patterns list expanded with 4 master/specialist violations.
- Existing "Multi-Agent Orchestration (v3)" section now framed as implementation detail of the Master rule.

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

[0.9.2]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.9.2
[0.9.1]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.9.1
[0.9.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.9.0
[0.8.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.8.0
[0.7.4]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.7.4
[0.3.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.3.0
[0.2.1]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.2.1
[0.2.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.2.0
[0.1.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.1.0
