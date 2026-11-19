#!/usr/bin/env python3
"""
kasi-status-nudge.py — PostToolUse hook

Long work with no word to the user feels like a hang. After each tool call,
count tool calls and elapsed time since the AI last wrote text to the user
(or since the user's prompt). Past a threshold, tell the AI to post a short
status line now — done / doing / next — then carry on.

Thresholds (main.md frontmatter, 0 = off):
  status_every      — tool calls since last text   (default 8)
  status_after_sec  — seconds since last text      (default 120)

After a nudge it waits another full threshold before nudging again, unless
the AI writes text (which resets everything). State per session in
$KASIDIT_CENTER/.status-nudge.json.

Limit: hooks only fire between tool calls — one long-running command
produces no status until it returns.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

from kasi_mainfile import CENTER, meta_value

DEFAULT_EVERY = 8
DEFAULT_AFTER_SEC = 120
STATE = CENTER / ".status-nudge.json"


def _ts(entry: dict) -> Optional[float]:
    raw = entry.get("timestamp")
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def _is_prompt(entry: dict) -> bool:
    if entry.get("type") != "user" or entry.get("isMeta") or "toolUseResult" in entry:
        return False
    return isinstance((entry.get("message") or {}).get("content"), str)


def since_last_text(transcript_path: str) -> Tuple[str, int, Optional[float]]:
    """(anchor_id, tool calls after anchor, anchor timestamp).

    Anchor = the last assistant text block, or the user's prompt if the AI has
    not written any text yet this turn.
    """
    anchor, anchor_ts, tools = "", None, 0
    for line in Path(transcript_path).read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if _is_prompt(e):
            anchor, anchor_ts, tools = e.get("uuid", ""), _ts(e), 0
            continue
        if e.get("type") != "assistant":
            continue
        content = (e.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text" and (block.get("text") or "").strip():
                anchor, anchor_ts, tools = e.get("uuid", ""), _ts(e), 0
            elif block.get("type") == "tool_use":
                tools += 1
    return anchor, tools, anchor_ts


def _threshold(cwd: Optional[str], key: str, default: int) -> int:
    raw = meta_value(cwd, key)
    try:
        return int(raw) if raw != "" else default
    except ValueError:
        return default


MAX_SESSIONS = 50


def _load_state() -> dict:
    try:
        return json.loads(STATE.read_text())
    except (OSError, ValueError):
        return {}


def _save_state(state: dict) -> None:
    if len(state) > MAX_SESSIONS:
        keep = sorted(state, key=lambda k: state[k].get("ts", 0))[-MAX_SESSIONS:]
        state = {k: state[k] for k in keep}
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state))


def main():
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    path = payload.get("transcript_path")
    if not path:
        return
    cwd = payload.get("cwd")
    every = _threshold(cwd, "status_every", DEFAULT_EVERY)
    after = _threshold(cwd, "status_after_sec", DEFAULT_AFTER_SEC)
    if every <= 0 and after <= 0:
        return

    anchor, tools, anchor_ts = since_last_text(path)
    now = datetime.now(timezone.utc).timestamp()
    session = payload.get("session_id") or path
    state = _load_state()
    s = state.get(session)
    if not s or s.get("anchor") != anchor:
        s = {"anchor": anchor, "tools": 0, "ts": anchor_ts or now}

    by_count = every > 0 and tools - s["tools"] >= every
    by_time = after > 0 and now - s["ts"] >= after
    if not (by_count or by_time):
        state[session] = s
        _save_state(state)
        return

    elapsed = int(now - (anchor_ts or now))
    reason = (f"[kasidit status] {tools} tool calls / {elapsed // 60}m{elapsed % 60:02d}s since you last wrote "
              "to the user. Post a short status now (1-2 lines, in the reply language): "
              "done / doing now / next. Then continue the work.")
    state[session] = {"anchor": anchor, "tools": tools, "ts": now}
    _save_state(state)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": reason}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
