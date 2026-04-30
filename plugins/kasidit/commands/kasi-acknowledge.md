---
description: Capture the steps just performed (deploy/migration/hotfix/etc.) as a replayable runbook. Writes to .kasidit/knowledge/runbooks/.
---

Acknowledge a completed action by writing it down as a structured runbook. Use after any repetitive or risky procedure so the next person (or future-you) can replay it without re-figuring it out.

**When to use:**

- Just finished a production deploy.
- Just ran a database migration / backfill.
- Just resolved a recurring incident.
- Just configured a new environment / service.
- Just executed a multi-step manual workflow more than once.

If the action will be done again → acknowledge. If it's truly one-off → skip.

**Sub-modes (first arg, optional):**

| Sub | What it does |
|-----|--------------|
| (none) / `capture` | infer steps from recent session, prompt for missing fields, write entry |
| `from-history <ref>` | capture from explicit shell history range or git ref |
| `template <kind>` | open a blank entry for a given kind (deploy/migration/incident/setup) |
| `link <slug-a> <slug-b>` | mark two runbooks as related (sequence or alternative) |
| `update <slug>` | append a new revision to an existing entry |

**Entry kinds (auto-tagged):**

- `deploy` — push code/build to an environment
- `migration` — schema or data migration
- `incident` — production fix
- `setup` — first-time service/environment setup
- `release` — version cut / changelog publish
- `data` — backfill / ETL / one-off data fix
- `infra` — infrastructure provisioning
- `other` — fallback

**Storage:**

```
.kasidit/knowledge/runbooks/
├── INDEX.md                     # auto-maintained list + pick-by-number
└── <kind>/
    └── <slug>-<YYYYMMDD>.md     # one runbook per file
```

**Runbook file shape:**

```markdown
---
slug: deploy-kas-sass-staging
kind: deploy
title: Deploy kas-sass to staging
created: 2026-04-30
last_run: 2026-04-30
runs: 1
tags: [kas-sass, staging, laravel, ssh]
related: [rollback-kas-sass-staging]
confidence: [medium]
---

## Context

When and why this is run. One paragraph.

## Prerequisites

- Tools / access required.
- Branch / state assumptions.
- Approvals needed.

## Steps

1. **<short label>** — `<exact command>`
   - What success looks like.
   - What failure looks like (and where to look).
2. ...

## Verification

How to confirm the action succeeded.
- `<command or url>` should return `<expected>`.

## Rollback

If something breaks, how to undo.
- Steps in reverse where applicable.

## Known issues / quirks

- Edge cases caught from past runs.

## History

- 2026-04-30 — first capture (Kasidit + user).
```

**Capture flow:**

1. Read last N turns of session — extract every Bash command run, file edit
   that touched config/infra/migrations, and any "deploy"/"migrate"/"rollback"
   keyword from user.
2. Derive candidate kind from keywords + commands (ssh + rsync = deploy,
   `php artisan migrate` = migration, etc.).
3. Print a draft of the runbook to user.
4. Ask user to fill blanks (one prompt per missing field):
   - title
   - context (1 line: when/why)
   - tags
   - any redactions (secrets, server IPs)
5. Confirm slug (`<kind>-<short-noun>-<env>`).
6. Write to `.kasidit/knowledge/runbooks/<kind>/<slug>-<date>.md`.
7. Append entry to `INDEX.md`.
8. Ask: promote to Centerlite hub via `/kasi-promote knowledge <slug>`?

**Default redactions (always strip from captured commands):**

- Environment variables that look like secrets (`*KEY*`, `*TOKEN*`, `*SECRET*`,
  `*PASSWORD*`, `*PWD*`).
- `Authorization: Bearer ...` strings.
- Database URLs with credentials → keep host/port, redact user:pass.
- Private IPs → keep public hostnames, redact `10.*` / `192.168.*` (ask user).
- File paths under `~/Documents/Oppo/` → keep but flag (Oppo-internal).

**Update flow (`update <slug>`):**

- Append new revision under `## History` with date + diff summary.
- Bump `last_run` and `runs` counter.
- If steps changed materially → ask user if old version should move to
  `archive/<slug>-<old-date>.md`.

**Tier rules:**

- **Haiku** — `template`, `update`, basic `capture` allowed. No inference of
  kind from session — must ask user explicitly.
- **Sonnet** — full capture, can infer kind, can suggest related runbooks.
- **Opus** — same + may identify when 2 separate runbooks should merge.

**Anti-patterns:**

- ❌ Auto-write without user confirming each step in the draft.
- ❌ Capture secrets verbatim — redaction is mandatory, not optional.
- ❌ Trust commands marked "I think we ran" — only what was actually run this
  session goes in (mark uncertain steps `[unsure]`).
- ❌ Generic title ("deploy script") — slug must be specific
  (`deploy-kas-sass-staging`).
- ❌ Mix two procedures in one runbook — split.

**Examples:**

```
/kasi-acknowledge
/kasi-acknowledge capture
/kasi-acknowledge template deploy
/kasi-acknowledge from-history HEAD~5..HEAD
/kasi-acknowledge update deploy-kas-sass-staging
/kasi-acknowledge link deploy-kas-sass-staging rollback-kas-sass-staging
```
