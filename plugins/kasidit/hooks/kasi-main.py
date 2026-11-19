#!/usr/bin/env python3
"""
kasi-main.py — SessionStart hook

Inject the user's pinned rules (main.md) into context. Registered without a
matcher, so it fires on startup, resume, clear and compact — the last one is
the point: rules loaded once at startup fade after a compact; this re-sends them.

Also runs onboarding:
  reply_language unset → tell Claude to ask the user's reply language FIRST,
                         before any other work, and save it via the CLI.
  onboarded not true   → after that, offer the optional next steps once.

Output (stdout, added to session context by Claude Code).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from kasi_mainfile import CENTER, load_full, onboarded, reply_language

CLI = f"python3 {Path(__file__).resolve().parent / 'kasi_mainfile.py'}"


def onboarding_text(cwd) -> str:
    if not reply_language(cwd):
        return (
            "[kasidit main] onboarding step 1/3 — reply language is not set.\n"
            "Before doing anything else this session (even if the first message is a task), "
            "ask the user ONE question: which language should all replies be in? "
            "Offer 3-4 likely choices based on the language they wrote in, plus 'other'.\n"
            f"Save the answer with: {CLI} set reply_language <code>  "
            "(codes: th en es fr de pt it id ms vi zh ja ko ru uk ar he hi).\n"
            "Then continue with their request in that language."
        )
    if not onboarded(cwd):
        return (
            "[kasidit main] onboarding steps 2-3 (optional — offer once, briefly, after the "
            "current request is handled):\n"
            "  2. Import must-follow rules from an existing CLAUDE.md / AGENTS.md into the "
            f"`## Always` section of {CENTER / 'main.md'} (keep it 3-7 lines; ask before writing).\n"
            "  3. Ask if they want to add a rule of their own (thinking style, tone, conventions).\n"
            f"When done or declined, run: {CLI} set onboarded true"
        )
    return ""


def main():
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    cwd = payload.get("cwd")
    text = load_full(cwd)
    if text:
        print("[kasidit main] pinned rules — follow these before anything else, every turn:")
        print(text)
    onboarding = onboarding_text(cwd)
    if onboarding:
        print(onboarding)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
