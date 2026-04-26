# /kasi-search

> Semantic search over `.kasidit/knowledge/` using local embeddings. No network calls.

## Usage

```
python3 ~/.claude/skills/kasidit/embedding/embed_build.py             # one-time build
python3 ~/.claude/skills/kasidit/embedding/embed_search.py "<query>"  # search
```

## What it does

- Builds a local embedding index across `.kasidit/knowledge/`.
- Returns top-k chunks with file path, line range, and similarity score.
- Runs entirely local — no outbound API calls.
- Falls back to `grep -r` if the embedding index is not built.

## Flow

1. User asks a question.
2. AI runs `kasi-search "<keywords>"`.
3. AI reads the top 3 results.
4. If relevant, answer grounds in that cached knowledge with an explicit citation.
5. If semantic score is weak (< 0.3), ignore results and proceed.

## When to use

- Before answering, check whether the project has relevant cached knowledge.
- "Have we seen this before?" lookups during long sessions.
- When `.kasidit/knowledge/` is large (> 20 files) and scanning by hand is slow.

## When NOT to use

- Tiny knowledge base where `grep` is already enough.
- Top-1 match with score < 0.3 — do not force weak signal into the answer.

## Anti-patterns

- Over-relying on top-1 — always consider top 3.
- Quoting a chunk without reading the full source file for context.
- Skipping citation — always cite as `Based on .kasidit/knowledge/<file>.md`.
- Treating low-similarity results as matches.

## Fallback

```
grep -r "keyword" .kasidit/knowledge/
```

Use when embeddings have not been built or the Python environment is unavailable.

## Since

Introduced in [[v0.8.0]].

## See also

- [[Commands]] (aggregate)
- [[Kasi-Docs]]
- [[Kasi-Scaffold]]
