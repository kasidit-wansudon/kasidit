#!/usr/bin/env python3
"""
kasi_transcript.py — shared helper: extract the current turn's assistant text +
tool_use events from a Claude Code transcript_path (JSONL).

Verified against the real Claude Code transcript schema (v2.x, checked
2026-08-02 against a live session transcript, not against docs):

  Each line is a JSON object with at least a "type" field:
    "user"      — message.content is either a plain string (a real user
                  prompt) or a list of tool_result blocks (a tool result,
                  NOT a user prompt — has a top-level "toolUseResult" key)
    "assistant" — message.content is a list of blocks, each block having
                  "type": "text" | "tool_use" (tool_use blocks carry
                  "name" and "input")
    other types ("summary", "last-prompt", "ai-title", "mode",
                 "permission-mode", ...) — no "message" key, ignore

A "turn" = everything from the last real user-prompt line to EOF.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple


def _is_real_user_prompt(entry: dict) -> bool:
    if entry.get("type") != "user":
        return False
    if "toolUseResult" in entry:
        return False
    content = (entry.get("message") or {}).get("content")
    return isinstance(content, str)


def load_current_turn(transcript_path: str) -> Tuple[str, List[dict]]:
    """Return (assistant_text, tool_events) for the most recent turn.

    tool_events is a list of {"tool_name": str, "tool_input": dict} —
    same shape the rest of this codebase already expects.
    """
    path = Path(transcript_path)
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

    entries = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    last_user_idx = -1
    for i, e in enumerate(entries):
        if _is_real_user_prompt(e):
            last_user_idx = i

    turn_entries = entries[last_user_idx + 1:] if last_user_idx >= 0 else entries

    text_parts: List[str] = []
    tool_events: List[dict] = []
    for e in turn_entries:
        if e.get("type") != "assistant":
            continue
        content = (e.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            btype = block.get("type")
            if btype == "text":
                text_parts.append(block.get("text") or "")
            elif btype == "tool_use":
                tool_events.append({
                    "tool_name": block.get("name") or "",
                    "tool_input": block.get("input") or {},
                })

    return "\n".join(text_parts), tool_events
