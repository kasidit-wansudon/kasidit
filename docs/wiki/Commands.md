# Commands

All `/kasi-*` commands shipped with the plugin. Invoke with `/` from Claude Code.

## Mode command (v0.10)

### `/kasi`

**Deep page:** [[Kasi-Mode]]

Toggle Kasidit framework intensity. Controls how much of `SKILL.md` is brought into context.

```
/kasi                       # show current mode
/kasi off                   # disable for this session
/kasi router                # default — thin classifier (~20 line)
/kasi lite                  # Rule 1 + Rule 11 only (~100 line)
/kasi full                  # all 11 rules + 8 agents + Gravity (~650 line)
/kasi ultra                 # full + verifier hook + master self-check
/kasi save                  # persist current mode to .kasidit/config.json
/kasi reset                 # drop session override
/kasi status                # resolved config: session > project > global > default
```

Heavy commands (`/kasi-review`, `/kasi-security`, `/kasi-fix`, `/kasi-ui`, `/kasi-multi`, `/kasi-cascade`, `/kasi-team`, `/kasi-deploy`) auto-escalate to `full` (or `ultra` for `/kasi-security`) for the duration, then revert. `/kasi-review-deploy` stays `lite` — read-only, no escalation needed.

**State precedence is spec, not runtime.** No code currently merges the three configs into a single resolved value — the AI and the user apply the chain by reading the files. See [[Kasi-Mode]] for full details.

## Mission commands

### `/kasi-review`

**Deep page:** [[Kasi-Review]]

Launch a code review mission with full Kasidit discipline: narrow scope → load or generate CHECKLISTS → dispatch per-file agents → synthesize findings with confidence labels + Top 5 priority.

Tier behavior: on Haiku, 1 file per agent + mandatory verifier pass.

### `/kasi-security`

**Deep page:** [[Kasi-Security]]

Security audit variant of review. Runs through `CHECKLISTS/security-<stack>.md`. Flags injection, auth, file handling, output, session, crypto issues. Confidence-labeled.

### `/kasi-fix`

**Deep page:** [[Kasi-Fix]]

Bug-fix mission with conservative discipline. Runs mandatory `git log --grep=<term>` and `git log -S <symbol>` before any fix (Rule 2.6). Minimal-change fix with regression test.

### `/kasi-ui`

**Deep page:** [[Kasi-Ui]]

UI/CSS mission in UI Override Mode. Requires visual target (screenshot / CSS values / Claude Design mockup). One change per round. Cache-aware.

### `/kasi-cascade`

**Deep page:** [[Kasi-Cascade]]

Tier Cascade orchestration ([[v0.8.0]]): Opus plans → Sonnet writes → Haiku greps. Invoke for missions large enough to benefit from multi-tier routing.

### `/kasi-multi`

**Deep page:** [[Kasi-Multi]]

```
/kasi-multi                    # default: 6 agents, auto-selected
/kasi-multi 4                  # 4 agents
/kasi-multi 6 <mission>        # 6 agents + explicit mission
sudo <mission>                 # shorthand for /kasi-multi 6 <mission>
sudo 8 <mission>               # shorthand + custom N
```

Fan-out mode — dispatch N specialists in parallel, each with an isolated context and a dispatch brief. Main synthesizes the N reports into one user-facing answer.

**Default roster at N=6** (v0.10): `architect-planner` / `deep-researcher` (scope), 3× `general-purpose` (parallel workers), `test-writer` (verification), `audit-specialist --focus=quality` (review slot — replaces standalone `code-reviewer`). Main swaps in `bug-hunter`, `audit-specialist --focus=perf|security`, `refactor-surgeon`, `migration-specialist`, `legacy-specialist` based on mission kind.

**`sudo` keyword** = fan-out by default + skip clarifying questions (narrate assumptions briefly) + still respect destructive-op confirmation.

**Tier caps:**

- Opus: fan out freely
- Sonnet: default, prefers N=4 on large contexts
- Haiku: **capped at N=4** — synthesis collapses above that

Introduced in [[v0.9.2]]. See [[Multi-Agent-Orchestration]].

### `/kasi-team`

**Deep page:** [[Kasi-Team]]

HYBRID panel brainstorm + user decision gate + parallel dispatch + QA synthesis ([[v0.15.0]]). Distinct from `/kasi-multi` / `sudo` (which execute a known approach) — Team Mode decides the approach first.

Composition: CORE (Lead = `architect-planner`, QA = `audit-specialist --focus=quality`) + DYNAMIC lenses (security/perf/migration) + implementation specialists, picked per mission from the Specialist Agent Registry. No new agent files.

