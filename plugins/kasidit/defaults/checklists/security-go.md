# Go Security Scan Checklist

For each handler/package, check:

## Injection
- [ ] SQL: `fmt.Sprintf` into `db.Exec` / `db.Query` (use `?` / `$1` placeholders)?
- [ ] Command: `exec.Command("sh", "-c", userInput)` with user input?
- [ ] Path traversal: `filepath.Join` without `filepath.Clean` + prefix check?
- [ ] SSRF: `http.Get(userURL)` without host whitelist?
- [ ] Regex: `regexp.MustCompile` compiled from user input (ReDoS)?

## Output / Templates
- [ ] `text/template` used for HTML output (should be `html/template`)?
- [ ] gorilla/mux path/query params echoed without sanitization?

## Crypto / Secrets
- [ ] `md5` / `sha1` used for auth / password hashing?
- [ ] `math/rand` used for tokens / IDs (should be `crypto/rand`)?
- [ ] Hardcoded secrets / API keys / DB creds in source?
- [ ] JWT `alg=none` accepted, or `HS256` secret committed to repo?

## TLS / Transport
- [ ] `tls.InsecureSkipVerify: true` in production client?
- [ ] `http.Server` missing `ReadTimeout` / `WriteTimeout` (slowloris)?

## Runtime safety
- [ ] `nil` map written to, or `nil` slice indexed (panic)?
- [ ] Shared state without mutex — run `go test -race`?
- [ ] `os.Open` / `os.ReadFile` on user-supplied path without scope check?
