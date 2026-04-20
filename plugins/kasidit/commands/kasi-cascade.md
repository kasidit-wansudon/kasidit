---
description: Tier cascade orchestration — Opus plans, Sonnet works, Haiku greps
---

Launch Kasidit tier cascade for complex mission.

**When to use:**
- Mission spans >3 files
- Mission has >5 distinct subtasks
- Cross-file refactor
- Multi-module bug fix

**When NOT to use:**
- Single-file edit
- One-line fix
- Trivial task (just use `/kasi-fix`)

**Flow:**
1. Opus decomposes mission into subtasks (plan phase)
2. Workers execute by type:
   - grep → Haiku
   - read → Haiku
   - work → Sonnet
   - nested plan → Opus
3. Opus verifies all outputs
4. Merge or escalate

**Execution paths:**
- **A. In Claude Code (simulated):** explain cascade plan to user, they run subtasks manually via `claude --model X`
- **B. Bash orchestrator:** `./orchestration/tier_cascade.sh "mission"`
- **C. Python API:** `python orchestration/python/orchestrator.py "mission"` (requires ANTHROPIC_API_KEY)

**Cost (Path B/C):**
- Typical: $0.20-0.50 per mission
- Compare all-Opus: 5-10× more expensive

**Output:**
- Plan JSON
- Per-subtask output files
- Final git diff
- Verifier verdict JSON

**Exit codes:**
- 0 = PASS (merge recommended)
- 2 = FAIL (review + retry)
- 3 = UNSURE (user review required)

**Rules:**
- Planner MUST output valid JSON (no prose)
- Workers respect tier constraints
- Verifier is last gate — do not skip
