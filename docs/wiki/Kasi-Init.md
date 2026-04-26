# /kasi-init

> One-shot bootstrap — chains scaffold + pull + docs + review + registers auto-invoke for a new or existing project.

## Usage

```
/kasi-init
/kasi-init skip docs
/kasi-init skip review
/kasi-init no auto-invoke
/kasi-init dry-run
```

## What it does

- Chains the essential Kasidit commands so a project goes from zero to framework-grounded in one invocation.
- Builds `.kasidit/` (INDEX / RELATIONS / MEMORY / PATTERNS / CHECKLISTS / knowledge).
- Pulls stack-matched checklists + knowledge from Centerlite (Gravity pull — one batch confirm).
- Fetches version-matched official docs for the detected stack, caches to `.kasidit/knowledge/`.
- Seeds a blank `.kasidit/MISSION.md` (mission / tier / counter / success criteria).
- Appends `.kasidit/knowledge/*.private.md` + Centerlite log note to `.gitignore` (privacy guard).
- Registers a `SessionStart` hook in `.claude/settings.local.json` so every future session starts grounded.
- Appends a pointer block to project `CLAUDE.md` (or creates it) pointing at `.kasidit/INDEX.md`.

## Flow

1. Detect stack from `composer.json` / `package.json` / `requirements.txt` / `go.mod` / `Cargo.toml`. If ambiguous → ask.
2. `/kasi-scaffold` — build `.kasidit/` structure.
3. Gravity pull — if `~/.claude/skills/kasidit/center/checklists/` has stack matches, invoke `/kasi-pull all-for <stack>`. One batch confirm.
4. `/kasi-docs` — fetch version-matched official docs, cache to `.kasidit/knowledge/`.
5. Seed `.kasidit/MISSION.md`.
6. Light `/kasi-review` on a user-picked module (skippable).
7. Append privacy guard to `.gitignore` (skipped on `dry-run`).
8. Register `SessionStart` hook + append guidance to `CLAUDE.md`.
9. Print summary + suggest next mission.

## When to use

- New project, fresh clone, want the framework wired in one shot.
- Existing project missing `.kasidit/`.
- Onboarding a teammate's machine to the Kasidit workflow.

## When NOT to use

- Shared / production repo you do not own — auto-invoke hook is invasive; ask first.
- `.kasidit/` already exists and you only want to refresh docs — use `/kasi-docs` directly.
- One-off scripts or throwaway sandboxes.

## Tier behavior

- **Opus / Sonnet** — full chain including review step.
- **Haiku** — skips step 6 (review) unless user insists. Haiku review without checklists is weak, and init is the wrong place to discover that.

## Anti-patterns

- ❌ Silent overwrite of existing `.kasidit/` — always ask: skip / merge / abort.
- ❌ Re-registering the global log hook per project (it already lives at user scope).
- ❌ Injecting auto-invoke into shared/production repos without user consent.
- ❌ Running full `/kasi-review` on Haiku during init — defer to a small module or skip.
- ❌ Assuming Laravel / React without stack detection.

## User commands during init

- `skip docs` — omit step 4 (offline or docs already cached).
- `skip review` — omit step 6.
- `no auto-invoke` — scaffold only, no hook registration.
- `dry-run` — print plan, write nothing.

## Since

Introduced in [[v0.9.2]].

## See also

- [[Commands]] (aggregate)
- [[Gravity-Pattern]]
- [[Kasi-Scaffold]]
- [[Kasi-Pull]]
