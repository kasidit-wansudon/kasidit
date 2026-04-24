# Node.js Security Scan Checklist

For each route/handler/module, check:

## Injection / Execution
- [ ] `child_process.exec` / `execSync` with user input — switch to `execFile` with arg array
- [ ] `spawn` / `exec` called with `shell: true` on untrusted input — drop `shell: true`
- [ ] `eval()`, `new Function()`, `vm.runInNewContext` on untrusted input — remove or sandbox
- [ ] Regex built from user input or known catastrophic pattern (ReDoS) — cap input length, use `re2`

## Prototype / Deserialization
- [ ] `Object.assign({}, req.body)` or lodash `_.merge` with request body — use allowlist / `Object.create(null)`
- [ ] `node-serialize` `unserialize()` or `serialize-javascript` unserialize on user input — replace with JSON
- [ ] Schema validation missing on `req.body` — add `zod` / `joi` / `ajv`

## Path / File
- [ ] `path.join(base, userInput)` without `path.resolve` + `startsWith(base)` check — add containment guard
- [ ] `fs.readFile` / `createReadStream` with raw user filename — whitelist + normalise first

## Auth / Session
- [ ] JWT `alg: none` accepted or algorithm not pinned — set `algorithms: ['HS256'|'RS256']` in `verify`
- [ ] JWT HS256 secret short / from default config — rotate to 32+ byte random secret
- [ ] Express CSRF token missing on state-changing POST — add `csurf` or double-submit cookie
- [ ] `Access-Control-Allow-Origin: *` combined with `credentials: true` — pin origin list

## Network / SSRF
- [ ] `fetch` / `axios` / `http.request` URL taken from request — allowlist host, block RFC1918 / `localhost`
- [ ] Redirect following on outbound request with user URL — set `maxRedirects: 0` or revalidate host

## Output / XSS
- [ ] React `dangerouslySetInnerHTML` fed by user content — sanitise with `DOMPurify`
- [ ] Vue `v-html` / Angular `[innerHTML]` on user content — same, sanitise first
- [ ] Response built by string concat of user input into HTML — use templating escape

## Crypto / Secrets
- [ ] `crypto.createCipher` (deprecated, no IV) — switch to `createCipheriv` with random 12/16-byte IV
- [ ] Hardcoded secret / API key in source — move to env, rotate the leaked value
- [ ] `.env` / `.env.*` committed to repo — `git rm --cached`, add to `.gitignore`, rotate

## Supply chain
- [ ] `npm audit` / `pnpm audit` shows high/critical — patch or pin
- [ ] Lockfile (`package-lock.json` / `pnpm-lock.yaml`) missing from repo — commit it
