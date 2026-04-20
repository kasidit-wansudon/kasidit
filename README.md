# Kasidit

> Mindful AI coding framework. Discipline over cleverness.
> Works on any model tier — compensates for weaker reasoning with external structure.

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
- **9 slash commands** — `/kasi-review`, `/kasi-security`, `/kasi-scaffold`, `/kasi-fix`, `/kasi-ui`, `/kasi-docs`, `/kasi-status`, `/kasi-search`, `/kasi-cascade`.
- **3 agents** — `security-auditor`, `code-reviewer`, `legacy-specialist`.
- **14 checklists** — mechanical audit lists for security, performance, and framework-specific work.
- **Tier-aware rules** — tighter discipline on Haiku, full framework on Opus.
- **Claude Design integration (v0.9)** — routes mockup/wireframe/deck work to the right tool.
- **Local embedding layer** — scoped knowledge at `.kasidit/knowledge/` (sentence-transformers).
- **Tier Cascade orchestration** — Opus plans, Sonnet works, Haiku greps.

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

| Command | Use |
| :--- | :--- |
| `/kasi-review` | Code review with confidence labels. |
| `/kasi-security` | Security audit with checklist-driven scan. |
| `/kasi-scaffold` | Scaffold `.kasidit/` structure (INDEX / RELATIONS / PATTERNS / CHECKLISTS). |
| `/kasi-fix` | Mission-scoped bug fix with git log protocol. |
| `/kasi-ui` | UI Override Mode (scoped class + !important). |
| `/kasi-docs` | Fetch + cache version-matched official docs. |
| `/kasi-status` | Show current mission, counter, pending items. |
| `/kasi-search` | Scope-limited grep inside `.kasidit/knowledge/`. |
| `/kasi-cascade` | Tier Cascade orchestration — plan/work/grep split. |

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
Web: [kasidit.ai](https://kasidit.ai) (pending launch).
Email: kasidit.wans@gmail.com

---

Contributions welcome. Issues and PRs at [github.com/kasidit-wansudon/kasidit](https://github.com/kasidit-wansudon/kasidit).
