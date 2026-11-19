# Kasidit

> **Stop fighting your AI. Give it discipline instead.**
> Mindful AI coding framework for Claude Code. Works the same on Opus, Sonnet, **and Haiku**.

[![release](https://img.shields.io/github/v/release/kasidit-wansudon/kasidit?style=flat-square&color=f59e0b)](https://github.com/kasidit-wansudon/kasidit/releases)
[![stars](https://img.shields.io/github/stars/kasidit-wansudon/kasidit?style=flat-square&color=fbbf24)](https://github.com/kasidit-wansudon/kasidit/stargazers)
[![license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](./LICENSE)

**Site:** [kasi web](https://kasi.kasion.dev/) · **Wiki:** [GitHub Wiki](https://github.com/kasidit-wansudon/kasidit/wiki) · **Changelog:** [CHANGELOG.md](./CHANGELOG.md)

---

## The problem

Your AI:

- confidently invents an API that doesn't exist,
- declares a fix "complete" without running the code,
- rewrites a working file because it "looked cleaner,"
- loops 40 minutes on a ghost bug.

These aren't model bugs. They're **discipline gaps** — AI lacks a grounded base, so it pattern-matches surface similarity and compounds errors.

The fix is not a bigger model. The fix is **scaffolding**: checklists, confidence labels, tier-aware rules, runtime verification, mission-driven scope.

## Why it's the best

| | Most prompt frameworks | Kasidit |
|---|---|---|
| Vague request like "review this" | proceeds and guesses | **refuses, demands narrowing** |
| AI claims `[high]` confidence | trusts it | **runtime hook downgrades it** if no Read/Bash call matches |
| Master agent spawns helpers, then edits files itself | nobody notices | **hook flags master-orchestrator violation** |
| Runs the same on Haiku as on Opus | "Haiku is too small" | **tier-aware rules — Haiku gets MORE scaffolding, not less** |
| Convention-only rules | model decides to ignore them | **7 runtime-enforced hooks** + 16 prompt-level rules |
| Your rules (reply language, style) fade after a long session or compact | AI drifts back to defaults | **`main.md` pinned rules** — re-sent every prompt, reply language checked before the turn ends |
| Knowledge resets every session | one-shot prompts | **Gravity hub** persists patterns / runbooks / route-memory across projects |
| One audit = one whole-repo grep | slow + noisy | **subgraph extraction** — scope to 10 functions, not 1000 |
| Deploy procedure forgotten | re-figure it next time | **`/kasi-acknowledge`** captures it as a replayable runbook |
| "Never let AI touch deploy" vs "just let it run anything" | pick one extreme | **`/kasi-deploy`** executes only on a fixed safe-platform table (typed confirm for prod); **`/kasi-review-deploy`** stays permanently read-only if you want zero execution risk |
| Approach unclear before a big change | AI just picks one and runs | **`/kasi-team`** — panel proposes options, **you** decide, then it dispatches |

**The real edge:** discipline turns Haiku into a senior engineer's executor. On Opus it unlocks depth. On Haiku it _replaces_ raw reasoning with checklists, verifier passes, and forced abstention. Same framework, every tier.

## Proof

- **87.5% valid fix rate on a SWE-bench Lite sample** (56/300 tasks, strict PASS 60.7%, v0.7.4)
- Production-tested on a **288K-line legacy PHP codebase**
- 7 runtime hooks. 27 slash commands. 8 specialist agents. 18 default checklists. 11 core rules — all enforced, not aspirational.

### Head-to-head benchmark (v0.17, 2026-11)

12 tasks (6 SWE-bench Lite + 6 SWE-bench Verified "1-4 hours"), scored with the official swebench Docker harness. Same prompt, same restricted permissions, each arm isolated from user config. Kasidit runs via `/kasi-fix`; [Superpowers](https://github.com/obra/superpowers) v7.0.2 self-activates via its hook.

| Resolved | Haiku | Fable | **Total (24)** | Cost | $ / resolved |
|---|---|---|---|---|---|
| **Kasidit** | **8/12** | 10/12 | **18/24 (75%)** | $37.18 | $2.07 |
| Superpowers | 6/12 | **11/12** | 17/24 (71%) | $44.07 | $2.59 |
| No framework | 6/12 | 9/12 | 15/24 (63%) | **$29.57** | **$1.97** |

- **Haiku:** Kasidit resolved the most *and* was the cheapest ($0.67 per resolved task vs $1.22 with no framework).
- **Fable:** Superpowers resolved the most; both frameworks cost more than no framework.
- **Caveats:** one run per arm; Kasidit vs Superpowers is a 1-task gap — a tie within noise. The clear signal is that both frameworks beat no framework on resolve rate.

## What you get

- **27 slash commands** — `/kasi-review · security · fix · ui · backend · graph · struc · devopt · deploy · review-deploy · diagram · acknowledge · knowledge-list · cascade · team · init · scaffold · docs · status · promote · pull · sync · search · multi · wiki-sync · main`
- **`/kasi` mode command** — pick intensity: `off / router / lite / full / ultra`
- **8 specialist agents** — `architect-planner`, `audit-specialist` (`--focus=quality|security|perf`), `bug-hunter`, `deep-researcher`, `legacy-specialist`, `migration-specialist`, `refactor-surgeon`, `test-writer`
- **7 runtime hooks** — prompt classifier, confidence-label verifier, backend-save recorder, update + drift check, pinned-rules injector + reply-language check
- **Pinned rules (`main.md`)** — your reply language and must-follow rules, re-sent every prompt; asks your language on first run
- **Master Orchestrator** — main agent delegates; never executes strong work itself
- **Gravity** — two-tier knowledge: Centerlite hub + per-project Dcenterlite, with promote / pull / sync
- **18 default checklists** — security · code-review · perf · backend across PHP / Node / Python / Go, plus domain checklists (money / datetime / locale) selected by what the mission touches
- **Tier-aware rules** — tighter discipline on Haiku, full framework on Opus

## Quick taste

```
> /kasi-fix the user export endpoint returns null on weekends

[kasidit] kind=bug-fix mode=lite history=12/14 avg_turns=2.1

Mission:    user export returns null on weekends
Hypothesis: timezone offset on the cutoff filter — Sat/Sun rolls into Mon
Fix:        app/Exports/UserExport.php:42 — use ->whereDate(..., $tz) not ->whereDay
Confidence: [medium] — pattern match, not yet runtime-verified
Verify:     curl /api/users/export?on=2026-04-26 → expect 142 rows
```

## Pinned rules — `main.md`

**The problem:** you write "reply in Thai" or "never commit without asking" in `CLAUDE.md`. It works for a while. Then the session gets long, or Claude compacts, and the AI quietly drifts back to its defaults. `CLAUDE.md` is loaded once at session start; nothing re-sends it.

**What Kasidit does:**

| When | Hook | What happens |
|---|---|---|
| Session start, resume, clear, **after compact** | `kasi-main.py` | Sends your whole `main.md` |
| **Every prompt** | `kasi-route.py` | Re-sends the reply-language rule + your `## Always` lines |
| Before the turn ends | `kasi-main-check.py` | If the reply contains a script foreign to your language, blocks it once and asks the AI to rewrite |

**First run asks your language.** After install, before doing anything else, the AI asks which language to reply in and saves it. Then it offers (optional) to import must-follow rules from your existing `CLAUDE.md` / `AGENTS.md`, and to add one rule of your own.

```markdown
---
reply_language: th          # set by onboarding; 18 languages supported
allow_scripts: chinese      # optional — let Chinese file names through
---
## Always                   # re-sent every prompt — keep it 3-7 lines
- One mission at a time; narrow vague requests before acting.
- Never commit without asking.

## Context                  # sent at session start + after compact
- Prefers tables over prose.
```

- Global file: `~/.claude/skills/kasidit/center/main.md`. Per project: `.kasidit/main.md` (merged on top).
- Manage it with `/kasi-main` — `show`, `language th`, `add <rule>`, `allow chinese`, `import`, `onboard`.
- The language check never blocks Latin text (code terms are English in every language), and ignores `code` and `> quoted` text.

**Honest limits:** re-sending a rule makes the AI *see* it every turn — it does not *force* compliance. Only the reply-language check is enforced, because only that can be checked by code. Keep `## Always` short: it costs tokens on every prompt (hard cap 1,200 characters).

## Install

```bash
# In Claude Code
/plugin marketplace add kasidit-wansudon/kasidit
/plugin install kasidit@kasidit
```

Or clone and run `bash plugins/kasidit/install.sh`.

### thClaws (v0.12+)

Kasidit also runs on [thClaws](https://github.com/thClaws/thClaws) — the native Rust agent harness:

```bash
git clone https://github.com/kasidit-wansudon/kasidit.git
cd kasidit
bash plugins/kasidit/install-thclaws.sh
```

~85% feature parity (4/5 hooks adapted to thClaws events; full SKILL.md + 25 commands + 8 agents + 18 checklists). See [docs/thclaws-setup.md](./docs/thclaws-setup.md) for hook event mapping and limitations.

## Update

Already installed? Pull the latest release:

```bash
# In Claude Code
/plugin marketplace update kasidit
```

Then re-run `bash plugins/kasidit/install.sh` (idempotent — safe to run again) to refresh hooks, settings.json, checklists, and scripts.

## Core rules

1. **One mission.** Refuse vague scope; demand narrowing.
2. **Design before code.** Show structure, ask, then build.
3. **Runtime is the judge.** Code _looks right_ ≠ done.
4. **Confidence labels.** No label = normal. Flag the exception only: `[unverified]` / `[assumed]` / `[unknown]`.
5. **Master delegates.** Strong work goes to specialists; main never executes it.
6. **Tier-aware.** Weaker model = more scaffolding, not more guessing.

(Full 11 rules + framework live in [SKILL.md](./plugins/kasidit/skills/kasidit/SKILL.md).)

## Honesty

The 11 core rules and Master Orchestrator are **prompt-level conventions** — the AI self-applies them. The 7 runtime hooks (`kasi-route.py`, `kasi-verify.py`, `kasi-record.py`, `kasi-update-check.sh`, `kasi-drift-check.sh`, `kasi-main.py`, `kasi-main-check.py`) are **harness-enforced** and run regardless of what the model decides.

`kasi-verify.py` and `kasi-record.py` run on the `Stop` event only — that's the only hook that carries `transcript_path`, which both hooks read to reconstruct the turn's assistant text and tool calls. (Prior to 2026-08-02, `kasi-verify.py` was also wired to `PostToolUse`, where it silently did nothing — that event never carries assistant text. Fixed; see `plugins/kasidit/hooks/test_hook_contract.py` for tests against the real payload shape, not an assumed one.) `kasi-verify.py` catches unverified `[unverified]`-worthy claims made without a matching tool call and flags master-orchestrator violations.

## License

MIT. Use freely, fork freely. Issues + PRs welcome at [kasidit-wansudon/kasidit/issues](https://github.com/kasidit-wansudon/kasidit/issues).

## Author

[Kasidit Wansudon](https://github.com/kasidit-wansudon) — self-taught Thai engineer.
Built through dogfooding on production legacy codebases.
