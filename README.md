# Kasidit

> **Stop fighting your AI. Give it discipline instead.**
> Mindful AI coding framework for Claude Code. Works the same on Opus, Sonnet, **and Haiku**.

[![release](https://img.shields.io/github/v/release/kasidit-wansudon/kasidit?style=flat-square&color=f59e0b)](https://github.com/kasidit-wansudon/kasidit/releases)
[![stars](https://img.shields.io/github/stars/kasidit-wansudon/kasidit?style=flat-square&color=fbbf24)](https://github.com/kasidit-wansudon/kasidit/stargazers)
[![license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](./LICENSE)

**Site:** https://kasidit-wansudon.github.io/kasidit-site/ · **Wiki:** [GitHub Wiki](https://github.com/kasidit-wansudon/kasidit/wiki) · **Changelog:** [CHANGELOG.md](./CHANGELOG.md)
**ภาษาไทย:** [อ่านสรุปภาษาไทย](#-สรุปภาษาไทย-thai-summary) ↓

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
| Convention-only rules | model decides to ignore them | **5 runtime-enforced hooks** + 16 prompt-level rules |
| Knowledge resets every session | one-shot prompts | **Gravity hub** persists patterns / runbooks / route-memory across projects |
| One audit = one whole-repo grep | slow + noisy | **subgraph extraction** — scope to 10 functions, not 1000 |
| Deploy procedure forgotten | re-figure it next time | **`/kasi-acknowledge`** captures it as a replayable runbook |

**The real edge:** discipline turns Haiku into a senior engineer's executor. On Opus it unlocks depth. On Haiku it _replaces_ raw reasoning with checklists, verifier passes, and forced abstention. Same framework, every tier.

## Proof

- **87.5% valid fix rate on a SWE-bench Lite sample** (56/300 tasks, strict PASS 60.7%, v0.7.4)
- Production-tested on a **288K-line legacy PHP codebase**
- 5 backend hooks. 21 slash commands. 8 specialist agents. 15 default checklists. 11 core rules — all enforced, not aspirational.

## What you get

- **21 slash commands** — `/kasi-review · security · fix · ui · backend · graph · struc · devopt · acknowledge · knowledge-list · cascade · init · scaffold · docs · status · promote · pull · sync · search · multi · wiki-sync`
- **`/kasi` mode command** — pick intensity: `off / router / lite / full / ultra`
- **8 specialist agents** — `architect-planner`, `audit-specialist` (`--focus=quality|security|perf`), `bug-hunter`, `deep-researcher`, `legacy-specialist`, `migration-specialist`, `refactor-surgeon`, `test-writer`
- **5 runtime hooks** — prompt classifier, confidence-label verifier, backend-save recorder, update + drift check
- **Master Orchestrator** — main agent delegates; never executes strong work itself
- **Gravity** — two-tier knowledge: Centerlite hub + per-project Dcenterlite, with promote / pull / sync
- **15 default checklists** — security · code-review · perf · backend across PHP / Node / Python / Go
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

## Install

```bash
# In Claude Code
/plugin marketplace add kasidit-wansudon/kasidit
/plugin install kasidit@kasidit
```

Or clone and run `bash plugins/kasidit/install.sh`.

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

### ทำไมต่างจาก framework อื่น

- **Refuse vague scope** — "ดูโปรเจกต์หน่อย" → AI ปฏิเสธ + ขอ narrow ก่อน
- **Runtime hook ตรวจ `[high]`** — AI claim high แต่ไม่มี Read/Bash → auto downgrade
- **Master delegate violation flag** — main agent edit ไฟล์เอง → hook เตือน
- **Tier-aware** — Haiku ได้ scaffolding หนักกว่า Opus (ไม่ใช่ปิด)
- **Gravity hub** — knowledge ข้าม session/project ไม่ reset
- **Subgraph audit** — scope ไป 10 fn ไม่ใช่ทั้ง repo

### หลักการ 6 ข้อ

- **1 mission, 1 focus, 1 step** — ห้ามทำหลายเรื่องพร้อมกัน
- **Design ก่อน code** — ห้าม dive ตรง implementation
- **Runtime is judge** — ไม่เชื่อที่ AI ว่าตัวเอง ต้องรันจริง
- **Confidence labels** — tag `[high|medium|low|unsure]` ทุก finding
- **Master delegate** — งานหนัก spawn specialist; main ไม่ทำเอง
- **Tier-aware** — รุ่นเล็กยิ่งใช้ scaffolding หนัก

### มีอะไรบ้าง (v0.11.0)

- **21 slash commands** — review, security, fix, ui, **backend, graph, struc, devopt, acknowledge, knowledge-list** (ใหม่ใน v0.11), cascade, init, scaffold, docs, status, promote, pull, sync, search, multi, wiki-sync
- **`/kasi` Mode** — `off / router / lite / full / ultra`
- **8 specialist agents** — architect-planner, audit-specialist (`--focus=quality|security|perf`), bug-hunter, deep-researcher, legacy-specialist, migration-specialist, refactor-surgeon, test-writer
- **5 runtime hooks** — prompt classifier, confidence verifier, backend recorder, update/drift check
- **15 default checklists** — security/code-review/perf/backend × PHP/Node/Python/Go
- **Master Orchestrator** — main delegate ไม่ทำงานหนักเอง
- **Gravity Pattern** — knowledge 2 ชั้น: hub กลาง + project orbit

### ติดตั้ง

```
/plugin marketplace add kasidit-wansudon/kasidit
/plugin install kasidit@kasidit
```

หรือ `git clone` แล้วรัน `bash plugins/kasidit/install.sh`

### ผลทดสอบ (ตรงไปตรงมา)

SWE-bench Lite (sample 56/300):
- PASS (line-match เข้ม): **60.7%** (34/56)
- PARTIAL: **27%** · Valid fix rate รวม: **87.5%**

**หมายเหตุ:** คนละ scoring กับเลข Anthropic/Copilot/Claude Code Opus base — รายงานเพื่อโปร่งใส ไม่ใช่ marketing claim. Full run scheduled

### ใครเหมาะ

- Solo dev / Freelance ที่ใช้ Claude Code อยู่แล้ว
- ทีมที่อยาก standardize การใช้ AI
- คนที่ใช้ Haiku/Sonnet เพื่อประหยัด แต่อยาก output คุณภาพ
- คนที่เบื่อ AI หลอก แล้วต้องตามแก้

---

## Core rules

1. **One mission.** Refuse vague scope; demand narrowing.
2. **Design before code.** Show structure, ask, then build.
3. **Runtime is the judge.** Code _looks right_ ≠ done.
4. **Confidence labels.** Tag every non-trivial finding `[high|medium|low|unsure]`.
5. **Master delegates.** Strong work goes to specialists; main never executes it.
6. **Tier-aware.** Weaker model = more scaffolding, not more guessing.

(Full 11 rules + framework live in [SKILL.md](./plugins/kasidit/skills/kasidit/SKILL.md).)

## Honesty

The 11 core rules and Master Orchestrator are **prompt-level conventions** — the AI self-applies them. The 5 runtime hooks (`kasi-route.py`, `kasi-verify.py`, `kasi-record.py`, `kasi-update-check.sh`, `kasi-drift-check.sh`) are **harness-enforced** and run regardless of what the model decides.

If you only want one thing from this repo, run `kasi-verify.py` — it catches `[high]` claims with no matching tool call and flags master-orchestrator violations. On its own, that single hook prevents most AI hallucination patterns.

## License

MIT. Use freely, fork freely. Issues + PRs welcome at [kasidit-wansudon/kasidit/issues](https://github.com/kasidit-wansudon/kasidit/issues).

## Author

[Kasidit Wansudon](https://github.com/kasidit-wansudon) — self-taught Thai engineer.
Built through dogfooding on production legacy codebases.
