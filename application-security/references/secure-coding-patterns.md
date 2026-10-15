# Secure Coding Patterns (Web, API, and Mobile)

Concrete vulnerable $\longrightarrow$ fixed patterns. Adapt to the project's language, framework, and architecture. Each pattern identifies the corresponding CWE.

---

## 1. SQL Injection (CWE-89)

```python
# Vulnerable: string formatting / concatenation
cur.execute(f"SELECT * FROM accounts WHERE email = '{email}' AND tenant_id = '{tenant}'")

# Fixed: parameterized query (bound parameters)
cur.execute("SELECT * FROM accounts WHERE email = %s AND tenant_id = %s", (email, tenant))
```
- In ORMs, avoid raw SQL string concatenation in `whereRaw()`, `.filter()`, or `.extra()`.
- Dynamic table/column names: Map user input against a hardcoded whitelist, never interpolate.

---

## 2. Cross-Site Scripting (XSS) (CWE-79)

```javascript
// Vulnerable: raw HTML insertion
element.innerHTML = userProvidedBio;

// Fixed: safe text sink
element.textContent = userProvidedBio;
```
- Modern frameworks (React, Vue, Angular) auto-escape bindings (`{bio}`).
- Avoid `dangerouslySetInnerHTML`, `v-html`, or `[innerHTML]` unless sanitized through a vetted library (e.g., DOMPurify) and backed by a strict Content Security Policy (`script-src 'self'`).

---

## 3. Broken Object Level Authorization (BOLA/IDOR) (CWE-862 / CWE-639)

```python
# Vulnerable: fetches resource by ID without checking ownership or tenant
order = Order.objects.get(id=order_id)

# Fixed: scope database query by caller's authenticated identity and tenant
order = get_object_or_404(Order, id=order_id, tenant_id=request.user.tenant_id, user=request.user)
```

---

## 4. Mass Assignment / Over-Posting (CWE-915)

```javascript
// Vulnerable: directly updating model from untrusted request body
await User.update(req.user.id, req.body); // Attacker sends { role: "admin", balance: 99999 }

// Fixed: explicit allowlist via schema validation (Zod, Joi, DTOs)
const { displayName, bio } = userUpdateSchema.parse(req.body);
await User.update(req.user.id, { displayName, bio });
```

---

## 5. Server-Side Request Forgery (SSRF) (CWE-918)

```python
# Vulnerable: blindly fetching user-supplied URL
response = requests.get(request.json['avatar_url'])

# Fixed: validate scheme, resolve IP, block private/cloud ranges, disable redirects
def safe_fetch(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("https",):
        raise ValueError("HTTPS only")
    ip = socket.gethostbyname(parsed.hostname)
    ip_addr = ipaddress.ip_address(ip)
    if ip_addr.is_private or ip_addr.is_loopback or ip_addr.is_link_local:
        raise ValueError("Forbidden internal IP")
    return requests.get(url, allow_redirects=False, timeout=5)
```

---

## 6. Android PendingIntent Mutability (CWE-927)

```kotlin
// Vulnerable: mutable PendingIntent passed to external app or notification
val pi = PendingIntent.getActivity(context, 0, intent, 0)

// Fixed: explicitly immutable unless modification is required
val pi = PendingIntent.getActivity(
    context,
    0,
    intent,
    PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
)
```
- If `FLAG_MUTABLE` is strictly required, always use an explicit Intent (`intent.setComponent(...)` or `intent.setClass(...)`) so the target cannot be hijacked.

---

## 7. Android Exported Components & Intent Injection (CWE-926 / CWE-927)

```xml
<!-- Vulnerable: implicitly or explicitly exported without permission -->
<activity android:name=".BillingCallbackActivity" android:exported="true" />
```
```xml
<!-- Fixed: non-exported by default, or protected with signature permission -->
<activity 
    android:name=".BillingCallbackActivity" 
    android:exported="false" />
```
- When an exported component is required (e.g., handling deep links), validate `callingUid` / `callingPackage` and sanitize every incoming Intent extra before processing.

---

## 8. Android WebView Security (CWE-749 / CWE-79)

```kotlin
// Vulnerable: arbitrary JavaScript execution with exposed native bridge
webView.settings.javaScriptEnabled = true
webView.addJavascriptInterface(NativeBridge(), "Android")
webView.loadUrl(untrustedUrl)

// Fixed: restrict bridge, disable file access, validate origins
webView.settings.apply {
    javaScriptEnabled = false // enable only if strictly required
    allowFileAccess = false
    allowContentAccess = false
}
// If bridge needed, ensure methods have @JavascriptInterface and enforce origin check in shouldOverrideUrlLoading
```

---

## 9. Android Deep Links & App Links (CWE-939)

```xml
<!-- Vulnerable: custom scheme susceptible to hijacking by other apps -->
<intent-filter>
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <data android:scheme="myapp" android:host="auth" />
</intent-filter>
```
```xml
<!-- Fixed: Android App Link with digital asset link verification -->
<intent-filter android:autoVerify="true">
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="https" android:host="app.example.com" android:pathPrefix="/auth" />
</intent-filter>
```

---

## 10. Path Traversal & File Uploads (CWE-22 / CWE-434)

```python
# Vulnerable: directly concatenating untrusted user filename
target = os.path.join("/srv/uploads", filename)

# Fixed: resolve canonical path, verify containment, or generate random UUID
safe_name = f"{uuid.uuid4().hex}_{secure_filename(filename)}"
target = (Path("/srv/uploads") / safe_name).resolve()
if Path("/srv/uploads").resolve() not in target.parents:
    raise ValueError("Path traversal detected")
```

---

## 11. Concurrency & Race Conditions (CWE-362)

```sql
-- Vulnerable: check-then-act allows double spending
SELECT balance FROM wallets WHERE user_id = 1;
-- (Application logic checks balance >= 50, then executes:)
UPDATE wallets SET balance = balance - 50 WHERE user_id = 1;

-- Fixed: atomic conditional update in a single transaction
UPDATE wallets 
SET balance = balance - 50 
WHERE user_id = 1 AND balance >= 50;
-- Verify affected rows == 1; abort transaction if 0.
```

---

## 12. Fix Workflow & Quality Gate

1. **Root Cause Fix**: Remediate the underlying flaw with framework controls (parameterization, allowlisting, Keystore binding).
2. **Regression Test**: Write an automated negative test that fails before the fix and passes after.
3. **No Compromised Protections**: Never disable linting, CSRF, TLS validation, or authentication to make tests pass.
