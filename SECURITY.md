# Security Policy

## Supported versions

Kasidit follows semantic-ish versioning. Security fixes land on the latest minor only. Older minors do not receive backports unless the user count justifies it.

| Version | Supported |
|---------|-----------|
| v0.10.x | ✓ |
| v0.9.x  | best-effort for severe issues |
| < v0.9  | unsupported |

## What counts as a security issue

- A hook that exfiltrates data, executes attacker-controlled input, or modifies files outside its documented scope
- An installer that overwrites unrelated user config without backup or notice
- A command that accepts user input and passes it unsafely to a shell, query, or template
- A documented agent that ignores its scope contract in a way that touches files / network / processes the user did not authorize
- Any case where Kasidit causes Claude Code or its environment to behave in a way the user did not consent to

Performance issues, ergonomic bugs, missing features, or framework opinions are **not** security issues. Use Issues / Discussions for those.

## How to report

Email **kasidit.wans@gmail.com** with:

1. A description of the issue
2. Steps to reproduce (or a minimal repro repo)
3. Affected version(s)
4. Any suggested mitigation

Please do **not** open a public Issue or Discussion for security topics. Public disclosure of an unpatched issue puts users at risk.

## Response

Acknowledgement: within 7 days.

Triage and fix: depends on severity. Critical issues that put user files or credentials at risk are prioritized over feature work.

You will be credited in the release notes (or kept anonymous, your choice).

## Out of scope

- Vulnerabilities in dependencies (`jq`, `python3`, Claude Code itself, Anthropic API). Report those upstream.
- Issues that require an attacker to already have write access to the user's home directory.
- Issues that require disabling existing OS security (running as root, disabling SIP / Gatekeeper / AppArmor).

## Disclosure timeline

- Day 0 — report received, acknowledged
- Day 0 to fix — fix developed privately
- Fix release — credit, public advisory, recommended action
- 30 days after fix release — full technical writeup if useful

If a reporter and maintainer disagree on disclosure timing, the maintainer's decision is final, but reasonable timelines for active exploitation will not be obstructed.
