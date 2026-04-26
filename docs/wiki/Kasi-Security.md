# /kasi-security

> Security audit mission — checklist-driven scan for injection, auth, file handling, output, session, crypto issues. Scan only, no fixes.

## Usage

```
/kasi-security <file-or-controller>
/kasi-security <endpoint>
/kasi-security --stack=php|node|python
```

## What it does

- Detects stack from project files and loads matching `CHECKLISTS/security-<stack>.md`.
- If no stack checklist exists, asks to build one before scanning.
- Fans out a security scan subagent per scope item.
- Collects findings across SQL injection, XSS, path traversal, CSRF, auth bypass, crypto, session, file handling.
- Runs a mandatory verifier pass to strip false positives (required on Haiku).
- Emits findings by severity tier with exact `file:line` refs and confidence labels.

## Flow

1. Detect stack (PHP / Node / Python / etc.) from project manifests.
2. Load matching `security-<stack>.md` checklist — build new if missing (ask user first).
3. Narrow scope — which files / controllers / endpoints?
4. Dispatch scan subagents, one per scope item.
5. Collect findings from all checklist categories.
6. Verifier pass — remove plausible-but-wrong matches.
7. Print severity buckets with file:line and confidence.

## Output priority

- CRITICAL — immediate fix.
- HIGH — fix soon.
- MEDIUM — plan and fix.
- LOW — backlog.
- UNSURE — human review required, never silently promoted.

## When to use

- Pre-deploy security gate on new or changed endpoints.
- Auditing a legacy controller before extending it.
- Scheduled security review on auth / payment / file-upload paths.

## When NOT to use

- You want the fix applied — this command is scan-only; hand findings to [[Kasi-Fix]].
- General code quality review — use [[Kasi-Review]].
- Scope "whole app" with no narrowing — refuse and narrow first.

## Tier behavior

- **Opus / Sonnet** — verifier pass is recommended.
- **Haiku** — verifier pass is **mandatory**; without it false-positive rate is too high.

## Anti-patterns

- ❌ Vague refs like "somewhere in the codebase" — always `file:line`.
- ❌ Silently merging `[unsure]` into HIGH — list separately.
- ❌ Auto-applying fix patches — this command scans; fixes go through [[Kasi-Fix]] with user approval.
- ❌ Running without a stack-specific checklist on Haiku.

## Since

Introduced in [[v0.3.0]].

## See also

- [[Commands]] (aggregate)
- [[Checklists]]
- [[Kasi-Review]]
- [[Kasi-Fix]]
