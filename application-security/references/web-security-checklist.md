# Security checklist

Status per item: Pass / Fail / Partial / N/A (reason) / Unknown. Evidence = file:line, config key, test name, or command output summary. Do not mark Pass without evidence. IDs below are local (`C-xx`) and map to OWASP Top 10:2025 (A01..A10) and ASVS 5.0.0 chapters; confirm exact ASVS requirement IDs against the document before citing them.

## Contents
1. Access control (A01; ASVS V8)
2. Authentication and sessions (A07; V6, V7)
3. Input, injection, output (A05; V1, V2, V3)
4. Files, SSRF, URLs (A01, A05; V5)
5. Cryptography and data protection (A04; V11, V12, V14)
6. Configuration and headers (A02; V13, V3)
7. Supply chain and integrity (A03, A08; V15)
8. Logging, errors, resilience (A09, A10; V16)
9. Business logic and abuse (A06; V2)
10. Frontend and browser (V3)
11. Data stores
12. Quick grep seeds

## 1. Access control
- C-01 Every route/handler has an explicit authorization decision; default is deny. List unprotected routes and justify each.
- C-02 Object-level checks: the resource is fetched with the caller's identity/tenant, not by bare ID.
- C-03 Function-level checks: admin/privileged actions check role/permission server-side, not by hiding UI.
- C-04 Property-level checks: users cannot read or write fields they should not (roles, `is_admin`, price, owner, tenant).
- C-05 Tenant isolation enforced in data layer; cross-tenant negative tests exist.
- C-06 No authorization decisions based on client-supplied data (hidden fields, JWT claims not verified, headers).
- C-07 CORS allowlist is explicit; credentials not allowed with wildcard/reflected origins.
- C-08 Service-to-service calls use scoped credentials; no shared super-admin keys.
- C-09 Forced browsing / predictable resource paths and directory listing are not exposing data.

## 2. Authentication and sessions
- C-10 Passwords hashed with Argon2id/scrypt/bcrypt (current OWASP parameters); no reversible storage.
- C-11 Brute-force defenses: rate limit per account and per IP, progressive delay, alerting.
- C-12 Uniform responses for login/reset/signup (no user enumeration).
- C-13 Reset/verification tokens: random >=128 bits, hashed at rest, single-use, short expiry, bound to account.
- C-14 MFA available and enforced for admins and sensitive operations; recovery flows do not bypass it.
- C-15 Session IDs random, rotated on login/privilege change, invalidated on logout/password change; idle and absolute timeouts.
- C-16 Cookies: `HttpOnly`, `Secure`, `SameSite`, appropriate `Domain`/`Path`, `__Host-` prefix where suitable.
- C-17 JWT/OAuth rules in authentication-and-authorization.md satisfied (alg pinned, aud/iss/exp, PKCE, redirect URI exact match).
- C-18 Default/test/hard-coded credentials absent from code and images.

## 3. Input, injection, output
- C-20 SQL/NoSQL/ORM raw queries parameterized; dynamic identifiers (ORDER BY, table) allowlisted.
- C-21 OS command execution avoided; if needed, no shell and argument arrays with allowlisted values.
- C-22 Template rendering never builds templates from user input (SSTI); auto-escaping on.
- C-23 XSS sinks reviewed; HTML sanitizer used where rich text is accepted; CSP present.
- C-24 XML parsers disable external entities/DTDs; YAML/pickle/Java/.NET/PHP deserialization of untrusted data absent or restricted.
- C-25 LDAP/XPath/GraphQL/header/log/CSV/email-header injection considered where relevant.
- C-26 Server-side schema validation on every input (type, size, range, format); unknown fields rejected on writes.
- C-27 Open redirect: redirect targets validated against an allowlist.
- C-28 Regex on untrusted input is not catastrophically backtracking (ReDoS).

## 4. Files, SSRF, URLs
- C-30 Upload: allowlisted types by content sniffing, size limits, random names, non-executable storage, malware scanning where applicable, no path from user input.
- C-31 Path handling: canonicalize and verify the resolved path stays inside the base directory; archive extraction guards against zip-slip.
- C-32 Server-side fetches of user-influenced URLs use SSRF controls (allowlist, post-DNS IP checks, redirect handling, metadata endpoint blocked, short timeouts, size caps).
- C-33 Image/document processors updated and sandboxed where possible.

