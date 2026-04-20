---
description: Build .kasidit/ knowledge structure for current project
---

Scaffold the `.kasidit/` directory with project-specific knowledge files.

**Creates:**
```
.kasidit/
├── INDEX.md              # file paths + one-line purpose
├── RELATIONS.md          # module relationship diagram
├── MEMORY.md             # user-confirmed project facts
├── PATTERNS.md           # project-specific code patterns
├── CHECKLISTS/           # scan checklists per domain
│   └── (copy relevant ones from skill)
└── knowledge/            # version-specific cached docs
    └── (populated on demand)
```

**Flow:**
1. Detect stack (composer.json, package.json, requirements.txt, go.mod, etc.)
2. Detect framework (Laravel, Django, React, Express, etc.)
3. Scan project structure — map controllers, models, services
4. Ask user to confirm/correct detected stack
5. Generate INDEX.md from actual file structure
6. Copy matching CHECKLISTS from skill library
7. Seed PATTERNS.md with detected conventions (naming, error handling, DB patterns)
8. Create empty MEMORY.md (grows via `remember` command)

**After scaffold:**
- Show summary of what was created
- Suggest next mission (`/kasi-review` or `/kasi-security`)
- Remind user: `.kasidit/` is source of truth, edit freely

**Rules:**
- Don't overwrite existing `.kasidit/` without asking
- If stack unclear, ask before generating
- Keep INDEX.md as pointers only, not content
