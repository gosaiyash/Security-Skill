# Authentication and authorization

## Contents
1. Principles
2. Passwords and credentials
3. Sessions and cookies
4. JWT and self-contained tokens
5. OAuth 2.0 / OIDC
6. MFA, recovery, and account lifecycle
7. Authorization models
8. Multi-tenancy
9. Tests to add

## 1. Principles
- Prefer a maintained identity provider or framework auth over custom code.
- Authentication proves identity; authorization decides access. Check authorization on every request, server-side, per object and per function.
- Deny by default. Centralize policy (middleware, policy classes, or a policy engine) so it is hard to forget.
- Fail closed: if the check errors, deny.

## 2. Passwords and credentials
- Hash with Argon2id (preferred), scrypt, or bcrypt using the current OWASP Password Storage Cheat Sheet parameters; check the sheet for current numbers rather than recalling them.
- Salt is per-user and handled by the library. Optional pepper lives in a secrets manager, not the DB.
- Allow long passphrases (at least 64 chars), allow paste and password managers, check against breached-password lists, no composition rules that reduce entropy, no periodic forced rotation without cause.
- Same response and similar timing for existing and non-existing accounts.
- Throttle by account and by IP; add progressive delay or CAPTCHA/step-up; alert on credential-stuffing patterns.
- API keys: random, prefix-identifiable, stored hashed, scoped, revocable, shown once.

## 3. Sessions and cookies
- Opaque random session IDs from a CSPRNG (at least 128 bits entropy), stored server-side (or signed/encrypted if stateless with revocation strategy).
- Rotate ID at login, privilege change, and MFA completion. Invalidate on logout, password change, and account disable.
- Idle timeout and absolute timeout suited to risk.
- Cookie flags: `Secure; HttpOnly; SameSite=Lax` (or `Strict`); consider `__Host-` prefix. Never put session IDs in URLs.
- CSRF: synchronizer or double-submit tokens (framework feature) for cookie-authenticated state changes; verify `Origin`/`Sec-Fetch-Site` as defense in depth; do not allow state change on GET.

## 4. JWT and self-contained tokens
- Use only when needed; sessions are simpler for browser apps.
- Pin the allowed algorithm(s) server-side; reject `none`; never let the token header choose the key or algorithm; prevent RS256/HS256 confusion by separate key handling.
- Validate signature, `iss`, `aud`, `exp`, `nbf`, and token type/purpose. Short access-token lifetime; refresh tokens rotated, bound, revocable, stored safely.
- Key management: `kid` lookup against a trusted key set only; rotate keys; asymmetric keys for multi-service verification.
- Do not put secrets or excess PII in claims (they are readable). Do not trust role claims unless issued by your own trusted issuer and validated.
- Logout/revocation strategy must be explicit (denylist, short TTL, token versioning).

## 5. OAuth 2.0 / OIDC
- Authorization Code flow with PKCE for public and confidential clients; do not use Implicit or Resource Owner Password flows.
- Exact-match registered redirect URIs; validate `state` (and `nonce` for OIDC); validate ID token per spec; use the issuer's discovery metadata over HTTPS.
- Request minimal scopes; verify scopes/audience at the resource server.
- Treat the `sub` plus `iss` pair as the stable user identity, not email alone (email can change or be unverified).
- Client secrets in a secrets manager; rotate. Native/SPA clients hold no secrets.
- Confirm exact requirements against ASVS 5.0.0 chapters on OAuth/OIDC and self-contained tokens and the relevant RFCs / OAuth security BCP before asserting compliance.

## 6. MFA, recovery, account lifecycle
- Phishing-resistant factors (WebAuthn/passkeys) preferred; TOTP acceptable; SMS only as a weaker fallback.
- Recovery must not be weaker than login (no security questions; no email-only reset for privileged accounts without extra checks).
- Re-authenticate for sensitive actions (email/password change, payout details, API key creation).
- Notify users of security-relevant changes; allow session review and revocation.
- Offboarding: disable accounts and revoke tokens and keys promptly.

## 7. Authorization models
- **RBAC** for coarse roles; **ABAC/ReBAC** for ownership, relationships, and attributes. Roles alone rarely express "owner of this document".
- Enforce at three levels (API1/API3/API5 in the API Top 10): object (BOLA/IDOR), property (read/write fields), function (admin endpoints).
- Pattern: load resource through a scoped query (`WHERE id = ? AND tenant_id = ? AND owner_id = ?`) or call a policy function before acting. Return 404 vs 403 consistently to avoid leaking existence where that matters.
- Never trust IDs, roles, prices, or flags from the client. Whitelist writable fields (DTOs/serializers with explicit fields) to stop mass assignment.
- Separation of duties for high-risk actions (approve vs create). Admin/support impersonation must be audited, time-boxed, and restricted.
- Service accounts and background jobs get their own least-privilege identities.

## 8. Multi-tenancy
- Tenant context derived from the authenticated identity, never from a request parameter alone.
- Enforce in the data layer: row-level security, mandatory tenant-scoped repository, or schema/database per tenant.
- Include tenant in cache keys, object-storage paths, queue messages, search indexes, and exports.
- Test: user A of tenant 1 requests every endpoint with IDs from tenant 2 and must get denial.

## 9. Tests to add
- Unauthenticated access to each protected route returns 401/redirect.
- Authenticated low-privilege user gets 403 on admin routes.
- Cross-user and cross-tenant object access denied (read, update, delete, list, export).
- Mass-assignment attempt on role/owner fields ignored or rejected.
- Expired/forged/wrong-audience/`alg=none` tokens rejected.
- Session fixation: pre-login ID is not valid post-login.
- Reset token single-use and expiring; password change invalidates sessions.
- Rate limit triggers on repeated failures.
