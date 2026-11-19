#!/usr/bin/env python3
"""
kasi_mainfile.py — shared helper: load the user's pinned rules (main.md).

Two files, both optional, merged in this order (project last = wins on conflict):
  1. $KASIDIT_CENTER/main.md          — global, every project
  2. <cwd>/.kasidit/main.md           — project override

main.md format:

  ---
  reply_language: th
  onboarded: true
  forbid_scripts:
  allow_scripts:
  ---
  ## Always
  - short rules re-sent on every prompt (keep 3-7 lines)

  ## Context
  - longer detail, sent only at session start / after compact

Frontmatter keys:
  reply_language — ISO code (th, en, ja, ...). Generates the language rule and
                   makes the Stop check block other scripts. Unset = onboarding.
  onboarded      — true once the onboarding steps after language were offered.
  forbid_scripts — extra scripts to block (comma-separated).
  allow_scripts  — scripts never blocked, e.g. han for Chinese file names.

CLI (used by /kasi-main so frontmatter is never hand-edited):
  python3 kasi_mainfile.py set <key> <value> [--project <dir>]
  python3 kasi_mainfile.py get <key> [--cwd <dir>]
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

CENTER = Path(os.environ.get("KASIDIT_CENTER",
    os.path.expanduser("~/.claude/skills/kasidit/center")))

# Hard cap on the per-prompt Always block — it rides on every turn.
ALWAYS_MAX_CHARS = 1200

# Letters unique to each script. Latin (English, Spanish, ...) is never listed:
# code terms and identifiers are Latin in every language.
SCRIPTS = {
    "vietnamese": re.compile('[Ạ-ỹƠơƯưĂăĐđ]'),
    "thai": re.compile('[฀-๿]'),
    "han": re.compile('[㐀-䶿一-鿿]'),
    "kana": re.compile('[぀-ヿ]'),
    "hangul": re.compile('[ᄀ-ᇿ가-힯]'),
    "cyrillic": re.compile('[Ѐ-ӿ]'),
    "arabic": re.compile('[؀-ۿ]'),
    "hebrew": re.compile('[֐-׿]'),
    "devanagari": re.compile('[ऀ-ॿ]'),
}
# Aliases accepted in forbid_scripts / allow_scripts.
SCRIPT_ALIASES = {"chinese": "han", "japanese": "kana", "korean": "hangul", "russian": "cyrillic"}

# reply_language → (display name, scripts that language itself uses)
LANGUAGES: Dict[str, Tuple[str, Set[str]]] = {
    "th": ("Thai", {"thai"}),
    "en": ("English", set()),
    "es": ("Spanish", set()),
    "fr": ("French", set()),
    "de": ("German", set()),
    "pt": ("Portuguese", set()),
    "it": ("Italian", set()),
    "id": ("Indonesian", set()),
    "ms": ("Malay", set()),
    "vi": ("Vietnamese", {"vietnamese"}),
    "zh": ("Chinese", {"han"}),
    "ja": ("Japanese", {"kana", "han"}),
    "ko": ("Korean", {"hangul", "han"}),
    "ru": ("Russian", {"cyrillic"}),
    "uk": ("Ukrainian", {"cyrillic"}),
    "ar": ("Arabic", {"arabic"}),
    "he": ("Hebrew", {"hebrew"}),
    "hi": ("Hindi", {"devanagari"}),
}

_FRONTMATTER = re.compile(r'\A---\n(.*?)\n---\n?', re.S)

NEW_FILE = """---
reply_language:
onboarded: false
forbid_scripts:
allow_scripts:
---
## Always

