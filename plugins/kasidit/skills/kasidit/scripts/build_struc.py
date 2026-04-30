#!/usr/bin/env python3
"""build_struc.py — project structure cache for /kasi-struc.

Writes .kasidit/STATE/:
  structure.json       overall summary
  modules.jsonl        one module (=directory) per line
  routes.jsonl         HTTP routes per file (Laravel + Node)
  config.json          detected configs (composer.json/package.json/etc.)
  changelog.jsonl      append-only state-change log (refresh mode only)
  last_sync            timestamp + git ref

Modes:
  build    full scan (overwrites)
  refresh  incremental — only re-scan files changed since last_sync
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

SKIP_DIRS = {"vendor", "node_modules", "dist", "build", ".git", ".next",
             "tests", "test", "__pycache__", ".venv", "venv", "coverage",
             "storage", "bootstrap/cache", ".kasidit"}
CODE_EXT = {".php", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
            ".py", ".go", ".rs", ".rb", ".java"}
CONFIG_FILES = {
    "composer.json", "package.json", "pyproject.toml", "go.mod",
    "Cargo.toml", "Gemfile", "pom.xml", "build.gradle",
    "wrangler.toml", "wrangler.jsonc", "vercel.json", "netlify.toml",
    "Dockerfile", "docker-compose.yml", "fly.toml", "Procfile",
    "serverless.yml", ".env.example",
}
MAX_FILE_BYTES = 1_000_000

# ---- route extractors -------------------------------------------------------

LARAVEL_ROUTE_RE = re.compile(
    r"Route::(get|post|put|patch|delete|any|match)\s*\(\s*['\"]([^'\"]+)['\"]"
    r"\s*,\s*(?:\[\s*([\w\\]+)::class\s*,\s*['\"](\w+)['\"]\s*\]"
    r"|['\"]([\w\\]+@\w+)['\"])"
)
LARAVEL_RESOURCE_RE = re.compile(
    r"Route::(?:apiResource|resource)\s*\(\s*['\"]([^'\"]+)['\"]\s*,"
    r"\s*([\w\\]+)::class"
)

EXPRESS_RE = re.compile(
    r"(?:app|router)\.(get|post|put|patch|delete|all|use)\s*"
    r"\(\s*['\"`]([^'\"`]+)['\"`]"
)
FASTIFY_RE = re.compile(
    r"fastify\.(get|post|put|patch|delete|all)\s*\(\s*['\"`]([^'\"`]+)['\"`]"
)
HONO_RE = re.compile(
    r"\bapp\.(get|post|put|patch|delete|all)\s*\(\s*['\"`]([^'\"`]+)['\"`]"
)
NEST_CONTROLLER_RE = re.compile(r"@Controller\s*\(\s*['\"`]?([^'\"`)]*)['\"`]?\s*\)")


def iter_files(root: Path):
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in files:
            yield Path(dirpath) / fn


def lang_of(path: Path) -> str:
    ext = path.suffix.lower()
    return {
        ".php": "php", ".js": "js", ".mjs": "js", ".cjs": "js",
        ".jsx": "jsx", ".ts": "ts", ".tsx": "tsx", ".py": "py",
        ".go": "go", ".rs": "rs", ".rb": "rb", ".java": "java",
    }.get(ext, "other")


def detect_config(root: Path):
    found = {}
    for name in CONFIG_FILES:
        p = root / name
        if p.exists():
            found[name] = str(p.relative_to(root))
    framework = []
    if (root / "composer.json").exists():
        try:
            data = json.loads((root / "composer.json").read_text())
            req = data.get("require", {})
            if "laravel/framework" in req:
                framework.append(f"laravel@{req['laravel/framework']}")
        except Exception:
            pass
    if (root / "package.json").exists():
        try:
            data = json.loads((root / "package.json").read_text())
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            for k in ("express", "fastify", "hono", "@nestjs/core", "koa", "next",
                      "vue", "react", "@sveltejs/kit"):
                if k in deps:
                    framework.append(f"{k}@{deps[k]}")
        except Exception:
            pass
    found["_frameworks"] = framework
    return found


def extract_routes(path: Path, text: str):
    routes = []
    rel = str(path)
    if path.suffix.lower() == ".php":
        for m in LARAVEL_ROUTE_RE.finditer(text):
            method, route = m.group(1).upper(), m.group(2)
            if m.group(3):
                handler = f"{m.group(3)}@{m.group(4)}"
            else:
                handler = m.group(5) or ""
            routes.append({"method": method, "path": route, "handler": handler,
                           "file": rel, "framework": "laravel"})
        for m in LARAVEL_RESOURCE_RE.finditer(text):
            routes.append({"method": "RESOURCE", "path": m.group(1),
                           "handler": m.group(2), "file": rel,
                           "framework": "laravel"})
    if path.suffix.lower() in {".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx"}:
        for rx, fw in ((EXPRESS_RE, "express"), (FASTIFY_RE, "fastify"),
                       (HONO_RE, "hono")):
            for m in rx.finditer(text):
                routes.append({"method": m.group(1).upper(),
                               "path": m.group(2), "handler": "",
                               "file": rel, "framework": fw})
        for m in NEST_CONTROLLER_RE.finditer(text):
            routes.append({"method": "CONTROLLER", "path": m.group(1) or "/",
                           "handler": "", "file": rel, "framework": "nest"})
    return routes


def list_modules(root: Path, files):
    """Group files by their first/second-level directory."""
    mod = defaultdict(lambda: {"files": [], "lang": defaultdict(int)})
    for p in files:
        rel = p.relative_to(root)
        parts = rel.parts
        # module = first 1 or 2 path segments depending on depth
        if len(parts) == 1:
            key = "<root>"
        elif parts[0] in {"app", "src", "lib", "pkg", "internal"} and len(parts) >= 2:
            key = "/".join(parts[:2])
        else:
            key = parts[0]
        mod[key]["files"].append(str(rel))
        mod[key]["lang"][lang_of(p)] += 1
    return mod


def git_head(root: Path):
    try:
        out = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=2)
        if out.returncode == 0:
            return out.stdout.strip()
    except Exception:
        pass
    return None


def git_changed(root: Path, since_ref: str):
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "diff", "--name-only",
             f"{since_ref}..HEAD"],
            capture_output=True, text=True, timeout=5)
        committed = out.stdout.strip().splitlines() if out.returncode == 0 else []
        out2 = subprocess.run(
            ["git", "-C", str(root), "diff", "--name-only"],
            capture_output=True, text=True, timeout=5)
        unstaged = out2.stdout.strip().splitlines() if out2.returncode == 0 else []
        out3 = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--others", "--exclude-standard"],
            capture_output=True, text=True, timeout=5)
        untracked = out3.stdout.strip().splitlines() if out3.returncode == 0 else []
        return set(committed) | set(unstaged) | set(untracked)
    except Exception:
        return None


def build(root: Path, mode: str):
    state = root / ".kasidit" / "STATE"
    state.mkdir(parents=True, exist_ok=True)

    last_sync_path = state / "last_sync"
    prev_ref = None
    prev_ts = None
    if last_sync_path.exists():
        try:
            d = json.loads(last_sync_path.read_text())
            prev_ref = d.get("git_ref")
            prev_ts = d.get("ts")
        except Exception:
            pass

    all_files = [p for p in iter_files(root)
                 if p.suffix.lower() in CODE_EXT and
                 p.stat().st_size < MAX_FILE_BYTES]

    # Refresh: filter to changed files only
    changed_set = None
    if mode == "refresh" and prev_ref:
        changed_set = git_changed(root, prev_ref)

    # config + modules: re-scan all (cheap, dir-walk only)
    cfg = detect_config(root)
    mods = list_modules(root, all_files)

    # routes: full or incremental
    routes = []
    target_files = all_files
    if changed_set is not None:
        target_files = [p for p in all_files
                        if str(p.relative_to(root)) in changed_set]

    for p in target_files:
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rs = extract_routes(p.relative_to(root), text)
        routes.extend(rs)

    # write outputs
    structure = {
        "scanned": len(all_files),
        "code_files": sum(1 for p in all_files),
        "module_count": len(mods),
        "route_count": len(routes),
        "languages": _lang_summary(all_files),
        "frameworks": cfg.get("_frameworks", []),
    }
    (state / "structure.json").write_text(
        json.dumps(structure, indent=2, ensure_ascii=False))

    with (state / "modules.jsonl").open("w", encoding="utf-8") as f:
        for name, info in sorted(mods.items()):
            row = {
                "name": name,
                "file_count": len(info["files"]),
                "lang": dict(info["lang"]),
                "files": info["files"][:200],  # cap
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    routes_path = state / "routes.jsonl"
    if mode == "build" or routes_path.exists() is False:
        routes_path.write_text("")
    with routes_path.open("a", encoding="utf-8") as f:
        for r in routes:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    (state / "config.json").write_text(
        json.dumps(cfg, indent=2, ensure_ascii=False))

    # changelog (refresh only)
    if mode == "refresh" and changed_set is not None:
        with (state / "changelog.jsonl").open("a", encoding="utf-8") as f:
            now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            for fp in sorted(changed_set):
                if not fp:
                    continue
                f.write(json.dumps({
                    "ts": now, "op": "modify", "kind": "file", "path": fp,
                    "by": "refresh"
                }, ensure_ascii=False) + "\n")

    last_sync_path.write_text(json.dumps({
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_ref": git_head(root),
        "mode": mode,
        "prev_ts": prev_ts,
    }, indent=2))

    print(f"[kasi-struc] mode={mode} files={len(all_files)} "
          f"modules={len(mods)} routes={len(routes)} state={state}")


def _lang_summary(files):
    out = defaultdict(int)
    for p in files:
        out[lang_of(p)] += 1
    return dict(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--mode", choices=["build", "refresh"], default="build")
    args = ap.parse_args()
    build(Path(args.root), args.mode)


if __name__ == "__main__":
    main()
