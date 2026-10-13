#!/usr/bin/env node
// kasi_diagram.mjs — soft bridge from Kasidit to Archify (https://github.com/tt-a1i/archify).
//
// Archify is NOT bundled. This script only locates an existing install and
// calls its CLI. If Archify is missing, it exits 3 and the caller falls back
// to a text diagram (Rule 3). Node >= 18, no dependencies.
//
// Usage:
//   kasi_diagram.mjs find
//   kasi_diagram.mjs langs [--json]
//   kasi_diagram.mjs render <type> <input.json> <output.html> [--lang <tag>] [--check] [--project <dir>]
//
// Exit codes: 0 ok · 2 usage/validation error · 3 archify not installed · 4 unknown language

import { existsSync, readFileSync, readdirSync, writeFileSync, mkdtempSync, rmSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { dirname, join, resolve, basename } from 'node:path';
import { homedir, tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const TYPES = ['architecture', 'workflow', 'sequence', 'dataflow', 'lifecycle'];
const BUILTIN = ['en', 'zh-CN'];

// Kasidit-owned catalogs. Installed layout: ~/.claude/skills/kasidit/{scripts,locales};
// plugin layout: skills/kasidit/{scripts,locales}. Both resolve to ../locales.
const KASI_LOCALES = resolve(HERE, '..', 'locales');

function fail(code, msg) {
  process.stderr.write(`[kasi-diagram] ${msg}\n`);
  process.exit(code);
}

function findArchify() {
  const home = homedir();
  const candidates = [
    process.env.ARCHIFY_HOME,
    join(home, '.claude', 'skills', 'archify'),
    join(home, '.agents', 'skills', 'archify'),
    join(home, '.codex', 'skills', 'archify'),
    join(home, '.cursor', 'skills', 'archify'),
    join(home, '.config', 'opencode', 'skills', 'archify'),
  ].filter(Boolean);
  for (const dir of candidates) {
    if (existsSync(join(dir, 'bin', 'archify.mjs'))) return dir;
  }
  return null;
}

function listLangs(archify) {
  const langs = new Map();
  for (const tag of BUILTIN) langs.set(tag, 'archify built-in');
  const scan = (dir, source) => {
    if (!dir || !existsSync(dir)) return;
    for (const f of readdirSync(dir)) {
      if (!f.endsWith('.json') || f.includes('.partial.')) continue;
      const tag = f.slice(0, -5);
      if (!langs.has(tag)) langs.set(tag, source);
    }
  };
  // Kasidit catalogs win over Archify examples for the same tag.
  scan(KASI_LOCALES, 'kasidit');
  scan(archify && join(archify, 'examples', 'locales'), 'archify examples');
  return langs;
}

function catalogPath(tag, archify) {
  for (const dir of [KASI_LOCALES, archify && join(archify, 'examples', 'locales')]) {
    if (!dir) continue;
    const p = join(dir, `${tag}.json`);
    if (existsSync(p)) return p;
  }
  return null;
}

function projectLang(projectDir) {
  const cfg = join(projectDir, '.kasidit', 'config.json');
  if (!existsSync(cfg)) return null;
  try {
    const j = JSON.parse(readFileSync(cfg, 'utf8'));
    return j?.diagram?.lang ?? null;
  } catch {
    return null;
  }
}

function parseFlags(argv) {
  const pos = [];
  const flags = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--check' || a === '--json') flags[a.slice(2)] = true;
    else if (a === '--lang' || a === '--project') flags[a.slice(2)] = argv[++i];
    else pos.push(a);
  }
  return { pos, flags };
}

function runArchify(archify, args) {
  const env = { ...process.env };
  // Update check is a network call; off unless the user opts back in.
  if (env.ARCHIFY_UPDATE_CHECK_DISABLED === undefined) env.ARCHIFY_UPDATE_CHECK_DISABLED = '1';
  const r = spawnSync(process.execPath, [join(archify, 'bin', 'archify.mjs'), ...args], {
    env,
    encoding: 'utf8',
  });
  if (r.stdout) process.stdout.write(r.stdout);
  if (r.stderr) process.stderr.write(r.stderr);
  return r.status ?? 1;
}

const [cmd, ...rest] = process.argv.slice(2);
const { pos, flags } = parseFlags(rest);
const archify = findArchify();

if (cmd === 'find') {
  if (!archify) fail(3, 'archify not installed. Install: npx skills add tt-a1i/archify -g  (or set ARCHIFY_HOME)');
  console.log(archify);
  process.exit(0);
}

if (cmd === 'langs') {
  const langs = listLangs(archify);
  if (flags.json) console.log(JSON.stringify(Object.fromEntries(langs)));
  else for (const [tag, src] of langs) console.log(`${tag}\t${src}`);
  process.exit(0);
}

if (cmd === 'render') {
  const [type, input, output] = pos;
  if (!TYPES.includes(type) || !input || !output) {
    fail(2, `usage: render <${TYPES.join('|')}> <input.json> <output.html> [--lang <tag>] [--check]`);
  }
  if (!archify) fail(3, 'archify not installed. Install: npx skills add tt-a1i/archify -g  (or set ARCHIFY_HOME)');

  let doc;
  try {
    doc = JSON.parse(readFileSync(input, 'utf8'));
  } catch (e) {
    fail(2, `cannot read ${input}: ${e.message}`);
  }
  doc.meta ??= {};
  if (!doc.meta.output) doc.meta.output = basename(output);

  const lang = flags.lang ?? projectLang(resolve(flags.project ?? process.cwd())) ?? doc.meta.locale ?? 'en';
  if (BUILTIN.includes(lang)) {
    doc.meta.locale = lang;
    delete doc.meta.translations;
  } else {
    const p = catalogPath(lang, archify);
    if (!p) {
      const avail = [...listLangs(archify).keys()].join(', ');
      fail(4, `no catalog for "${lang}". Available: ${avail}. Add one at ${KASI_LOCALES}/${lang}.json`);
    }
    doc.meta.locale = lang;
    doc.meta.translations = JSON.parse(readFileSync(p, 'utf8'));
  }

  // Work on a temp copy so the user's authored JSON stays free of the 400+ key catalog.
  const tmp = mkdtempSync(join(tmpdir(), 'kasi-diagram-'));
  const staged = join(tmp, basename(input));
  writeFileSync(staged, JSON.stringify(doc, null, 2));
  try {
    let code = runArchify(archify, ['validate', type, staged]);
    if (code !== 0) process.exit(2);
    code = runArchify(archify, ['render', type, staged, resolve(output)]);
    if (code !== 0) process.exit(code);
    if (flags.check) {
      code = runArchify(archify, ['visual-check', resolve(output), '--summary', '--out-dir', join(dirname(resolve(output)), '.archify-check')]);
      if (code !== 0) process.exit(code);
    }
    console.log(`[kasi-diagram] ok lang=${lang} -> ${resolve(output)}`);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
  process.exit(0);
}

fail(2, 'usage: kasi_diagram.mjs <find|langs|render> ...');
