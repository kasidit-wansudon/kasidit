# Kasidit on thClaws

Kasidit v0.12+ supports [thClaws](https://github.com/thClaws/thClaws) — the native Rust agent harness from ThaiGPT Co. — alongside Claude Code.

This guide is for thClaws users. For Claude Code, see the main [README](../README.md).

---

## What works on thClaws

| Component | Support |
|---|---|
| 21 slash commands (`/kasi-*`) | ✅ Full |
| 8 specialist agents | ✅ Full |
| 15 default checklists | ✅ Full |
| Helper scripts (`build_graph`, `build_struc`) | ✅ Full |
| `SKILL.md` + framework rules | ✅ Full |
| Master Orchestrator + tier-aware rules | ✅ Full (prompt-level) |
| Gravity hub (`~/.config/thclaws/skills/kasidit/center/`) | ✅ Full |
| Hook: `kasi-update-check.sh` (`session_start`) | ✅ Direct port |
| Hook: `kasi-drift-check.sh` (`session_start`) | ✅ Direct port |
| Hook: `kasi-verify.py` (`post_tool_use`) | ⚠️ Partial — fires per-tool, no per-turn aggregation |
| Hook: `kasi-record.py` (`session_end`) | ⚠️ Partial — per-session aggregation, not per-turn |
| Hook: `kasi-route.py` (`UserPromptSubmit`) | ❌ Skipped — thClaws has no equivalent event |
| Hook: `kasi-log.sh` / `kasi-log.py` (`UserPromptSubmit`) | ❌ Skipped — same |

**Net:** ~85% of Kasidit ports cleanly. The 2 skipped hooks are the global prompt-classifier and prompt-log — useful but not load-bearing for the discipline framework. Discipline rules, commands, agents, and checklists all work fully.

---

## Install

```bash
git clone https://github.com/kasidit-wansudon/kasidit.git
cd kasidit
bash plugins/kasidit/install-thclaws.sh
```

The installer:
- Copies the 4 thClaws-compatible hooks to `~/.config/thclaws/hooks/`
- Seeds the Gravity hub at `~/.config/thclaws/skills/kasidit/center/`
- Seeds the 15 default checklists
- Seeds the 4 helper scripts
- Merges hook registrations into `~/.config/thclaws/settings.json`

Idempotent — safe to re-run after updates.

```bash
# Dry-run (preview without writing)
bash plugins/kasidit/install-thclaws.sh --dry-run

# Set initial mode
bash plugins/kasidit/install-thclaws.sh --mode=full

# Skip settings.json merge (hook copy only)
KASIDIT_SKIP_SETTINGS=1 bash plugins/kasidit/install-thclaws.sh
```

---

## Hook event mapping (thClaws → Claude Code)

| Kasidit hook | Claude Code event | thClaws event | What changes |
|---|---|---|---|
| `kasi-update-check.sh` | `SessionStart` | `session_start` | none |
| `kasi-drift-check.sh` | `SessionStart` | `session_start` | none |
| `kasi-verify.py` | `PostToolUse` + `Stop` | `post_tool_use` | per-tool only; no end-of-turn aggregation |
| `kasi-record.py` | `Stop` | `session_end` | aggregates over the whole session, not per turn |
| `kasi-route.py` | `UserPromptSubmit` | — | dropped on thClaws; mode classification falls back to user-applied |
| `kasi-log.sh` | `UserPromptSubmit` | — | dropped; prompt logging unavailable |

The `[kasidit-log|pattern|memory|rule]` emit-token protocol still works on thClaws via `kasi-record.py`, but it batches at session end instead of mission end. If you run multiple missions per session, the JSONL writes are coalesced — slight loss of fidelity, no impact on subsequent router behavior on Claude Code.

---

## Uninstall

```bash
# Remove hooks
rm ~/.config/thclaws/hooks/kasi-*.{py,sh}

# Remove Kasidit hook entries from settings.json
python3 -c "
import json, os
p = os.path.expanduser('~/.config/thclaws/settings.json')
with open(p) as f: d = json.load(f)
for evt in ('session_start','post_tool_use','session_end'):
    if evt in d.get('hooks', {}) and 'kasi-' in d['hooks'][evt]:
        del d['hooks'][evt]
with open(p, 'w') as f: json.dump(d, f, indent=2)
"

# Remove Gravity hub (keeps centered checklists for portability)
# rm -rf ~/.config/thclaws/skills/kasidit
```

---

## Differences from Claude Code

1. **No prompt classifier line at turn start.** On Claude Code, `kasi-route.py` injects `[kasidit] kind=... mode=... history=N/M` into the turn context. On thClaws this doesn't run — mode selection is fully manual (`/kasi off|router|lite|full|ultra`).
2. **No global prompt log.** Claude Code's `~/.claude/skills/kasidit/center/logs/YYYY-MM-DD.jsonl` is not populated under thClaws. `kasi-search` still works on `.kasidit/knowledge/`, but no cross-project prompt history.
3. **`kasi-verify.py` runs more often.** On Claude Code it fires twice (post-tool + Stop). On thClaws it fires once per tool — same end signal, different cadence. If you see verification messages mid-turn instead of end-of-turn, that's why.
4. **`kasi-record.py` batches.** Per-session JSONL write instead of per-turn. The store is the same JSONL; consumer code does not need to change.

---

## Recommended workflow on thClaws

1. Run `/kasi-init` (or `/kasi-scaffold`) on a new project to seed `.kasidit/`.
2. Use `/kasi router|lite|full|ultra` to set framework intensity for the session — Claude Code's auto-classification is not running.
3. Run `/kasi-fix`, `/kasi-review`, `/kasi-backend`, `/kasi-graph` etc. as documented.
4. The Master Orchestrator Rule + tier-aware behavior is enforced by `SKILL.md` (prompt-level convention), same as on Claude Code.

---

## Compatible runtimes summary

| Runtime | Install command | Hook coverage |
|---|---|---|
| Claude Code | `bash plugins/kasidit/install.sh` | 5/5 hooks (full) |
| thClaws | `bash plugins/kasidit/install-thclaws.sh` | 4/5 hooks adapted, 1 skipped (degraded mode) |

---

## Why the gap

thClaws's hook model is shell-snippet based on lifecycle events (`pre_tool_use`, `post_tool_use`, `session_start`, `session_end`, etc.). Claude Code's hook model includes a `UserPromptSubmit` event that fires per turn — Kasidit's prompt classifier (`kasi-route.py`) and global prompt log (`kasi-log.sh`) ride on this. thClaws does not currently expose a per-turn pre-LLM hook, so these two pieces have no port target.

If thClaws adds a `pre_turn` or `user_prompt_submit` event in a later release, both hooks port over with minimal change.

---

## Related

- [thClaws repository](https://github.com/thClaws/thClaws) — the runtime
- [thClaws hooks chapter](https://github.com/thClaws/thClaws/blob/main/user-manual/ch13-hooks.md)
- [Kasidit main README](../README.md)
- [Kasidit SKILL.md](../plugins/kasidit/skills/kasidit/SKILL.md) — full framework spec
