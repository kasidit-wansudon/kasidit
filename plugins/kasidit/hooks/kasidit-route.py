#!/usr/bin/env python3
"""
kasidit-route.py — UserPromptSubmit hook

Classify incoming user message + query route-memory → inject 1-line recommendation
into context. Keeps LLM side dumb and thin. All logic runs here.

Output (stdout, appended to turn context by Claude Code hook system):
  [kasidit] kind=<kind> mode=<recommended> history=<n_pass>/<n_total> avg_turns=<x>

If no history or off-topic → output nothing. Zero token cost on quiet path.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from collections import defaultdict
from typing import List, Optional, Tuple

CENTER = Path(os.environ.get("KASIDIT_CENTER",
    os.path.expanduser("~/.claude/skills/kasidit/center")))
MEM_FILE = CENTER / "route-memory.jsonl"

KEYWORDS = {
    "security": ("security-audit", "ultra"),
    "owasp": ("security-audit", "ultra"),
    "cve": ("security-audit", "ultra"),
    "migration": ("migration", "ultra"),
    "audit": ("audit", "full"),
    "review": ("review", "full"),
    "refactor": ("refactor", "full"),
    "perf": ("perf", "full"),
    "n+1": ("perf", "full"),
    "bug": ("bug-fix", "lite"),
    "fix": ("bug-fix", "lite"),
    "error": ("bug-fix", "lite"),
    "slow": ("perf", "lite"),
    "ui": ("ui", "lite"),
    "css": ("ui", "lite"),
    "layout": ("ui", "lite"),
    "rename": ("refactor-rename", "router"),
    "question": ("question", "router"),
    "explain": ("question", "router"),
    "what is": ("question", "router"),
    "how do i": ("question", "lite"),
}


def classify(msg: str) -> Tuple[str, str]:
    m = msg.lower()
    for kw, (kind, mode) in KEYWORDS.items():
        if re.search(r'\b' + re.escape(kw) + r'\b', m):
            return kind, mode
    return "unclassified", "router"


def load_memory() -> List[dict]:
    if not MEM_FILE.exists():
        return []
    out = []
    with MEM_FILE.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def shortest_successful_mode(kind: str, records: List[dict]) -> Optional[dict]:
    matches = [r for r in records if r.get("kind") == kind and r.get("outcome") == "pass"]
    if not matches:
        return None
    by_mode = defaultdict(list)
    for r in matches:
        by_mode[r.get("mode_used", "router")].append(r)
    ranked = []
    for mode, rs in by_mode.items():
        avg_turns = sum(r.get("turns", 0) for r in rs) / len(rs)
        ranked.append({"mode": mode, "n_pass": len(rs), "avg_turns": avg_turns})
    ranked.sort(key=lambda x: (x["avg_turns"], -x["n_pass"]))
    return ranked[0]


def main():
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    msg = payload.get("prompt", "") or " ".join(sys.argv[1:])
    if not msg.strip():
        return

    kind, default_mode = classify(msg)
    records = load_memory()
    best = shortest_successful_mode(kind, records)

    if best and best["n_pass"] >= 3:
        total = sum(1 for r in records if r.get("kind") == kind)
        line = (f"[kasidit] kind={kind} mode={best['mode']} "
                f"history={best['n_pass']}/{total} avg_turns={best['avg_turns']:.1f}")
    elif kind == "unclassified":
        return
    else:
        line = f"[kasidit] kind={kind} mode={default_mode} [low-history]"

    print(line)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
