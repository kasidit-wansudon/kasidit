# Kasidit

> Mindful AI coding framework. Discipline over cleverness.
> Works on any model tier — compensates for weaker reasoning with external structure.

**Site:** https://kasidit-wansudon.github.io/kasidit-site/
**Wiki:** https://github.com/kasidit-wansudon/kasidit/wiki
**Changelog:** [CHANGELOG.md](./CHANGELOG.md)

Kasidit is a Claude Code plugin that forces AI coding assistants into disciplined, grounded workflows. It was built after watching senior-engineer-quality models still fabricate APIs, invent fixes, and loop on ghost bugs — not because the models were too small, but because they lacked **a grounded base**.

The fix is not a bigger model. The fix is scaffolding: checklists, confidence labels, tier-aware rules, runtime verification, and right-tool routing.

## Why it exists

AI coding fails for one root reason: **no grounded base**.

AI searches, guesses, believes what it reads, and compounds errors. Senior engineers reason from mental models of the real system; AI pattern-matches surface similarity. Kasidit enforces the discipline that bridges this gap.

- One mission. One focus. One step.
- Design before code.
- Runtime is the judge, not self-report.
- Point, do not explain. Explanation breeds hallucination.
- Weaker model → more scaffolding, not more guessing.
- For visual work, use Claude Design — not hand-coded HTML mockups.

## What you get

- **1 skill** (`kasidit`) — the core framework, auto-triggered on coding tasks.
- **15 slash commands** — mission (`/kasi-review`, `/kasi-security`, `/kasi-fix`, `/kasi-ui`, `/kasi-cascade`), project (`/kasi-init`, `/kasi-scaffold`, `/kasi-docs`, `/kasi-status`), Gravity (`/kasi-promote`, `/kasi-pull`, `/kasi-sync`), semantic (`/kasi-search`), meta (`/kasi-wiki-sync`), and fan-out (`/kasi-multi`).
- **`sudo <mission>` shorthand** — parallel fan-out to 6 specialists with assumption-narrated pacing (v0.9.2).
- **10 specialist agents** — `architect-planner`, `bug-hunter`, `code-reviewer`, `deep-researcher`, `legacy-specialist`, `migration-specialist`, `perf-profiler`, `refactor-surgeon`, `security-auditor`, `test-writer`.
- **Master Orchestrator Rule** (v0.9.1) — main agent delegates strong work; never executes it itself.
- **Gravity Pattern** (v0.9.2) — two-tier knowledge: Centerlite hub (`~/.claude/skills/kasidit/center/`) + Dcenterlite project (`.kasidit/`), with promote / pull / sync commands.
- **Global prompt log** (v0.9.2) — `UserPromptSubmit` hook writes to `~/.claude/skills/kasidit/center/logs/*.jsonl`, 200-line trim.
- **14 checklists** — mechanical audit lists for security, performance, framework-specific work.
- **Tier-aware rules** — tighter discipline on Haiku, full framework on Opus.
- **Claude Design integration (v0.9)** — routes mockup / wireframe / deck work to the right tool.
- **Local embedding layer** (v0.8) — scoped knowledge at `.kasidit/knowledge/` (sentence-transformers).
- **Tier Cascade orchestration** (v0.8) — Opus plans, Sonnet works, Haiku greps.

## Install

### Via Claude Code plugin marketplace (recommended)

```bash
/plugin marketplace add kasidit-wansudon/kasidit
/plugin install kasidit@kasidit
```

Update later with:

```bash
/plugin marketplace update kasidit
```

### Manual install (advanced)

```bash
git clone https://github.com/kasidit-wansudon/kasidit.git
cp -r kasidit/plugins/kasidit/skills/kasidit ~/.claude/skills/kasidit
cp -r kasidit/plugins/kasidit/commands/* ~/.claude/commands/
cp -r kasidit/plugins/kasidit/agents/* ~/.claude/agents/
```

## Evidence (honest numbers)

Tested against a sequential sample of 56 SWE-bench Lite tasks (of 300), line-match scoring:

| Metric | Result |
| :--- | :--- |
| PASS (strict line-match) | 34/56 (60.7%) |
| PARTIAL | 15/56 (27%) |
| FAIL | 7/56 (12.5%) |
| Valid fix rate (PASS + PARTIAL) | 49/56 (87.5%) |
| Infra errors | 1 timeout |

**Comparison caveat:** published benchmarks use different sampling, different scoring, and often Verified vs Lite splits. This is not apples-to-apples against Copilot (GPT-4o) 72.5% SWE-bench Verified or Claude Code Opus (no Kasidit) 80.8% real test. Reported here for transparency, not as a competitive claim.

Smaller earlier tests:
- 15 curated tasks: 8/15 PASS strict (53%), 15/15 valid (100%), 0 FAIL.
- 7 curated tasks (Opus): 6/7 PASS (86%), 7/7 valid (100%).
- 7 curated tasks (Haiku v0.7.4): 3/7 PASS (43%), 5/7 valid (71%).

