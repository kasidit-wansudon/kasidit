# Confidence Labels

> Tag every non-trivial claim. `[unsure]` never gets silently guessed.

Introduced in [[v0.3.0]] as Rule 11. Mandatory on Haiku, recommended on Sonnet/Opus for security, architecture, and cross-file findings.

## The four labels

| Label | Meaning | How to earn it |
|---|---|---|
| `[high]` | verified by running code, reading source, or official docs | runtime confirmed / source cited / docs linked |
| `[medium]` | strong pattern match from codebase, not yet runtime-verified | same pattern seen 2+ times in the same repo, behavior inferred not measured |
| `[low]` | inferred from naming/comments, not actual behavior | best guess from symbols, no behavioral evidence |
| `[unsure]` | do not know | missing context, ambiguous code, conflicting signals |

## The rule

> `[unsure]` items are listed **separately** for user decision. Never silently guessed.

A finding with no label is a finding without provenance. On Haiku, that is treated as a framework violation. The label is the *claim to truth* the agent is making.

## Output format

```
🔴 HIGH severity
[high] SalesController.php:3708 SQL injection — $var concat in raw()
       Fix: use ? placeholder with execute([$var])

[high] FinanceController.php:894 path traversal — $_FILES direct use
       Fix: basename() before fopen; whitelist upload dir

🟡 MED severity
[medium] PoController.php:113 N+1 query
         Pattern match; not profiled. Profile before optimize.

❓ UNSURE — requires user review
[unsure] NewWmsController.php:531 possible race condition
         Need concurrency context. User to confirm transaction boundary.
```

Severity (HIGH/MED/LOW) is a *separate* axis from confidence. A finding can be `[high] LOW severity` or `[unsure] HIGH severity`. Both dimensions matter.

## Per-tier enforcement

- **Opus** — should tag on security, architecture, and cross-file findings. Trivial findings may skip tags.
- **Sonnet** — same as Opus; tag more aggressively for security-critical output.
- **Haiku** — **mandatory on every non-trivial finding**. Missing tag = framework violation. `[unsure]` items must be listed separately, never silently guessed. The verifier pass (see [[Checklists]]) re-reads findings and lowers confidence where unjustified.

## Why this matters

Observed pattern before Rule 11: agents produced 20 findings with identical assertive tone. User accepted all as equally valid. ~40% turned out wrong.

With confidence labels: agents produce the same 20 findings, but user can triage — act on `[high]` immediately, defer `[medium]` to profiling, escalate `[unsure]` to decision. False-positive cost drops; signal-to-noise rises. This was the single largest quality lift on Haiku-class models observed during framework validation ([[v0.7.4]]).

## Downgrading labels

Agents self-downgrade when a pattern's confidence drops:

- Contradictory evidence found → downgrade `[high]` → `[medium]`
- Pattern match count drops below 2 → `[medium]` → `[low]`
- Still cannot determine after retry → `[low]` → `[unsure]`

Upgrading requires new evidence (new test, new doc citation, runtime confirmation). Label inflation is an anti-pattern.

## Anti-patterns

- ❌ Stripping `[unsure]` to make a report look confident
- ❌ Tagging `[high]` without citing source / file:line / doc URL
- ❌ Mixing severity and confidence into one tag (`[critical]`, `[likely]` — both lose information)
- ❌ Silently dropping `[unsure]` items — user must see them to decide
- ❌ On Haiku, producing any non-trivial finding without a label

## v0.10 runtime verification

`kasidit-verify.py` (PostToolUse + Stop hooks) cross-checks `[high]` claims against actual tool calls in the same turn:

- A `[high]` finding pointing at `file:line` with **no `Read` of that file** in the turn → downgrade notice printed
- A `[high]` claim with **no `Bash` / runtime confirmation** for "verified" wording → downgrade notice
- "Delegating to specialist" claim paired with direct `Edit` / `Write` / `Bash` → master orchestrator violation flagged

The hook does not modify the AI output — it logs and prints, the AI sees the flag in subsequent turns and adjusts. See [[Backend-Hooks#kasidit-verify]] for the payload contract.

This is the first runtime layer enforcing label discipline. Prior versions relied entirely on prompt-level convention.

## See also

- [[Checklists]] — the verifier pass enforces label discipline
- [[Master-Orchestrator]] — synthesizes labeled findings from specialists
- [[Backend-Hooks]] — `kasidit-verify` runtime check (v0.10)
- [[Model-Tiers]] — which tier must tag
- [[v0.3.0]] — introduction
- [[v0.10.0]] — runtime verification added
- [[v0.7.4]] — framework validation data
