#!/usr/bin/env python3
"""Snapshot tests for Kasidit hooks.

Runs each hook with representative payloads and asserts expected stdout.
No framework dep — plain assert + subprocess.

Each test owns an isolated KASIDIT_CENTER tempdir. No shared state between
tests — discovery order changes cannot break the suite.

Usage:
  python3 test_hooks.py            # quiet
  python3 test_hooks.py --verbose  # prints fresh tempdir per test

Exit 0 = all pass. Exit 1 = any fail.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HOOKS_DIR = Path(__file__).parent

FAIL = []
VERBOSE = False


def fresh_center():
    """Allocate an isolated center dir + return (path, cleanup_fn).

    Every test calls this at entry and invokes the cleanup in `finally`.
    """
    d = tempfile.mkdtemp(prefix="kasidit-test-")
    if VERBOSE:
        print(f"[verbose] test center: {d}")
    return d, lambda: shutil.rmtree(d, ignore_errors=True)


def run(center: str, hook: str, payload: dict) -> tuple[int, str]:
    env = os.environ.copy()
    env["KASIDIT_CENTER"] = center
    proc = subprocess.run(
        [sys.executable, str(HOOKS_DIR / hook)],
        input=json.dumps(payload).encode(),
        capture_output=True, env=env, timeout=5,
    )
    return proc.returncode, proc.stdout.decode()


def assert_contains(desc: str, actual: str, needle: str) -> None:
    if needle not in actual:
        FAIL.append(f"FAIL [{desc}] — expected substring `{needle}` not in output: {actual!r}")
    else:
        print(f"ok   {desc}")


def assert_empty(desc: str, actual: str) -> None:
    if actual.strip():
        FAIL.append(f"FAIL [{desc}] — expected empty output, got: {actual!r}")
    else:
        print(f"ok   {desc}")


def test_route_security_keyword():
    center, cleanup = fresh_center()
    try:
        _, out = run(center, "kasidit-route.py", {"prompt": "review security of AuthController.php"})
        assert_contains("route classifies security keyword", out, "kind=security-audit")
        assert_contains("route recommends ultra on security", out, "mode=ultra")
    finally:
        cleanup()


def test_route_bug_keyword():
    center, cleanup = fresh_center()
    try:
        _, out = run(center, "kasidit-route.py", {"prompt": "fix this bug in login code"})
        assert_contains("route classifies bug keyword", out, "kind=bug-fix")
        assert_contains("route recommends lite on bug-fix", out, "mode=lite")
    finally:
        cleanup()


def test_route_unclassified_silent():
    center, cleanup = fresh_center()
    try:
        _, out = run(center, "kasidit-route.py", {"prompt": "hello, how are you"})
        assert_empty("route silent on unclassified greeting", out)
    finally:
        cleanup()


def test_verify_downgrade_high():
    center, cleanup = fresh_center()
    try:
        payload = {
            "assistant_text": "[high] auth.php:42 SQL injection risk",
            "tool_uses": [],
        }
        _, out = run(center, "kasidit-verify.py", payload)
        assert_contains("verify downgrades unverified [high]", out, "downgraded 1 [high]")
    finally:
        cleanup()


def test_verify_high_with_read_passes():
    center, cleanup = fresh_center()
    try:
        payload = {
            "assistant_text": "[high] auth.php:42 SQL injection risk",
            "tool_uses": [{"tool_name": "Read", "tool_input": {"file_path": "/some/path/auth.php"}}],
        }
        _, out = run(center, "kasidit-verify.py", payload)
        assert_empty("verify silent when [high] matches Read tool call", out)
    finally:
        cleanup()


def test_verify_master_violation():
    center, cleanup = fresh_center()
    try:
        payload = {
            "assistant_text": "Delegating to audit-specialist for review.",
            "tool_uses": [{"tool_name": "Edit", "tool_input": {"file_path": "x.php"}}],
        }
        _, out = run(center, "kasidit-verify.py", payload)
        assert_contains("verify flags master violation", out, "master violation")
    finally:
        cleanup()


def test_record_parses_log_emit():
    center, cleanup = fresh_center()
    try:
        payload = {
            "assistant_text": "[kasidit-log] kind=bug-fix mode=lite turns=2 outcome=pass"
        }
        _, out = run(center, "kasidit-record.py", payload)
        assert_contains("record appends log emit", out, "backend entries saved")

        mem_file = Path(center) / "route-memory.jsonl"
        if not mem_file.exists():
            FAIL.append("FAIL [record writes route-memory.jsonl] — file missing")
        else:
            data = json.loads(mem_file.read_text().splitlines()[-1])
            if data.get("mode_used") != "lite":
                FAIL.append(f"FAIL [record normalizes mode→mode_used] — got {data}")
            elif data.get("turns") != 2:
                FAIL.append(f"FAIL [record coerces turns to int] — got {data.get('turns')!r}")
            else:
                print("ok   record stores normalized record (mode_used, int turns)")
    finally:
        cleanup()


def test_record_pattern_emit():
    center, cleanup = fresh_center()
    try:
        payload = {
            "assistant_text": '[kasidit-pattern] name=bearer-auth file=x.php note="trust hierarchy"'
        }
        run(center, "kasidit-record.py", payload)
        pat_file = Path(center) / "patterns.jsonl"
        if not pat_file.exists():
            FAIL.append("FAIL [record pattern emit] — patterns.jsonl missing")
        else:
            print("ok   record pattern emit persists")
    finally:
        cleanup()


def test_route_reads_history():
    center, cleanup = fresh_center()
    try:
        # Isolated center — seed 4 bug-fix pass records from scratch.
        payload = {"assistant_text": "[kasidit-log] kind=bug-fix mode=lite turns=2 outcome=pass"}
        for _ in range(4):
            run(center, "kasidit-record.py", payload)
        _, out = run(center, "kasidit-route.py", {"prompt": "fix the bug in login"})
        assert_contains("route reads history after >=3 records", out, "history=")
    finally:
        cleanup()


def test_e2e_record_then_route_recommends_from_history():
    """End-to-end: record hook writes history, route hook reads it and emits
    a recommendation that reflects the stored mode + kind on isolated state.
    """
    center, cleanup = fresh_center()
    try:
        # Emit 4 records matching the classifier kind for the later prompt.
        # Prompt "UI overflow on card layout" classifies as kind=ui (first
        # matching keyword in kasidit-route.KEYWORDS), mode=lite.
        record_payload = {
            "assistant_text": "[kasidit-log] kind=ui mode=lite turns=1 outcome=pass"
        }
        for _ in range(4):
            code, _ = run(center, "kasidit-record.py", record_payload)
            if code != 0:
                FAIL.append(f"FAIL [e2e record step] — non-zero exit: {code}")
                return

        mem_file = Path(center) / "route-memory.jsonl"
        if not mem_file.exists():
            FAIL.append("FAIL [e2e] — route-memory.jsonl not created by record hook")
            return

        lines = [l for l in mem_file.read_text().splitlines() if l.strip()]
        if len(lines) != 4:
            FAIL.append(f"FAIL [e2e] — expected 4 memory lines, got {len(lines)}")
            return

        _, out = run(center, "kasidit-route.py", {"prompt": "UI overflow on card layout"})
        assert_contains("e2e route recommends kind=ui from recorded history", out, "kind=ui")
        assert_contains("e2e route recommends mode=lite from recorded history", out, "mode=lite")
        assert_contains("e2e route emits history= after >=3 records", out, "history=")
    finally:
        cleanup()


def main():
    global VERBOSE
    argv = sys.argv[1:]
    if "--verbose" in argv or "-v" in argv:
        VERBOSE = True

    tests = [(k, v) for k, v in globals().items() if k.startswith("test_") and callable(v)]
    print(f"Running {len(tests)} tests (isolated per-test centers)...\n")

    for name, fn in tests:
        if VERBOSE:
            print(f"--> {name}")
        try:
            fn()
        except Exception as e:
            FAIL.append(f"FAIL [{name}] — exception: {e!r}")

    print()
    if FAIL:
        for f in FAIL:
            print(f)
        print(f"\n{len(FAIL)} failed")
        sys.exit(1)
    print(f"\nall {len(tests)} tests passed")


if __name__ == "__main__":
    main()
