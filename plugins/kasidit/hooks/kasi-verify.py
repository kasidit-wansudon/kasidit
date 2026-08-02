#!/usr/bin/env python3
"""
kasi-verify.py — Stop hook only

Scan assistant output for confidence labels ([unverified]/[assumed]/[unknown],
plus legacy [high]/[medium]/[low]/[unsure]) and cross-check against the tool
calls made in the same turn.

Two checks:
1. A file:line claim tagged with a legacy `[high]` label must have at least
   one Read/Bash tool call that plausibly inspected it, or it's flagged as
   unverified.
2. A `verified: <cmd>` citation (the v4 replacement for self-graded [high])
   must match an actual Bash tool call made this turn, or it's flagged as
   an unbacked claim.

Output: one line per mismatch type found. No output on clean pass.

NOTE: this hook must only ever be registered on Stop, not PostToolUse.
PostToolUse fires per tool call and never carries assistant text — a
confidence-label check there is a structural no-op (see P0-1 audit,
2026-08-02). Stop carries `transcript_path`, which is read via
kasi_transcript.load_current_turn() to reconstruct the current turn's text
and tool calls — the real payload has no `assistant_text`/`tool_uses`
fields the previous version read.

Zero dependency beyond stdlib.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kasi_transcript import load_current_turn  # noqa: E402

CENTER = Path(os.environ.get("KASIDIT_CENTER",
    os.path.expanduser("~/.claude/skills/kasidit/center")))
LOG_FILE = CENTER / "verify.log"
ERROR_LOG = CENTER / "hook-errors.log"


def _log_error(hook: str, exc: Exception) -> None:
    try:
        CENTER.mkdir(parents=True, exist_ok=True)
        with ERROR_LOG.open("a") as f:
            f.write(json.dumps({
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "hook": hook,
                "error": repr(exc),
            }) + "\n")
    except Exception:
        pass

LABEL_RE = re.compile(r"(?:^|\s)\[(high|medium|low|unsure|unverified|assumed|unknown)\]\s+([^\s:`]+(?::\d+)?)", re.IGNORECASE | re.MULTILINE)

# Rule 11 (v4): `[high]` is retired as a bare self-grade. A claim only counts
# as verified when it cites the command that verified it — `verified: <cmd>`.
# This hook checks that <cmd> was actually run as a Bash tool call this turn.
VERIFIED_RE = re.compile(r"verified:\s*`?([^`\n]+?)`?\s*(?:\n|$)", re.IGNORECASE)


def extract_labels(text: str) -> List[Tuple[str, str]]:
    return [(m.group(1).lower(), m.group(2)) for m in LABEL_RE.finditer(text)]


def bash_commands_run(tool_events: List[dict]) -> List[str]:
    out = []
    for e in tool_events:
        name = e.get("tool_name") or e.get("name") or ""
        if name == "Bash":
            cmd = (e.get("tool_input") or e.get("input") or {}).get("command") or ""
            if cmd:
                out.append(cmd)
    return out


def check_verified_citations(text: str, tool_events: List[dict]) -> List[str]:
    """Return citations claimed via `verified: <cmd>` that don't match any
    Bash call actually made this turn — an unbacked verification claim."""
    ran = bash_commands_run(tool_events)
    unbacked = []
    for m in VERIFIED_RE.finditer(text):
        claim = m.group(1).strip().rstrip(".,;")
        if not claim:
            continue
        if not any(claim in cmd or cmd in claim for cmd in ran):
            unbacked.append(claim)
    return unbacked


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

    transcript_path = payload.get("transcript_path") or ""
    if not transcript_path or not Path(transcript_path).exists():
        return
    text, tool_events = load_current_turn(transcript_path)

    master_warn = check_master_counter(text, tool_events)
    if master_warn:
        print(master_warn)

    unbacked = check_verified_citations(text, tool_events)
    if unbacked:
        print(f"[kasidit-verify] unbacked verification claim — cited `verified: ...` "
              f"but no matching Bash call this turn: {', '.join(unbacked[:5])}")

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
    except Exception as exc:
        _log_error("kasi-verify", exc)
