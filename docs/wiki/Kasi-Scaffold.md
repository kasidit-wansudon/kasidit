# /kasi-scaffold

> Build the `.kasidit/` knowledge structure for the current project — stack-detected, checklist-seeded.

## Usage

```
/kasi-scaffold             # detect stack, generate .kasidit/
```

## What it does

- Detects stack via `composer.json` / `package.json` / `requirements.txt` / `go.mod` / `Cargo.toml`.
- Detects framework (Laravel, Django, React, Express, Vue, etc.).
- Scans project structure — maps controllers, models, services.
- Creates `.kasidit/INDEX.md`, `RELATIONS.md`, `MEMORY.md`, `PATTERNS.md`, `CHECKLISTS/`, `knowledge/`.
- Copies matching CHECKLISTS from the skill library.
- Seeds `PATTERNS.md` with detected conventions (naming, error handling, DB access).

## Directory created

```
.kasidit/
├── INDEX.md              # file paths + one-line purpose
├── RELATIONS.md          # module relationship diagram
├── MEMORY.md             # user-confirmed project facts
├── PATTERNS.md           # project-specific code patterns
├── CHECKLISTS/           # scan checklists per domain
└── knowledge/            # version-specific cached docs
```

## Flow

1. Detect stack from dependency manifests.
2. Detect framework.
3. Scan project structure (controllers / models / services).
4. Ask user to confirm or correct detected stack.
5. Generate `INDEX.md` from the actual file tree.
6. Copy matching CHECKLISTS from the skill library.
7. Seed `PATTERNS.md` with detected conventions.
8. Create empty `MEMORY.md` — grows via the `remember` shorthand.

## After scaffold

- Summary of what was created.
- Suggest next mission ([[Kasi-Review]] or [[Kasi-Security]]).
- Reminder that `.kasidit/` is the source of truth — user can edit freely.

## When to use

- Standalone scaffold of an existing project (when `/kasi-init` full chain is overkill).
- Re-seeding after an accidental delete of `.kasidit/`.
- Manually bootstrapping on a branch where auto-invoke hook is not wanted.

## When NOT to use

- When `.kasidit/` already exists — do not overwrite without asking.
- Unclear stack — ask before generating.
- Full bootstrap is needed — use [[Kasi-Init]] which chains scaffold + docs + review + hook.

## Anti-patterns

- Overwriting existing `.kasidit/` without confirmation.
- Writing full content into `INDEX.md` — it stays pointers only.
- Guessing the stack instead of asking the user.

## Since

Introduced in [[v0.1.0]].

## See also

- [[Commands]] (aggregate)
- [[Gravity-Pattern]]
- [[Kasi-Init]]
- [[Checklists]]
