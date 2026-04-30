# Kasidit

> Mindful AI coding framework. Discipline over cleverness.
> Works on any model tier — compensates for weaker reasoning with external structure.

**Site:** https://kasidit-wansudon.github.io/kasidit-site/
**Wiki:** https://github.com/kasidit-wansudon/kasidit/wiki
**Changelog:** [CHANGELOG.md](./CHANGELOG.md)
**ภาษาไทย:** [อ่านสรุปภาษาไทย](#-สรุปภาษาไทย-thai-summary) ↓

Kasidit is a Claude Code plugin that forces AI coding assistants into disciplined, grounded workflows. It was built after watching senior-engineer-quality models still fabricate APIs, invent fixes, and loop on ghost bugs — not because the models were too small, but because they lacked **a grounded base**.

The fix is not a bigger model. The fix is scaffolding: checklists, confidence labels, tier-aware rules, runtime verification, and right-tool routing.

---

## 🇹🇭 สรุปภาษาไทย (Thai Summary)

> **Kasidit** = framework สำหรับให้ AI โค้ดอย่างมีวินัย ใช้กับ Claude Code

### ปัญหาที่แก้

AI โค้ดเก่งแต่หลอก:
- เรียก function ที่ไม่มีจริง
- บอกว่า fix แล้วทั้งที่ยังพัง
- วน loop debug bug เดิม
- รุ่นเล็ก (Haiku) ยิ่งหลอกหนัก

ปัญหาไม่ใช่ "AI โง่" — แต่ "AI ไม่มี discipline". Senior dev เก่งเพราะ process ไม่ใช่ IQ. Kasidit บังคับ process เดียวกันให้ AI

### หลักการ 6 ข้อ

- **1 mission, 1 focus, 1 step** — ห้ามทำหลายเรื่องพร้อมกัน
- **Design ก่อน code** — ห้าม dive ตรง implementation
- **Runtime is judge** — ไม่เชื่อที่ AI ว่าตัวเอง ต้องรันจริง
- **Point ไม่ Explain** — Explanation บ่อย = hallucination เริ่ม
- **Tier-aware** — รุ่นเล็กยิ่งใช้ scaffolding หนัก
- **งาน visual ใช้ Claude Design** — ไม่ใช่ hand-code HTML

### มีอะไรบ้าง (v0.10.0)

- **1 skill** (`kasidit`) — auto-trigger ตอนโค้ด
- **`/kasi` Mode command** (v0.10) — เลือกความเข้ม: `off` / `router` / `lite` / `full` / `ultra`
- **15 slash commands** — mission, project, Gravity, semantic, meta, fan-out
- **8 specialist agents** (v0.10 ลด: รวม code-reviewer + security-auditor + perf-profiler → audit-specialist)
- **Backend hooks** (v0.10) — runtime classifier + verifier + recorder + update/drift checks
- **12 default checklists** — security/code-review/perf สำหรับ PHP / Node / Python / Go
- **Master Orchestrator** — main delegate ไม่ทำงานหนักเอง
- **Gravity Pattern** — knowledge 2 ชั้น: hub กลาง + project orbit
- **Tier Cascade** — Opus คิด → Sonnet ทำ → Haiku grep

### ติดตั้ง

**Plugin marketplace (แนะนำ):**
```
/plugin marketplace add kasidit-wansudon/kasidit
/plugin install kasidit@kasidit
```

**install.sh (ครบสุด — มี hooks + Gravity hub seed + settings merge):**
```
git clone https://github.com/kasidit-wansudon/kasidit.git
cd kasidit
./install.sh
```

อัปเดต:
```
/plugin marketplace update kasidit
```

### ผลทดสอบ (ตรงไปตรงมา)

SWE-bench Lite (sample 56/300):
- PASS (line-match เข้ม): **60.7%** (34/56)
- PARTIAL (fix ใช้ได้แต่ไม่ตรง line): **27%**
- Valid fix rate รวม: **87.5%**

**หมายเหตุ:** คนละ scoring กับเลขที่ Anthropic/GitHub โพสต์ ไม่ได้เปรียบเทียบกับ Copilot (GPT-4o) 72.5% SWE-bench Verified หรือ Claude Code Opus base 80.8%. ตัวเลขนี้แค่ baseline ของ framework — รายงานเพื่อโปร่งใส ไม่ใช่ marketing claim. Full run (244 task ที่เหลือ) scheduled อยู่

### ใครเหมาะ

- Solo dev / Freelance ที่ใช้ Claude Code อยู่แล้ว
- ทีม dev ที่อยาก standardize การใช้ AI
- คนที่ใช้ Haiku/Sonnet เพื่อประหยัด แต่อยากได้ output คุณภาพ
- คนที่เบื่อ AI หลอก แล้วต้องตามแก้

### License

MIT — ใช้ฟรี fork ได้ ไม่ต้อง credit

### Feedback

เปิด issue ที่ https://github.com/kasidit-wansudon/kasidit/issues หรือ email kasidit.wans@gmail.com

---

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
- **`/kasi` Mode command** (v0.10) — select framework intensity: `off` / `router` / `lite` / `full` / `ultra`. Default = `router`. Mode gating is a prompt-level convention — see the Honesty section below.
- **15 slash commands** — mission (`/kasi-review`, `/kasi-security`, `/kasi-fix`, `/kasi-ui`, `/kasi-cascade`), project (`/kasi-init`, `/kasi-scaffold`, `/kasi-docs`, `/kasi-status`), Gravity (`/kasi-promote`, `/kasi-pull`, `/kasi-sync`), semantic (`/kasi-search`), meta (`/kasi-wiki-sync`), and fan-out (`/kasi-multi`).
- **Backend hooks** (v0.10, runtime-enforced) — `kasi-route.py` (prompt classifier + memory query on `UserPromptSubmit`), `kasi-verify.py` (confidence-label + orchestrator-violation check on `PostToolUse` and `Stop`), `kasi-record.py` (parses `[kasidit-log|pattern|memory|rule]` emit lines into JSONL on `Stop`), `kasi-update-check.sh` (1×/day release-tag check on `SessionStart`), `kasi-drift-check.sh` (Centerlite-sync reminder on `SessionStart`).
- **Incremental backend save** (v0.10) — AI emits `[kasidit-log] kind=... mode=... turns=... outcome=...` lines at mission end; router learns shortest successful route per mission kind over time.
- **`sudo <mission>` shorthand** — parallel fan-out, min 2 agents, assumption-narrated pacing. Session-only speed shortcut, **not** a permission escalation. `/kasi-multi --fast` is an equivalent alternative (v0.10).
- **8 specialist agents** — `architect-planner`, `audit-specialist` (merged `code-reviewer` / `security-auditor` / `perf-profiler` via `--focus=quality|security|perf|all`, v0.10), `bug-hunter`, `deep-researcher`, `legacy-specialist`, `migration-specialist`, `refactor-surgeon`, `test-writer`. Old agent files kept as thin stubs for name resolution; removed in v0.11.
- **Master Orchestrator Rule** (v0.9.1) — main agent delegates strong work; never executes it itself.
- **Gravity Pattern** (v0.9.2) — two-tier knowledge: Centerlite hub (`~/.claude/skills/kasidit/center/`) + Dcenterlite project (`.kasidit/`), with promote / pull / sync commands.
- **Global prompt log** (v0.9.2) — `UserPromptSubmit` hook writes to `~/.claude/skills/kasidit/center/logs/*.jsonl`, 200-line trim.
- **12 default checklists** (v0.10) — `defaults/checklists/` ships security / code-review / perf lists for PHP, Node, Python, Go (4 stacks × 3 lenses). Seeded into `~/.claude/skills/kasidit/center/checklists/` at install time.
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

### Via `install.sh` (canonical for hooks + settings merge)

`install.sh` is the recommended flow if you want the v0.10 backend hooks, the Gravity hub seed, and the permission allow-list merged into `~/.claude/settings.json`. Idempotent — safe to re-run.

```bash
git clone https://github.com/kasidit-wansudon/kasidit.git
cd kasidit
./install.sh
```

It will:

- copy hooks into `~/.claude/hooks/`
- merge `~/.claude/settings.json` (via `jq`, with `python3` stdlib fallback)
- seed the Gravity hub under `~/.claude/skills/kasidit/center/` with 5 JSONL files
- install default checklists for PHP / Node / Python / Go

### Manual `cp` (debugging only)

Use this if `install.sh` fails or you need to inspect individual pieces:

```bash
git clone https://github.com/kasidit-wansudon/kasidit.git
cp -r kasidit/plugins/kasidit/skills/kasidit ~/.claude/skills/kasidit
cp -r kasidit/plugins/kasidit/commands/* ~/.claude/commands/
cp -r kasidit/plugins/kasidit/agents/* ~/.claude/agents/
cp -r kasidit/plugins/kasidit/hooks/* ~/.claude/hooks/
```

Manual copy does **not** merge `settings.json` or seed the Gravity hub — hooks won't fire without those.

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

Kasidit enforces 11 core rules plus 4 sub-rules. The most load-bearing:

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

## Honesty — enforced vs. convention

Kasidit is part runtime-enforced (hooks), part prompt-level convention (discipline the AI self-applies). Being clear about which is which:

- **Runtime-enforced (hooks):** `kasi-route.py` (`UserPromptSubmit`), `kasi-verify.py` (`PostToolUse`), `kasi-record.py` (`Stop`), and `kasi-update-check.sh`. These run in the Claude Code harness regardless of what the model decides. They classify prompts, cross-check confidence labels, flag master-orchestrator violations, and append JSONL emit lines to the Gravity hub.
- **Convention (prompt-level):** Mode gating (`off` / `router` / `lite` / `full` / `ultra`) is a section in `SKILL.md` the AI reads and self-applies. The harness does not enforce mode boundaries. A model can in principle ignore the declared mode — discipline comes from the prompt, not a runtime sandbox.
- **Convention (prompt-level):** Master Orchestrator Rule, Tier Cascade routing, and the 11 core rules live in `SKILL.md`. `kasi-verify.py` flags some orchestrator violations after the fact, but the rules themselves are AI-applied, not harness-applied.
- **No auto-remap:** the router does not silently rewrite old agent names (`code-reviewer`, `security-auditor`, `perf-profiler`) to `audit-specialist`. They resolve to their own stub files until v0.11 removes them.
- **No new benchmarks:** the 60.7% strict / 87.5% valid figure is still the v0.7.4 SWE-bench Lite sample (56/300). v0.10 has not been re-benchmarked. Numbers will be republished only after a real re-run.

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
