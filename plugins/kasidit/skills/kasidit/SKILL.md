---
name: kasidit
description: Mindful AI coding discipline framework. Activate ONLY when user invokes /kasi-* command, explicitly requests code review / security audit / migration plan / legacy refactor, complains the AI is hallucinating or looping on ghost bugs, or asks for disciplined / checklist-driven work. Do NOT auto-trigger on routine coding edits, trivial bug fixes, or single-file changes — those should run without the framework loaded. Also routes UI mockup / prototype / pitch deck / visual design requests through Claude Design instead of hand-coding markup. Mode-gated: respects `/kasi off|router|lite|full|ultra` session state and project `.kasidit/config.json`.
---

# Kasidit — Mindful AI Coding Framework

**Framework version: v0.17.0** (2026-10-13 — `/kasi-diagram`: soft bridge to Archify, selectable diagram language). See [CHANGELOG.md](https://github.com/kasidit-wansudon/kasidit/blob/main/CHANGELOG.md) for the full history. Inline `(vX.Y)` tags on individual rules/commands below mark when that specific piece was introduced — they are not the file's current version; the line above is the single source of truth for that.

## Router Mode (default)

> Thin classifier. Keep guardrails on, escalate only when the work needs it.

In router / lite mode, only this file is "live" — the reference files below are loaded on demand, not by default. Router does three things:

1. Classify each user message into a mission kind.
2. Recommend a mode (`off` / `router` / `lite` / `full` / `ultra`).
3. Keep two always-on guardrails: **Rule 1 (mission-driven)** and **Rule 11 (confidence labels)**.

### Rule 1 — Mission-driven (always on)

Every session has **one mission**. If the user's request is vague or multi-part, narrow it first. Never start coding on "improve this" or "check the project".

Vague keywords that must be refused with numbered options:

- `check`, `review`, `audit`, `look at`
- `ดูดี`, `สวย`, `เหมาะสม`, `ปรับ`, `เพี้ยน`, `แปลก`, `ไม่ตรง`
- `improve`, `better`, `fix`, `optimize`, `all`, `every`, `entire`, `whole`

On these, output numbered options (Rule 2.4 style) and wait for a number. Applies in every mode except `off`.

### Rule 11 — Confidence labels (always on)

**No label = normal, default state.** Labels exist to flag the exception — the moment you have NOT verified something the reader would assume you had. A label on every line teaches the reader to ignore all of them.

Use a label only when it's true and the exception applies:

- `[unverified]` — plausible, but not run and not read from source.
- `[assumed]` — inferred from a name/comment, not from observed behavior.
- `[unknown]` — you don't know; the user must decide.

**`[high]` is retired.** Self-issued confidence grades don't add information — they tell the reader "trust me," which has already failed in practice (a `[high]` label was issued on logic that later scored 12/26 on real tests). If a claim is genuinely runtime-verified, say what verified it instead of grading it: `verified: pytest tests/auth_test.py -k injection passes`. The `kasi-verify.py` Stop hook checks that the cited command was actually run in the transcript, not that a label was typed.

**Never silently guess.** `[unknown]` items go in a separate list for user decision.

### Router classification triggers

Word-boundary match (first hit wins, dict-insert order). Keywords exactly as implemented in `kasi-route.py:KEYWORDS`:

| Keywords in message | kind | Recommended mode |
|---|---|---|
| `security`, `owasp`, `cve` | security-audit | `ultra` |
| `migration` | migration | `ultra` |
| `audit` | audit | `full` |
| `review` | review | `full` |
| `refactor` | refactor | `full` |
| `perf`, `n+1` | perf | `full` |
| `bug`, `fix`, `error` | bug-fix | `lite` |
| `slow` | perf | `lite` |
| `ui`, `css`, `layout` | ui | `lite` |
| `rename` | refactor-rename | `router` |
| `question`, `explain`, `what is` | question | `router` |
| `how do i` | question | `lite` |
| no match | unclassified | (silent — router stays default) |

Thai / extended phrases (e.g. `auth boundary`, `เพี้ยน`, `check the project`) are **not** matched by the `kasi-route.py` `KEYWORDS` dict as of v0.14.0 — add them there if you want hook-level routing (the LLM still narrows them per Rule 1).

When `kasi-route.py` runs on `UserPromptSubmit`, it prepends 1 line to the turn:

```
[kasidit] kind=<kind> mode=<recommended> history=<n_pass>/<n_total> avg_turns=<x>
```

If history shows a lighter mode succeeded for this kind, recommend the lighter mode.

### When router escalates

Router itself never writes code or reads source files beyond `.kasidit/` index files. On escalation, read the relevant reference file(s) below — do not assume their content, read them:

- `/kasi-*` heavy commands (init, scaffold, docs, review, security, fix, ui, multi, cascade, team) → read `references/full.md` (Model Tier, Core Principles, Mission Counter, Domain Detection, Workflow, Communication Style, Examples, Anti-patterns, Project Init, User Commands, Philosophy, Version history).
- Explicit `/kasi full` / `/kasi ultra` → `references/full.md` active for the session.
- Multi-file refactor / audit / review → `references/full.md`.
- Delegation to specialist agents, Team Mode, or fan-out → `references/agents.md` (Master Orchestrator Rule, Team Mode, Multi-Agent Orchestration, Multi-Agent Fan-Out).
- Cross-session/cross-project memory, patterns, or the running mission index → `references/gravity.md` (สารบัญ System, Gravity Pattern, Global Prompt Log).
- UI mockup, visual design, or CSS/layout work → `references/ui.md` (UI Override Mode, Claude Design Integration).
- Interactive architecture / sequence / data-flow diagram → `/kasi-diagram` (soft bridge to Archify; text diagram if not installed).

Domain checklists (money / datetime / locale) live in `defaults/checklists/correctness-*.md` — see `references/full.md` § CHECKLISTS/ for the selection rule.

### Stop phrases

- `stop kasidit` — disable for rest of session.
- `normal mode` — synonym.
- `/kasi off` — explicit.
