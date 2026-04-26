# Version History

Side-by-side comparison. Detailed per-version notes live on each release page.

| Version | Date | Theme | Headline change |
|---|---|---|---|
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

### v0.9.1 → v0.9.2 (this release)

- **New pattern:** Gravity — a formalized two-tier knowledge layout. `~/.claude/skills/kasidit/center/` (Centerlite) + `<project>/.kasidit/` (Dcenterlite). Before this, the split existed implicitly (per-project `.kasidit/` plus a vague "user scope") but had no name, no sync commands, and no discipline about what belonged where.
- **New commands:** `/kasi-init`, `/kasi-promote`, `/kasi-pull`, `/kasi-sync`, `/kasi-wiki-sync`.
- **New hook:** `UserPromptSubmit` → `~/.claude/hooks/kasidit-log.sh` → writes every user prompt to `~/.claude/skills/kasidit/center/logs/YYYY-MM-DD.jsonl`. 200-line trim with head/tail preservation.
- **Permissions:** default allow-list expanded for common Kasidit bash / git / read patterns.
- **Docs:** a `docs/wiki/` source tree lands for the GitHub wiki (this page is part of it).

### v0.9.0 → v0.9.1

- Added **Master Orchestrator Rule** — the main agent is forbidden from executing strong work (multi-file changes, migrations, perf hunts, security audits, new features, deep research). It only narrows, dispatches, synthesizes.
- Added **7 specialist agents**: `bug-hunter`, `architect-planner`, `perf-profiler`, `test-writer`, `refactor-surgeon`, `deep-researcher`, `migration-specialist`. Plus the pre-existing `code-reviewer`, `security-auditor`, `legacy-specialist` = 10 total.
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
