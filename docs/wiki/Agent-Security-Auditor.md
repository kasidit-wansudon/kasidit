# Agent: security-auditor

> ⚠️ **Deprecated in v0.10.** Merged into [[Agent-Audit-Specialist]]. Invoke as `audit-specialist --focus=security <target>` instead. This file kept for name resolution only; removed in v0.11. No automatic mapping — invoke explicitly.

---

> OWASP / CVE / auth-boundary focused scanner. One file per invocation. Reports raw findings only.

## When to invoke

- Pre-merge security gate on sensitive modules (auth, payments, file upload, admin endpoints)
- Periodic sweep of a specific file
- Main agent runs sibling auditors in parallel across a module
- User asks "is this endpoint safe" with a single file in scope

## What it does

- Loads matching checklist from `.kasidit/CHECKLISTS/security-*.md` ([[Checklists]])
- Reads target file end-to-end
- For each checklist item, searches the file mechanically
- Records findings with:
  - Exact `file:line`
  - Vulnerability type (SQL inject / XSS / path traversal / etc.)
  - Severity: CRITICAL / HIGH / MEDIUM / LOW
  - Confidence: high / medium / low / unsure
  - Template-based fix hint (not invented)

## What it will NOT do

- Emit false positives — prefers `[unsure]` over confident wrong
- Ship fix patches — scan only; main agent decides action
- Reason across files — stays in scope
- Make architectural suggestions (outside role)

## Inputs expected

- Single target file path
- Scope: one file or one module at a time
- Checklist hint (optional — matched automatically)

## Outputs

JSON array of findings:

```json
[
  {
    "file": "path/to/file.php",
    "line": 123,
    "type": "sql_injection",
    "severity": "CRITICAL",
    "confidence": "high",
    "evidence": "$user_input concatenated in raw query",
    "fix_hint": "Use parameterized query with ? placeholders"
  }
]
```

When uncertain, tags `"confidence": "unsure"` with a note on what info would resolve it.

## Tier behavior

Not tier-pinned. Designed to run in parallel as sibling auditors, so Sonnet is typical per-instance; Opus reserved for cross-cutting review via `audit-specialist --focus=quality` (in v0.10) or pre-v0.10 the standalone `code-reviewer` agent.

## Anti-patterns

- ❌ Guessing to appear competent
- ❌ Cross-file reasoning ("this function is unsafe because caller in other file...")
- ❌ Writing the patch instead of the hint
- ❌ Over-reporting — every line flagged "review this" is noise

## Since

Introduced pre-[[v0.9.1]] (early release).

## See also

- [[Master-Orchestrator]]
- [[Multi-Agent-Orchestration]]
- [[Checklists]]
- [[Agent-Code-Reviewer]]
- [[Agent-Bug-Hunter]]