Full run (remaining 244 tasks) is scheduled.

## Core rules

Kasidit enforces 13 core rules plus 6 sub-rules. The most load-bearing:

1. **Mission-driven** — one mission per session, vague missions refused.
2. **Minimal requirement** — narrowest interpretation. No uninvited refactor.
3. **Design before code** — show the design, wait for confirmation, then implement.
4. **Official documentation only** — no memory-based coding on libraries.
5. **Check environment before generating code** — match project versions, not latest.
6. **Step one by one** — verify before moving on.
7. **Explain = Hallucinate** — terse output, points not paragraphs.
8. **Runtime is the judge** — execution confirms, not self-report.
9. **Problem is in data, not in UI** (unless visual proves otherwise).
10. **Confidence labels** — `[high|medium|low|unsure]` on every non-trivial finding.
11. **Tier Cascade** — Opus plans, Sonnet works, Haiku greps.

Sub-rules:
- 2.3 No fake metrics. No "expected/projected/theoretical" labels.
- 2.4 Number all options when asking (1/2/3).
- 2.5 Native language (Thai user → Thai reply).
- 2.6 `git log --grep` + `git log -S` before fixing bugs.

See [`plugins/kasidit/skills/kasidit/SKILL.md`](./plugins/kasidit/skills/kasidit/SKILL.md) for the full framework.

## Commands

### Mission

| Command | Use |
| :--- | :--- |
| `/kasi-review` | Code review with confidence labels. |
| `/kasi-security` | Security audit with checklist-driven scan. |
| `/kasi-fix` | Mission-scoped bug fix with mandatory `git log --grep` / `-S` protocol. |
| `/kasi-ui` | UI Override Mode (scoped class + `!important`). |
| `/kasi-cascade` | Tier Cascade orchestration — Opus plans, Sonnet works, Haiku greps. |
| `/kasi-multi [N] [mission]` | Fan-out to N specialists in parallel (default N=6). |
| `sudo <mission>` | Shorthand for `/kasi-multi 6 <mission>` with skip-clarifying pacing. |

### Project

| Command | Use |
| :--- | :--- |
| `/kasi-init` | One-shot bootstrap: scaffold → pull → docs → MISSION → review → auto-invoke. |
| `/kasi-scaffold` | Build `.kasidit/` (INDEX / RELATIONS / MEMORY / PATTERNS / CHECKLISTS / knowledge). |
| `/kasi-docs` | Fetch + cache version-matched official docs. |
| `/kasi-status` | Show current mission, counter, pending items. |

### Gravity (v0.9.2)

| Command | Use |
| :--- | :--- |
| `/kasi-promote <type> <name>` | Lift pattern / checklist / knowledge from `.kasidit/` into Centerlite hub. |
| `/kasi-pull <type> <name>` | Fetch item from Centerlite into current `.kasidit/`. |
| `/kasi-sync` | Audit drift between local and hub. Read-only. |

### Semantic + Meta

| Command | Use |
| :--- | :--- |
| `/kasi-search "<query>"` | Semantic search over `.kasidit/knowledge/` via local embeddings. |
| `/kasi-wiki-sync [apply]` | Push `docs/wiki/*` to the GitHub wiki (dry-run by default). |

## Claude Design integration (v0.9)

Visual work routes to Claude Design — mockups, wireframes, pitch decks, one-pagers, landing pages. Kasidit handles the code that implements the visual; Claude Design handles the visual itself. See the "Claude Design Integration" section in SKILL.md for routing rules.

## Platforms

Kasidit works with:
- Claude Code (primary, this repo).
- Cursor (via `.cursor/rules/` mirror — in progress).
- Windsurf (via `.windsurfrules` — in progress).
- GitHub Copilot (via system prompt snippet — in progress).

## Philosophy

> AI coding fails not because models are too small,
> but because they lack a grounded base.

The fix is discipline:
- Discipline in scope (one mission).
- Discipline in verification (runtime judges).
- Discipline in output (point, not paragraph).
- Discipline in failure (escalate, do not spiral).
- Discipline in uncertainty (label, do not guess).
- Discipline in tool choice (Claude Design for visuals, Kasidit for code).

When AI follows discipline, it amplifies a senior engineer. Without discipline, it replaces them with hallucination.

**On Opus, discipline unlocks depth. On Haiku, discipline IS the reasoning.**

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).

## License

MIT. See [LICENSE](./LICENSE).

## Author

Kasidit Wansudon — self-taught Thai engineer.
Site: https://kasidit-wansudon.github.io/kasidit-site/
Email: kasidit.wans@gmail.com

---

Contributions welcome. Issues and PRs at [github.com/kasidit-wansudon/kasidit](https://github.com/kasidit-wansudon/kasidit).
