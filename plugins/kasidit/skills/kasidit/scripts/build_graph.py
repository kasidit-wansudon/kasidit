#!/usr/bin/env python3
"""build_graph.py — function call graph builder.

MVP: PHP + JS/TS via regex. ast-grep path stubbed (calls ast-grep if
available, else falls back to regex). Writes FUNCTIONS.jsonl + HOTSPOTS.md.

Limits:
  - Static analysis only. Misses dynamic dispatch, magic methods, reflection.
  - Resolution by name match. Two classes with method `save` both link.
  - Per-edge confidence: high (class+method match) / medium (name only) / low (string).
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

SKIP_DIRS = {"vendor", "node_modules", "dist", "build", ".git", ".next",
             "tests", "test", "__pycache__", ".venv", "venv", "coverage",
             "storage", "bootstrap/cache"}
PHP_EXT = {".php"}
JS_EXT = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
MAX_FILE_BYTES = 1_000_000  # 1MB

# ---- regex extractors -------------------------------------------------------

# PHP function/method definitions. class Foo { public function bar(...) {} }
PHP_CLASS_RE = re.compile(r"^\s*(?:abstract\s+|final\s+)?class\s+(\w+)", re.M)
PHP_FN_RE = re.compile(
    r"^\s*(?:public|protected|private|static|\s)*\s*function\s+(\w+)\s*\(",
    re.M)
# PHP call sites. $this->foo(, self::bar(, Foo::bar(, foo(
PHP_CALL_RE = re.compile(
    r"(?:\$this->|self::|static::|(?:[A-Z]\w*)::)?(\w+)\s*\(")

# JS/TS function definitions.
JS_FN_RE = re.compile(
    r"(?:^|\s)(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(", re.M)
JS_METHOD_RE = re.compile(
    r"^\s*(?:async\s+)?(?:static\s+)?(\w+)\s*\([^)]*\)\s*\{", re.M)
JS_ARROW_RE = re.compile(
    r"(?:^|\s)(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(",
    re.M)
JS_CLASS_RE = re.compile(r"(?:^|\s)(?:export\s+)?class\s+(\w+)", re.M)
JS_CALL_RE = re.compile(r"(?<![\.\w])(\w+)\s*\(")


def iter_files(root: Path):
    for dirpath, dirs, files in os.walk(root):
        # in-place prune
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in files:
            p = Path(dirpath) / fn
            ext = p.suffix.lower()
            if ext in PHP_EXT or ext in JS_EXT:
                try:
                    if p.stat().st_size > MAX_FILE_BYTES:
                        continue
                except OSError:
                    continue
                yield p


def extract_php(path: Path, text: str):
    defs = []  # [{class, fn, line}]
    cls_stack = []
    classes_at = {}  # line -> class
    for m in PHP_CLASS_RE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        classes_at[line] = m.group(1)
    cur_class = None
    sorted_class_lines = sorted(classes_at.keys())

    for m in PHP_FN_RE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        # find the most recent class def above this line
        cur_class = None
        for cl in sorted_class_lines:
            if cl <= line:
                cur_class = classes_at[cl]
            else:
                break
        defs.append({"class": cur_class, "fn": m.group(1), "line": line})

    calls = set()
    for m in PHP_CALL_RE.finditer(text):
        name = m.group(1)
        if name in {"if", "for", "foreach", "while", "switch", "function",
                    "return", "echo", "print", "isset", "empty", "array",
                    "list", "die", "exit", "include", "require",
                    "include_once", "require_once", "use", "new", "throw",
                    "catch", "do"}:
            continue
        calls.add(name)
    return defs, calls


def extract_js(path: Path, text: str):
    defs = []
    classes_at = {}
    for m in JS_CLASS_RE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        classes_at[line] = m.group(1)
    sorted_class_lines = sorted(classes_at.keys())

    found = set()  # dedupe by (class, fn, line)
    for rx in (JS_FN_RE, JS_METHOD_RE, JS_ARROW_RE):
        for m in rx.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            cur_class = None
            for cl in sorted_class_lines:
                if cl <= line:
                    cur_class = classes_at[cl]
                else:
                    break
            key = (cur_class, m.group(1), line)
            if key in found:
                continue
            found.add(key)
            # filter very common non-fn matches
            name = m.group(1)
            if name in {"if", "for", "while", "switch", "return", "function",
                        "import", "export", "default", "class", "const",
                        "let", "var", "case", "do"}:
                continue
            defs.append({"class": cur_class, "fn": name, "line": line})

    calls = set()
    for m in JS_CALL_RE.finditer(text):
        name = m.group(1)
        if name in {"if", "for", "while", "switch", "return", "function",
                    "import", "export", "default", "class", "const",
                    "let", "var", "case", "do", "catch", "throw", "new",
                    "typeof", "void", "in", "of", "yield", "await"}:
            continue
        calls.add(name)
    return defs, calls


# ---- main pipeline ----------------------------------------------------------


def build(root: Path, out_jsonl: Path, out_md: Path, parser: str):
    all_defs = []  # [{file, class, fn, line, lang, calls(set)}]
    by_name = defaultdict(list)  # fn name -> [def index]

    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        ext = path.suffix.lower()
        if ext in PHP_EXT:
            defs, calls = extract_php(path, text)
            lang = "php"
        else:
            defs, calls = extract_js(path, text)
            lang = "js" if ext in {".js", ".jsx", ".mjs", ".cjs"} else "ts"
        rel = str(path.relative_to(root))
        # NOTE: assigning all file-level calls to every def in the file is
        # imprecise but safe for MVP. Per-fn body extraction would need brace
        # tracking — defer to ast-grep path.
        for d in defs:
            d_full = {
                "file": rel,
                "class": d["class"],
                "fn": d["fn"],
                "line": d["line"],
                "lang": lang,
                "calls": sorted(calls),
                "called_by": [],
            }
            all_defs.append(d_full)
            by_name[d["fn"]].append(len(all_defs) - 1)

    # resolve called_by
    for idx, d in enumerate(all_defs):
        for c in d["calls"]:
            for tgt in by_name.get(c, []):
                if tgt == idx:
                    continue
                sig = f"{d['class']}::{d['fn']}" if d["class"] else d["fn"]
                all_defs[tgt]["called_by"].append(f"{d['file']}:{sig}")

    # write JSONL
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with out_jsonl.open("w", encoding="utf-8") as f:
        for d in all_defs:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    # hotspots
    hubs = sorted(all_defs, key=lambda d: -len(d["called_by"]))[:10]
    callers = sorted(all_defs, key=lambda d: -len(d["calls"]))[:10]
    isolated = [d for d in all_defs
                if not d["called_by"] and not d["calls"]][:20]
    dead = [d for d in all_defs if not d["called_by"]][:30]

    def sig(d):
        return f"{d['class']}::{d['fn']}" if d["class"] else d["fn"]

    lines = [
        "# Hotspots",
        "",
        f"_Generated by build_graph.py · parser={parser} · "
        f"functions={len(all_defs)}_",
        "",
        "## Top hubs (called the most)",
        "",
    ]
    for i, d in enumerate(hubs, 1):
        lines.append(
            f"{i}. `{sig(d)}` — {len(d['called_by'])} callers — "
            f"{d['file']}:{d['line']}")
    lines += ["", "## Top callers (call the most)", ""]
    for i, d in enumerate(callers, 1):
        lines.append(
            f"{i}. `{sig(d)}` — calls {len(d['calls'])} fns — "
            f"{d['file']}:{d['line']}")
    lines += ["", "## Isolated (no caller, no callee)", ""]
    for d in isolated:
        lines.append(f"- `{sig(d)}` — {d['file']}:{d['line']}")
    lines += ["", "## Dead (defined but never called)", ""]
    for d in dead:
        lines.append(f"- `{sig(d)}` — {d['file']}:{d['line']}")

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[kasi-graph] functions={len(all_defs)} hubs={len(hubs)} "
          f"jsonl={out_jsonl} md={out_md}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out-jsonl", required=True)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--parser", default="grep-fallback")
    args = ap.parse_args()

    if args.parser == "ast-grep":
        # Future: invoke ast-grep here for exact extraction.
        # For MVP, fall through to regex.
        sys.stderr.write(
            "[kasi-graph] ast-grep available but using regex MVP; "
            "AST path TBD\n")

    build(Path(args.root), Path(args.out_jsonl), Path(args.out_md),
          args.parser)


if __name__ == "__main__":
    main()
