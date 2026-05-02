# Changelog

All notable changes to Kasidit are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.13.1] — 2026-05-02

### Fixed

- **`SKILL.md` Version section now reflects v0.12 + v0.13.** Prior release-pipeline updates only bumped `marketplace.json` / `plugin.json` and `CHANGELOG.md`, leaving the in-skill `## Version` block stuck at v0.11. Result: when users asked Kasidit "what version", the framework reported v0.11 even though the marketplace was at v0.13.0. Added v0.13 + v0.12 entries to `plugins/kasidit/skills/kasidit/SKILL.md`.

### Pipeline note

The release pipeline checklist now includes "update SKILL.md Version section" alongside the existing manifest + CHANGELOG bumps. See `~/.claude/projects/.../memory/feedback_release_pipeline_full_loop.md`.

## [0.13.0] — 2026-05-02

### Added

Consolidated **thClaws Runtime Support** release — supersedes the partial v0.12.0/v0.12.1 sequence. Single complete install path; no migration steps required.

- **`plugins/kasidit/install-thclaws.sh`** — full installer for [thClaws](https://github.com/thClaws/thClaws). Targets `~/.config/thclaws/` paths and uses thClaws's shell-snippet hook config format. On a fresh install, produces:
  - `~/.config/thclaws/skills/kasidit/SKILL.md` — main framework spec
  - `~/.config/thclaws/skills/kasidit/includes/` — patterns + design-system templates
  - `~/.config/thclaws/skills/kasidit/center/` — Gravity hub (route-memory, patterns, memory, rules, missions JSONL × 5)
  - `~/.config/thclaws/skills/kasidit/scripts/` — `build_graph.{sh,py}` + `build_struc.{sh,py}`
  - `~/.config/thclaws/commands/kasi-*.md` — 22 slash commands
  - `~/.config/thclaws/agents/*.md` — 11 specialist agents (8 active + 3 deprecated stubs)
  - `~/.config/thclaws/hooks/kasi-{update-check,drift-check,verify,record}.{sh,py}` — 4 hooks
  - `~/.config/thclaws/settings.json` — 3 hook entries (`session_start`, `post_tool_use`, `session_end`)
- **Mirrored plugin manifests** under `.thclaws-plugin/marketplace.json` + `plugins/kasidit/.thclaws-plugin/plugin.json` (parallel to existing `.claude-plugin/`).
- **`docs/thclaws-setup.md`** — full guide for thClaws users.

### Hook event mapping

| Kasidit hook | Claude Code event | thClaws event | Status |
|---|---|---|---|
| `kasi-update-check.sh` | `SessionStart` | `session_start` | ✅ direct port |
| `kasi-drift-check.sh` | `SessionStart` | `session_start` | ✅ direct port |
| `kasi-verify.py` | `PostToolUse` + `Stop` | `post_tool_use` | ⚠️ per-tool only |
| `kasi-record.py` | `Stop` | `session_end` | ⚠️ per-session aggregation |
| `kasi-route.py` | `UserPromptSubmit` | — | ❌ skipped (no equivalent event) |
| `kasi-log.{sh,py}` | `UserPromptSubmit` | — | ❌ skipped (same reason) |

Net: ~85% feature parity. The 2 skipped hooks are the global prompt classifier and prompt log — useful but not load-bearing for the discipline framework.

### Verified

Real install on `~/.config/thclaws/` confirmed via `thclaws --cli` + `/skills`:

```
[commands] 22 command(s) loaded
[skills] 2 skill(s) loaded
  kasidit [+scripts] (user)
  kasidit-default (claude)
```

### Bug fix

`install.sh` (Claude Code installer) — leftover glob `kasidit-*` from before the v0.11 hook rename was preventing fresh installs from copying `kasi-*` hooks. Fixed.

### Notes

- v0.12.0 and v0.12.1 are superseded by this release. Both are kept on the GitHub release page for historical reference, but new installs should use v0.13.0.
- No breaking changes for Claude Code users.
- Cross-runtime Gravity hub sync is deferred to v0.14.

## [0.12.1] — 2026-05-02

Patch release. Fixed `install-thclaws.sh` missing copy of SKILL.md / commands / agents. Superseded by v0.13.0.

## [0.12.0] — 2026-05-02

### Added

- **thClaws runtime support.** Kasidit now installs on [thClaws](https://github.com/thClaws/thClaws) (native Rust agent harness from ThaiGPT Co.) alongside Claude Code.
  - New installer: `plugins/kasidit/install-thclaws.sh` — copies hooks to `~/.config/thclaws/hooks/`, seeds Gravity hub at `~/.config/thclaws/skills/kasidit/center/`, registers hooks in `~/.config/thclaws/settings.json`.
  - Mirrored manifests: `.thclaws-plugin/marketplace.json` + `plugins/kasidit/.thclaws-plugin/plugin.json` (parallel to existing `.claude-plugin/` layout).
  - New docs: `docs/thclaws-setup.md` — full guide including hook event mapping, install/uninstall, and limitations.
- Hook event mapping for thClaws:
  - `kasi-update-check.sh` → `session_start` (direct port)
  - `kasi-drift-check.sh` → `session_start` (direct port)
  - `kasi-verify.py` → `post_tool_use` (per-tool, no per-turn aggregation)
  - `kasi-record.py` → `session_end` (per-session aggregation; emit-token protocol still works)
  - `kasi-route.py` and `kasi-log.{sh,py}` are SKIPPED on thClaws — no `UserPromptSubmit` equivalent
- New keywords on plugin manifest: `thclaws`, `multi-runtime`.

### Changed

- Plugin metadata bumped 0.11.0 → 0.12.0 across `marketplace.json` + `plugin.json` files (4 manifests total).
- `install.sh` (Claude Code installer) — fixed leftover glob bug `kasidit-*` → `kasi-*` (was preventing fresh-install hook copy after the v0.11 file rename).
- README.md — added thClaws install section + link to `docs/thclaws-setup.md`.

### Notes

- Kasidit on thClaws runs in **degraded mode** for 2 hooks (route + log) — discipline framework, commands, agents, checklists, scripts all work fully. The framework's prompt-level rules (Master Orchestrator, tier-aware, confidence labels, mission-driven) are runtime-agnostic and apply identically on both runtimes.
- Gravity hub paths split per runtime: Claude Code `~/.claude/skills/kasidit/center/` vs thClaws `~/.config/thclaws/skills/kasidit/center/`. Cross-runtime sync is deferred to v0.13.
- No breaking changes for existing Claude Code installs.

## [0.11.0] — 2026-04-30

### Added

- New mission commands:
  - `/kasi-backend <fix|audit|scaffold|design|perf|security> <scope>` — backend counterpart of `/kasi-ui`. Auto-detects Laravel (composer.json) / Node (express|fastify|hono|nest|koa).
  - `/kasi-graph <build|show|extract|impact|trace|cycles|dead>` — function call graph; consumed by `/kasi-backend audit|perf` to scope specialists to a subgraph.
  - `/kasi-struc <build|refresh|show|tree|module|path|bridge|verify>` — project structure cache (`.kasidit/STATE/`); other kasi-* commands read state instead of rescanning.
  - `/kasi-devopt <deploy|env|data|infra|secrets|runbook|health|connect>` — DevOps mission. Outputs deploy plan, never executes the deploy itself.
  - `/kasi-acknowledge [capture|template|update|link]` — capture last-performed steps as a replayable runbook. Writes `.kasidit/knowledge/runbooks/<kind>/<slug>-<date>.md`.
  - `/kasi-knowledge-list [list|show|recent|tag|kind|search|replay|stats|stale]` — browse + step-by-step replay of stored runbooks.
- New checklists in `~/.claude/skills/kasidit/CHECKLISTS/`:
  - `backend-laravel.md` (A–M sections + severity guide)
  - `backend-node.md` (A–N sections)
  - `backend-api-design.md` (stack-agnostic API rules)
- New scripts in `~/.claude/skills/kasidit/scripts/`:
  - `build_graph.sh` — entry script (delegates to Python).
  - `build_graph.py` — regex MVP for PHP + JS/TS function call extraction. ast-grep AST path stubbed for future.

### Changed

- **File-path standardization** — all `kasidit-{route,verify,record,log,update-check,drift-check}.{py,sh}` hooks renamed to `kasi-*` in both `~/.claude/hooks/` and the plugin marketplace.
- Skill `~/.claude/skills/kasidit-default/` → `kasi-default/`.
- `~/.claude/settings.json` hook commands and permission glob updated to `kasi-*` paths.
- `install.sh`, `test_hooks.py`, SKILL.md, README.md, this CHANGELOG.md updated to reference the new file paths.
- Backward-compat symlinks (`kasidit-X` → `kasi-X`) added in `~/.claude/hooks/` so cached settings.json paths in running sessions keep working until the next Claude Code reload.

### Retained (intentionally not renamed)

- Internal emit-token protocol: `[kasidit-log]`, `[kasidit-pattern]`, `[kasidit-memory]`, `[kasidit-rule]`, `[kasidit-verify]`, `[kasidit-record]` — would break the AI-emit ↔ parser-regex contract and existing JSONL stores.
- Brand prefix in route output: `[kasidit] kind=... mode=...`.
- Env vars: `KASIDIT_CENTER`, `KASIDIT_PROJECT_DIR`, `KASIDIT_LOG_DIR`.
- Top-level skill / plugin / GitHub names: `~/.claude/skills/kasidit/`, `~/.claude/plugins/marketplaces/kasidit/`, `kasidit-wansudon/kasidit`.

### Notes

- `/kasi-struc` and `/kasi-devopt` ship as command specs; their bridge-state writers (`.kasidit/STATE/*.json`, `.kasidit/STATE/changelog.jsonl`) are spec-only in v0.11. The state schema is documented in the command files; a Python builder analogous to `build_graph.py` will land in v0.12.
- `/kasi-acknowledge` and `/kasi-knowledge-list` perform their work via the AI prompt + Read/Write tools; no separate runner script is required for v0.11.

## [0.10.0] — 2026-04-24

### Added

- **`/kasi` Mode command** — selects framework intensity for the current session. Values: `off` / `router` / `lite` / `full` / `ultra`. Default = `router`.
  - **Caveat (honest):** mode gating is a prompt-level convention. The AI reads the declared mode from `SKILL.md` sections and self-applies. The Claude Code harness does NOT enforce mode boundaries at runtime.
- **`SKILL.md` restructure** — Router Mode default section + Full Framework section live in the **same file**. No lazy-loading. The file explicitly documents that mode gating is prompt-level, not harness-enforced.
- **Backend hooks** (runtime-enforced, bundled under `plugins/kasidit/hooks/`):
  - `kasi-route.py` — `UserPromptSubmit` classifier + memory query. Routes prompts by mission-kind heuristic.
  - `kasi-verify.py` — `PostToolUse` + `Stop` cross-check. Flags missing confidence labels and detects master-orchestrator violations (main agent executing strong work instead of delegating).
  - `kasi-record.py` — `Stop` hook. Parses `[kasidit-log|pattern|memory|rule]` emit lines from the AI output and appends them to JSONL files.
  - `kasi-update-check.sh` — 1×/day GitHub release tag check. Soft-notifies on new versions.
- **Incremental backend save ("ออม")** — AI emits `[kasidit-log] kind=<mission-kind> mode=<mode> turns=<n> outcome=<pass|fail>` lines at mission end. `kasi-record.py` appends to JSONL. Router learns the shortest successful route per mission kind over successive sessions.
- **`audit-specialist` agent** — merges `code-reviewer` / `security-auditor` / `perf-profiler` behind a single entry point with `--focus=quality|security|perf|all`. Old agent files kept as thin stubs for name resolution; scheduled for removal in v0.11.
- **`sudo <mission>` keyword** — session-only speed shortcut. Minimum 2 parallel agents. **Not** a permission escalation, does not bypass destructive-op confirmation.
- **`/kasi-multi --fast` flag** — alternative surface for the same speed shortcut as `sudo`.
- **`install.sh`** — idempotent installer. Copies hooks, merges `~/.claude/settings.json` via `jq` with a `python3` stdlib fallback, seeds Gravity hub with 5 JSONL files and PHP / Node / Python / Go default checklists. Safe to re-run.
- **`test_hooks.py`** — 10 isolated snapshot tests for the new hook scripts. No shared state between tests.

### Changed

- `SKILL.md` reorganized into Router Mode (default, minimal) + Full Framework (opt-in via `/kasi full` or `ultra`). Router Mode is intentionally thin so the framework does not inflate short missions.
- Install path — `install.sh` is now the canonical install flow. Manual `cp` remains supported but is documented as a debugging path.

### Fixed

- Python 3.9 compatibility — added `from __future__ import annotations` to hook scripts so they run on macOS default Python without `TypeError` on PEP 604 unions.
- Isolated test state — `test_hooks.py` no longer shares temp paths between cases; fixes flake when run in parallel.

### Deprecated

- `code-reviewer`, `security-auditor`, `perf-profiler` agent files — now thin stubs that forward to `audit-specialist`. Scheduled for removal in **v0.11**.

### Removed

- Nothing removed in v0.10. (Old agent files deprecated but retained for name-resolution back-compat.)

### Honesty notes

- Mode gating (`off` / `router` / `lite` / `full` / `ultra`) is a **prompt-level convention**. The AI reads the declared mode and self-applies. The Claude Code harness does not enforce mode boundaries.
- Router does **not** auto-map old agent names to `audit-specialist` — old names still resolve to their stub files; no silent rerouting.
- Session mode precedence is resolved by user or AI applying config files directly. There is no runtime resolver.
- No new benchmark numbers. The v0.7.4 SWE-bench Lite sample (60.7% strict / 87.5% valid on 56/300) remains the published figure. A re-run on v0.10 has not been performed.

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

- **Multi-Agent Mode** — `/kasi-multi [N] [mission]` fan-out command dispatches N specialist agents in parallel (default N=6) with mission-kind-heuristic roster selection and a single-pass synthesis step. New `sudo <mission>` / `sudo <N> <mission>` keyword shorthand enters fan-out mode with reasonable-assumption pacing (does NOT bypass destructive-op confirmation). Haiku tier caps N at 4 to avoid synthesis collapse. See `commands/kasi-multi.md` + new SKILL.md section **Multi-Agent Mode — Fan-Out (v0.9.2)**.

- **`/kasi-init`** — one-shot project bootstrap. Chains `/kasi-scaffold` → `/kasi-docs` → `.kasidit/MISSION.md` seed → optional `/kasi-review` → registers project-level auto-invoke (SessionStart hook in `.claude/settings.local.json` + pointer in project `CLAUDE.md`). Skip flags: `skip docs`, `skip review`, `no auto-invoke`, `dry-run`.

- **Global prompt log** — new `UserPromptSubmit` hook (`~/.claude/hooks/kasi-log.sh` + `kasi-log.py`) writes every user prompt to `~/.claude/skills/kasidit/center/logs/YYYY-MM-DD.jsonl`. Prompts > 200 lines are trimmed to first 40 + last 20 lines with a `[trimmed N lines] ...` marker. Shared across all projects (user scope). Never blocks prompt; errors swallowed. Hook script + `README.md` bundled under `plugins/kasidit/hooks/` for install reference.

- **Default allow-list** for Kasidit workflows — adds `Bash(kasidit-*:*)`, `Read/Write(.kasidit/**)`, `Read(~/.claude/skills/kasidit/**)`, `Read(~/.claude/plugins/marketplaces/kasidit/**)`, and common read-only patterns (`grep`, `rg`, `find`, `git log/status/diff/blame/show`, version checks) so `kasi-*` missions run with fewer permission prompts.

- **Wiki source tree** — `docs/wiki/` with detailed per-version pages describing every release from `v0.1.0` to `v0.9.2` and the major subsystems (Gravity, Model Tiers, Multi-Agent Orchestration, Claude Design Integration, UI Override, Commands, FAQ). Intended to be pushed to the GitHub wiki via `/kasi-wiki-sync`.

### Changed

- `SKILL.md` — new sections **Gravity Pattern (v0.9.2)**, **Global Prompt Log (v0.9.2)**, **Project Init (v0.9.2)** inserted before User Commands. User Commands list gains five v0.9.2 entries (`/kasi-init`, `/kasi-promote`, `/kasi-pull`, `/kasi-sync`, `/kasi-wiki-sync`).
- `~/.claude/skills/kasidit/logs/` path canonicalized under Centerlite (`center/logs/`). Old path kept as a symlink for backward compat.
- `plugins/kasidit/hooks/kasi-log.sh` default `LOG_DIR` points at the new Centerlite path.

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

[0.10.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.10.0
[0.9.2]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.9.2
[0.9.1]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.9.1
[0.9.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.9.0
[0.8.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.8.0
[0.7.4]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.7.4
[0.3.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.3.0
[0.2.1]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.2.1
[0.2.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.2.0
[0.1.0]: https://github.com/kasidit-wansudon/kasidit/releases/tag/v0.1.0
