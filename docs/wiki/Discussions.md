# Discussions — where to talk about Kasidit

Kasidit uses GitHub Discussions for everything that is **not a defect report**. Issues are reserved for actual bugs.

➡️ **Open the tab:** [github.com/kasidit-wansudon/kasidit/discussions](https://github.com/kasidit-wansudon/kasidit/discussions)

## Issues vs Discussions — pick the right place

| What you have | Goes to |
|---------------|---------|
| Plugin misbehaves, hook fails, install errors out | **Issues** (bug template) |
| Concrete feature proposal with a name + shape | **Issues** (feature template) |
| "How do I X" / usage question | **Discussions → Q&A** |
| "Wouldn't it be nice if" / pre-scope idea | **Discussions → Ideas** |
| Sharing your `.kasidit/` config / checklist / war story | **Discussions → Show & Tell** |
| Release notes / deprecation calls / roadmap | **Discussions → Announcements** (maintainer-only) |
| Security issue (vulnerability, data leak, unauthorized exec) | **Email** — see [SECURITY.md](https://github.com/kasidit-wansudon/kasidit/blob/main/SECURITY.md), do **not** post in public |

If unsure: open a **Q&A discussion**. Maintainer or another user will reroute if it belongs elsewhere.

## Categories

### 📣 Announcements
Maintainer-only. Releases, deprecation notices, breaking-change calls, roadmap updates. Subscribe if you want to know when v0.11 lands.

Template: `.github/DISCUSSION_TEMPLATE/announcement.yml`

### ❓ Q&A
Marked-answer category. Ask a usage question; mark the helpful reply as answer; the thread becomes a searchable knowledge artifact.

Good question shape:
- Specific mission you were running
- Tier + Mode (`/kasi status`)
- What you expected vs what you got
- Already-tried approaches

Template: `.github/DISCUSSION_TEMPLATE/q-and-a.yml`

### 💡 Ideas
Pre-scope brainstorm. Loose enough that "I am not sure if this is even good" is fine. If an idea congeals into a concrete shape, the maintainer (or you) opens a feature-request Issue and links back here.

Template: `.github/DISCUSSION_TEMPLATE/ideas.yml`

### 🎉 Show & Tell
Share what worked. Patterns from `.kasidit/PATTERNS.md`, custom checklists, hairy missions Kasidit handled (or stumbled on — also useful). Sanitize PII.

Template: `.github/DISCUSSION_TEMPLATE/show-and-tell.yml`

### 💬 General
Anything else. Conferences, community projects, Kasidit-adjacent tooling. Keep technical and on-topic.

## Etiquette

- One topic per thread. Threading does the rest.
- Search before posting — Q&A is most valuable when answers compound, not when the same question gets asked five times.
- Mark answers in Q&A. Future readers thank you.
- Quote with `>` for context, not full re-paste.
- Code blocks for code, file:line for code locations.
- For Thai contributors: post in either Thai or English — both fine. Mix is fine. The maintainer answers in whichever you used.
- The same Code of Conduct applies as in Issues and PRs.

## How a discussion becomes an Issue or PR

A Q&A reveals a real bug → open an Issue, link the discussion.

An Idea congeals into a concrete proposal → open a feature-request Issue, link.

A Show & Tell pattern is broadly useful → maintainer may open a PR to add to defaults (with attribution) or invite the author to PR it themselves.

Discussions are the funnel; Issues are the filter; PRs are the output.

## Why we use Discussions

Issues are for things that need fixing. They have a state (open / closed) and a notion of "done". Most user conversation is not like that — it is a question that gets answered, an idea that branches into three sub-ideas, a config someone shares so others can copy. Discussions is the right shape for those. Mixing them into Issues makes both worse.

This split is the same reason Kasidit has the **Mode gate** — different conversational contexts need different scaffolding. Q&A is `lite` mode for the project; Issues are `ultra`.

## Subscribing

- Announcements only — subscribe to the [Announcements category](https://github.com/kasidit-wansudon/kasidit/discussions/categories/announcements)
- Everything — Watch the repo with "All Activity"
- Specific tag — use the GitHub label/tag filters in the Discussions list

## See also

- [[FAQ]] — many questions are answered there first
- [[Home]] — wiki landing
- [Issues](https://github.com/kasidit-wansudon/kasidit/issues) — defect reports
- [SECURITY.md](https://github.com/kasidit-wansudon/kasidit/blob/main/SECURITY.md) — private channel for vulnerabilities
- [CONTRIBUTING.md](https://github.com/kasidit-wansudon/kasidit/blob/main/CONTRIBUTING.md) — full contribution flow
