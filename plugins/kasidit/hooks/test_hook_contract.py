#!/usr/bin/env python3
"""Contract tests for Kasidit hooks — verify against REAL harness payload
shapes, not payloads the hooks themselves expect.

test_hooks.py feeds hooks payloads shaped the way the hook authors assumed
(`assistant_text`, `tool_uses`). That only proves the code does what the
code thinks it does. It shipped 10/10 green for multiple releases while
kasi-verify.py and kasi-record.py were completely dead in production,
because the real PostToolUse/Stop payload never carries those fields.

This file uses the actual Claude Code hook payload shape instead:

  Stop payload:
    {"session_id", "transcript_path", "cwd", "hook_event_name",
     "stop_hook_active"}

  transcript_path points at a JSONL transcript. Verified 2026-08-02 against
  a live session transcript on Claude Code (see plugins/kasidit/hooks/
  fixtures/*.jsonl for captured/derived shapes; schema fields:
  type: "user" | "assistant" | other-metadata (ignored);
  assistant message.content: list of {"type": "text"|"tool_use", ...};
  a REAL user prompt has message.content as a plain string and no
  top-level "toolUseResult" key — tool-result "user" entries have both.

Do not trust this file's fixtures blindly either — if Claude Code changes
its transcript schema, re-derive fixtures/*.jsonl from a live transcript
(~/.claude/projects/<project>/<session-id>.jsonl) before trusting a green
run here.
"""

import json
import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

HOOKS_DIR = Path(__file__).parent
FIXTURES = HOOKS_DIR / "fixtures"

FAIL = []


def fresh_center():
    d = tempfile.mkdtemp(prefix="kasidit-contract-")
    return d, lambda: shutil.rmtree(d, ignore_errors=True)


def run_hook(center: str, hook: str, payload: dict) -> tuple[int, str]:
    env = os.environ.copy()
    env["KASIDIT_CENTER"] = center
    proc = subprocess.run(
        [sys.executable, str(HOOKS_DIR / hook)],
        input=json.dumps(payload).encode(),
        capture_output=True, env=env, timeout=5,
    )
    return proc.returncode, proc.stdout.decode()


def stop_payload(transcript_name: str) -> dict:
    return {
        "session_id": "test-session",
        "transcript_path": str(FIXTURES / transcript_name),
        "cwd": "/tmp",
        "hook_event_name": "Stop",
        "stop_hook_active": False,
    }


def assert_contains(desc, actual, needle):
    if needle not in actual:
        FAIL.append(f"FAIL [{desc}] — expected substring `{needle}` not in output: {actual!r}")
    else:
        print(f"ok   {desc}")


def assert_empty(desc, actual):
    if actual.strip():
        FAIL.append(f"FAIL [{desc}] — expected empty output, got: {actual!r}")
    else:
        print(f"ok   {desc}")


def assert_no_crash(desc, returncode):
    if returncode != 0:
        FAIL.append(f"FAIL [{desc}] — hook exited {returncode}, expected 0 (hooks must never crash the harness)")
    else:
        print(f"ok   {desc}")


# --- kasi-verify.py --------------------------------------------------------

def test_verify_stop_high_no_read_downgrades():
    center, cleanup = fresh_center()
    try:
        rc, out = run_hook(center, "kasi-verify.py", stop_payload("transcript_high_no_read.jsonl"))
        assert_no_crash("verify/stop real payload does not crash", rc)
        assert_contains("verify/stop downgrades unverified [high]", out, "downgraded 1 [high]")
        assert_contains("verify/stop names the unverified target", out, "auth.php:42")
    finally:
        cleanup()


def test_verify_stop_high_with_read_clean():
    center, cleanup = fresh_center()
    try:
        rc, out = run_hook(center, "kasi-verify.py", stop_payload("transcript_high_with_read.jsonl"))
        assert_no_crash("verify/stop real payload (with Read) does not crash", rc)
        assert_empty("verify/stop stays silent when Read backs the [high] claim", out)
    finally:
        cleanup()


def test_verify_stop_ignores_prior_turn():
    """A [high] claim from an earlier turn must not resurface once the user
    has moved on to a new turn — the hook must scope to the CURRENT turn
    only, not the whole transcript."""
    center, cleanup = fresh_center()
    try:
        rc, out = run_hook(center, "kasi-verify.py", stop_payload("transcript_high_prior_turn_only.jsonl"))
        assert_no_crash("verify/stop turn-scoping does not crash", rc)
        assert_empty("verify/stop ignores [high] claim from a prior turn", out)
    finally:
        cleanup()


