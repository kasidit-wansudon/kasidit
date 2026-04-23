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
