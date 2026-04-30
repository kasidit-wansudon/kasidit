# Kasidit

> Mindful AI coding framework for Claude Code. Discipline over cleverness.
> Works on any model tier — compensates for weaker reasoning with structure.

**Site:** https://kasidit-wansudon.github.io/kasidit-site/
**Wiki:** https://github.com/kasidit-wansudon/kasidit/wiki
**Changelog:** [CHANGELOG.md](./CHANGELOG.md)

## What you get

- **21 slash commands** — mission (`/kasi-review · security · fix · ui · backend · graph · struc · devopt · acknowledge · knowledge-list · cascade`), project (`/kasi-init · scaffold · docs · status`), Gravity (`/kasi-promote · pull · sync`), semantic (`/kasi-search`), fan-out (`/kasi-multi`), wiki (`/kasi-wiki-sync`).
- **`/kasi` mode command** — pick intensity: `off / router / lite / full / ultra`.
- **8 specialist agents** — `architect-planner`, `audit-specialist` (`--focus=quality|security|perf`), `bug-hunter`, `deep-researcher`, `legacy-specialist`, `migration-specialist`, `refactor-surgeon`, `test-writer`.
- **Master Orchestrator** — main agent delegates; never executes strong work itself.
- **Runtime hooks** — prompt classifier, confidence-label verifier, backend-save recorder, update + drift check.
- **Gravity** — two-tier knowledge: Centerlite hub + per-project Dcenterlite, with promote / pull / sync.
- **15 default checklists** — security · code-review · perf · backend, across PHP / Node / Python / Go.
- **Tier-aware rules** — tighter discipline on Haiku, full framework on Opus.

## Install

```bash
# In Claude Code
/plugin marketplace add kasidit-wansudon/kasidit
/plugin install kasidit@kasidit
```

Or clone and run `bash plugins/kasidit/install.sh`.

## Core rules

1. **One mission.** Refuse vague scope; ask for narrowing.
2. **Design before code.** Show structure, ask, then build.
3. **Runtime is the judge.** Code looks right ≠ done.
4. **Confidence labels.** Tag every non-trivial finding `[high|medium|low|unsure]`.
5. **Master delegates.** Strong work goes to specialists; main never executes it.
6. **Tier-aware.** Weaker model = more scaffolding, not more guessing.

## Honesty

Mode gating, the Master Orchestrator Rule, and the core rules are **prompt-level conventions** — the AI self-applies them. The runtime hooks (`kasi-route.py`, `kasi-verify.py`, `kasi-record.py`, `kasi-update-check.sh`, `kasi-drift-check.sh`) are harness-enforced and run regardless of what the model decides.

## License

MIT.

## Author

[Kasidit Wansudon](https://github.com/kasidit-wansudon) — self-taught Thai engineer.
