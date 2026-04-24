---
description: Toggle Kasidit intensity — off / router / lite / full / ultra. Session-level by default; use `save` to persist.
---

Mode toggle for Kasidit framework load depth. Controls how much of SKILL.md is brought into context.

## Usage

```
/kasi                       # show current mode + source
/kasi off                   # disable skill this session
/kasi router                # default — thin classifier, ~20 line. Routes each message to right mode.
/kasi lite                  # Rule 1 (mission) + Rule 11 (confidence) only — ~100 line
/kasi full                  # all 11 rules + 8 active agents (+ 3 v0.10 deprecated stubs) + Gravity — ~650 line, opt-in for audit/refactor/new-feature
/kasi ultra                 # full + mandatory verifier pass + master orchestrator every task — rare, high-stakes only
/kasi save                  # persist current session mode to .kasidit/config.json
/kasi reset                 # drop session override, use project/global config
/kasi status                # resolved config: session > project > global > default
```

## Intensity levels

| Level | Load | When |
|---|---|---|
| `off` | 0 line | user explicitly stops, or one-off throwaway |
| `router` | ~20 line | **default.** Classifies each user message and escalates only when needed. |
| `lite` | Rule 1 narrow-mission + Rule 11 confidence labels | routine coding with light discipline |
| `full` | all rules, agent registry, UI Override, Gravity | audit, refactor >2 files, new feature, unfamiliar codebase |
| `ultra` | full + verifier hook + master self-check each turn | rare — security audit, migration, compliance-critical |

## State precedence (spec — implementation pending)

```
session override  (/kasi <level> this turn)
  > project config  (.kasidit/config.json)
  > global config   (~/.claude/skills/kasidit/center/config.json)
  > default         (router — thinnest layer, escalates on demand)
```

`/kasi status` prints each layer + resolved value.

> Honest caveat: this chain is a spec, not a runtime resolver. No code in this plugin currently reads the three config files, merges them, and returns a single resolved mode — the effective precedence is applied by the user and the AI reading the config files directly and behaving accordingly. Treat this table as documentation of intended priority order, not as a guarantee that a runtime layer enforces it.

## Session vs persisted

- `/kasi full` → affects current session only. Next session reverts to config.
- `/kasi full` then `/kasi save` → writes to `.kasidit/config.json`. Persistent.
- `/kasi reset` → drops session override.
- `stop kasidit` → synonym for `/kasi off` + skip for rest of session.

## Integration with other commands

**Heavy commands auto-escalate temporarily, then revert to router.** User stays in router for day-to-day chat; framework loads only when the work actually needs it.

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
- Escalation does not touch persisted config. Next session loads from `.kasidit/config.json` unchanged.
- User can lock at a higher level with `/kasi full` + `/kasi save` — auto-revert is skipped until they `/kasi reset`.

## Parallel speed (session-level default)

When mode escalates to `full` or `ultra` (via heavy command or explicit `/kasi full|ultra`), the orchestrator spawns **minimum 2 specialist agents in parallel** by default — never serial single-agent — for speed.

- Applies to: `/kasi-review`, `/kasi-security`, `/kasi-fix`, `/kasi-ui`, `/kasi-multi`, `/kasi-cascade`, any `full`/`ultra` mission.
- Not applies to: router, lite, or explicit `/kasi-multi 1`.
- Scope: **session only.** Not persisted. Next session follows config defaults.
- User override per session: `/kasi parallel 1` (serial) or `/kasi parallel N` (force N).
- Tier cap still holds: Haiku max 4, others up to 10.

Rationale: synthesis cost on 2 agents is negligible; latency win is the point.

## Update check (1× per UTC day)

`kasidit-update-check.sh` runs on SessionStart. Hits GitHub releases endpoint (gh CLI or curl fallback), compares against installed `marketplace.json` version. Prints one line if newer:

```
[kasidit] update available: v0.9.3 → v0.10.0 — run: /plugin marketplace update kasidit
```

Silent on match, offline, missing gh+curl, or already checked today (stamp file at `~/.claude/skills/kasidit/center/.last_update_check`). No blocking, no upload.

## Behavior by level

### `off`
- SKILL.md not loaded into context.
- `/kasi-*` commands still work but each loads its own scope only.
- No confidence labels required.
- Respect user's existing CLAUDE.md / personal rules.

### `router` (default)

Thin classifier. ~20 lines loaded. Single job: read each user message, decide which mode fits, escalate if needed.

**Classifier rules (the only rules loaded at this level):**