## Context
"""


def main_paths(cwd: Optional[str]) -> List[Path]:
    paths = [CENTER / "main.md"]
    if cwd:
        paths.append(Path(cwd) / ".kasidit" / "main.md")
    return [p for p in paths if p.is_file()]


def _split(text: str):
    """Return (frontmatter_dict, body)."""
    meta = {}
    m = _FRONTMATTER.match(text)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text


def _read(p: Path):
    return _split(p.read_text(encoding="utf-8", errors="replace"))


def _section(body: str, name: str) -> str:
    """Text under `## <name>` up to the next `## ` heading."""
    m = re.search(r'^##\s+' + re.escape(name) + r'\s*$(.*?)(?=^##\s|\Z)', body, re.M | re.S)
    return m.group(1).strip() if m else ""


def meta_value(cwd: Optional[str], key: str) -> str:
    """Frontmatter value, project file overriding center. Empty if unset."""
    value = ""
    for p in main_paths(cwd):
        meta, _ = _read(p)
        if meta.get(key):
            value = meta[key]
    return value


def reply_language(cwd: Optional[str]) -> str:
    return meta_value(cwd, "reply_language").lower()


def onboarded(cwd: Optional[str]) -> bool:
    return meta_value(cwd, "onboarded").lower() == "true"


def language_rule(code: str) -> str:
    name = LANGUAGES.get(code, (code, set()))[0]
    return (f"- Reply in {name} — every user-facing sentence, including short progress notes. "
            f"Code, comments and identifiers stay in English.")


def load_full(cwd: Optional[str]) -> str:
    """Full main.md bodies (frontmatter stripped), center first then project."""
    parts = []
    code = reply_language(cwd)
    if code:
        parts.append(language_rule(code))
    for p in main_paths(cwd):
        _, body = _read(p)
        if body.strip():
            parts.append(f"<!-- {p} -->\n{body.strip()}")
    return "\n\n".join(parts)


def load_always(cwd: Optional[str]) -> str:
    """Language rule + merged `## Always` sections, capped at ALWAYS_MAX_CHARS."""
    parts = []
    code = reply_language(cwd)
    if code:
        parts.append(language_rule(code))
    for p in main_paths(cwd):
        _, body = _read(p)
        sec = _section(body, "Always")
        if sec:
            parts.append(sec)
    text = "\n".join(parts)
    if len(text) > ALWAYS_MAX_CHARS:
        text = text[:ALWAYS_MAX_CHARS].rstrip() + "\n[kasidit main] Always section truncated — shorten main.md"
    return text


def _script_names(raw: str) -> Set[str]:
    out = set()
    for name in raw.split(","):
        name = SCRIPT_ALIASES.get(name.strip().lower(), name.strip().lower())
        if name in SCRIPTS:
            out.add(name)
    return out


def forbidden_scripts(cwd: Optional[str]) -> Set[str]:
    """Scripts the Stop check blocks: every script foreign to reply_language,
    plus forbid_scripts, minus allow_scripts."""
    forbid: Set[str] = set()
    allow: Set[str] = set()
    for p in main_paths(cwd):
        meta, _ = _read(p)
        forbid |= _script_names(meta.get("forbid_scripts", ""))
        allow |= _script_names(meta.get("allow_scripts", ""))
    code = reply_language(cwd)
    if code in LANGUAGES:
        forbid |= set(SCRIPTS) - LANGUAGES[code][1]
    return forbid - allow


def set_value(path: Path, key: str, value: str) -> None:
    """Set one frontmatter key in main.md, creating the file if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = path.read_text(encoding="utf-8") if path.is_file() else NEW_FILE
    m = _FRONTMATTER.match(text)
    if not m:
        text = NEW_FILE.split("## Always")[0] + text
        m = _FRONTMATTER.match(text)
    lines = m.group(1).splitlines()
    for i, line in enumerate(lines):
        if line.split(":", 1)[0].strip() == key:
            lines[i] = f"{key}: {value}"
            break
    else:
        lines.append(f"{key}: {value}")
    path.write_text("---\n" + "\n".join(lines) + "\n---\n" + text[m.end():], encoding="utf-8")


def _cli(argv: List[str]) -> int:
    def opt(name):
        if name in argv:
            i = argv.index(name)
            val = argv[i + 1]
            del argv[i:i + 2]
            return val
        return None

    project = opt("--project")
    cwd = opt("--cwd")
    if len(argv) == 3 and argv[0] == "set":
        _, key, value = argv
        if key == "reply_language" and value.lower() not in LANGUAGES:
            print(f"unknown language code '{value}'. known: {', '.join(sorted(LANGUAGES))}", file=sys.stderr)
            return 2
        target = Path(project) / ".kasidit" / "main.md" if project else CENTER / "main.md"
        set_value(target, key, value.lower() if key == "reply_language" else value)
        print(f"{target}: {key} = {value}")
        return 0
    if len(argv) == 2 and argv[0] == "get":
        print(meta_value(cwd, argv[1]))
        return 0
    print(__doc__.split("CLI")[1].strip(), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(_cli(sys.argv[1:]))
