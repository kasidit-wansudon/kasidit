---
description: Show current mission state, counter, and context usage
---

Output current Kasidit session state.

**Show:**
- Current mission (what / scope)
- Mission counter (rounds failed)
- Domain detected (backend / UI / review / audit)
- Tier (Haiku / Sonnet / Opus)
- Mode (interactive / batch)
- `.kasidit/` contents summary
- Pending items / blockers
- Last action taken
- Next suggested step

**Format:**
```
Mission: <narrow goal>
Domain: <detected>
Tier: <model>
Mode: interactive | batch
Counter: N/4 (N/2 Haiku)

.kasidit/ status:
  - INDEX.md: exists | missing
  - CHECKLISTS/: N files
  - MEMORY.md: N lines
  - knowledge/: N cached docs

Last: <last action>
Next: <suggested>
Blocker: <if any>
```

**Use when:**
- Long session, lost track
- Switching contexts
- Before `/clear` to snapshot state
- Debugging why Kasidit behavior seems off