Flow: panel proposes 2-3 options with trade-offs → **mandatory user decision gate** → dispatch implementation specialists in parallel (reuses `/kasi-multi` mechanics) → mandatory QA pass before final synthesis.

Refinement Counter capped at **1 round** for the brainstorm phase (vs framework default 3) to prevent option proliferation. Haiku: panel reduced to N=2, 0 refinement rounds, dispatch cap N=4; refuses missions needing a security/migration lens.

## Backend & DevOps commands ([[v0.11.0]])

### `/kasi-backend`

**Deep page:** [[Kasi-Backend]]

```
/kasi-backend <fix|audit|scaffold|design|perf|security> <scope>
```

Multi-mode backend mission router — counterpart to `/kasi-ui`. Auto-detects Laravel / Node stack from `composer.json` / `package.json`.

### `/kasi-graph`

**Deep page:** [[Kasi-Graph]]

```
/kasi-graph <build|show|extract|impact|trace|cycles|dead>
```

Function call graph build + subgraph extraction. Consumed by `/kasi-backend audit|perf` for scoped analysis. Regex-MVP (file-level call attribution) — per-function-body extraction via ast-grep AST path is a roadmap item, not shipped.

### `/kasi-struc`

**Deep page:** [[Kasi-Struc]]

```
/kasi-struc <build|refresh|show|tree|module|path|bridge|verify>
```

Project structure index + auto-bridge cache at `.kasidit/STATE/`. Commands read cached state instead of rescanning the repo every invocation. `refresh` does an incremental update via `git diff` since last build.

### `/kasi-devopt`

**Deep page:** [[Kasi-Devopt]]

```
/kasi-devopt <env|data|infra|secrets|runbook|health|connect>
```

DevOps mission — env var diffing, data-flow mapping, secrets audit, infra-as-code review, runbook generation, health checks, service-connection docs. Its `deploy <env>` sub-mode is **superseded by `/kasi-deploy` + `/kasi-review-deploy`** ([[v0.16.0]]) — invoking it now redirects to those two commands; the old never-executes flow is kept inline for reference only.

### `/kasi-acknowledge`

**Deep page:** [[Kasi-Acknowledge]]

```
/kasi-acknowledge [capture|template|update|link]
```

Capture the steps just performed (deploy, migration, hotfix, etc.) as a replayable runbook in `.kasidit/knowledge/runbooks/`.

### `/kasi-knowledge-list`

**Deep page:** [[Kasi-Knowledge-List]]

```
/kasi-knowledge-list [list|show|recent|tag|kind|search|replay|stats|stale]
```

Browse stored runbooks and knowledge entries. `replay` prints "how to do it again" step-by-step.

## Deploy commands ([[v0.16.0]])

### `/kasi-deploy`

**Deep page:** [[Kasi-Deploy]]

```
/kasi-deploy staging
/kasi-deploy prod
/kasi-deploy prod --allow-dirty
```

Deploy mission with a **real execute path** — the first Kasidit command permitted to run a deploy command itself, and only under a fixed platform capability table:

| Platform | Mode |
|---|---|
| Cloudflare Workers/Pages, Vercel, Netlify | **auto-executable** — first-party idempotent one-shot CLI |
| SSH/bare-VPS, Docker/k8s/Terraform/Serverless/Fly/Platform.sh | **plan-only** — shows commands, user runs them (same as the old `/kasi-devopt deploy` behavior) |

Always runs the `/kasi-review-deploy` preflight first — blocks entirely on a NOT READY verdict. Prod execution requires a **typed** `confirm: deploy-prod` gate (a plain "yes" is not accepted); staging/preview needs only a plain confirm. Dirty working tree forces plan-only unless `--allow-dirty`. On failure: reports the error, never auto-retries or auto-rollbacks — that's a separate user decision.

**Tier gating:** Haiku is restricted to the plan-only path regardless of platform — auto-execute requires Sonnet or Opus. See [[Model Tiers]].

### `/kasi-review-deploy`

**Deep page:** [[Kasi-Review-Deploy]]

```
/kasi-review-deploy staging
/kasi-review-deploy prod diff
/kasi-review-deploy prod secrets
```

Read-only deploy preflight — the strict extraction of the old `/kasi-devopt deploy` checklist. **Zero execution, zero file writes, on any platform, at any tier** (including Haiku — a mechanical checklist scan carries no execution risk). Answers "is it safe to deploy", not "how do I deploy". Verdict: ready / ready with warnings / not ready.

## Project commands

### `/kasi-init`

**Deep page:** [[Kasi-Init]]

Bootstrap a new or existing project. Chains:

