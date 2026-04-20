---
description: Semantic search over .kasidit/knowledge/ using local embeddings
---

Semantic search through project knowledge notes.

**Setup (one-time):**
```bash
python3 ~/.claude/skills/kasidit/embedding/embed_build.py
```

**Search:**
```bash
python3 ~/.claude/skills/kasidit/embedding/embed_search.py "<query>"
```

**When to use:**
- Before answering, check if project has relevant cached knowledge
- When user asks "have we seen this before?"
- When `.kasidit/knowledge/` is large (>20 files)

**Integration flow:**
1. User asks question
2. AI runs: `kasi-search "keywords from question"`
3. AI reads top 3 results
4. If relevant knowledge found → answer grounded in that
5. If no relevant → proceed without

**Rules:**
- Search returns chunks, not full files
- AI must read full source file if chunk is relevant
- Cite source: "Based on .kasidit/knowledge/auth-flow.md..."
- Don't over-rely on top-1 — check top 3
- If semantic match is weak (score <0.3), ignore and proceed

**Fallback:**
If embeddings not built, fall back to grep:
```bash
grep -r "keyword" .kasidit/knowledge/
```
