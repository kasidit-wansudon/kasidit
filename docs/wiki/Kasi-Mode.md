# /kasi — Mode Command (v0.10)

> Toggle Kasidit framework intensity for the current session (or persist to project config).

Controls how much of `SKILL.md` is active in context and which guardrails apply. Default is `router` — thin classifier mode that escalates only when the work needs it.

## Usage

```
/kasi                       # show current mode + source
/kasi off                   # disable skill this session
/kasi router                # default — thin classifier (~20 line)
/kasi lite                  # Rule 1 + Rule 11 only (~100 line)
/kasi full                  # all 11 rules + 8 agents + Gravity (~650 line)
/kasi ultra                 # full + verifier pass + master self-check each turn
/kasi save                  # persist current session mode to .kasidit/config.json
/kasi reset                 # drop session override, use project/global config
/kasi status                # resolved config: session > project > global > default
/kasi parallel N            # session-only min-N parallel dispatch for heavy cmds
stop kasidit                # synonym for /kasi off, sticky for session
```

## Intensity levels

| Level | Context load | When to use |
|---|---|---|
| `off` | 0 line | User explicitly stops, one-off throwaway, debugging |
| `router` | ~20 line | **Default.** Classifies each message, escalates only when needed |
| `lite` | Rule 1 + Rule 11 (~100 line) | Routine coding with light discipline |
| `full` | All rules + agent registry + Gravity + UI Override (~650 line) | Audit, refactor >2 files, new feature, unfamiliar codebase |
| `ultra` | Full + mandatory verifier + master self-check each turn | Rare — security audit, migration, compliance-critical |

## Router mode (default)

The thin layer. Three jobs, nothing more:

1. Classify each user message into a mission kind via [[Backend-Hooks]] `kasidit-route.py`.
2. Recommend a mode (`off` / `router` / `lite` / `full` / `ultra`).
3. Keep two always-on guardrails: **Rule 1 (mission-driven)** and **Rule 11 (confidence labels)**.

### Router classification triggers (as implemented)

Word-boundary match, first hit wins (dict-insert order). Exactly as in `kasidit-route.py:KEYWORDS`:

| Keyword(s) in message | kind | Recommended mode |
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
| no match | unclassified | silent (router stays default) |

Thai phrases (`เพี้ยน`) and multi-token triggers (`auth boundary`, `check the project`) are **not** implemented yet — add to `KEYWORDS` if needed.

### Router data-over-rules

Instead of loading SKILL.md rules, router reads project state on demand:

- `.kasidit/INDEX.md` — file map, 1-line purposes (cheap lookup, no reasoning load).
- `.kasidit/MEMORY.md` — user-confirmed facts from prior sessions.
- `.kasidit/PATTERNS.md` — codebase patterns (only if message touches a new area).
- `.kasidit/MISSION.md` — current mission state if one is active.

Router pulls **only the files the current message actually needs**. A "how does auth work" question reads `INDEX.md` + maybe one `knowledge/*.md` file — not the full framework.

## Heavy commands auto-escalate

Users stay in router for day-to-day chat; framework loads only when the work needs it. The following commands temporarily escalate and revert on mission end:

| Command | Auto-escalates to | Revert after |
|---|---|---|
| `/kasi-init` | `full` | command completes |
| `/kasi-scaffold` | `full` | command completes |
| `/kasi-docs` | `full` | command completes |
| `/kasi-review` | `full` | mission ends (runtime pass or Wave 2) |
| `/kasi-security` | `ultra` | mission ends |
| `/kasi-fix` | `full` | mission ends |
| `/kasi-ui` | `full` | mission ends |
| `/kasi-multi` / `/kasi-cascade` | `full` | command completes |
| `/kasi-promote` / `/kasi-pull` / `/kasi-sync` | `lite` | command completes |
| `/kasi-search` / `/kasi-status` | no change | — |
| casual chat, `/kasi`, `/kasi status` | stay router | — |

**Revert contract:**

- Mission end = runtime verification pass OR user types `/kasi reset` / `stop kasidit` / next mission starts.
- Escalation does **not** touch persisted config — next session loads from `.kasidit/config.json` unchanged.
- User can lock at a higher level with `/kasi full` + `/kasi save` — auto-revert is skipped until they `/kasi reset`.

## Parallel speed (session-level)

When mode escalates to `full` or `ultra` (via heavy command or explicit `/kasi full|ultra`), the orchestrator spawns **minimum 2 specialist agents in parallel** by default. Never serial single-agent.

