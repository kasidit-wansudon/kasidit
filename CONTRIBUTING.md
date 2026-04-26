# Contributing to Kasidit

Kasidit is a discipline framework for AI coding. The same rules apply when contributing as when using it: narrow missions, design before code, runtime-as-judge, point not paragraph.

## Where to start

| Want to | Go to |
|---------|-------|
| Report a defect | [Issues](https://github.com/kasidit-wansudon/kasidit/issues) — use the bug template |
| Suggest a feature | [Discussions → Ideas](https://github.com/kasidit-wansudon/kasidit/discussions) |
| Ask a usage question | [Discussions → Q&A](https://github.com/kasidit-wansudon/kasidit/discussions) |
| Share a `.kasidit/` config / checklist / pattern | [Discussions → Show & Tell](https://github.com/kasidit-wansudon/kasidit/discussions) |
| Submit a code change | Pull request (read below first) |
| Disclose a security issue | See [SECURITY.md](./SECURITY.md) — do **not** use public Issues |

## Pull request flow

1. **Open an Issue or Discussion first** for non-trivial changes. Avoid surprise PRs that touch SKILL.md, hooks, or agent contracts. Trivial fixes (typo, broken link, doc clarification) can skip this step.
2. **Fork** and branch from `main`. Branch name: `<type>/<short-description>` — `feat/router-memory-export`, `fix/install-sh-jq-detection`, `docs/wiki-v0.10-cleanup`.
3. **Match the style of the file you are editing.** Kasidit favors terse output, point lists, file:line references, and minimal preamble.
4. **One mission per PR.** No drive-by refactors in unrelated files.
5. **Test runtime, not self-report.** If you change a hook, run `python3 plugins/kasidit/hooks/test_hooks.py`. If you change `install.sh`, run with `--dry-run` first, then real on a test home dir.
6. **Update the wiki source.** Any user-visible behavior change → update the matching page in `docs/wiki/` in the same PR.
7. **Conventional Commits** for the subject line: `feat(scope): ...`, `fix(scope): ...`, `docs(wiki): ...`, `chore: ...`.
8. **Open the PR** with the template (auto-loaded from `.github/PULL_REQUEST_TEMPLATE.md`). Fill it out — the questions are short.

## Repo layout

```
plugins/kasidit/
├── skills/kasidit/SKILL.md       # the framework spec
├── commands/                     # /kasi-* slash commands
├── agents/                       # specialist subagents
├── hooks/                        # backend hooks (v0.10)
├── defaults/checklists/          # 12 default checklists seeded at install
└── install.sh                    # canonical installer
docs/wiki/                        # wiki source (sync to GitHub wiki via /kasi-wiki-sync)
```

## What the project values

- **Honesty over polish.** If a feature is spec-only and not runtime-enforced, the docs say so. v0.10 was named "Honesty Cleanup" specifically to remove drift between claimed behavior and actual behavior.
- **Minimal changes.** Surface area is liability. Adding a flag is cheaper than adding a subsystem; adding a subsystem is cheaper than adding a paradigm.
- **Tier awareness.** Anything that "works on Opus" must also be tested or annotated for Haiku behavior. Haiku is the harder problem and usually the better tester.
- **Compatibility.** Old `code-reviewer` / `security-auditor` / `perf-profiler` agents are kept as stubs in v0.10 even though `audit-specialist` replaces them. Removal happens in v0.11 — one full release of warning.

## What gets rejected

- PRs that wholesale rewrite SKILL.md philosophy without prior discussion
- Changes that add LLM-context bloat without an opt-out (Mode gate)
- New agents whose scope overlaps an existing one (we just merged 3 into `audit-specialist` — do not re-fragment)
- Hooks that block prompt submission, fail on common environments, or require non-stdlib deps
- Anything that uploads user data anywhere

## Commit message hygiene

Read the recent commit log before writing your first commit on a branch. Match the style.

```
feat(site): add bilingual EN/TH language toggle
docs(wiki): consolidate v0.10 release notes — keep dotted form, drop short stub
fix(install.sh): handle missing jq with python3 stdlib fallback
```

Body, when present, explains **why** — the diff already shows what.

## Local development

```bash
git clone https://github.com/kasidit-wansudon/kasidit.git
cd kasidit
bash plugins/kasidit/install.sh --dry-run   # preview install
bash plugins/kasidit/install.sh             # real install on your home dir
python3 plugins/kasidit/hooks/test_hooks.py # 10/10 pass = ready
```

To test changes against a fresh home, point the installer at a sandbox:

```bash
HOME=/tmp/kasidit-sandbox bash plugins/kasidit/install.sh
```

## Reviewers

PRs are reviewed by the maintainer. Response time is best-effort — small clear PRs land faster. Large PRs that did not start as an Issue/Discussion may be asked to back up and discuss first.

## Code of conduct

Be respectful, be clear, be technical. See [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

## License

Kasidit is MIT. By contributing you agree that your contributions are licensed under the same.