1. If message matches **high-stakes** keywords (`security`, `audit`, `migration`, `OWASP`, `CVE`, `auth boundary`, `compliance`) → respond: `[kasidit] routing → ultra recommended. /kasi ultra to enable, or continue for one-shot.`
2. If message matches **heavy-work** keywords (`refactor`, `new feature`, `unfamiliar codebase`, `review >1 file`, `multi-file`, `architecture`, `design system`) → respond: `[kasidit] routing → full recommended.`
3. If message matches **routine-coding** keywords (`fix`, `bug`, `edit`, `rename`, `add function`, `why does X fail`) → respond: `[kasidit] routing → lite.`
4. If message matches **off-topic** (casual chat, question about framework, docs lookup) → respond: `[kasidit] routing → off.`
5. If ambiguous → default `lite` + one-liner: `[kasidit] unclear mission. Using lite. /kasi full if heavier discipline needed.`

**Router never writes code itself.** Its output is a 1-line routing decision + any recommended `/kasi <level>` command. User accepts by continuing or runs the command.

**Data-over-rules**: instead of loading SKILL.md rules, router reads project state on demand:
- `.kasidit/INDEX.md` — file map, 1-line purposes (cheap lookup, no reasoning load).
- `.kasidit/MEMORY.md` — user-confirmed facts from prior sessions.
- `.kasidit/PATTERNS.md` — codebase patterns (only if message touches a new area).
- `.kasidit/MISSION.md` — current mission state if one is active.

Router pulls **only the files it needs for the current message**. A "how does auth work" question reads `INDEX.md` + maybe one `knowledge/*.md` file — not the full framework.

**Router auto-escalates** when the user's next message clearly fits a heavier bucket, or when a `/kasi-*` heavy command is invoked. No need for user to type `/kasi full` manually for an obvious audit request.

**Memory-driven routing** (learns shortest route per mission kind):

Every completed mission writes a record to `~/.claude/skills/kasidit/center/route-memory.jsonl`:

```json
{"ts":"2026-04-23T21:45:00Z","kind":"security-audit-php","mode_used":"full","turns":4,"tokens":18200,"outcome":"pass","escalated_from":"router"}
{"ts":"2026-04-23T22:10:00Z","kind":"bug-fix-single-file","mode_used":"lite","turns":2,"tokens":3100,"outcome":"pass"}
{"ts":"2026-04-23T22:40:00Z","kind":"refactor-rename","mode_used":"router","turns":1,"tokens":800,"outcome":"pass"}
```

**Before routing a new message**, router queries this store:

1. Classify incoming message → `kind` (e.g. `security-audit-php`, `bug-fix-single-file`, `ui-override`, `refactor-rename`).
2. Lookup all past records with same `kind`.
3. Pick mode with **highest pass rate at lowest turns/tokens** → recommend that.
4. If history < 3 records for this kind → fall back to keyword rules above + tag recommendation `[unsure, low-history]`.
5. If history shows a heavier mode was over-kill (e.g. 5× `security-audit` all passed in `full`, 0 needed `ultra`) → **suggest downgrade** `[kasidit] history: full succeeded 5/5 for this kind. Skipping ultra.`

**Mission-kind classifier** (router does this in one pass):

```
<file-scope>  = single | multi | project-wide
<work-type>   = fix | review | security | perf | refactor | feature | migration | ui | docs | question
<novelty>     = familiar-area | new-area
kind = <work-type>-<file-scope>[-<stack>]
```

Examples:
- `fix-single-file` — router or lite
- `review-multi` — lite or full
- `security-project-wide` — full or ultra
- `refactor-multi` — full

**User override always wins**: explicit `/kasi <level>` beats memory recommendation. Memory is a suggestion layer, not a decision layer.

**Inspect memory (manual for now):**
- Raw file: `cat ~/.claude/skills/kasidit/center/route-memory.jsonl`
- Quick stats: `jq -s 'group_by(.kind) | map({kind:.[0].kind,n:length})' ~/.claude/skills/kasidit/center/route-memory.jsonl`
- Forget a kind: `jq -c 'select(.kind!="<kind>")' route-memory.jsonl > tmp && mv tmp route-memory.jsonl`

A dedicated `/kasi-memory` subcommand is not shipped in v0.10 — listed in roadmap.

**Privacy:** `route-memory.jsonl` contains only mission kind + metrics. No prompt text. No file paths. Safe to keep local.

**Token cost**: router adds ~20 lines of rules + whatever `.kasidit/` data the message actually needs + 1 line memory lookup result. Far cheaper than loading SKILL.md up front.

## Backend-offloaded logic

Heavy lifting runs in Python hooks, not LLM context. AI sees 1-line results only.