## 5. Cryptography and data protection
- C-40 TLS 1.2+ (prefer 1.3) externally; internal traffic protected where the threat model requires; HSTS.
- C-41 No MD5/SHA-1/DES/RC4/ECB for security; AEAD for encryption; random via CSPRNG; unique nonces/IVs.
- C-42 Keys stored in KMS/secrets manager, rotated, separated by environment; none in source or client bundles.
- C-43 Sensitive data classified; minimized; encrypted at rest where required; masked in UI/logs; retention and deletion defined.
- C-44 Backups and exports inherit protections; debug/admin endpoints do not dump sensitive data.
- C-45 Security-relevant comparisons use constant-time functions.

## 6. Configuration and headers
- C-50 Debug mode, stack traces, directory listing, sample apps, default accounts disabled in production.
- C-51 Security headers set (see infrastructure-and-deployment.md) and verified on real responses.
- C-52 Separate config per environment; production secrets not shared with dev/staging.
- C-53 Admin interfaces not internet-exposed without strong auth and network restriction.
- C-54 Verbose server banners and framework fingerprints reduced where practical.
- C-55 HTTP methods restricted per route; unneeded methods (TRACE) disabled.

## 7. Supply chain and integrity
- C-60 Lockfiles committed; installs reproducible (`npm ci`, `pip --require-hashes` where practical, `go.sum`).
- C-61 Dependencies scanned for known vulnerabilities; abandoned or typosquat-prone packages reviewed.
- C-62 CI actions/plugins pinned to commit SHAs or verified digests; least-privilege CI tokens; no secrets echoed.
- C-63 Container base images pinned by digest, minimal, rebuilt regularly, run as non-root.
- C-64 Third-party scripts use Subresource Integrity or are self-hosted; CSP restricts sources.
- C-65 Build artifacts are produced in CI, not on laptops; provenance/signing considered (SLSA, Sigstore) for release-critical software.
- C-66 Auto-update, plugin, and deserialization paths verify integrity/signatures.

## 8. Logging, errors, resilience
- C-70 Auth events, access-control failures, input validation failures at boundaries, admin actions, and security config changes are logged with user/tenant/request IDs.
- C-71 Logs exclude secrets, tokens, full card/ID numbers; log injection prevented; logs access-controlled and retained.
- C-72 Alerts exist for credential stuffing, privilege changes, mass access, error spikes.
- C-73 Error handling fails closed: exceptions never grant access, skip checks, or leak internals; resource cleanup on failure; consistent error responses (A10).
- C-74 Timeouts, retries with backoff, circuit breakers, and queue limits protect availability.
- C-75 Rate limits and quotas on expensive/sensitive operations (signup, reset, search, export, LLM calls).

## 9. Business logic and abuse
- C-80 State machines enforced server-side (cannot skip payment/verification steps).
- C-81 Prices, discounts, quantities, balances recomputed server-side; negative/overflow values handled.
- C-82 Idempotency and locking for money/inventory/quotas; race-condition tests.
- C-83 One-time actions (coupons, invites, votes) are atomically enforced.
- C-84 Sensitive flows have abuse limits and monitoring (A06; API6).

## 10. Frontend and browser
- C-90 No secrets or privileged logic in client code or source maps in production.
- C-91 `postMessage` handlers validate origin; `target=_blank` links use `rel=noopener`.
- C-92 localStorage/sessionStorage do not hold long-lived tokens when HttpOnly cookies are feasible.
- C-93 Clickjacking protection via `frame-ancestors`/`X-Frame-Options`.
- C-94 Third-party widgets, analytics, and tag managers reviewed for data exposure.

## 11. Data stores
- C-100 DB accounts least-privilege per service; no app use of DBA/root; network-restricted.
- C-101 Redis/Mongo/Elasticsearch/queues not exposed publicly and require auth/TLS.
- C-102 Object storage buckets private by default; signed URLs short-lived and scoped.
- C-103 Migrations and seed data contain no real secrets or real PII.

## 12. Quick grep seeds (read-only, adapt to stack)
Secrets: `password|passwd|secret|api[_-]?key|token|BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY|AKIA[0-9A-Z]{16}`
Injection/exec: `eval\(|exec\(|child_process|subprocess|os\.system|Runtime\.getRuntime|shell=True|\+ *["']SELECT|f["']SELECT|innerHTML|dangerouslySetInnerHTML|\|safe|v-html|Html\.Raw`
Deserialization: `pickle\.loads|yaml\.load\(|ObjectInputStream|unserialize|BinaryFormatter|Marshal\.load`
Crypto: `md5|sha1|DES|ECB|Math\.random|random\.random|verify=False|rejectUnauthorized: *false|InsecureSkipVerify`
CORS/CSRF off: `Access-Control-Allow-Origin|csrf_exempt|csrf *: *false|cors\(\)`
Treat hits as leads. Confirm reachability and data flow before reporting.
