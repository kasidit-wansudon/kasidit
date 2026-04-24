# Python Security Scan Checklist

For each module / view / handler, check:

## Injection
- [ ] SQL: `cursor.execute(f"...{var}...")` / `%` formatting — use parameterized `execute(sql, params)`?
- [ ] Command: `subprocess.run(..., shell=True)` / `os.system` with user input — drop `shell=True`, pass list?
- [ ] LDAP / XPath: filter / expression built by string concat — escape via `ldap.filter.escape_filter_chars` / parameterized query?

## Deserialization / Code exec
- [ ] `pickle.load` / `marshal.loads` / `yaml.load` without `SafeLoader` on untrusted input — switch to `yaml.safe_load` / JSON?
- [ ] `eval` / `exec` / `compile` on user input — remove or sandbox?
- [ ] `joblib.load` / `torch.load` on untrusted model files — verify source / use `weights_only=True`?

## File / Network
- [ ] `open(user_path)` without `os.path.abspath` + boundary check — path traversal risk?
- [ ] `requests.get(user_url)` / `urllib.urlopen` without host allowlist — SSRF risk?
- [ ] XML: `lxml` / `xml.etree.ElementTree` with external entities — use `defusedxml`?

## Config / Crypto / Secrets
- [ ] Flask/Django `DEBUG=True` in prod — gate on env?
- [ ] `hashlib.md5` / `sha1` for passwords or `random.random` for tokens — use `bcrypt`/`argon2` + `secrets`?
- [ ] Hardcoded API keys / DB passwords in source — move to env / secret store (grep `API_KEY=`, `password=`)?

## Web framework
- [ ] Django/Flask form missing CSRF token — `{% csrf_token %}` / `flask-wtf`?
- [ ] Jinja2 `autoescape=False` or `| safe` on user content — re-enable autoescape?

## Supply chain
- [ ] Dependency CVEs — run `pip-audit` / `safety check` in CI?
