---
description: Security audit mission with checklist-driven scanning
---

Run a security audit using Kasidit discipline.

**Flow:**
1. Detect stack (PHP / Node / Python / etc.) from project files
2. Load matching security checklist from `.kasidit/CHECKLISTS/`:
   - `security-php.md` for PHP
   - `security-node.md` for Node.js
   - `security-python.md` for Python
   - Build new if missing — ask user first
3. Narrow scope — which files/controllers/endpoints?
4. For each scope item, spawn security scan subagent with checklist
5. Collect findings: SQL inject, XSS, path traversal, CSRF, auth bypass, etc.
6. Mandatory verifier pass (remove false positives) — required on Haiku
7. Output with confidence labels `[high|medium|low|unsure]`

**Priority output:**
- 🔴 CRITICAL (immediate)
- 🟠 HIGH (fix soon)
- 🟡 MEDIUM
- 🟢 LOW
- ❓ UNSURE (human review required)

**Rules:**
- Use exact file:line refs — no "somewhere in the codebase"
- [unsure] findings listed separately, never silently guessed
- Do not submit fix patches without user approval — this is scan only
