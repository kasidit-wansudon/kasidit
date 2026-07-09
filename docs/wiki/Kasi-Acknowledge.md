# /kasi-acknowledge

> Capture a completed action as a structured, replayable runbook — so the next person (or future-you) doesn't have to re-figure it out.

## Usage

```
/kasi-acknowledge
/kasi-acknowledge capture
/kasi-acknowledge from-history <ref>
/kasi-acknowledge template <kind>
/kasi-acknowledge update <slug>
/kasi-acknowledge link <slug-a> <slug-b>
```

## What it does

- Reads the last N turns of the session, extracts every Bash command run and any config/infra/migration-touching edit, plus deploy/migrate/rollback keywords.
- Derives a candidate runbook `kind` (deploy / migration / incident / setup / release / data / infra / other) from the commands and keywords.
- Drafts a runbook, prompts the user to fill blanks (title, one-line context, tags, redactions), confirms a slug, and writes it to `.kasidit/knowledge/runbooks/<kind>/<slug>-<date>.md`.
- **Redacts secrets by default** — env vars matching `*KEY*`/`*TOKEN*`/`*SECRET*`/`*PASSWORD*`, `Authorization: Bearer` strings, DB credential segments, private IPs.
- Offers to promote the new runbook to the Centerlite hub via `/kasi-promote knowledge <slug>`.

## When to use

- Right after a production deploy, a migration/backfill, resolving a recurring incident, or configuring a new environment.
- Any multi-step manual workflow you've now done more than once.

If the action will genuinely never be repeated, skip it — capturing a true one-off just adds noise to the runbook index.

## Runbook file shape

```markdown
---
slug: deploy-kas-sass-staging
kind: deploy
title: Deploy kas-sass to staging
created: 2026-04-30
last_run: 2026-04-30
runs: 1
tags: [kas-sass, staging, laravel, ssh]
confidence: [medium]
---

## Context
## Prerequisites
## Steps
## Verification
## Rollback
## Known issues / quirks
## History
```

## Flow

1. Read session history, derive candidate `kind` + draft.
2. Print the draft to the user.
3. Ask for missing fields one at a time (title, context, tags, redactions).
4. Confirm slug (`<kind>-<short-noun>-<env>`).
5. Write the file, append to `INDEX.md`.
6. Offer `/kasi-promote knowledge <slug>`.

## Tier behavior

- **Haiku** — `template`, `update`, basic `capture` allowed, but must ask the user explicitly for `kind` rather than inferring it.
- **Sonnet** — full capture with inference, can suggest related runbooks.
- **Opus** — same, plus can identify when two runbooks should merge.

## Anti-patterns

- ❌ Auto-write without the user confirming each field in the draft.
- ❌ Capture secrets verbatim — redaction is mandatory, not optional.
- ❌ Record a step the user only "thinks" was run — mark uncertain steps `[unsure]`, only actually-executed commands go in.
- ❌ Generic title like "deploy script" — the slug must be specific.
- ❌ Mix two procedures into one runbook — split them.

## Since

Introduced in [[v0.11.0]].

## See also

- [[Commands]] (aggregate)
- [[Kasi-Knowledge-List]] — browse and replay what this command writes
- [[Kasi-Devopt]] — `runbook` sub-mode uses the same storage
- [[Gravity Pattern]] — promotion path to Centerlite
