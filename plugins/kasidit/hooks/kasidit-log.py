#!/usr/bin/env python3
"""Kasidit log ingester — called by kasidit-log.sh.

Reads UserPromptSubmit JSON payload from stdin.
Trims prompts longer than 200 lines (head 40 + tail 20 + marker).
Appends one JSONL record to the log file passed as argv[1].
Fails silently — never blocks the hook.
"""

import json
import os
import sys
from datetime import datetime, timezone

MAX_LINES = 200
HEAD_LINES = 40
TAIL_LINES = 20


def main() -> int:
    if len(sys.argv) < 2:
        return 0
    log_file = sys.argv[1]

    try:
        raw = sys.stdin.read()
    except Exception:
        return 0

    try:
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {"_raw": raw[:500]}

    prompt = (
        data.get("prompt")
        or data.get("user_prompt")
        or data.get("_raw")
        or ""
    )
    session = data.get("session_id") or data.get("sessionId") or ""
    cwd = data.get("cwd") or os.getcwd()

    lines = prompt.split("\n")
    line_count = len(lines)
    char_count = len(prompt)
    trimmed = False

    if line_count > MAX_LINES:
        head = "\n".join(lines[:HEAD_LINES])
        tail = "\n".join(lines[-TAIL_LINES:])
        dropped = line_count - HEAD_LINES - TAIL_LINES
        prompt = f"{head}\n\n... [trimmed {dropped} lines] ...\n\n{tail}"
        trimmed = True

    record = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "session": session,
        "cwd": cwd,
        "lines": line_count,
        "chars": char_count,
        "trimmed": trimmed,
        "prompt": prompt,
    }

    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
