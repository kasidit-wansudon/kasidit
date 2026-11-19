#!/usr/bin/env python3
"""Snapshot tests for Kasidit hooks.

NOTE (P0-2, 2026-08-02): this file is NOT proof that these hooks connect to
the real Claude Code harness. It builds payloads to the shape each hook's
code expects, which for a while (v0.10–v0.16) was `assistant_text`/
`tool_uses` — fields the real PostToolUse/Stop payload never sends. This
suite was 10/10 green the entire time kasi-verify.py and kasi-record.py
were dead in production. See test_hook_contract.py for tests against the
real payload shape (transcript_path pointing at a real transcript JSONL) —
that file is the one that would have caught the regression.

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


def stop_payload_for(tmp_dir: str, text: str, tool_events=None) -> dict:
    """Build a real Stop-shaped payload backed by a throwaway transcript
    file, matching what kasi-verify.py / kasi-record.py actually receive."""
    content = []
    for e in (tool_events or []):
        content.append({"type": "tool_use", "name": e["tool_name"], "input": e["tool_input"]})
    if text:
        content.append({"type": "text", "text": text})
    lines = [
        {"type": "user", "message": {"content": "do the thing"}},
        {"type": "assistant", "message": {"content": content}},
    ]
    tp = Path(tmp_dir) / "transcript.jsonl"
    with tp.open("w") as f:
        for l in lines:
            f.write(json.dumps(l) + "\n")
    return {
        "session_id": "test", "transcript_path": str(tp), "cwd": "/tmp",
        "hook_event_name": "Stop", "stop_hook_active": False,
    }


def test_route_security_keyword():
    center, cleanup = fresh_center()
    try:
        _, out = run(center, "kasi-route.py", {"prompt": "review security of AuthController.php"})
        assert_contains("route classifies security keyword", out, "kind=security-audit")
        assert_contains("route recommends ultra on security", out, "mode=ultra")
    finally:
        cleanup()


def test_route_bug_keyword():
    center, cleanup = fresh_center()
    try:
        _, out = run(center, "kasi-route.py", {"prompt": "fix this bug in login code"})
        assert_contains("route classifies bug keyword", out, "kind=bug-fix")
        assert_contains("route recommends lite on bug-fix", out, "mode=lite")
    finally:
        cleanup()


def test_route_unclassified_silent():
    center, cleanup = fresh_center()
    try:
        _, out = run(center, "kasi-route.py", {"prompt": "hello, how are you"})
        if "kind=" in out:
            FAIL.append(f"FAIL [route no kind line on unclassified greeting] — got: {out!r}")
        else:
            print("ok   route no kind line on unclassified greeting")
    finally:
        cleanup()


def test_verify_downgrade_high():
    center, cleanup = fresh_center()
    try:
        payload = stop_payload_for(center, "[high] auth.php:42 SQL injection risk")
        _, out = run(center, "kasi-verify.py", payload)
        assert_contains("verify downgrades unverified [high]", out, "downgraded 1 [high]")
    finally:
        cleanup()


def test_verify_high_with_read_passes():
    center, cleanup = fresh_center()
    try:
        payload = stop_payload_for(
            center, "[high] auth.php:42 SQL injection risk",
            tool_events=[{"tool_name": "Read", "tool_input": {"file_path": "/some/path/auth.php"}}],
        )
        _, out = run(center, "kasi-verify.py", payload)
        assert_empty("verify silent when [high] matches Read tool call", out)
    finally:
        cleanup()


def test_verify_master_violation():
    center, cleanup = fresh_center()
    try:
        payload = stop_payload_for(
            center, "Delegating to audit-specialist for review.",
            tool_events=[{"tool_name": "Edit", "tool_input": {"file_path": "x.php"}}],
        )
        _, out = run(center, "kasi-verify.py", payload)
        assert_contains("verify flags master violation", out, "master violation")
    finally:
        cleanup()


def test_record_parses_log_emit():
    center, cleanup = fresh_center()
    try:
        payload = stop_payload_for(center, "[kasidit-log] kind=bug-fix mode=lite turns=2 outcome=pass")
        _, out = run(center, "kasi-record.py", payload)
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
        payload = stop_payload_for(
            center, '[kasidit-pattern] name=bearer-auth file=x.php note="trust hierarchy"')
        run(center, "kasi-record.py", payload)
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
        payload = stop_payload_for(center, "[kasidit-log] kind=bug-fix mode=lite turns=2 outcome=pass")
        for _ in range(4):
            run(center, "kasi-record.py", payload)
        _, out = run(center, "kasi-route.py", {"prompt": "fix the bug in login"})
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
        record_payload = stop_payload_for(center, "[kasidit-log] kind=ui mode=lite turns=1 outcome=pass")
        for _ in range(4):
            code, _ = run(center, "kasi-record.py", record_payload)
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

        _, out = run(center, "kasi-route.py", {"prompt": "UI overflow on card layout"})
        assert_contains("e2e route recommends kind=ui from recorded history", out, "kind=ui")
        assert_contains("e2e route recommends mode=lite from recorded history", out, "mode=lite")
        assert_contains("e2e route emits history= after >=3 records", out, "history=")
    finally:
        cleanup()


MAIN_MD = """---
forbid_scripts: vietnamese
---
## Always
- Reply in Thai.
- One mission at a time.

