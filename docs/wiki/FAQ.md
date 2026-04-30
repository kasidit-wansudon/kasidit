# FAQ

## General

### What is Kasidit?

A Claude Code plugin that externalizes coding discipline into rules, checklists, and commands. It makes AI coding grounded instead of hallucinated. See [[Home]].

### Does it work on Haiku?

Yes — in fact, Haiku is the tier Kasidit was most designed for. Haiku without scaffolding hallucinates; Haiku with checklists + PATTERNS.md + Centerlite executes faithfully. See [[Model Tiers]].

### Does it phone home?

No. Everything is local filesystem. The prompt log ([[v0.9.2]]) writes to disk only. The embedding layer ([[v0.8.0]]) runs on your machine.

### What gets sent to the model provider?

Whatever you type, plus whatever files the agent loads. No Kasidit-specific telemetry, no usage counters uploaded, no logs exfiltrated. Logs stay in `~/.claude/skills/kasidit/center/logs/`.

## Installation + setup

### How do I install?

See [[Installation]]. Summary (v0.10): install plugin → run `bash ~/.claude/plugins/marketplaces/kasidit/plugins/kasidit/install.sh` (handles all 5 backend hooks + `settings.json` merge + Gravity hub seed) → run `/kasi-init` per project.

### Do I have to install the backend hooks?

No — the plugin still works without them. You lose:
- **router** memory (`route-memory.jsonl`) — no learning from past missions
- **runtime verifier** — no automatic downgrade of unverified `[high]` claims
- **incremental backend save** — patterns / memory / rules emit lines have nowhere to go
- **prompt log** — cross-session history not captured

Hooks are stdlib-only (Python 3.9+, no extra deps). Recommended unless your environment blocks them.

### What's new in v0.10?

See [[v0.10.0]]. Five things:
1. **Backend hooks** — runtime enforcement layer (route, verify, record, update-check, drift-check).
2. **Mode gate** (`/kasi off|router|lite|full|ultra`) — control framework load depth per session.
3. **`audit-specialist`** — single agent merges `code-reviewer` + `security-auditor` + `perf-profiler` via `--focus=`.
4. **`install.sh`** — canonical installer replaces manual copy + settings edit.
5. **12 default checklists** — PHP / Node / Python / Go × code-review / security / perf, seeded at install.

### Does `/kasi-init` modify my repo?

Yes — it creates `.kasidit/` in the project root and optionally adds a `.claude/settings.local.json` + a pointer in `CLAUDE.md`. It also adds `.kasidit/` and `center/logs` to `.gitignore`. All changes are confirmed with you first.

### Can I uninstall cleanly?

