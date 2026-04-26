# Checklists

> Audit by mechanical list. When reasoning is weak, the checklist is the reasoning.

Pre-built audit lists that turn reasoning-heavy tasks into mechanical execution. The agent does not think its way through a security review — it reads a checklist, scans files against each item, and reports findings. Single biggest enabler for running Kasidit on weaker models.

## Why checklists

Checklists exist because reasoning fails before scaffolding does.

- Introduced in [[v0.3.0]] as the answer to Haiku collapse. Before v0.3.0, Kasidit worked on Opus and fell apart on Haiku — the agent invented controller boundaries, hallucinated CVE-sounding bugs, spiraled. After CHECKLISTS/, Haiku executes faithfully because it is no longer asked to reason about what to look for.
- Operationalize the senior-engineer habit of "I'll walk through my 20-item list before signing off" instead of trusting gut. AI does not have gut; it has pattern match. A written list removes the gap.
- Work on every tier. Opus gets a sharper audit too — it just does not collapse without one. See [[Model-Tiers]] for why Haiku depends on them.

## Location

Two-tier, following the [[Gravity-Pattern]]:

**Project scope (dcenterlite)** — `.kasidit/CHECKLISTS/*.md`

Project-local, authoritative for the project, customizable. Every Kasidit-initialized repo has this directory. Findings feed back into the project's own `CHECKLISTS/` when patterns repeat.

**Shared scope (Centerlite)** — `~/.claude/skills/kasidit/center/checklists/*.md`

Global library, the upstream source. Pulls down into any project via `/kasi-pull checklist <name>`. Local edits do not push back until promoted with `/kasi-promote checklist <name>`. See [[Gravity-Pattern]] for full sync rules.

Read order: project first, hub fallback. If `.kasidit/CHECKLISTS/security-php.md` is missing and a mission needs it, the agent copies from Centerlite on demand.

## What a checklist looks like

Plain markdown, checkboxes, grouped by category. No prose. Example from `security-php.md`:

```markdown
# PHP Security Scan Checklist

For each controller/action, check:

## Injection
- [ ] SQL: any `query()`, `raw()`, `DB::select()` with string concatenation?
- [ ] SQL: `->where()` with concatenated user input?
- [ ] Command: `exec()`, `system()`, `shell_exec()` with user input?
- [ ] LDAP: raw filter with user input?
- [ ] XPath: raw expression with user input?

## Auth / Access
- [ ] Action accessible without login check?
- [ ] Action modifies data with GET method (CSRF)?
- [ ] User ID taken from request instead of session?
- [ ] Role check before sensitive action?

## File handling
- [ ] `$_FILES` used without `basename()`?
- [ ] File path built from user input without whitelist?
- [ ] MIME type validated before save?
- [ ] Upload destination outside web root?

## Output
- [ ] `echo` / `print` of user input without `htmlspecialchars()`?
- [ ] JSON response contains raw user input?
- [ ] Header value built from user input (response splitting)?

## Session / Crypto
- [ ] `md5()` / `sha1()` for passwords (should be `password_hash`)?
- [ ] Session regenerated after login?
- [ ] Secure + HttpOnly flags on cookies?
```

One question per checkbox. Concrete, greppable, unambiguous. The checklist answers "what do I look for" so the agent only has to answer "is this present in this file".

## How the agent uses them

Wired into Review Mode (see [[Kasi-Review]]):

1. **Load or generate.** Review Mode resolves `CHECKLISTS/security-<stack>.md` from project, then hub. If neither exists, offer `build checklist <domain>` to scaffold before proceeding.
2. **Subagent dispatch.** One agent per file on Haiku, one per module on Opus/Sonnet. Each agent receives file path + checklist path + `PATTERNS.md`.
3. **Mechanical pass.** Agent walks each checkbox against the file. Not "does anything look wrong" — literally "does item 1 apply, does item 2 apply".
4. **Confidence tagging.** Every finding gets `[high | medium | low | unsure]` per [[Confidence-Labels]]. `[unsure]` findings are listed separately for user review, never silently filled in.
5. **Verifier pass.** Mandatory on Haiku, recommended on Sonnet security work. A second agent reads the first's findings and marks which reproduce vs which were speculative. False positives die here.

See [[Master-Orchestrator]] for how the main agent delegates without reading source itself.

## Built-in checklist domains

Shipped in Centerlite, pull into any project:

| Checklist | Scope | Tier fit |
|---|---|---|
| `security-php` | Laravel + raw PHP: injection, auth, file handling, output, crypto | any |
| `security-node` | Express / Node: same categories, JS-shaped | any |
| `performance-sql` | N+1, missing indexes, unbounded SELECTs, transaction leaks | Sonnet+ (needs profiling context) |
| `css-audit` | specificity wars, dead rules, width constraint traps | any |
| `api-review` | REST shape, status codes, pagination, error envelope | any |
| *more coming* | stack-specific variants as they graduate from project-level | — |

Detailed per-list contents live in each file. This table is a registry, not the content.

## Custom checklists

When a domain is missing, build one:

```
build checklist <domain>
```

Agent asks for stack + concern (e.g. "Vue 3 XSS", "Django ORM"), scaffolds a draft, saves to `.kasidit/CHECKLISTS/<domain>.md`. User edits. After it has proven itself on 2+ audits:

```
/kasi-promote checklist <name>
```

Lifts it into Centerlite so other projects can pull it down. Promotion requires confirmation — the hub stays lightweight by default. See [[Gravity-Pattern]] for the full promote/pull/sync flow.

## Why this beats reasoning

Observed pattern across Haiku audits:

- **Reasoning mode** — agent generates ~X "maybe this" findings, half of them speculative, confidence mixed, verifier throws out 40%+.
- **Checklist mode** — agent generates ~2X verified findings, ~0 false positives after verifier pass, confidence cleanly tagged.

The checklist removes the step where Haiku confabulates. It no longer has to decide what counts as a bug — the list decides. The agent becomes a pattern scanner, which is what it is good at.

This is why CHECKLISTS/ was the [[v0.3.0]] change that made Haiku viable. Not tier detection. Not confidence labels. The checklists. Everything else supports them.

## Anti-patterns

- Running Haiku review without a checklist. Output will look plausible and be mostly wrong. Refuse the mission or generate a checklist first.
- Writing a bespoke checklist per mission. Defeats the point — checklists compound value through reuse. If the domain is new, build once, promote, pull across projects.
- Skipping the verifier pass on Haiku. First-pass findings always include false positives from pattern match on names rather than behavior. Verifier is not optional.
- Using checklists as a report template instead of an audit tool. The file is a scanner, not a section header.
- Hub checklists with project-specific details (table names, client names). Centerlite stays generic; customize in `.kasidit/` only.

## See also

- [[Kasi-Review]] — the command that loads and runs checklists
- [[Kasi-Security]] — security-specific review flow
- [[Model-Tiers]] — why Haiku depends on these
- [[Gravity-Pattern]] — promote / pull / sync between project and hub
- [[Confidence-Labels]] — tagging rules for findings
- [[v0.3.0]] — release where CHECKLISTS/ was introduced