```
/kasi-scaffold → /kasi-pull (stack defaults) → /kasi-docs →
.kasidit/MISSION.md seed → optional /kasi-review →
register SessionStart hook in .claude/settings.local.json → CLAUDE.md pointer
```

Skip flags: `skip docs`, `skip review`, `no auto-invoke`, `dry-run`.

Haiku: skips the review step during init unless user insists.

### `/kasi-scaffold`

**Deep page:** [[Kasi-Scaffold]]

Build `.kasidit/` structure: INDEX, RELATIONS, MEMORY, PATTERNS, CHECKLISTS, knowledge. Detects stack from `composer.json` / `package.json` / etc. Asks to confirm detection before generating.

### `/kasi-docs`

**Deep page:** [[Kasi-Docs]]

Fetch version-matched official documentation for the detected stack. Caches to `.kasidit/knowledge/<stack>-<version>-<topic>.md`. Follows the Trust Hierarchy from [[v0.2.1]].

### `/kasi-status`

**Deep page:** [[Kasi-Status]]

Show current mission state, failure counter, context usage. Quick health check.

## Gravity commands

### `/kasi-promote`

**Deep page:** [[Kasi-Promote]]

```
/kasi-promote <type> <name>
```

Lift item from `.kasidit/` into `~/.claude/skills/kasidit/center/`. Types:

| Type | Source | Target |
|---|---|---|
| `pattern` | `.kasidit/PATTERNS.md` section | append to `center/patterns.jsonl` |
| `checklist` | `.kasidit/CHECKLISTS/<name>.md` | copy to `center/checklists/<name>.md` |
| `knowledge` | `.kasidit/knowledge/<file>.md` | copy to `center/knowledge/<file>.md` |
| `rule` | free text | append to `center/rules.md` |
| `mission` | `.kasidit/MISSION.md` | append summary to `center/missions.jsonl` |

Always asks confirmation. Never auto-promotes. See [[Gravity Pattern]].

### `/kasi-pull`

**Deep page:** [[Kasi-Pull]]

```
/kasi-pull <type> <name>
/kasi-pull all-for <stack>
```

Fetch item from Centerlite into project `.kasidit/`. Diffs before overwrite; `(o)verwrite / (m)erge-append / (s)kip` on conflict. See [[Gravity Pattern]].

### `/kasi-sync`

**Deep page:** [[Kasi-Sync]]

```
/kasi-sync              # everything
/kasi-sync checklists   # one type
/kasi-sync <name>       # one item
```

Audit drift between dcenterlite and centerlite. Read-only. Prints per-item status: `up-to-date / local ahead / center ahead / conflict / local only / center only` with suggested command.

### `/kasi-search`

**Deep page:** [[Kasi-Search]]

```
/kasi-search "<query>"
```

Semantic search over `.kasidit/knowledge/` via local embeddings ([[v0.8.0]]). Returns top-k snippets with file path, line range, similarity score. No network calls.

## Design commands ([[v0.9.0]])

### `design <what>`

Route to Claude Design for visual work. Asks audience / platform / brand constraints, pre-fills the Claude Design brief.

### `mockup <screen>`

Shortcut for `design mockup <screen>`.

### `extract-system`

Claude Design reads codebase CSS and component files, produces a draft `.kasidit/DESIGN_SYSTEM.md`.

### `parity <mockup-id>`

Compare current UI screenshot vs saved `.kasidit/prototypes/<mockup-id>-after.png`. Report `[parity high | medium | low]` with per-token diffs.

### `report visual`

Export last findings as a one-pager via Claude Design. Useful for non-technical audiences.

## Meta commands

### `/kasi-wiki-sync`

**Deep page:** [[Kasi-Wiki-Sync]]

```
/kasi-wiki-sync          # dry-run (default)
/kasi-wiki-sync apply    # actually push
/kasi-wiki-sync <page>   # one page only
```

Push `docs/wiki/*.md` into `github.com/kasidit-wansudon/kasidit.wiki.git`. Manual — not wired to commit hooks. Requires auth to the wiki repo.

## Steering shorthand (informal, not slash commands)

Useful phrases recognized by the skill:

- `task status` — summary of mission, counter, pending items
- `clear` — reset working context, keep สารบัญ and MEMORY.md
- `remember <fact>` — save to `.kasidit/MEMORY.md`
- `forget that` — drop last failed attempt
- `wave 2` — force escalation
- `tier opus | sonnet | haiku` — override tier auto-detect
- `verify` — run verification pass on last findings
- `build index` — generate `.kasidit/INDEX.md` from structure
- `build checklist <domain>` — scaffold a stack-specific checklist

## See also

- [[Getting Started]]
- [[Gravity Pattern]]
- [[Model Tiers]]
