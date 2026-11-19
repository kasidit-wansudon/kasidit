---
reply_language:
onboarded: false
forbid_scripts:
allow_scripts:
status_every: 8
status_after_sec: 120
---
# main.md — pinned rules

Rules here come before everything else, in every session.
- `reply_language` (frontmatter) is set on first use — Kasidit asks you. It adds
  the language rule automatically and blocks replies in other scripts.
- `## Always` is re-sent on every prompt (keep it 3-7 short lines).
- `## Context` is sent at session start and after every compact.
- `allow_scripts` lets a script through, e.g. `han` for Chinese file names.
- `status_every` / `status_after_sec`: on long work, after this many tool calls
  or seconds without a word to you, the AI is told to post a short status. 0 = off.
A project can add `.kasidit/main.md` on top of this file. Manage it with /kasi-main.

## Always
- One mission at a time; narrow vague requests before acting.
- Runtime is the judge: say what verified a claim, or mark it [unverified].

## Context
- Add longer preferences here: tone, thinking style, team conventions.
