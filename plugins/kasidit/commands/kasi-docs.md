---
description: Fetch and cache version-matched official documentation
---

Documentation retrieval mission.

**Flow:**
1. Detect stack version:
   - `composer.json` (PHP)
   - `package.json` (Node)
   - `requirements.txt` / `pyproject.toml` (Python)
   - `go.mod` (Go)
   - Framework CLI: `artisan --version`, `php -v`, `node -v`
2. User specifies topic or function name
3. Fetch in this priority order:
   - Project source: `grep -r "functionName" vendor/ node_modules/`
   - Official docs at exact version
   - GitHub source at matching release tag
4. Extract specific snippet needed (not full page)
5. Cache to `.kasidit/knowledge/<stack>-<version>-<topic>.md`
6. Output concise answer with source URL + cached path

**Trust hierarchy:**
1. Project source (local, actual)
2. Official docs at project's version
3. Official docs latest
4. GitHub release tag
5. ❌ Stack Overflow (only for keywords)
6. ❌ AI memory for version-specific syntax

**Rules:**
- Never fetch latest docs for old project version
- Version mismatch produces confident wrong code
- If cached file exists, read cache first
- Cache snippet only, not whole page
