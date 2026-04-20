# Publishing Kasidit

End-to-end checklist for shipping v0.9.0 to GitHub + Claude Code plugin marketplace.

## 1. Replace placeholders

Find and replace in ALL files:

| Placeholder | Replace with |
| :--- | :--- |
| `kasidit-wansudon` | your actual GitHub username or org |

Quick command:

```bash
cd ~/path/to/kasidit-marketplace
grep -rl "kasidit-wansudon" . | xargs sed -i '' 's|kasidit-wansudon|kasidit|g'
```

(Change `kasidit` to the real username.)

## 2. Populate commands and agents

```bash
# extract your v0.8 tarball
mkdir -p /tmp/kasidit-v0.8
tar -xzf ~/Downloads/kasidit-v0.8.tar.gz -C /tmp/kasidit-v0.8

# copy commands + agents into the plugin structure
cp /tmp/kasidit-v0.8/commands/*.md plugins/kasidit/commands/
cp /tmp/kasidit-v0.8/agents/*.md plugins/kasidit/agents/

# remove the placeholder READMEs
rm plugins/kasidit/commands/README.md
rm plugins/kasidit/agents/README.md
```

## 3. Validate locally

```bash
claude plugin validate .
```

Should output no errors. If it warns about missing description or kebab-case, fix and re-run.

## 4. Test locally

```bash
/plugin marketplace add ./kasidit-marketplace
/plugin install kasidit@kasidit
```

Try `/kasi-status` — if the command responds, it works.

Uninstall before publishing:

```bash
/plugin uninstall kasidit@kasidit
/plugin marketplace remove kasidit
```

## 5. Initialize Git

```bash
cd ~/path/to/kasidit-marketplace
git init
git add .
git commit -m "feat: initial Kasidit v0.9.0 — Claude Design integration"
```

## 6. Create GitHub repo and push

Via gh CLI:

```bash
gh repo create kasidit --public --description "Mindful AI coding framework. Works on any model tier." --homepage "https://kasidit.ai"
git remote add origin git@github.com:kasidit-wansudon/kasidit.git
git branch -M main
git push -u origin main
```

Or via web: create an empty public repo at `github.com/new`, then:

```bash
git remote add origin git@github.com:kasidit-wansudon/kasidit.git
git branch -M main
git push -u origin main
```

## 7. Tag a release

```bash
git tag -a v0.9.0 -m "Kasidit v0.9.0 — Claude Design integration"
git push origin v0.9.0
```

Then on GitHub: Releases → Draft new release → select `v0.9.0` → paste the `CHANGELOG.md` v0.9.0 section as release notes → Publish.

## 8. Test public install

From a different machine or after clearing local cache:

```bash
/plugin marketplace add kasidit-wansudon/kasidit
/plugin install kasidit@kasidit
```

If that works, the marketplace is live.

## 9. Submit to official directories (optional, recommended)

### Anthropic official directory

Fork and PR: `github.com/anthropics/claude-plugins-official`. Add an entry pointing at `kasidit-wansudon/kasidit`. See that repo's CONTRIBUTING.md for the exact format.

### Community directories

- `claudemarketplaces.com` — submit via their form (check site).
- `buildwithclaude.com` — submit via their form (check site).
- `aitmpl.com/plugins` — directory listing.

## 10. Launch

Suggested launch sequence once the repo is public:

1. **Landing page** at `kasidit.ai` — link to the repo.
2. **Blog post** — "I tested SOTA tools on legacy PHP" (use honest 56-task numbers).
3. **HN Show HN** — title: "Show HN: Kasidit — Mindful AI coding framework for any model tier".
4. **Reddit r/ClaudeAI + r/LocalLLaMA + r/programming** — link to repo + blog.
5. **Twitter/X** — thread with screenshots of `/kasi-review` output.

## 11. Post-launch maintenance

- Respond to issues within 48h for the first 2 weeks.
- Run remaining 244 SWE-bench tasks → update numbers in README.
- Cut v0.9.1 patch for any critical fixes.
- Plan v1.0.0 once feedback settles.

---

## Quick reference: repo structure

```
kasidit-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # marketplace manifest
├── plugins/
│   └── kasidit/
│       ├── .claude-plugin/
│       │   └── plugin.json       # plugin manifest
│       ├── skills/
│       │   └── kasidit/
│       │       └── SKILL.md      # core framework (v0.9)
│       ├── commands/             # 9 slash commands
│       │   ├── kasi-review.md
│       │   ├── kasi-security.md
│       │   └── ...
│       └── agents/               # 3 agents
│           ├── security-auditor.md
│           ├── code-reviewer.md
│           └── legacy-specialist.md
├── docs/
│   └── PUBLISH.md                # this file
├── README.md
├── LICENSE
├── CHANGELOG.md
└── .gitignore
```
