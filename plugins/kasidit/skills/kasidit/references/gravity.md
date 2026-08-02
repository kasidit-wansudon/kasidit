# Kasidit — Gravity + สารบัญ + Global Log

> Cross-project/cross-session knowledge persistence. Referenced from ../SKILL.md.

---

## สารบัญ System (Index-Driven Knowledge)

Build a project index to give AI a stable base. **Essential for Haiku** — compensates for weak cross-file reasoning by making relationships explicit.

### Structure

```
.kasidit/
├── INDEX.md              # Table of contents — file path + purpose
├── RELATIONS.md          # Relation diagram between modules
├── MEMORY.md             # User-confirmed facts across sessions
├── PATTERNS.md           # Codebase-specific patterns (copy, do not invent)
├── DESIGN_SYSTEM.md      # Visual patterns — colors, spacing, components (v0.9)
├── CHECKLISTS/           # Scan checklists for repeatable audits
│   ├── security-php.md
│   ├── security-node.md
│   ├── performance-sql.md
│   └── css-audit.md
├── prototypes/           # Claude Design exports (v0.9)
│   ├── <mission-id>-before.png
│   ├── <mission-id>-after.png
│   └── <mission-id>.url
└── knowledge/
    ├── api-conventions.md
    ├── db-schema.md
    ├── auth-flow.md
    └── <stack>-<version>-<topic>.md
```

### Rules for สารบัญ

