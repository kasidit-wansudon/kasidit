# Version History

Side-by-side comparison. Detailed per-version notes live on each release page.

| Version | Date | Theme | Headline change |
|---|---|---|---|
| [[v0.16.0]] | 2026-07-09 | **Deploy Split** | `/kasi-deploy` (real execute path, Cloudflare/Vercel/Netlify auto-run behind a typed prod confirm gate) + `/kasi-review-deploy` (strict read-only preflight, any tier). Supersedes `/kasi-devopt deploy`. Haiku tier-gated off auto-execute. 23 → 25 commands. |
| [[v0.15.0]] | 2026-06-02 | **Team Mode** | `/kasi-team` — HYBRID panel brainstorm + mandatory user decision gate + parallel dispatch + QA synthesis. CORE (lead/QA) + DYNAMIC specialist composition, no new agent files. `sudo` shorthand now defaults to N=6 (was N=2). Hook internal references renamed `kasidit-*` → `kasi-*`. |
| [[v0.14.0]] | 2026-05-26 | **MAST-Evidence Dispatch Hardening** | `DONE WHEN:` field + `PRIOR CONTEXT` split into `COMPLETED:`/`OPEN:` with `[agent-name]` attribution (targets MAST FM-1.5 + FM-1.3, the top 2 multi-agent failure modes, NeurIPS 2025). Specialist Registry gets a `Default Tier` column (Haiku for read-only research, cutting typical `/kasi-multi 6` dispatch cost ~50%). Refinement Counter added (caps same-hypothesis polish at 3 rounds). Rule 8 reframed positive per Pink Elephant Problem evidence. |
| [[v0.13.0]] | 2026-05-02 | **thClaws Runtime Support (Consolidated)** | Supersedes v0.12.0/v0.12.1. Single clean install path. New `install-thclaws.sh` (full file install: SKILL.md + 22 commands + 11 agents + 4 hooks + 15 checklists + scripts). ~85% feature parity. Hook event mapping (4/5 hooks adapted). |
| [[v0.12.0]] | 2026-05-02 | **thClaws Runtime Support** | Kasidit now runs on Claude Code **and** [thClaws](https://github.com/thClaws/thClaws). New `install-thclaws.sh`, mirrored `.thclaws-plugin/` manifests, hook event mapping (4/5 hooks adapted, 1 skipped), `docs/thclaws-setup.md`. ~85% feature parity. Bug fix: leftover `kasidit-*` glob in `install.sh`. |
| [[v0.11.0]] | 2026-04-30 | **Backend + Bridge + Runbook** | 6 new commands: `/kasi-backend` (mission router), `/kasi-graph` (function call graph), `/kasi-struc` (project-state cache + auto-bridge), `/kasi-devopt` (DevOps mission, never executes), `/kasi-acknowledge` + `/kasi-knowledge-list` (runbook capture + replay). 3 new backend checklists. 4 helper scripts. Hooks renamed `kasidit-*` → `kasi-*`. |
| [[v0.10.0]] | 2026-04-26 | **Honesty Cleanup** | SKILL-full split reverted (Mode-gated single file), `audit-specialist` merges 3 audit agents, runtime backend hooks (route/verify/record/update/drift), `install.sh`, 12 default checklists, incremental backend save (`route-memory.jsonl`) |
| [[v0.9.2]] | 2026-04-23 | **Gravity Pattern** | Two-tier knowledge (Centerlite hub + Dcenterlite project), prompt log hook, `/kasi-init`, `/kasi-promote`, `/kasi-pull`, `/kasi-sync`, `/kasi-wiki-sync` |
| [[v0.9.1]] | 2026-04-22 | **Master Orchestrator** | Master delegates all strong work to 10 specialist agents; dispatch brief format |
| [[v0.9.0]] | 2026-04-20 | **Claude Design** | Design/Visual Mode, `.kasidit/prototypes/`, DESIGN_SYSTEM.md, mockup-to-code parity |
| [[v0.8.0]] | 2026-04-15 | **Tier Cascade** | Opus plans → Sonnet works → Haiku greps. Local embedding layer for `.kasidit/knowledge/` |
| [[v0.7.4]] | 2026-04-10 | **SWE-bench + rules** | 60.7% PASS on 56 SWE-bench Lite tasks. Rules 2.3 (no fake metrics), 2.4 (numbered options), 2.5 (native language), 2.6 (mandatory git-log/git-S on bug fix) |
| [[v0.3.0]] | 2026-03 | **Tier adaptation** | Opus/Sonnet/Haiku rules diverge. Confidence labels `[high/medium/low/unsure]`. CHECKLISTS/. PATTERNS.md. Multi-agent orchestration. Verifier pass |
| [[v0.2.1]] | 2026-02 | **Docs protocol** | Trust hierarchy (source → official docs → release notes → blogs), version matching, `.kasidit/knowledge/` cache |
| [[v0.2.0]] | 2026-02 | **UI Override** | Scoped class + `!important`, cache-aware, one-change-per-round, override > audit for legacy CSS |
| [[v0.1.0]] | 2026-01 | **Core** | Core principles, mission counter, สารบัญ (INDEX/RELATIONS/MEMORY) |

## What changed between each pair

### v0.15.0 → v0.16.0 (this release)

- **`/kasi-deploy` — first command permitted to execute a deploy itself.** Fixed capability table: Cloudflare (`wrangler`), Vercel, and Netlify are auto-executable (first-party idempotent one-shot CLI); SSH/bare-VPS and infra-as-code platforms (Docker/k8s/Terraform/Serverless/Fly/Platform.sh) stay plan-only, exactly as `/kasi-devopt deploy` always was. Prod execution requires a **typed** `confirm: deploy-prod` gate — a plain "yes" is rejected. Staging/preview needs only a plain confirm. Dirty working tree forces plan-only unless `--allow-dirty`. Always runs the preflight first; blocks entirely on a NOT READY verdict. On failure: reports the error, never auto-retries or auto-rollbacks.
- **`/kasi-review-deploy` — the never-executes guarantee, extracted.** Strict read-only preflight checklist, zero execution and zero file writes on any platform, at any tier including Haiku. Pulled out of `/kasi-devopt deploy <env>` as its own command so "never runs anything" is an unconditional property of the command, not a soft rule embedded in a multi-mode one.
- **`/kasi-devopt`'s `deploy <env>` sub-mode superseded.** Redirects to the two new commands on invocation; old flow kept inline for reference, not run for new missions. Other sub-modes (`env`, `data`, `infra`, `secrets`, `runbook`, `health`, `connect`) unchanged.
- **Tier gating for deploy execution.** Haiku restricted to the plan-only path on `/kasi-deploy` regardless of platform — auto-execute requires Sonnet or Opus, matching the existing pattern of refusing high-stakes work at the cheapest tier.
- **Command count** 23 → 25.

### v0.14.0 → v0.15.0

- **Team Mode — `/kasi-team`.** HYBRID dev-team workflow: Main spawns a brainstorm panel (default N=3) whose role-agents each propose an approach + top-3 risks, synthesizes into 2-3 options with trade-offs, presents to the **user for a mandatory decision gate**. After the pick: dispatches implementation specialists in parallel (reusing `/kasi-multi` fan-out mechanics) + mandatory QA pass (`audit-specialist --focus=quality`) before final synthesis. Distinct from `/kasi-multi`/`sudo` (which execute a known approach) — Team Mode decides the approach first.
- **CORE + DYNAMIC composition.** Core roles (Lead = `architect-planner`, QA = `audit-specialist --focus=quality`) always present; dynamic lenses (security/perf/migration) + implementation specialists picked per mission from the existing registry. No new agent files.
- **Refinement Counter capped at 1 round** for the brainstorm phase (vs framework default 3) to prevent option proliferation. `--fast` skips the refinement round only — QA pass never skipped.
- **Haiku tier:** panel reduced to N=2, 0 refinement rounds, dispatch cap N=4; refuses missions requiring a security/migration lens.
- **`sudo` shorthand now defaults to N=6** (was N=2), matching `/kasi-multi`'s default roster. Still a pacing signal, not a permission escalation.
- **Hook internal references renamed `kasidit-*` → `kasi-*`** (docstrings, comment headers, `kasi-log.sh` → `kasi-log.py` cross-call). JSONL log-marker tokens (`[kasidit-log]`, `[kasidit-pattern]`, …) intentionally unchanged for parser compatibility.
- **Counter/tier specs made Sonnet-explicit** across several command docs; deprecated-agent stubs (`code-reviewer`, `perf-profiler`, `security-auditor`) reworded — they're kept **indefinitely** for name resolution, not "removed in v0.11" as previously claimed.

### v0.13.0 → v0.14.0

- **Dispatch brief — `DONE WHEN:` field.** Specialist briefs must declare measurable completion signals (tests pass, no lint, curl returns expected shape). Addresses MAST taxonomy (arXiv 2503.13657, NeurIPS 2025) failure mode FM-1.5 "unaware of termination conditions" — 12.4% of multi-agent failures across 1,600+ production traces.
- **`PRIOR CONTEXT` split into `COMPLETED:` + `OPEN:` with `[agent-name]` attribution.** Addresses MAST FM-1.3 step repetition (15.7%, the #1 multi-agent failure mode) by making progress state explicit and preventing specialists from re-executing finished work.
- **Specialist Agent Registry gets a `Default Tier` column.** Read-only research = Haiku, analytical/synthesis = Sonnet, creative/high-stakes = Opus. Includes a 20% correction-rate watch to escalate Haiku → Sonnet when re-prompt cost negates the savings. Projected cost reduction on read-heavy multi-agent runs: 50-80% (`/kasi-multi 6` typical dispatch ~$0.45 → ~$0.23).
- **Refinement Counter** (separate from the Failure Counter) added. Caps same-hypothesis polish at 3 rounds; halts on confidence-same-or-lower across iterations — guards against the "coherence trap" (Reflexion ICLR 2024) of increasingly polished but still-wrong reasoning.
- **Rule 8 reframed positive.** "Output direct, reserve explanation" replaces "Explain = Hallucinate" per Pink Elephant Problem evidence (arXiv 2503.22395, 2025) — LLMs systematically underperform under negation. Behavior identical; framing is now actionable rather than prohibitive.
- **Agent model tier defaults tuned:** `deep-researcher` sonnet → haiku (3× cheaper for read-only), `architect-planner` opus → sonnet (was over-provisioned for plan-only work), `legacy-specialist` → haiku explicit for read-only paths.
- Evidence base: 80+ verified URLs — Anthropic official docs, arXiv 2025-2026 (MAST taxonomy, Pink Elephant, Reflexion), production retrospectives (Shopify/Stripe/Airbnb/GitHub Copilot/Cursor).

### v0.12.0 → v0.13.0

- **Consolidates v0.12.0 + v0.12.1 into a single clean release.** v0.12.0 install was partial (missed copying SKILL.md / commands / agents to thClaws skill dirs). v0.12.1 patched it. v0.13.0 ships the full `install-thclaws.sh` as the canonical install path; v0.12.x are superseded.
- **Same install-thclaws.sh as v0.12.1** — full file copy (SKILL.md + includes/ + 22 commands + 11 agents + 4 hooks + 15 checklists + 4 scripts + Gravity hub + settings.json hook entries).
- **CHANGELOG narrative cleaned** — no migration steps required. New users install v0.13.0; existing v0.12.x users `git pull` + re-run installer (idempotent).
- **No breaking changes** for Claude Code users.

### v0.11.0 → v0.12.0

- **thClaws runtime support.** Kasidit now installs on [thClaws](https://github.com/thClaws/thClaws) (native Rust agent harness from ThaiGPT Co.) alongside Claude Code. New `plugins/kasidit/install-thclaws.sh` handles thClaws's `~/.config/thclaws/` directory layout and shell-snippet hook config format (distinct from Claude Code's array-of-objects format).
- **Hook event mapping.** Claude Code → thClaws: `SessionStart` → `session_start` (direct: kasi-update-check, kasi-drift-check), `PostToolUse`+`Stop` → `post_tool_use` (per-tool, no per-turn aggregation: kasi-verify), `Stop` → `session_end` (per-session aggregation: kasi-record). Skipped on thClaws: `kasi-route.py` and `kasi-log.{sh,py}` (no `UserPromptSubmit` equivalent event yet). Net ~85% feature parity.
- **Mirrored plugin manifests** under `.thclaws-plugin/` (parallel to `.claude-plugin/`). Same metadata + version (0.12.0) + keywords.
- **`docs/thclaws-setup.md`** — full guide for thClaws users: install/uninstall, hook event mapping, behavior differences vs Claude Code, recommended workflow.
- **README.md** adds thClaws install section between Claude Code install and Update section.
- **Bug fix:** `install.sh` (Claude Code installer) had a leftover glob `kasidit-*` from before the v0.11 hook rename to `kasi-*`. Fresh installs were silently failing to copy hooks. Fixed.
- **No breaking changes** for existing Claude Code installs.
- **Cross-runtime Gravity hub sync** is deferred to v0.13. Today the two hubs (Claude Code at `~/.claude/skills/kasidit/center/`, thClaws at `~/.config/thclaws/skills/kasidit/center/`) are independent.

### v0.10.0 → v0.11.0 (this release)

- **6 new mission commands.** `/kasi-backend` (multi-mode backend router: fix · audit · scaffold · design · perf · security; auto-detects Laravel / Node), `/kasi-graph` (function call graph build/show/extract/impact/trace/cycles/dead with subgraph extraction), `/kasi-struc` (project state cache `.kasidit/STATE/` + auto-bridge so kasi-* read state, never rescan; incremental refresh via `git diff`), `/kasi-devopt` (DevOps mission — outputs deploy plan, env diff, data flow map, secrets audit, runbook scaffold; **never executes a deploy**), `/kasi-acknowledge` + `/kasi-knowledge-list` (capture last-performed steps as a structured runbook with auto-redaction; browse + step-by-step replay).
- **3 new default checklists.** `backend-laravel.md` (sections A–M + severity guide), `backend-node.md` (sections A–N), `backend-api-design.md` (stack-agnostic API rules). Total 12 → **15**.
- **4 new helper scripts.** `build_graph.{sh,py}` (regex MVP function call graph for PHP + JS/TS; ast-grep AST path stubbed for v0.12), `build_struc.{sh,py}` (state cache writer with full + incremental modes). `install.sh` extended (section 5b) to seed scripts dir.
- **File-path standardisation.** `kasidit-{route,verify,record,log,update-check,drift-check}.{py,sh}` → `kasi-*` via `git mv` (history preserved). Skill `kasidit-default` → `kasi-default`. `install.sh`, `test_hooks.py`, SKILL.md, README.md updated. **Retained intentionally** (would break protocol or existing JSONL stores): emit tokens `[kasidit-log|pattern|memory|rule|verify|record]`, brand prefix `[kasidit]`, env vars `KASIDIT_CENTER` / `KASIDIT_PROJECT_DIR` / `KASIDIT_LOG_DIR`, top-level skill/plugin/GitHub names. The parser regex in `kasi-record.py` accepts both `[kasi-X]` and `[kasidit-X]` for backward compatibility.
- **Honesty:** function call graph is regex-MVP (file-level call attribution shared across all fns in a file); per-fn-body extraction requires brace-tracking, deferred to ast-grep AST path in v0.12. Most kasi-* commands do not yet read `STATE/` — wiring is progressive. `/kasi-devopt` is AI-driven (no separate Python runner) — the command file documents the flow; the AI executes it via Read / Write / Bash tools.

### v0.9.2 → v0.10.0

- **Honesty Cleanup:** the prior `SKILL-full.md` split is reverted. Full Framework merges back into `SKILL.md` behind a prompt-level `/kasi off|router|lite|full|ultra` Mode gate. One file, mode-gated load depth.
- **Backend hooks** (runtime-enforced for the first time): `kasidit-route.py` (UserPromptSubmit classifier + memory query), `kasidit-verify.py` (PostToolUse + Stop confidence + orchestrator check), `kasidit-record.py` (Stop emit-line parser → JSONL stores), `kasidit-update-check.sh` (1×/day release tag check), `kasidit-drift-check.sh` (SessionStart Centerlite-sync reminder).
- **`audit-specialist`** consolidates `code-reviewer` + `security-auditor` + `perf-profiler` via `--focus=quality|security|perf|all`. Old agents kept as **name-resolution stubs** (no automatic mapping; users must invoke `audit-specialist --focus=` explicitly). Stubs disappear in v0.11. Active registry now **8 + 3 stubs**.
- **`install.sh`** canonical installer — copies hooks, merges `~/.claude/settings.json` (jq primary / python3 fallback, idempotent), seeds Gravity hub with 5 JSONL stores + 12 default checklists + 2 knowledge templates, writes `config.json`, manages `.last_sync` / `.last_update_check` stamps.
- **12 default checklists** seeded: PHP / Node / Python / Go × code-review / security / perf.
- **Incremental backend save** ("ออม") — AI emits `[kasidit-log|pattern|memory|rule]` lines at mission end; `kasidit-record.py` appends to matching JSONL. Router learns shortest successful route per mission kind over time.
- **`sudo <mission>`** clarified — parallel fan-out, **min 2 agents**, assumption-narrated pacing. **Not** a permission escalation. `/kasi-multi --fast` is an equivalent flag form.
- **Docs honesty:** `/kasi` precedence chain marked **spec, not runtime**. No code currently merges the three configs into a resolved value — applied by user + AI reading the files.

### v0.9.1 → v0.9.2

- **New pattern:** Gravity — a formalized two-tier knowledge layout. `~/.claude/skills/kasidit/center/` (Centerlite) + `<project>/.kasidit/` (Dcenterlite). Before this, the split existed implicitly (per-project `.kasidit/` plus a vague "user scope") but had no name, no sync commands, and no discipline about what belonged where.
- **New commands:** `/kasi-init`, `/kasi-promote`, `/kasi-pull`, `/kasi-sync`, `/kasi-wiki-sync`.
- **New hook:** `UserPromptSubmit` → `~/.claude/hooks/kasidit-log.sh` → writes every user prompt to `~/.claude/skills/kasidit/center/logs/YYYY-MM-DD.jsonl`. 200-line trim with head/tail preservation.
- **Permissions:** default allow-list expanded for common Kasidit bash / git / read patterns.
- **Docs:** a `docs/wiki/` source tree lands for the GitHub wiki (this page is part of it).

### v0.9.0 → v0.9.1

- Added **Master Orchestrator Rule** — the main agent is forbidden from executing strong work (multi-file changes, migrations, perf hunts, security audits, new features, deep research). It only narrows, dispatches, synthesizes.
- Added **7 specialist agents**: `bug-hunter`, `architect-planner`, `perf-profiler`, `test-writer`, `refactor-surgeon`, `deep-researcher`, `migration-specialist`. Plus the pre-existing `code-reviewer`, `security-auditor`, `legacy-specialist` = 10 total. *(In v0.10 this collapses to 8 + 3 stubs as the 3 audit agents merge into `audit-specialist`.)*
- **Dispatch brief format** standardized: `MISSION / INPUTS / CONSTRAINTS / EXPECTED OUTPUT / PRIOR CONTEXT`.
- The older Multi-Agent Orchestration section became an *implementation detail* of the master rule.

### v0.8.0 → v0.9.0

- Introduced **Design / Visual Mode.** Triggers: `mockup`, `wireframe`, `deck`, `slide`, `one-pager`, `landing page`, `pre-code sketch`, `ยังไม่ code`.
- **Rule 3 (Design before code)** now offers Claude Design prototypes for UI-touching missions instead of text diagrams.
- **UI Override Rule 1** adds "Claude Design mockup" as a third valid visual target (besides screenshot and raw CSS values).
- **New storage:** `.kasidit/prototypes/<mission-id>-{before,after}.png|url|pptx`.
- **DESIGN_SYSTEM.md** — visual counterpart to `PATTERNS.md`; records colors, spacing, typography, components extracted from the codebase.
- **Mockup → code handoff** with per-round token-level parity check (UI Override Rule 8).
- **Haiku rule:** never hand-code mockups. Always route to Claude Design.
- **New commands:** `design <what>`, `mockup <screen>`, `extract-system`, `parity <mockup-id>`, `report visual`.

### v0.7.4 → v0.8.0

- **Tier Cascade orchestration** — Opus plans, Sonnet works, Haiku greps. Before this, tier awareness existed (v0.3.0) but was per-session; v0.8.0 routed work across tiers within one mission.
- **Local embedding layer** — `sentence-transformers` over `.kasidit/knowledge/`; enables `/kasi-search` semantic queries without phoning home.
- `/kasi-cascade` command added.

### v0.3.0 → v0.7.4

- **Rule 2.3** — ban on analytical / theoretical / expected / projected metrics. Numbers must be measured before claimed. Prior versions tolerated "expected 10x speedup" language.
- **Rule 2.4** — every list of options must be numbered (1/2/3) so the user can reply by number instead of paraphrasing.
- **Rule 2.5** — reply in the user's native language. Thai user → Thai response (code/identifiers stay English).
- **Rule 2.6** — mandatory `git log --grep=<term>` and `git log -S <symbol>` before proposing a bug fix. Prior versions allowed skipping when the cause "seemed obvious".
- **Validation:** SWE-bench Lite sequential sample — 56/300 tasks, 60.7% strict PASS, 87.5% valid rate.

### v0.2.1 → v0.3.0

- **Model tier adaptation.** Before this, the skill was tier-blind — the same rules for Opus and Haiku. v0.3.0 tightens Haiku (no architecture decisions, checklist-driven only, confidence labels mandatory, verifier pass required) and loosens Opus (cross-file reasoning OK, architecture suggestions OK).
- **Confidence labels** — `[high / medium / low / unsure]`. `[unsure]` items are *always* listed separately for user decision, never silently guessed.
- **CHECKLISTS/** directory — pre-built mechanical audit lists per stack. This is "checklist does the thinking" — Haiku's biggest enabler.
- **PATTERNS.md** — project-specific patterns that AI **copies**, not reinvents.
- **Multi-agent orchestration** — split heavy missions (code review, refactor) across subagents for context isolation + parallelism.
- **Verifier pass** — mandatory on Haiku reviews. A second agent reads the first's findings and removes false positives.
- **Vague mission detection** — specific trigger words (check / review / audit / "ดูดี") force narrowing before work begins.
- **CSS width audit protocol** — grep-before-fix for UI work; no assuming selector scope.

### v0.2.0 → v0.2.1

- **Documentation retrieval protocol** — explicit trust hierarchy (project source > official docs at exact version > docs latest > framework source at release tag > release notes > blogs). No Stack Overflow / Medium / AI memory for version-specific syntax.
- **Version detection first** — `composer.json`, `package.json`, `go.mod`, `requirements.txt` read before coding.
- **Knowledge caching** at `.kasidit/knowledge/<stack>-<version>-<topic>.md`. Never cache whole pages — only the snippet that answered the question.

### v0.1.0 → v0.2.0

- **UI Override Mode** — for legacy CSS: scoped class + `!important`, cache-aware, one change per round. Does not refactor cascade.
- **Cache protocol** — every CSS/JS change bumps `?v=X`, user hard-refreshes, confirms new version loaded before evaluating the fix.
- **Domain detection** — splits backend / UI / review missions; each gets its own flow.
- **Override-first strategy** — when you can see the bug, override beats cascade audit.

## Upgrade path

Each version is backward-compatible with prior `.kasidit/` directories. Upgrading = re-enabling the plugin from the marketplace; old `.kasidit/` content remains valid. v0.9.2 adds `center/` at user scope — no project edits required.

The only behavior that changes silently on upgrade is the Centerlite prompt-log hook: if you installed the hook per the v0.9.2 instructions, every prompt from that point on is logged. Remove the `UserPromptSubmit` block from `~/.claude/settings.json` to opt out.
