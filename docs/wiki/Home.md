# Kasidit Wiki

> **Mindful AI coding framework. Discipline over cleverness. Works on any model tier.**

Kasidit is a Claude Code plugin that makes AI coding grounded instead of hallucinated. It scaffolds the discipline a senior engineer carries in their head — mission narrowing, design-before-code, runtime-as-judge, confidence labels, checklists, and tier-aware behavior — into an operational framework any model can follow.

## Start here

- [[Installation]] — install the plugin, verify the log hook, init a project.
- [[Getting Started]] — your first mission in under 5 minutes.
- [[Commands]] — full reference for every `/kasi-*` command.
- [[Gravity Pattern]] — the v0.9.2 two-tier knowledge system (Centerlite + Dcenterlite).
- [[Model Tiers]] — what changes on Opus vs Sonnet vs Haiku.
- [[FAQ]] — common questions.

## Version history

Deep per-release notes, in descending order:

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
