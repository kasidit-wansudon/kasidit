---
description: Browse stored runbooks and knowledge entries — pick one by number to print "how to do it again".
---

List runbooks and knowledge entries captured by `/kasi-acknowledge` (and other knowledge writers). Pick one by number or slug to replay the steps.

**Sub-modes (first arg, optional):**

| Sub | What it does |
|-----|--------------|
| (none) / `list` | print numbered index of all runbooks, grouped by kind |
| `show <n\|slug>` | print one runbook in full |
| `recent [n]` | last N runbooks by `last_run` (default n=10) |
| `tag <tag>` | filter by tag (e.g. `kas-sass`, `staging`) |
| `kind <kind>` | filter by kind (deploy / migration / incident / setup / release / data / infra) |
| `search <query>` | grep title + tags + context |
| `replay <slug>` | print steps in interactive form, prompt user before each step |
| `archive <slug>` | move runbook to `archive/`, keep INDEX entry |
| `delete <slug>` | remove runbook (asks confirmation) |
| `stats` | counts per kind + tag + freshness summary |
| `stale` | runbooks not run in >90 days (candidates for review) |

If no sub-mode → run `list`.

**Sources scanned (in order):**

1. `.kasidit/knowledge/runbooks/` — project-local (dcenterlite).
2. `~/.claude/skills/kasidit/center/knowledge/runbooks/` — global hub
   (centerlite). Marked `[hub]` in output.
3. `.kasidit/knowledge/*.md` — non-runbook knowledge (auto-conventions, docs
   snippets). Marked `[doc]` in output.

Local entries override hub entries with the same slug (project-specific
takes precedence — `replay` reads local first).

**`list` output:**

```
Runbooks (12 local + 4 hub)

DEPLOY (4)
  1. deploy-kas-sass-staging          last 2026-04-30 · runs 3 · staging,laravel,ssh
  2. deploy-kasion-site-prod          last 2026-04-22 · runs 7 · prod,cloudflare,wrangler
  3. deploy-ai-router-prod            last 2026-04-18 · runs 2 · prod,cloudflare-workers
  4. [hub] deploy-generic-cf-pages    last 2026-03-10 · runs 5 · cloudflare,pages

MIGRATION (3)
  5. migrate-kas-sass-add-quota       last 2026-04-29 · runs 1 · kas-sass,laravel
  6. migrate-mysql-utf8mb4-conversion last 2026-03-12 · runs 1 · mysql8,one-shot

INCIDENT (2)
  7. incident-kas-sass-503-on-deploy  last 2026-04-15 · runs 2 · prod,nginx
  ...

SETUP (2)
  ...

[stale: 2 runbooks not run >90d — see /kasi-knowledge-list stale]

Pick by number, slug, or sub-mode (recent / tag / kind / search / replay).
```

**`show <n|slug>` output:**

Prints the full markdown of the runbook plus a banner:

```
===== RUNBOOK: deploy-kas-sass-staging =====
Source: local · last run 2026-04-30 · runs 3 · confidence [medium]

[full runbook content]

----- ACTIONS -----
- [r] replay this runbook step-by-step
- [u] update with this run
- [a] archive
- [l] link to another runbook
- [b] back to list
```

**`replay <slug>` flow:**

Interactive walkthrough — Kasidit prints one step at a time, waits for user
to confirm before showing the next:

```
Step 1/7 — Connect to staging
  ssh deploy@staging.kasion.dev
  Success: prompt shows `deploy@staging:~$`
  → press [Enter] when done, [s] to skip, [a] to abort
```

**Hard rules (replay):**

- Kasidit never executes commands during replay — it prints and waits.
- User runs each command themselves (matches `/kasi-devopt` discipline:
  deploy commands = user-executed).
- If a command requires sudo / production access → an extra confirmation
  banner appears.
- If `confidence: [low]` or `[unsure]` on the runbook → warn at start of
  replay.

**Filter examples:**

```
/kasi-knowledge-list tag staging
/kasi-knowledge-list kind incident
/kasi-knowledge-list search "rollback"
/kasi-knowledge-list recent 5
```

**`stats` output:**

```
Total runbooks: 16 (12 local + 4 hub)
By kind:
  deploy:    4
  migration: 3
  incident:  2
  setup:     2
  release:   2
  data:      2
  infra:     1
By freshness:
  fresh (≤30d):  9
  warm (31-90d): 5
  stale (>90d):  2
Top tags: staging(6), prod(5), kas-sass(4), cloudflare(3), laravel(3)
```

**`stale` output:**

Lists runbooks not run in >90 days. Suggests:

- Run `/kasi-knowledge-list show <slug>` then `replay` to verify still works.
- Run `/kasi-acknowledge update <slug>` after a fresh run to bump
  `last_run`.
- If procedure deprecated → `/kasi-knowledge-list archive <slug>`.

**Tier rules:**

- **Haiku** — `list`, `show`, `recent`, `tag`, `kind`, `stats`, `stale`,
  `archive`, `delete`. No `search` (semantic ranking needs Sonnet+).
- **Sonnet** — all sub-modes including `replay` walkthrough.
- **Opus** — same + can suggest merging similar runbooks or flag drift
  between hub and local versions.

**Anti-patterns:**

- ❌ Print all runbooks in full on `list` — only the index.
- ❌ Execute `replay` commands automatically — user runs them.
- ❌ Hide hub entries from list — mark `[hub]` so user knows source.
- ❌ Trust stale runbook without warning user.
- ❌ Embed secrets in runbook output (redaction rules from `/kasi-acknowledge`
  carry over — list view should never reveal redacted strings).

**Bridge with other commands:**

- `/kasi-devopt deploy <env>` checks for matching runbook first
  (`deploy-<service>-<env>`) and offers to `replay` it.
- `/kasi-fix` suggests an `incident` runbook if symptoms match a recent
  entry's `## Known issues / quirks` section.
- `/kasi-promote knowledge <slug>` lifts a local runbook to hub
  (Gravity pattern).

**Examples:**

```
/kasi-knowledge-list
/kasi-knowledge-list recent
/kasi-knowledge-list tag prod
/kasi-knowledge-list kind deploy
/kasi-knowledge-list search "kas-sass"
/kasi-knowledge-list show 3
/kasi-knowledge-list show deploy-kas-sass-staging
/kasi-knowledge-list replay deploy-kas-sass-staging
/kasi-knowledge-list stats
/kasi-knowledge-list stale
```