def test_verify_unbacked_citation_flagged():
    center, cleanup = fresh_center()
    try:
        tp = Path(FIXTURES) / "_tmp_unbacked.jsonl"
        lines = [
            {"type": "user", "message": {"content": "check the fix"}},
            {"type": "assistant", "message": {"content": [
                {"type": "text", "text": "verified: pytest tests/auth_test.py -k injection passes"}
            ]}},
        ]
        tp.write_text("\n".join(json.dumps(l) for l in lines) + "\n")
        try:
            payload = stop_payload(tp.name)
            rc, out = run_hook(center, "kasi-verify.py", payload)
            assert_no_crash("verify/unbacked citation does not crash", rc)
            assert_contains("verify/unbacked citation flagged (no matching Bash call)",
                             out, "unbacked verification claim")
        finally:
            tp.unlink(missing_ok=True)
    finally:
        cleanup()


def test_verify_backed_citation_clean():
    center, cleanup = fresh_center()
    try:
        tp = Path(FIXTURES) / "_tmp_backed.jsonl"
        lines = [
            {"type": "user", "message": {"content": "check the fix"}},
            {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "name": "Bash", "input": {"command": "pytest tests/auth_test.py -k injection"}}
            ]}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "content": "1 passed"}]}, "toolUseResult": {}},
            {"type": "assistant", "message": {"content": [
                {"type": "text", "text": "verified: pytest tests/auth_test.py -k injection passes"}
            ]}},
        ]
        tp.write_text("\n".join(json.dumps(l) for l in lines) + "\n")
        try:
            payload = stop_payload(tp.name)
            rc, out = run_hook(center, "kasi-verify.py", payload)
            assert_no_crash("verify/backed citation does not crash", rc)
            assert_empty("verify/backed citation stays silent when the Bash call matches", out)
        finally:
            tp.unlink(missing_ok=True)
    finally:
        cleanup()


def test_verify_empty_payload_no_crash():
    center, cleanup = fresh_center()
    try:
        rc, out = run_hook(center, "kasi-verify.py", {})
        assert_no_crash("verify/{} does not crash", rc)
        assert_empty("verify/{} produces no output", out)
        err_log = Path(center) / "hook-errors.log"
        if err_log.exists():
            FAIL.append(f"FAIL [verify/{{}} error log] — {{}} is a normal non-Stop-shaped input, "
                        f"should not be logged as an error: {err_log.read_text()!r}")
        else:
            print("ok   verify/{} does not write to hook-errors.log for a benign missing-field payload")
    finally:
        cleanup()


# --- kasi-record.py ---------------------------------------------------------

def test_record_stop_extracts_emit_line():
    center, cleanup = fresh_center()
    try:
        rc, out = run_hook(center, "kasi-record.py", stop_payload("transcript_kasi_record.jsonl"))
        assert_no_crash("record/stop real payload does not crash", rc)
        assert_contains("record/stop saves the emitted [kasidit-log] line", out, "+1 backend entries saved")

        route_log = Path(center) / "route-memory.jsonl"
        if not route_log.exists():
            FAIL.append("FAIL [record/stop persists to route-memory.jsonl] — file was not created")
        else:
            line = json.loads(route_log.read_text().strip().splitlines()[-1])
            if line.get("kind") != "fix" or line.get("outcome") != "pass":
                FAIL.append(f"FAIL [record/stop persisted record shape] — got {line!r}")
            else:
                print("ok   record/stop persists parsed kind/outcome to route-memory.jsonl")
    finally:
        cleanup()


def test_record_empty_payload_no_crash():
    center, cleanup = fresh_center()
    try:
        rc, out = run_hook(center, "kasi-record.py", {})
        assert_no_crash("record/{} does not crash", rc)
        assert_empty("record/{} produces no output", out)
    finally:
        cleanup()


def test_record_missing_transcript_path_no_crash():
    """transcript_path pointing at a nonexistent file must not crash —
    e.g. a transcript rotated/deleted between hook registration and Stop."""
    center, cleanup = fresh_center()
    try:
        payload = stop_payload("does-not-exist.jsonl")
        rc, out = run_hook(center, "kasi-record.py", payload)
        assert_no_crash("record/missing-transcript does not crash", rc)
        assert_empty("record/missing-transcript produces no output", out)
    finally:
        cleanup()


def main():
    tests = [(k, v) for k, v in globals().items() if k.startswith("test_") and callable(v)]
    print(f"Running {len(tests)} contract tests against real payload shapes...\n")

    for name, fn in tests:
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
    print(f"all {len(tests)} contract tests passed")


if __name__ == "__main__":
    main()
