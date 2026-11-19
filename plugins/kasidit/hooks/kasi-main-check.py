#!/usr/bin/env python3
"""
kasi-main-check.py — Stop hook

Enforce the one kind of main.md rule that code can check: the reply's script.
Blocked scripts = every script foreign to `reply_language` + `forbid_scripts`,
minus `allow_scripts` (see kasi_mainfile.forbidden_scripts). Latin is never
blocked — code terms are Latin in every language.
Scans this turn's assistant text; text inside `code` / ``` blocks and `>`
blockquotes is ignored so quoting foreign text does not trip it.

On a hit → {"decision": "block", "reason": ...} so Claude rewrites the reply.
Blocks at most once per stop (stop_hook_active) to avoid a loop.
"""

from __future__ import annotations

import json
import re
import sys

from kasi_mainfile import SCRIPTS, forbidden_scripts
from kasi_transcript import load_current_turn

CODE = re.compile(r'```.*?```|`[^`\n]*`', re.S)
QUOTE = re.compile(r'^>.*$', re.M)


def main():
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    if payload.get("stop_hook_active"):
        return
    scripts = forbidden_scripts(payload.get("cwd"))
    path = payload.get("transcript_path")
    if not scripts or not path:
        return

    text, _ = load_current_turn(path)
    prose = QUOTE.sub("", CODE.sub("", text))
    for name in sorted(scripts):
        m = SCRIPTS[name].search(prose)
        if not m:
            continue
        sample = prose[max(0, m.start() - 20):m.start() + 30].replace("\n", " ")
        reason = (f'[kasidit main] {name} script in your reply ("{sample}") — main.md forbids it. '
                  f'Rewrite every user-facing sentence following the main.md language rule. '
                  f'Quoting foreign text on purpose? Put it in `backticks` or a > blockquote.')
        print(json.dumps({"decision": "block", "reason": reason}))
        return


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
