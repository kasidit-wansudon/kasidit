#!/usr/bin/env python3
"""
kasidit-record.py — Stop / SubagentStop / PostToolUse hook

Incremental backend save. AI emits tiny structured lines at mission end or
pattern discovery; this hook parses them out of assistant text and appends
to the appropriate backend store. Cost per mission: ~20-50 tokens on AI side.
Compounds into a rich router memory and pattern library over time.

Recognised emit formats (AI prints these as plain text in final output):

  [kasidit-log] kind=<kind> mode=<mode> turns=<n> outcome=<pass|fail|partial>
  [kasidit-pattern] name=<slug> file=<path> note=<short>
  [kasidit-memory] fact=<short-sentence>
  [kasidit-rule] scope=<project|global> rule=<short>

Lines are extracted by this hook to append to backend JSONL stores. They
remain visible in the assistant output as harmless telemetry breadcrumbs
(not removed from context).

Storage:
  route-memory.jsonl    ← [kasidit-log]
  patterns.jsonl        ← [kasidit-pattern]
  memory.jsonl          ← [kasidit-memory]
  rules.jsonl           ← [kasidit-rule]  (scope=project writes .kasidit/rules.jsonl)
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

CENTER = Path(os.environ.get("KASIDIT_CENTER",
    os.path.expanduser("~/.claude/skills/kasidit/center")))

EMIT_RE = re.compile(
    r"\[kasidit-(log|pattern|memory|rule)\]\s+(.+?)(?=$|\n)",
    re.MULTILINE,
)

KV_RE = re.compile(r"(\w+)=((?:\"[^\"]*\")|(?:\S+))")


NUMERIC_KEYS = {"turns", "tokens", "rounds", "n"}
MODE_ALIAS = {"mode": "mode_used"}


def parse_kv(body: str) -> dict:
    out = {}
    for m in KV_RE.finditer(body):
        k, v = m.group(1), m.group(2)
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        else:
            v = v.rstrip(".,;:")
        if k in NUMERIC_KEYS:
            try:
                v = int(v)
            except ValueError:
                try:
                    v = float(v)
                except ValueError:
                    pass
        k = MODE_ALIAS.get(k, k)
        out[k] = v
    return out


def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **record}
    with path.open("a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


_PROJECT_KASIDIT: Optional[Path] = None


def _project_kasidit_dir() -> Path:
    """Resolve the project-scope .kasidit dir. Prefers the value set by main()
    (derived from payload cwd); falls back to env var or current working dir."""
    if _PROJECT_KASIDIT is not None:
        return _PROJECT_KASIDIT
    return Path(os.environ.get("KASIDIT_PROJECT_DIR",
        os.path.join(os.getcwd(), ".kasidit")))


def route_store(kind: str, scope: str) -> Path:
    if kind == "log":
        return CENTER / "route-memory.jsonl"
    if kind == "pattern":
        return CENTER / "patterns.jsonl"
    if kind == "memory":
        return CENTER / "memory.jsonl"
    if kind == "rule":
        if scope == "project":
            return _project_kasidit_dir() / "rules.jsonl"
        return CENTER / "rules.jsonl"
    return CENTER / "misc.jsonl"


def main():
    global _PROJECT_KASIDIT
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return

    cwd = payload.get("cwd") or os.environ.get("KASIDIT_PROJECT_DIR") or os.getcwd()
    # If KASIDIT_PROJECT_DIR is set, it already points at the .kasidit dir
    # directly (per original semantics); otherwise append ".kasidit".
    if os.environ.get("KASIDIT_PROJECT_DIR"):
        _PROJECT_KASIDIT = Path(os.environ["KASIDIT_PROJECT_DIR"])
    else:
        _PROJECT_KASIDIT = Path(cwd) / ".kasidit"

    text = payload.get("assistant_text") or payload.get("text") or ""
    if "[kasidit-" not in text:
        return

    appended = 0
    for m in EMIT_RE.finditer(text):
        kind = m.group(1)
        body = m.group(2).strip()
        kv = parse_kv(body)
        scope = kv.pop("scope", "global")
        target = route_store(kind, scope)
        try:
            append_jsonl(target, kv)
            appended += 1
        except Exception:
            continue

    if appended:
        print(f"[kasidit-record] +{appended} backend entries saved")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
