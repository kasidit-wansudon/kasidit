---
description: Bug fix mission with conservative discipline
---

Fix a specific bug using Kasidit conservative fix principles.

**Flow:**
1. Narrow mission — what's the exact bug, expected vs actual?
2. Design before code — show hypothesis + fix location
3. Apply Rule A: Literal fix first — only what issue states
4. Apply Rule B: Match existing pattern in same file
5. Apply Rule C: Solution location — modify existing > create new
6. Apply Rule D: Blast radius check — smallest change
7. Anti-rationalization — refuse "while I'm here" temptations
8. Runtime verify — test, curl, screenshot, or user confirmation

**Output format:**
```
Mission: <one-line statement>
Design: <hypothesis + location>
Fix: <diff with file:line>
Confidence: [high|medium|low|unsure]
Blast radius: N files, M lines
Next: <how to verify>
```

**Rules:**
- Counter max 4 (Opus) / 3 (Sonnet) / 2 (Haiku) before Wave 1
- Never declare done without runtime evidence
- If [unsure], list separately — do not guess