Yes. `/plugin uninstall kasidit`, remove the hook block from `settings.json` (or restore from `settings.json.kasidit-backup-<ts>`), `rm -rf ~/.claude/skills/kasidit/center/` and `.kasidit/` per project. See [[Installation#Uninstall]].

### How do I update from v0.9 to v0.10?

```
/plugin marketplace update kasidit
/plugin install kasidit@kasidit
bash ~/.claude/plugins/marketplaces/kasidit/plugins/kasidit/install.sh
```

The installer is idempotent — safe to re-run. It backs up `settings.json` before merging. Old `kasi-*` standalone command files at `~/.claude/commands/` (from earlier installs) coexist with the new `kasidit:*` namespaced commands; clean them manually if drift bothers you.

`SKILL.md` at `~/.claude/skills/kasidit/SKILL.md` is **not auto-replaced** by `install.sh`. To pick up the v0.10 framework rules manually:
```bash
cp ~/.claude/plugins/marketplaces/kasidit/plugins/kasidit/skills/kasidit/SKILL.md \
   ~/.claude/skills/kasidit/SKILL.md
```

### Where do I ask questions vs report bugs?

- **Bugs** (the plugin misbehaves, hooks fail, install errors) → [Issues](https://github.com/kasidit-wansudon/kasidit/issues)
- **Questions** (how do I X, why does it Y, best practice for Z) → [Discussions Q&A](https://github.com/kasidit-wansudon/kasidit/discussions)
- **Ideas / feature requests** → [Discussions Ideas](https://github.com/kasidit-wansudon/kasidit/discussions)
- **Show & tell** (your `.kasidit/` config, custom checklists, war stories) → [Discussions Show & Tell](https://github.com/kasidit-wansudon/kasidit/discussions)
- **Security disclosures** → see [SECURITY.md](https://github.com/kasidit-wansudon/kasidit/blob/main/SECURITY.md) (do **not** post in public Issues)

## Behavior

### Why does the agent refuse my mission?

Kasidit refuses missions that are too vague (triggers: "check", "review", "improve", "ดูดี", etc.). It will give you a numbered list of narrower options. Pick one. See [[v0.3.0#Vague-mission-detection]].

### Why does the main agent keep delegating?

In [[v0.9.1]], the master agent is forbidden from executing strong work. It narrows, dispatches a specialist, synthesizes. This prevents context pollution and improves output quality, especially on mixed missions.

### Why all these `[high] [medium] [unsure]` tags?

Confidence labels. Mandatory on Haiku, recommended on Sonnet/Opus for security + architecture work. `[unsure]` items are **always** listed separately — never silently guessed. See [[v0.3.0#Confidence-labels]].

### Why does it keep asking me to hard-refresh?

UI Override Mode ([[v0.2.0]]) treats cache as part of runtime. Every CSS/JS change bumps a version query and requires you to confirm the new version loaded in DevTools. This catches the single most common UI-fix failure mode: the fix worked; the browser showed the old file.

### Why does it run `git log` before fixing my bug?

Rule 2.6 from [[v0.7.4]]. Most "new" bugs are re-regressions of bugs fixed before. The earlier fix's commit message is the shortest path to the cause. Skipping the git log step produces fixes that re-introduce bugs.

## Gravity ([[v0.9.2]])

### What is the difference between Centerlite and Dcenterlite?

- **Centerlite** is global — one hub at `~/.claude/skills/kasidit/center/` shared across every project.
- **Dcenterlite** is per-project — `<project>/.kasidit/`, source of truth for the project.

See [[Gravity Pattern]].

### Does anything auto-sync between them?

Only **prompt logs** flow automatically (one way: prompt → Centerlite). Promotions and pulls are **always user-confirmed**. No noise gets into the hub by accident.

### Can I share my Centerlite across machines?

Not automatically. You can `rsync ~/.claude/skills/kasidit/center/` manually, but review PII in `center/logs/` first. A PII-filtered, git-backed shared Centerlite is on the roadmap (post v0.9.2).

### What if I want a clean Centerlite?

`rm -rf ~/.claude/skills/kasidit/center/*` — it rebuilds on next use. Your project `.kasidit/` directories are unaffected.

## Claude Design ([[v0.9.0]])

### Do I need Claude Design?

Only for mockup / wireframe / deck / one-pager missions. Without access, Kasidit still works — it just can't handle the visual-prototype step directly. You can substitute screenshots / CSS values as visual targets.

### Why won't Haiku hand-code my mockup?

Haiku hand-coded mockups are consistently wrong in the author's observation. Always route to Claude Design. Opus may hand-code small internal sketches.

## Troubleshooting

### The log hook doesn't fire

1. Validate JSON: `python3 -m json.tool ~/.claude/settings.json > /dev/null`
2. Check script is executable: `ls -la ~/.claude/hooks/kasidit-log.sh`
3. Check python3 is on PATH: `which python3`
4. Test manually: `echo '{"prompt":"x"}' | bash ~/.claude/hooks/kasidit-log.sh`

### `/kasi-sync` shows "conflict" — which wins?

Neither, automatically. Kasidit refuses to pick a winner on conflict. Resolve manually (open both files, merge, save). Then re-run `/kasi-sync`.

### The agent keeps spawning subagents — is that expensive?

Each subagent call consumes tokens. Subagents are used when context isolation matters more than token cost (large reviews, refactors). For small missions, single-agent execution is used. You can force single-agent with narrower mission framing.

### Can I force a tier?

Yes: `tier opus | sonnet | haiku` in any message.

## Contributing

### How do I report a bug?

Open an issue at https://github.com/kasidit-wansudon/kasidit/issues with the mission, the failure, and the `.kasidit/MISSION.md` contents if available.

### How do I add a checklist for a new stack?

Write it, test it on a real project, then `/kasi-promote checklist <name>` to Centerlite. If it is useful enough, open a PR to add it to `plugins/kasidit/CHECKLISTS/`.

### How do I add a specialist agent?

See `plugins/kasidit/agents/` for the format. Each agent is a single markdown file with mission, inputs, output shape, and anti-patterns. Open a PR.

## See also

- [[Home]]
- [[Installation]]
- [[Commands]]