| Hook | Trigger | Job | Token cost to AI |
|---|---|---|---|
| `kasidit-route.py` | UserPromptSubmit | classify message, query memory, inject 1-line recommendation | ~15 tokens |
| `kasidit-verify.py` | PostToolUse / Stop | cross-check `[high]` labels vs Read/Bash calls, auto-downgrade | ~20 tokens if mismatch |
| `kasidit-record.py` | Stop / SubagentStop | parse AI emit lines → append to backend stores | ~0 (hook output stays local) |
| `kasidit-log.py` | UserPromptSubmit (opt-in) | prompt log, trim >200 line | ~0 |
| `kasidit-drift-check.sh` | SessionStart | stale center/.last_sync warning | ~0 if fresh |

All hooks stdlib-only Python 3. No extra deps. Run locally.

## Incremental backend save ("ออม")

At mission end or when AI notices a new pattern, it emits tiny structured lines (~20 tokens each). `kasidit-record.py` parses them and appends to the right backend store. AI pays a little per mission; router memory compounds over months.

**AI emit contract** (print in final output):

```
[kasidit-log] kind=bug-fix-single-file mode=lite turns=2 outcome=pass
[kasidit-pattern] name=sanctum-bearer-auth file=app/Http/Middleware/ApiAuth.php note="matches v3 trust hierarchy"
[kasidit-memory] fact="mex_canteen uses PHP 7.4 + Laravel 8 with custom Auth facade"
[kasidit-rule] scope=project rule="no composer update without lock diff"
```

**Parsed → backend:**

| Emit tag | File | Used by |
|---|---|---|
| `[kasidit-log]` | `center/route-memory.jsonl` | router recommendation |
| `[kasidit-pattern]` | `center/patterns.jsonl` | `/kasi-pull pattern`, PATTERNS.md seed |
| `[kasidit-memory]` | `center/memory.jsonl` | cross-session fact recall |
| `[kasidit-rule] scope=project` | `.kasidit/rules.jsonl` | project-local rules |
| `[kasidit-rule] scope=global` | `center/rules.jsonl` | user rules across projects |

**Cost model:**
- AI per mission: 20–50 extra tokens to emit 1–3 lines.
- Storage: JSONL, cheap, local.
- Return: router saves far more tokens on future similar missions (skips escalation, skips full-load) because memory knows the shortest successful path.

**Net** — save-as-you-go. Small regular deposit, compound interest.

### `lite`
- Only Rule 1 (mission-driven / vague refusal) and Rule 11 (confidence labels) active.
- No agent orchestration, no Gravity, no UI Override rules.
- Terse output still enforced.

### `full` (opt-in for heavy missions)
- All 11 core rules + sub-rules 2.3–2.6.
- Master Orchestrator soft-gate active on strong-work missions.
- Agent registry available.
- Gravity read-fallback (local → hub).

### `ultra`
- All of `full`, plus:
- Verifier hook **required** — confidence labels cross-checked vs tool calls.
- Master self-check runs every turn (not just strong-work).
- Dispatch brief mandatory on every specialist call.
- Mission counter tighter (Opus 3 / Sonnet 2 / Haiku 1 before Wave 1).

## Config file format

`~/.claude/skills/kasidit/center/config.json` (global) or `.kasidit/config.json` (project):

```json
{
  "version": "0.10.0",
  "mode": "full",
  "prompt_log": false,
  "last_changed": "2026-04-23T21:30:00Z"
}
```

Project file overrides global. Absent fields fall through to next layer.

## Install first-run

On first `/kasi-init`, ask ONE question:

```
Q. Kasidit default mode? Type 1, 2, or 3 (default: 1)
  1. router    — thin classifier. ~20 line. Routes each message, escalates on demand. (recommended)
  2. lite      — always Rule 1 + Rule 11. ~100 line. Light discipline baseline.
  3. full      — always full framework. ~650 line. Audit / refactor / security projects.
```

Map: `1 → router`, `2 → lite`, `3 → full`. Anything that is not 1/2/3 (blank, word, etc.) → treat as `1`. Save to global config. Skip if config already exists — use `/kasi reset` + `/kasi-init` to reconfigure. Ultra is opt-in only via `/kasi ultra`, never offered at install.

## Stop phrase

`stop kasidit` → `/kasi off` for rest of session, regardless of config. Same pattern as `stop caveman`.

## Implementation notes

- Command reads/writes JSON config files via host shell.
- No auto-migration on schema bump — print warning, ask user to re-run `/kasi-init`.
- Session state stored in `~/.claude/skills/kasidit/center/session-<id>.json` (ephemeral).
- SessionStart hook (optional, registered by `/kasi-init`) reads resolved config, prints one line: `[kasidit] mode: full (project)`.

## Examples

```
/kasi
→ mode: full (project)
  session: -
  project: full (.kasidit/config.json)
  global:  lite (~/.claude/skills/kasidit/center/config.json)
  default: lite

/kasi lite
→ session override: lite (project config unchanged)

/kasi save
→ project config updated: full → lite
  .kasidit/config.json written
```