## Context
- Prefers tables over prose.
"""


def write_main(dir_path: str, text: str = MAIN_MD) -> None:
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    (Path(dir_path) / "main.md").write_text(text, encoding="utf-8")


def test_route_appends_always_on_unclassified():
    center, cleanup = fresh_center()
    try:
        write_main(center)
        _, out = run(center, "kasi-route.py", {"prompt": "hello, how are you", "cwd": "/tmp"})
        assert_contains("route sends Always on unclassified prompt", out, "[kasidit main] always:")
        assert_contains("route sends the Always rule text", out, "Reply in Thai.")
        if "Prefers tables" in out:
            FAIL.append("FAIL [route sends Always only] — Context section leaked into per-prompt output")
    finally:
        cleanup()


def test_route_keeps_kind_line_with_always():
    center, cleanup = fresh_center()
    try:
        write_main(center)
        _, out = run(center, "kasi-route.py", {"prompt": "fix this bug in login code", "cwd": "/tmp"})
        assert_contains("route still classifies with main.md present", out, "kind=bug-fix")
        assert_contains("route appends Always after kind line", out, "Reply in Thai.")
    finally:
        cleanup()


def test_main_session_start_sends_full_file():
    center, cleanup = fresh_center()
    try:
        write_main(center)
        _, out = run(center, "kasi-main.py", {"cwd": "/tmp", "source": "compact"})
        assert_contains("session start sends Always", out, "Reply in Thai.")
        assert_contains("session start sends Context", out, "Prefers tables over prose.")
        if "forbid_scripts" in out:
            FAIL.append("FAIL [session start strips frontmatter] — frontmatter leaked into context")
    finally:
        cleanup()


def run_cli(center: str, *args: str) -> tuple[int, str]:
    env = os.environ.copy()
    env["KASIDIT_CENTER"] = center
    proc = subprocess.run(
        [sys.executable, str(HOOKS_DIR / "kasi_mainfile.py"), *args],
        capture_output=True, env=env, timeout=5,
    )
    return proc.returncode, proc.stdout.decode() + proc.stderr.decode()


def test_onboarding_asks_language_first_without_file():
    center, cleanup = fresh_center()
    try:
        _, out = run(center, "kasi-main.py", {"cwd": "/tmp", "source": "startup"})
        assert_contains("fresh install starts onboarding step 1", out, "onboarding step 1/3")
        assert_contains("step 1 asks reply language first", out, "which language should all replies be in")
        assert_contains("step 1 gives the save command", out, "set reply_language")
        _, out = run(center, "kasi-route.py", {"prompt": "fix this bug", "cwd": "/tmp"})
        assert_contains("route reminds every prompt until language set", out, "reply language not set")
    finally:
        cleanup()


def test_onboarding_offers_next_steps_after_language():
    center, cleanup = fresh_center()
    try:
        run_cli(center, "set", "reply_language", "th")
        _, out = run(center, "kasi-main.py", {"cwd": "/tmp", "source": "startup"})
        assert_contains("after language, onboarding offers steps 2-3", out, "onboarding steps 2-3")
        assert_contains("language rule generated from reply_language", out, "Reply in Thai")
        if "step 1/3" in out:
            FAIL.append("FAIL [step 1 not repeated] — language already set but step 1 still shown")
        run_cli(center, "set", "onboarded", "true")
        _, out = run(center, "kasi-main.py", {"cwd": "/tmp", "source": "startup"})
        if "onboarding" in out:
            FAIL.append(f"FAIL [onboarding quiet when done] — got: {out!r}")
        else:
            print("ok   onboarding quiet when done")
    finally:
        cleanup()


def test_cli_set_language_drives_route():
    center, cleanup = fresh_center()
    try:
        code, _ = run_cli(center, "set", "reply_language", "TH")
        _, got = run_cli(center, "get", "reply_language")
        assert_contains("cli set writes lowercase code", got, "th")
        _, out = run(center, "kasi-route.py", {"prompt": "hello", "cwd": "/tmp"})
        assert_contains("route sends generated language rule", out, "Reply in Thai")
        if "reply language not set" in out:
            FAIL.append("FAIL [route stops reminding] — reminder still shown after set")
        code, out = run_cli(center, "set", "reply_language", "klingon")
        if code == 0:
            FAIL.append("FAIL [cli rejects unknown language] — exit 0")
        else:
            print("ok   cli rejects unknown language")
    finally:
        cleanup()


def test_check_reply_language_blocks_foreign_scripts():
    center, cleanup = fresh_center()
    try:
        run_cli(center, "set", "reply_language", "th")
        for desc, text in [("Chinese", "结果已经完成"), ("Vietnamese", "Đang kiểm tra."),
                           ("Russian", "Проверка готова")]:
            _, out = run(center, "kasi-main-check.py", stop_payload_for(center, text))
            assert_contains(f"th reply_language blocks {desc}", out, '"decision": "block"')
        _, out = run(center, "kasi-main-check.py",
                     stop_payload_for(center, "แก้ไฟล์ AuthController.php แล้ว, tests pass"))
        assert_empty("th reply with English code terms passes", out)
        _, out = run(center, "kasi-main-check.py",
                     stop_payload_for(center, "เขาตอบว่า:\n> 结果已经完成\nแปลว่าเสร็จแล้ว"))
        assert_empty("blockquoted foreign text passes", out)
    finally:
        cleanup()


def test_check_allow_scripts_and_japanese():
    center, cleanup = fresh_center()
    try:
        run_cli(center, "set", "reply_language", "th")
        run_cli(center, "set", "allow_scripts", "chinese")
        _, out = run(center, "kasi-main-check.py",
                     stop_payload_for(center, "อ่านไฟล์ 进销存看板开发文档.pdf แล้ว"))
        assert_empty("allow_scripts chinese lets Han through", out)
        run_cli(center, "set", "allow_scripts", "")
        run_cli(center, "set", "reply_language", "ja")
        _, out = run(center, "kasi-main-check.py",
                     stop_payload_for(center, "テストは完了しました。"))
        assert_empty("ja reply_language allows kana + han", out)
    finally:
        cleanup()


def test_main_project_merges_with_center():
    center, cleanup = fresh_center()
    try:
        write_main(center)
        project = Path(center) / "proj"
        write_main(str(project / ".kasidit"), "## Always\n- Use Laravel 8 conventions.\n")
        _, out = run(center, "kasi-route.py", {"prompt": "hello", "cwd": str(project)})
        assert_contains("route keeps center Always", out, "Reply in Thai.")
        assert_contains("route adds project Always", out, "Use Laravel 8 conventions.")
    finally:
        cleanup()


def test_main_always_truncated_when_too_long():
    center, cleanup = fresh_center()
    try:
        write_main(center, "## Always\n" + "- rule line that is long enough\n" * 100)
        _, out = run(center, "kasi-route.py", {"prompt": "hello", "cwd": "/tmp"})
        assert_contains("route truncates oversized Always", out, "Always section truncated")
    finally:
        cleanup()


def test_main_check_blocks_forbidden_script():
    center, cleanup = fresh_center()
    try:
        write_main(center)
        payload = stop_payload_for(center, "Đang kiểm tra kết quả benchmark.")
        _, out = run(center, "kasi-main-check.py", payload)
        assert_contains("check blocks Vietnamese reply", out, '"decision": "block"')
    finally:
        cleanup()


def test_main_check_ignores_code_blocks():
    center, cleanup = fresh_center()
    try:
        write_main(center)
        payload = stop_payload_for(center, "ผลลัพธ์คือ `Đang` ในโค้ดเท่านั้น")
        _, out = run(center, "kasi-main-check.py", payload)
        assert_empty("check ignores script inside inline code", out)
    finally:
        cleanup()


def test_main_check_no_loop_when_stop_active():
    center, cleanup = fresh_center()
    try:
        write_main(center)
        payload = stop_payload_for(center, "Đang kiểm tra.")
        payload["stop_hook_active"] = True
        _, out = run(center, "kasi-main-check.py", payload)
        assert_empty("check does not block twice in one stop", out)
    finally:
        cleanup()


def test_main_check_off_without_forbid():
    center, cleanup = fresh_center()
    try:
        write_main(center, "## Always\n- Reply in Thai.\n")
        payload = stop_payload_for(center, "Đang kiểm tra.")
        _, out = run(center, "kasi-main-check.py", payload)
        assert_empty("check is off when forbid_scripts unset", out)
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
