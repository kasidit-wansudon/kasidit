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

1. **(v0.10) Mode question** — type `1`, `2`, or `3`:
   ```
   1. router    — thin classifier (recommended)
   2. lite      — Rule 1 + Rule 11 always-on
   3. full      — full framework always-on
   ```
   Anything not `1`/`2`/`3` falls back to `1`. Saved to `.kasidit/config.json`. See [[Kasi-Mode]] for what each level loads.
2. Detect stack from `composer.json` / `package.json` / `requirements.txt` / `go.mod` / `Cargo.toml`. If ambiguous → ask.
3. `/kasi-scaffold` — build `.kasidit/` structure.
4. Gravity pull — if `~/.claude/skills/kasidit/center/checklists/` has stack matches, invoke `/kasi-pull all-for <stack>`. One batch confirm.
5. `/kasi-docs` — fetch version-matched official docs, cache to `.kasidit/knowledge/`.
6. Seed `.kasidit/MISSION.md`.
7. Light `/kasi-review` on a user-picked module (skippable).
8. Append privacy guard to `.gitignore` (skipped on `dry-run`).
9. Register `SessionStart` hook + append guidance to `CLAUDE.md`.
10. Print summary + suggest next mission.

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

Introduced in [[v0.9.2]]. v0.10 added the Mode question at step 1 (digit-only input, `1`=router default).

## See also

- [[Commands]] (aggregate)
- [[Gravity-Pattern]]
- [[Kasi-Mode]]
- [[Kasi-Scaffold]]
- [[Kasi-Pull]]
- [[v0.10.0]]
