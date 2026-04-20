---
description: Launch code review mission with Kasidit discipline
---

Start a code review mission using Kasidit framework.

**Flow:**
1. Narrow scope — ask user which module/file/commits to review
2. Detect domain — backend, UI, security, performance
3. Load matching CHECKLIST from `.kasidit/CHECKLISTS/`
4. Spawn subagents (1 per file for Haiku, 1 per module for Opus/Sonnet)
5. Each subagent scans mechanically via checklist
6. Main synthesizes findings with `[high|medium|low|unsure]` confidence
7. Output: HIGH/MED/LOW severity buckets + Top-5 actionable

**Rules:**
- Refuse vague scope ("all code", "check everything")
- Demand specific files/modules/commits
- Use mission counter — escalate at 4 rounds (Opus) / 2 rounds (Haiku)
- Never declare victory without runtime evidence
