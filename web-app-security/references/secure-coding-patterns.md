# Secure coding patterns

Vulnerable -> fixed examples. Adapt to the project's language, framework, and conventions; do not paste blindly. Each pattern names the CWE.

## Contents
1. SQL injection (CWE-89)
2. OS command injection (CWE-78)
3. XSS (CWE-79)
4. Broken object authorization (CWE-862 / CWE-639 / CWE-863)
5. Mass assignment (CWE-915)
6. Path traversal and uploads (CWE-22, CWE-434)
7. SSRF (CWE-918)
8. CSRF (CWE-352)
9. Unsafe deserialization (CWE-502)
10. Secrets (CWE-798, CWE-312)
11. Open redirect (CWE-601)
12. Race conditions (CWE-362)
13. Error handling that fails open (CWE-755)
14. Fix workflow

## 1. SQL injection
```python
# Vulnerable
cur.execute(f"SELECT * FROM users WHERE email = '{email}'")
# Fixed: bound parameter
cur.execute("SELECT * FROM users WHERE email = %s", (email,))
```
Dynamic column/table/ORDER BY: map user choice to an allowlist, never interpolate. ORMs: avoid raw fragments with user input; use the ORM's parameter binding in `raw()` calls.

## 2. OS command injection
```python
# Vulnerable
os.system("convert " + filename + " out.png")
# Fixed: no shell, argument list, validated input
subprocess.run(["convert", safe_path, "out.png"], check=True, timeout=10)
```
Prefer a library over spawning a process. If a process is unavoidable, allowlist arguments and drop privileges.

## 3. XSS
```js
// Vulnerable
el.innerHTML = userComment;
// Fixed: text sink
el.textContent = userComment;
```
React/Vue/Angular escape by default; flag `dangerouslySetInnerHTML`, `v-html`, `bypassSecurityTrust*`. For required rich text, sanitize with a maintained sanitizer (e.g. DOMPurify on the client or a server-side equivalent) and add a CSP. Encode for the context (HTML body, attribute, JS, URL, CSS).

## 4. Broken object authorization
```python
# Vulnerable: any logged-in user can read any invoice
inv = Invoice.objects.get(id=invoice_id)
# Fixed: scope by caller/tenant, 404 if not theirs
inv = get_object_or_404(Invoice, id=invoice_id, tenant_id=request.user.tenant_id, owner=request.user)
```
Put the check in a shared policy layer; add a test per endpoint.

## 5. Mass assignment
```js
// Vulnerable
await User.update(req.params.id, req.body);
// Fixed: explicit allowlist (DTO / schema), reject unknown keys
const { displayName, bio } = schema.parse(req.body);
await User.update(req.user.id, { displayName, bio });
```

## 6. Path traversal and uploads
```python
base = Path("/srv/uploads").resolve()
target = (base / user_filename).resolve()
if base not in target.parents:  # also reject when target == base
    abort(400)
```
Better: never use the user filename; generate a random name, keep the original name as metadata. Check content type by magic bytes, enforce size limits, store outside the web root, serve with `Content-Disposition` and `X-Content-Type-Options: nosniff`. Guard archive extraction against `../` entries (zip-slip). Treat SVG and HTML uploads as active content.

## 7. SSRF
Validate scheme (`https` only if possible), resolve the hostname yourself, reject loopback, private (RFC 1918), link-local (including 169.254.169.254 metadata), and unique-local IPv6 ranges, then connect to the validated IP (avoid check-then-use DNS rebinding), disable or re-validate redirects, set timeouts and response size caps. Prefer allowlisting destination hosts. Use cloud features that harden metadata access (e.g. IMDSv2 on AWS) as defense in depth.

## 8. CSRF
Enable the framework's CSRF middleware for cookie-based sessions; send tokens in a header or hidden field; `SameSite=Lax/Strict`; verify `Origin`; state changes via POST/PUT/PATCH/DELETE only. Token-in-header APIs using bearer tokens (not cookies) are not CSRF-prone but must protect token storage.

## 9. Unsafe deserialization
Never `pickle.loads`, `yaml.load` (use `safe_load`), Java native serialization, PHP `unserialize`, .NET `BinaryFormatter`, or similar on untrusted data. Use JSON with schema validation; if polymorphic types are required, allowlist classes.

## 10. Secrets
```python
# Vulnerable
API_KEY = "sk_live_..."
# Fixed
API_KEY = os.environ["PAYMENT_API_KEY"]  # injected by platform/secrets manager
```
Add secret scanning (pre-commit and CI). If a real secret was committed: rotate first, then remove from history only as a secondary step (it is already compromised).

## 11. Open redirect
Redirect only to relative paths or to an allowlist of hosts; parse with a URL library; reject `//evil.com`, backslash tricks, and encoded variants.

## 12. Race conditions
Use DB transactions with row locks or atomic conditional updates:
```sql
UPDATE coupons SET used = true WHERE id = $1 AND used = false;  -- check affected rows == 1
```
Use unique constraints and idempotency keys instead of check-then-act in app code.

## 13. Fail-open error handling
```python
# Vulnerable
try:
    allowed = check_permission(user, res)
except Exception:
    allowed = True
# Fixed
try:
    allowed = check_permission(user, res)
except Exception:
    log.exception("authz error")
    allowed = False
```

## 14. Fix workflow
1. Reproduce or prove the code path. 2. Write a failing test. 3. Fix at the root cause (shared helper/policy if the bug class is repeated). 4. Search the codebase for the same pattern. 5. Run tests, linters, scanners. 6. Document residual risk.
