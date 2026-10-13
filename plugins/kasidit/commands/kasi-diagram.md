---
description: Interactive diagram mission — soft bridge to Archify (architecture/workflow/sequence/dataflow/lifecycle) with selectable UI language
---

Render a design (Rule 3) as an interactive HTML diagram via [Archify](https://github.com/tt-a1i/archify). Kasidit does **not** bundle Archify — it calls an install in the user's skills dir, auto-installing it on first use. Install fails → fall back to a text diagram.

**Usage:** `/kasi-diagram [type] [--lang <tag>] [subject]`

| Arg | Values |
|-----|--------|
| `type` | `architecture` · `workflow` · `sequence` · `dataflow` · `lifecycle` (ask if missing) |
| `--lang` | any tag from `langs` (e.g. `en`, `th`, `ja`, `zh-CN`) |
| `subject` | what to draw — must be one concrete scope (Rule 1) |

**Bridge script:** `~/.claude/skills/kasidit/scripts/kasi_diagram.mjs`

```bash
node ~/.claude/skills/kasidit/scripts/kasi_diagram.mjs find          # exit 3 = not installed
node ~/.claude/skills/kasidit/scripts/kasi_diagram.mjs ensure        # find, else auto-install (exit 3 = install failed)
node ~/.claude/skills/kasidit/scripts/kasi_diagram.mjs langs         # available UI languages
node ~/.claude/skills/kasidit/scripts/kasi_diagram.mjs render <type> <in.json> <out.html> --lang <tag> [--check]
```

**Flow:**

1. **Detect / install** — run `ensure`. If Archify is missing it runs `npx skills add tt-a1i/archify -g --agent claude-code -y` automatically (needs Node >= 20.12 for the `skills` CLI; picks the newest nvm/Homebrew Node if the current one is older) and tells the user it did so. Exit 3 → install failed: draw a text diagram (Rule 3 default) and show the manual command. Other agents: `ensure --agent <name>`.
2. **Narrow** — one subject, one diagram type. Vague ("diagram the whole project") → numbered options (Rule 1).
3. **Pick language** — resolution order:
   1. `--lang` flag
   2. `.kasidit/config.json` → `{"diagram": {"lang": "<tag>"}}`
   3. otherwise run `langs` and ask with numbered options, e.g.
      ```
      Diagram language?
      1. en (built-in)   2. th (kasidit)   3. zh-CN (built-in)   4. ja   5. other: <list>
      ```
      After the answer, offer once to save it as the project default in `.kasidit/config.json` (merge the key, never overwrite other fields).
   The language controls the viewer UI (legend, toolbar, export menu). Write node/message **labels** in the same language yourself; keep code names, endpoints, framework and product names in English.
4. **Source facts** — build the diagram from real structure, not memory: prefer `.kasidit/RELATIONS.md`, `/kasi-struc` and `/kasi-graph` output, or files actually read this session. Anything not read from source → mark `[assumed]` in a card item or tell the user.
5. **Author JSON** — read `<archify>/references/` and the matching `<archify>/examples/*.<type>.json` before writing. Save to `.kasidit/diagrams/<mission-id>.<type>.json`. Do not paste translation catalogs into it — the bridge injects them.
6. **Render** — `render <type> <json> .kasidit/diagrams/<mission-id>.html --lang <tag> --check`. On validation error, fix exactly what the error names (e.g. message spacing ≥ 28px, missing `meta.output`) and rerun. Same error 3× → hand back to user (Mission Counter).
7. **Report** — output path, language, `verified: kasi_diagram.mjs render ... --check` result. Do not describe the picture at length; the file is the answer.

**Storage:**

```
.kasidit/diagrams/
├── <mission-id>.<type>.json   # authored source — commit this
└── <mission-id>.html          # ~750 KB standalone render — usually gitignore
```

**Languages:** built-in `en`, `zh-CN` (Archify); `th` (Kasidit, `skills/kasidit/locales/th.json`); `de es fr it ja ko pt ru` (Archify `examples/locales`). Add a language by dropping `<tag>.json` into `~/.claude/skills/kasidit/locales/` — all 438 keys, placeholders must match English (the bridge's `validate` step reports mismatches).

**Network:** the bridge sets `ARCHIFY_UPDATE_CHECK_DISABLED=1` unless already set. Do not run `archify brands capture <url>` without user approval — it fetches remote pages.

**When NOT to use:** single-file change, trivial fix, or the user just needs the text arrow diagram. UI mockups still go to Claude Design (`references/ui.md`).