- Applies to: `/kasi-review`, `/kasi-security`, `/kasi-fix`, `/kasi-ui`, `/kasi-multi`, `/kasi-cascade`, any `full`/`ultra` mission.
- Does **not** apply to: router, lite, or explicit `/kasi-multi 1`.
- **Session only** — not persisted. Next session follows config defaults.
- User override per session: `/kasi parallel 1` (serial) or `/kasi parallel N` (force N).
- Tier cap still holds: Haiku max 4, Sonnet/Opus up to 10.

Rationale: synthesis cost on 2 agents is negligible; latency win from parallelism is the point.

## State precedence

```
session override  (/kasi <level> this turn)
  > project config  (.kasidit/config.json)
  > global config   (~/.claude/skills/kasidit/center/config.json)
  > default         (router — thinnest layer, escalates on demand)
```

`/kasi status` prints each layer + the resolved value.

> **Honest caveat:** this chain is a **spec, not a runtime resolver**. No code in this plugin currently reads the three config files, merges them, and returns a single resolved mode. The effective precedence is applied by the user and the AI reading the config files directly and behaving accordingly. Treat this table as documentation of intended priority order, not as a guarantee that a runtime layer enforces it.

## Session vs persisted

- `/kasi full` → affects current session only. Next session reverts to config.
- `/kasi full` then `/kasi save` → writes to `.kasidit/config.json`. Persistent.
- `/kasi reset` → drops session override.
- `stop kasidit` → synonym for `/kasi off` for rest of session, regardless of config.

## Install first-run

On first `/kasi-init`, one question:

```
Q. Kasidit default mode? Type 1, 2, or 3 (default: 1)
  1. router    — thin classifier. ~20 line. Routes each message. (recommended)
  2. lite      — always Rule 1 + Rule 11. Light discipline baseline.
  3. full      — always full framework. Audit / refactor / security projects.
```

Saved to `~/.claude/skills/kasidit/center/config.json`. Any non-1/2/3 input is treated as `1`. `ultra` opt-in only via `/kasi ultra` at runtime — never offered at install.

## Config file format

`~/.claude/skills/kasidit/center/config.json` (global) or `.kasidit/config.json` (project):

```json
{
  "mode": "router",
  "created": "2026-04-24T04:20:00Z"
}
```

Project file overrides global. Absent fields fall through.

## Integration with `kasidit-route.py`

Every `UserPromptSubmit` hook event runs `kasidit-route.py`:

1. Read the prompt from stdin payload.
2. Classify via `KEYWORDS` word-boundary match.
3. Query `~/.claude/skills/kasidit/center/route-memory.jsonl` for past outcomes of this `kind`.
4. If history >= 3 successful runs exist for this `kind`, recommend the mode with lowest `avg_turns`.
5. Emit one line into context:

```
[kasidit] kind=bug-fix mode=lite history=4/4 avg_turns=2.0
```

AI sees this and can respect the recommendation, or escalate manually. User sees it as a subtle classifier breadcrumb. No token cost when prompt is unclassified — hook emits nothing.

See [[Backend-Hooks]] for the full contract.

## Inspect memory (manual for now)

A dedicated `/kasi-memory` subcommand is **not shipped** in v0.10. Use `jq`:

```bash
# Raw dump
cat ~/.claude/skills/kasidit/center/route-memory.jsonl

# Quick stats by kind
jq -s 'group_by(.kind) | map({kind:.[0].kind, n:length, passes:map(select(.outcome=="pass"))|length})' \
  ~/.claude/skills/kasidit/center/route-memory.jsonl

# Forget a kind (e.g. bad data)
jq -c 'select(.kind != "<kind>")' route-memory.jsonl > tmp && mv tmp route-memory.jsonl
```

## Anti-patterns

- ❌ Running every session in `ultra` to "be safe" — wastes tokens. Escalate per mission.
- ❌ Using `off` to skip Rule 1 when the mission is vague — narrow first, then decide mode.
- ❌ Locking `full` globally on machines where most sessions are casual chat.
- ❌ Treating `/kasi status` as authoritative — it reports what the AI reads, not a runtime-resolved value.
- ❌ Expecting `/kasi save` to affect another project — it writes project-local config only.

## Since

v0.10.0 — introduced.

## See also

- [[Backend-Hooks]]
- [[Agent-Audit-Specialist]]
- [[Checklists]]
- [[Master-Orchestrator]]
- [[Multi-Agent-Orchestration]]
- [[v0.10]]
