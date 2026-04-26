<!--
Read CONTRIBUTING.md if this is your first PR:
https://github.com/kasidit-wansudon/kasidit/blob/main/CONTRIBUTING.md

One mission per PR. No drive-by refactors.
-->

## What this PR does

<!-- One sentence. The diff already shows the code; tell us the goal. -->

## Why

<!-- The user pain or product reason. Link to the Issue / Discussion if there is one. -->

Fixes #
Discussion:

## Scope

<!-- Tick all that apply. -->

- [ ] SKILL.md (framework rule)
- [ ] command (`commands/kasi-*.md`)
- [ ] agent (`agents/*.md`)
- [ ] hook (`hooks/*`)
- [ ] `install.sh`
- [ ] checklist (`defaults/checklists/`)
- [ ] wiki (`docs/wiki/`)
- [ ] kasidit-site (separate repo — link the site PR)
- [ ] docs / README / CHANGELOG only

## Test plan

<!-- Runtime is the judge, not self-report. -->

- [ ] `bash plugins/kasidit/install.sh --dry-run` produces the expected plan
- [ ] `bash plugins/kasidit/install.sh` is idempotent on a fresh `HOME=/tmp/...` sandbox
- [ ] `python3 plugins/kasidit/hooks/test_hooks.py` → 10/10 pass
- [ ] Manual mission tested end-to-end: ___
- [ ] Wiki page in `docs/wiki/` updated (if user-visible behavior changed)

## Tier impact

<!-- Anything Haiku-specific to call out? -->

## Backward compatibility

<!-- Does this break existing users? If yes, is there a deprecation path? -->

## Honesty section

<!-- v0.10's theme. Anything that is "spec only, not runtime-enforced" should be flagged. -->

- [ ] All claimed behavior in this PR is runtime-enforced, OR is documented as spec-only with a clear caveat
