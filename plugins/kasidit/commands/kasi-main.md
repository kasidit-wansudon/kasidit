---
description: Pinned rules (main.md) — reply language, thinking style — re-sent every prompt, checked at stop
---

Manage the user's pinned rules. Two files, merged (project last):

- Global: `~/.claude/skills/kasidit/center/main.md`
- Project: `.kasidit/main.md` in the current project

Hooks that read them (on by default after install):
- `kasi-main.py` (SessionStart, also after compact) — sends the whole file + onboarding.
- `kasi-route.py` (every prompt) — sends the language rule + `## Always`.
- `kasi-main-check.py` (Stop) — blocks a reply in a script foreign to `reply_language`.
- `kasi-status-nudge.py` (PostToolUse) — on long work, tells the AI to post a short status after `status_every` tool calls (default 8) or `status_after_sec` seconds (default 120) without a word to the user. `status <n|off>` sets `status_every`.

Frontmatter is written only through the CLI, never by hand:

```
python3 ~/.claude/hooks/kasi_mainfile.py set <key> <value> [--project <dir>]
python3 ~/.claude/hooks/kasi_mainfile.py get <key> [--cwd <dir>]
```

**Sub-commands** (argument after `/kasi-main`):

| Arg | Action |
|---|---|
| (none) / `show` | Print both files (or "not set"), current `reply_language`, and which kasi-main hooks are registered in `~/.claude/settings.json` |
| `language <code>` | `set reply_language <code>` (th en es fr de pt it id ms vi zh ja ko ru uk ar he hi) |
| `add <rule>` | Append `- <rule>` under `## Always` of the global file. Ask "global or project?" only if the user hints at a project |
| `context <text>` | Append under `## Context` |
| `allow <script>` / `forbid <script>` | Add to `allow_scripts` / `forbid_scripts` (vietnamese thai han kana hangul cyrillic arabic hebrew devanagari) |
| `import` | Read the project's CLAUDE.md / AGENTS.md, propose the must-follow rules as 3-7 Always lines, write only after the user confirms |
| `onboard` | Re-run onboarding: `set onboarded false` (and clear `reply_language` if the user wants to re-pick) |
| `path` | Print both paths |

**Onboarding** (driven by `kasi-main.py`, first session after install):
1. **Reply language — asked first**, before any other work: one question, 3-4 likely options from the language the user wrote in, plus "other". Save with `set reply_language <code>`.
2. Offer `import` from an existing CLAUDE.md / AGENTS.md.
3. Offer to add one rule of their own (thinking style, tone, conventions).
Then `set onboarded true`. Steps 2-3 are optional — offer once, briefly, after the user's current request.

**Rules:**
- Keep `## Always` at 3-7 short lines. If an add would exceed 7 lines or ~1200 chars, say so and suggest moving detail to `## Context`.
- Never delete or reword an existing rule without the user asking.
- After a change, show the resulting `## Always` block.
- Changes apply from the next prompt (language, Always) or next session/compact (Context) — say so.
