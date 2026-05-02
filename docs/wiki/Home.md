# Kasidit Wiki

> **Mindful AI coding framework. Discipline over cleverness. Works on any model tier.**

Kasidit is a Claude Code plugin that makes AI coding grounded instead of hallucinated. It scaffolds the discipline a senior engineer carries in their head — mission narrowing, design-before-code, runtime-as-judge, confidence labels, checklists, and tier-aware behavior — into an operational framework any model can follow.

## Start here

- [[Installation]] — install the plugin, run the v0.10 backend installer, init a project.
- [[Getting Started]] — your first mission in under 5 minutes.
- [[Commands]] — full reference for every command (Mode + missions + Gravity).
- [[Kasi-Mode]] — `/kasi off|router|lite|full|ultra` (v0.10).
- [[Backend-Hooks]] — runtime hooks (v0.10).
- [[Gravity Pattern]] — two-tier knowledge system (Centerlite + Dcenterlite).
- [[Model Tiers]] — what changes on Opus vs Sonnet vs Haiku.
- [[FAQ]] — common questions.

## Community

- 🐛 [Issues](https://github.com/kasidit-wansudon/kasidit/issues) — defect reports (use the bug template)
- 💬 [Discussions](https://github.com/kasidit-wansudon/kasidit/discussions) — Q&A, ideas, show & tell, announcements ([[Discussions]] page explains the categories)
- 🔒 [SECURITY.md](https://github.com/kasidit-wansudon/kasidit/blob/main/SECURITY.md) — private channel for vulnerabilities
- 📜 [CONTRIBUTING.md](https://github.com/kasidit-wansudon/kasidit/blob/main/CONTRIBUTING.md) — how to send a PR
- 📝 [Code of Conduct](https://github.com/kasidit-wansudon/kasidit/blob/main/CODE_OF_CONDUCT.md)

## Version history

Deep per-release notes, in descending order:

- [[v0.12.0]] — **thClaws Runtime Support.** Kasidit now runs on both Claude Code and [thClaws](https://github.com/thClaws/thClaws). New `install-thclaws.sh`, mirrored `.thclaws-plugin/` manifests, hook event mapping (4/5 hooks adapted), `docs/thclaws-setup.md`. ~85% feature parity on thClaws.
- [[v0.11.0]] — **Backend Mission Router + Structure Bridge + Runbook Capture.** 6 new commands (`/kasi-backend`, `/kasi-graph`, `/kasi-struc`, `/kasi-devopt`, `/kasi-acknowledge`, `/kasi-knowledge-list`), 3 new backend checklists (Laravel · Node · API design), 4 helper scripts (function call graph + state cache writers). Hooks renamed `kasidit-*` → `kasi-*` (history preserved; emit-token protocol kept).
- [[v0.10.0]] — **Honesty Cleanup.** SKILL-full split reverted (Mode-gated single file), `audit-specialist` consolidates code-reviewer/security-auditor/perf-profiler, runtime backend hooks (route/verify/record/update/drift), `install.sh` canonical installer, 12 default checklists, incremental backend save (`route-memory.jsonl`).
- [[v0.9.2]] — **Gravity Pattern.** Two-tier knowledge (Centerlite + Dcenterlite), global prompt log, `/kasi-init`, promote/pull/sync commands, wiki sync.
- [[v0.9.1]] — **Master Orchestrator Rule.** 7 specialist agents; master delegates all strong work.
- [[v0.9.0]] — **Claude Design Integration.** Route visual missions to Claude Design; stop hand-coding mockups.
- [[v0.8.0]] — **Tier Cascade orchestration** + local embedding knowledge layer.
- [[v0.7.4]] — **SWE-bench validation** + Rules 2.3–2.6 (no fake metrics, numbered options, native language, mandatory git-log on bug fix).
- [[v0.3.0]] — **Model tier adaptation**, confidence labels, CHECKLISTS/, PATTERNS.md, multi-agent orchestration, verifier pass.
- [[v0.2.1]] — **Documentation retrieval protocol** (trust hierarchy, version-matched docs, knowledge caching).
- [[v0.2.0]] — **UI Override Mode** + cache protocol + domain detection.
- [[v0.1.0]] — **Core principles**, mission counter, สารบัญ (index) system.

See [[Version History]] for a side-by-side comparison table.

## Why Kasidit exists

> AI coding fails not because models are too small,
> but because they lack a grounded base.

The fix is not a bigger model — it is **discipline** externalized into files, checklists, and commands. Kasidit provides that scaffold.

## License + source

- Repository: https://github.com/kasidit-wansudon/kasidit
- License: MIT
- Author: Kasidit Wansudon (Thailand)
