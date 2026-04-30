#!/usr/bin/env python3
"""
kasidit-verify.py — PostToolUse / Stop hook

Scan assistant output for confidence labels ([high]/[medium]/[low]/[unsure])
and cross-check against the tool calls made in the same turn.

Rule: a [high] claim about a file/line must have at least one Read or Bash
tool call that plausibly inspected it. Otherwise downgrade to [medium] by
emitting a context message.

Output: if any mismatch, print a single line to stdout:
  [kasidit-verify] downgraded N [high] → [medium] — no matching Read/Bash call

No output on clean pass.

Zero dependency beyond stdlib.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

CENTER = Path(os.environ.get("KASIDIT_CENTER",
    os.path.expanduser("~/.claude/skills/kasidit/center")))
LOG_FILE = CENTER / "verify.log"

LABEL_RE = re.compile(r"(?:^|\s)\[(high|medium|low|unsure)\]\s+([^\s:`]+(?::\d+)?)", re.IGNORECASE | re.MULTILINE)


def extract_labels(text: str) -> List[Tuple[str, str]]:
    return [(m.group(1).lower(), m.group(2)) for m in LABEL_RE.finditer(text)]


def files_touched_by_tools(tool_events: List[dict]) -> set:
    out = set()
    for e in tool_events:
        name = e.get("tool_name") or e.get("name") or ""
        inp = e.get("tool_input") or e.get("input") or {}
        if name in ("Read", "Edit", "Write"):
            p = inp.get("file_path") or ""
            if p:
                out.add(os.path.basename(p))
                out.add(p)
        elif name == "Bash":
            cmd = inp.get("command") or ""
            for tok in re.findall(r"[\w./\-]+\.\w+", cmd):
                out.add(os.path.basename(tok))
                out.add(tok)
        elif name in ("Grep", "Glob"):
            p = inp.get("path") or inp.get("pattern") or ""
            if p:
                out.add(p)
    return out


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return

    text = payload.get("assistant_text") or payload.get("text") or ""
    tool_events = payload.get("tool_uses") or payload.get("tool_events") or []

    master_warn = check_master_counter(text, tool_events)
    if master_warn:
        print(master_warn)

    labels = extract_labels(text)
    high_claims = [(lab, tgt) for lab, tgt in labels if lab == "high"]
    if not high_claims:
        return

    touched = files_touched_by_tools(tool_events)
    unverified = []
    for lab, tgt in high_claims:
        base = tgt.split(":")[0]
        if base not in touched and os.path.basename(base) not in touched:
            unverified.append(tgt)

    if not unverified:
        return

    line = (f"[kasidit-verify] downgraded {len(unverified)} [high] → [medium] "
            f"— no matching Read/Bash call: {', '.join(unverified[:5])}")
    print(line)

    try:
        CENTER.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a") as f:
            f.write(json.dumps({
                "ts": payload.get("ts", ""),
                "unverified": unverified,
            }) + "\n")
    except Exception:
        pass


MASTER_CLAIM_RE = re.compile(
    r"(delegat(?:e|ing|ion)|dispatch(?:ing)?|spawn(?:ing)?|handoff|invocation)\s+(?:to\s+)?(?:the\s+)?(?:specialist|agent|sub-?agent|bug-hunter|architect|audit-specialist|migration-specialist|refactor-surgeon)",
    re.IGNORECASE,
)


def check_master_counter(text: str, tool_events: List[dict]) -> Optional[str]:
    """If assistant claims 'delegating to specialist' on a strong-work mission
    but still performs Edit/Write/Bash itself in the same turn → flag.
    """
    if not MASTER_CLAIM_RE.search(text):
        return None
    direct_work = 0
    for e in tool_events:
        name = e.get("tool_name") or e.get("name") or ""
        if name in ("Edit", "Write"):
            direct_work += 1
        elif name == "Bash":
            cmd = (e.get("tool_input") or e.get("input") or {}).get("command", "")
            if any(k in cmd for k in ("git commit", "rm ", "mv ", "cp ", "chmod")):
                direct_work += 1
    if direct_work == 0:
        return None
    return (f"[kasidit-verify] master violation — claimed delegation but performed "
            f"{direct_work} direct Edit/Write/Bash call(s). Master should spawn, not execute.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