1. **INDEX.md stores paths only** — `path/to/file.md — one-line purpose`.
2. **Each knowledge/*.md = verified clean truth** — written or approved by user.
3. **Relations auto-detected + user-approved** — if wrong, reorder.
4. **On error recurrence** — before debugging a repeated error, look up RELATIONS.md.
5. **Markdown format** — standard, linkable, greppable.
6. **Prototypes/ stores Claude Design exports** — referenced by mission id.

### Point-based output with lazy loading

When replying about code or structure:
- Output a list of points.
- Each point references `.kasidit/knowledge/X.md` if deeper context exists.
- AI does **not** load .md content into own context — the user clicks to read.
- This keeps AI context lean, makes knowledge auditable by user.

Example reply:
```
Fix plan:
- [K-AUTH-03] JWT refresh token flow
- [K-DB-12] user_sessions schema
- [K-API-07] /refresh endpoint shape

Apply change to app/Auth/TokenService.php:L45?
```

### PATTERNS.md — v3 addition

File that records project-specific patterns for AI to **copy, not reinvent**. Template: `includes/patterns-template.md`.

**Why PATTERNS.md matters for Haiku:**
Haiku invents plausible-but-wrong patterns when unconstrained. With PATTERNS.md, it copies from proven examples. Quality jumps significantly.

### DESIGN_SYSTEM.md — v0.9 addition

Visual counterpart to PATTERNS.md. Records visual rules extracted from the codebase so Claude Design and hand-coded UI stay consistent. Template: `includes/design-system-template.md`.

**Generation flow:** `build design-system` command → Claude Design reads codebase CSS/component files → generates draft → user approves → save here.

### CHECKLISTS/ — v3 addition

Pre-built audit lists AI runs through mechanically, not via reasoning. Starter checklist (PHP): `defaults/checklists/security-php.md`.

AI reads this, scans files mechanically, reports findings. No "reasoning" needed — **checklist does the thinking**.

**This is the single biggest Haiku enabler in v3.**

**Domain-based selection — v0.16 addition.** Language-only selection (`code-review-node`, `security-php`) misses bugs that are cross-language: money math, date/time handling, and locale/i18n break the same way in Node, PHP, Python, or Go, and no per-language checklist ever names them. Select by what the mission actually touches, not only by file extension:

- Mission touches prices, totals, discounts, tax, payouts, currency → load `defaults/checklists/correctness-money.md`
- Mission touches scheduling, dates, timestamps, recurring events, "days until/since" → load `defaults/checklists/correctness-datetime.md`
- Mission touches translations, multi-language UI, sorting user-facing text, RTL layout → load `defaults/checklists/correctness-locale.md`

These stack with the language checklist — e.g. a Laravel invoice endpoint loads `backend-laravel.md` **and** `correctness-money.md`, not one or the other.

---

## Gravity Pattern — Centerlite + Dcenterlite (v0.9.2)

> Two-tier knowledge system. Center has mass. Local has autonomy. Things fall in when proven.

Kasidit splits knowledge into **Centerlite** (global, shared, stable) and **Dcenterlite** (project-local, full-fidelity). The sync logic between them is named **Gravity**: items with proven utility fall inward to the hub; items needed in a project orbit outward from the hub. Nothing moves automatically — the user promotes or pulls deliberately.

### Centerlite — `~/.claude/skills/kasidit/center/`

The **mass**. Global, user scope, shared across every project.

```
center/
├── logs/              # prompt logs (UserPromptSubmit hook writes here)
├── patterns.jsonl     # cross-project patterns validated and promoted
├── checklists/        # master checklist library (upstream source for .kasidit/CHECKLISTS/)
├── knowledge/         # doc snippets shared across projects (version-matched)
├── missions.jsonl     # mission history — ts, project, tier, outcome
└── rules.md           # user's accumulated personal rules
```

**Discipline:**

- **Lightweight.** Facts, pointers, small snippets. No code dumps. Target <1MB per file.
- **Append-only** for `*.jsonl`. History is load-bearing.
- **Never project-specific.** No table names, no client names, no internal vars.
- **Promotions require user confirmation.** Every item earns its place.

### Dcenterlite — `<project>/.kasidit/`

The **orbit**. Project-local, full-fidelity, authoritative for the project.

```
.kasidit/
├── INDEX.md RELATIONS.md MEMORY.md PATTERNS.md
├── DESIGN_SYSTEM.md MISSION.md
├── CHECKLISTS/    # copies from Centerlite, customizable
├── knowledge/     # project-version-matched docs
└── prototypes/    # Claude Design exports
```

**Discipline:**

- **Source of truth for the project.** Full detail allowed.
- **Pulled items are detached.** Local edits do not push back — use `/kasi-promote` when an improvement is general enough to share.
- **Customize freely.** Dcenterlite is yours; Centerlite is the garden.

### Gravity Sync Logic

| Operation | Direction | Trigger |
|-----------|-----------|---------|
| **Read** | dcenterlite → centerlite fallback | missing local file → check hub → copy down if matched |
| **Write** | local only | every mission writes to `.kasidit/`, never hub |
| **Promote** | dcenterlite → centerlite | explicit `/kasi-promote <type> <name>` + confirm |
| **Pull** | centerlite → dcenterlite | explicit `/kasi-pull <type> <name>` + confirm |
| **Sync audit** | both sides compared, no mutation | `/kasi-sync` prints drift report |
| **Log flow** | user prompts → centerlite | opt-in via `KASIDIT_LOG_ENABLED=1` (one-way) |

**Rule:** auto-scan aggregation (e.g. "pattern seen in 3 projects → suggest promote") is **deferred to post-v0.9.2**. First ship the surface, validate usage, then automate.

### Drift reminder (passive nudge)

Centerlite goes stale when patterns accumulate in `.kasidit/` but are never promoted. To prevent silent drift:

- `/kasi-init` writes `~/.claude/skills/kasidit/center/.last_sync` with the current timestamp.
- `/kasi-sync` and `/kasi-promote` update this timestamp on success.
- On `SessionStart`, if `center/.last_sync` is **older than 7 days**, print:

  ```
  [kasidit] Centerlite last synced >7d ago. Run /kasi-sync to check drift.
  ```

- This is a reminder, not a block. User may dismiss and continue.
- If `center/.last_sync` does not exist (first run or pre-v0.9.3 install), skip the reminder and create the file silently on next sync.

The `SessionStart` hook that fires this check lives at `~/.claude/hooks/kasi-drift-check.sh`. It is registered by `/kasi-init` at user scope (one-time, not per project).

### Why Gravity matters per tier

- **Opus** — can reason across projects; Gravity gives it a canonical place to cite validated patterns instead of reinventing.
- **Sonnet** — uses Centerlite as a grounding base when switching contexts.
- **Haiku** — **essential.** Haiku lacks cross-file cross-project reasoning. Centerlite pre-builds the scaffolding it cannot synthesize.

### Tier-specific use

- **Opus:** may **suggest** promotions after completing a mission, but never executes without user confirm.
- **Sonnet:** default. Pull during `/kasi-init`, promote after validated patterns show up 2+ times.
- **Haiku:** pull aggressively during init (use Centerlite as the scaffold). Promote rarely — Haiku's pattern-matching is not authoritative enough to change the hub.

### Privacy

Centerlite is user-scope, local filesystem. Nothing uploads anywhere. `center/logs/` contains verbatim prompts — **do not sync Centerlite into shared storage or git** without reviewing PII. The plugin's bundled hooks `.gitignore` this automatically when `/kasi-init` runs.

### Anti-patterns

- ❌ Auto-promoting every pattern — pollutes the hub.
- ❌ Editing Centerlite directly when the edit belongs to a single project (use `.kasidit/` instead).
- ❌ Pulling entire hub into every project — defeats "lightweight".
- ❌ Silent overwrite on pull when local is customized — always diff and ask.
- ❌ Committing `~/.claude/skills/kasidit/center/logs/` to any repo.

### Commands (Gravity)

- **`/kasi-promote <type> <name>`** — lift item into Centerlite.
- **`/kasi-pull <type> <name>`** — fetch item into project.
- **`/kasi-sync`** — audit drift, print per-item suggestions.

See `commands/kasi-promote.md` / `kasi-pull.md` / `kasi-sync.md` for full flows.

---

## Global Prompt Log (v0.9.2)

> Capture user intent across projects so Kasidit can reason over past missions.

A global `UserPromptSubmit` hook writes every user prompt to a date-partitioned JSONL file under `~/.claude/skills/kasidit/center/logs/YYYY-MM-DD.jsonl`. Prompts longer than 200 lines are trimmed to first 40 + last 20 lines with a `[trimmed N lines] ...` marker — enough signal to reconstruct intent without exploding the log.

**Location:**
```
~/.claude/hooks/kasi-log.sh       # hook entry (registered in settings.json)
~/.claude/hooks/kasi-log.py       # trim + append JSONL
~/.claude/skills/kasidit/center/logs/       # global log store, all projects
```

**Record shape:**
```json
{"ts":"2026-04-23T16:31:03Z","session":"<id>","cwd":"<path>","lines":250,"chars":12034,"trimmed":true,"prompt":"<head>\n\n... [trimmed 190 lines] ...\n\n<tail>"}
```

**Rules:**
- Hook **never blocks** prompt submission. All errors swallowed; logging is best-effort.
- Logs are global (user scope), not per-project — any Kasidit invocation, any project, feeds the same store.
- Log path relocatable via `KASIDIT_LOG_DIR` env var. Trim threshold (200-line cap, 40 head / 20 tail) is hardcoded — edit `MAX_LINES` / `HEAD_LINES` / `TAIL_LINES` in `kasi-log.py` to change.
- PII: prompts contain whatever user typed. Do not commit the `logs/` directory. `.gitignore` recommended.
- Downstream tools (`kasi-search`, future analytics) may index this store.

**Opt-out:** remove the `UserPromptSubmit` block from `~/.claude/settings.json`.

---

