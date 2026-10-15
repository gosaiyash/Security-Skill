# Authentication and Authorization (Web, API, and Mobile)

Governed by **ASVS Chapters V2/V3/V4** and **MASVS-AUTH**.
**Fundamental Axiom**: The client (browser, mobile app, desktop app) is untrusted. Authentication proves identity; authorization decides access. Sensitive authorization decisions and state-changing checks must **always** be evaluated and enforced server-side.

---

## 1. Core Principles

- **Prefer Vetted Implementations**: Rely on framework-provided authentication or maintained identity providers (OIDC/OAuth 2.0) rather than rolling custom schemes.
- **Deny by Default**: Explicitly deny access unless an access control rule allows it.
- **Fail Closed**: Any error, exception, or ambiguity during authentication or authorization must immediately deny access.
- **Context-Bound Authorization**: Check authorization on every single request, per function and per data object. Never rely on the client having passed an initial login screen.

---

## 2. Passwords, Credentials & Local Authentication

### Server-Side Credential Storage
- Hash passwords using **Argon2id** (preferred), **scrypt**, or **bcrypt** with parameters meeting current OWASP Password Storage standards.
- Unique per-user cryptographically random salt handled automatically by the hashing library. Optional pepper stored in a separate secrets manager (never alongside DB hashes).
- Enforce uniform response times and generic error messages ("Invalid credentials") across login and password reset to prevent user enumeration.
- Enforce server-side rate limiting, IP backoff, and step-up challenge against credential stuffing.

### Mobile Local Authentication & Biometrics (Android)
- Use `BiometricPrompt` with appropriate authenticator strength (`BIOMETRIC_STRONG` for cryptographic operations).
- **The Biometric Trap**: Never use `if (biometricSucceeded) { makeApiCall(); }` as a security control. An attacker on a rooted device or with Frida can trivially hook the boolean callback.
- **Correct Pattern**: Bind local operations to an Android Keystore `KeyGenParameterSpec.Builder(..., PURPOSE_SIGN)` requiring `setUserAuthenticationRequired(true)`. Pass a `CryptoObject` to `BiometricPrompt.authenticate()`. Use the unlocked private key to sign a server-supplied challenge, and verify the signature on the server.
- App PIN / Lock screens: Store only salted, slow-derived hashes (PBKDF2/Argon2); rate-limit attempts; verify time against server clocks or `SystemClock.elapsedRealtime()`.

---

## 3. Sessions, Cookies, and Mobile Tokens

### Web Browser Sessions & Cookies
- Generate opaque session IDs from a CSPRNG with at least 128 bits of entropy.
- Rotate session IDs upon authentication, privilege elevation, and MFA completion. Invalidate server-side on logout, password change, or administrative lock.
- Cookie flags: `Secure; HttpOnly; SameSite=Lax` (or `Strict`); use `__Host-` prefix where applicable. Never transmit session IDs in query parameters.
- CSRF defense: Framework synchronizer tokens or double-submit cookies for state-changing operations; verify `Origin`/`Sec-Fetch-Site` headers.

### Mobile Client Tokens (JWT & Bearer Tokens)
- Issue short-lived access tokens (e.g., 5–15 minutes).
- Store refresh tokens in app-private encrypted storage (e.g., Android Keystore-backed DataStore/EncryptedSharedPreferences).
- Explicit logout: The mobile client must discard local tokens AND call the server revocation endpoint to invalidate the refresh token server-side.
- Handle `401 Unauthorized` cleanly by attempting token refresh once; if refresh fails, wipe local credentials and route the user to login.

---

## 4. JWT & Self-Contained Token Validation

1. **Algorithm Pinning**: Strictly whitelist expected algorithms (e.g., `RS256`, `ES256`). Explicitly reject `alg: none`.
2. **Algorithm Confusion**: Enforce separate verification logic for symmetric (`HS256`) and asymmetric (`RS256`) tokens to prevent public key-as-secret HMAC attacks.
3. **Claim Validation**: Cryptographically verify signature, `iss` (issuer), `aud` (audience), `exp` (expiration), and `nbf` (not before).
4. **Key Management**: Look up `kid` (Key ID) exclusively against a local trusted key set or validated JWKS endpoint. Never blindly fetch untrusted remote keys from token headers.
5. **No Secrets in Payload**: JWT payloads are Base64URL-encoded and readable by anyone. Do not store passwords, API keys, or raw PII in claims.

---

## 5. OAuth 2.0 and OpenID Connect (OIDC)

- **Flow**: Use **Authorization Code Flow with PKCE** (`code_challenge` / `code_verifier`) for both Web SPAs and Mobile clients. Never use Implicit Flow or Resource Owner Password Credentials (ROPC).
- **Native/Mobile Client Auth**:
  - Perform authorization flows inside the **system browser** (Chrome Custom Tabs on Android / `ASWebAuthenticationSession` on iOS).
  - **Never use embedded WebViews** for OAuth: WebViews allow the hosting application to sniff keystrokes, steal credentials, and intercept authorization codes.
  - Redirect URIs: Use verified Android App Links (`autoVerify="true"`) or custom schemes strictly registered to the app. Exact-match registered redirect URIs on the authorization server.
- **Public Client Security**: Mobile and SPA clients cannot keep secrets. Never embed `client_secret` in mobile APKs or frontend JavaScript.
- **Identity Binding**: Use `sub` (subject identifier) + `iss` (issuer) as the immutable user identifier, never unverified emails.

---

## 6. Server-Side Authorization Models & Patterns

### Multi-Level Access Control
- **Object-Level (BOLA/IDOR)**: Verify that the authenticated user/tenant owns or is explicitly authorized to access the specific requested entity (e.g., `WHERE id = ? AND tenant_id = ?`).
- **Property-Level (BOPLA)**: Whitelist fields on read and write (DTOs / serializers). Reject unexpected client input to prevent mass assignment (e.g., client injecting `role: "admin"` or `is_premium: true`).
- **Function-Level (BFLA)**: Restrict privileged endpoints (admin, billing, support) via strict server-side middleware and role checks.

### Multi-Tenancy Architecture
- Derive tenant identity exclusively from the authenticated session/token, never from request query params or body parameters.
- Enforce tenant isolation in the data layer: Row-Level Security (RLS) in PostgreSQL, mandatory tenant filters in ORM repositories, or separate database schemas.
- Ensure tenant ID is embedded in cache keys, object storage prefixes (S3 keys), asynchronous queue messages, and search engine indices.

---

## 7. Client-Controlled Trust Traps (Mobile & Web)

Never trust the client for:
- User roles, permissions, or access tiers (`isAdmin`, `role`, `tier`).
- Feature flags or entitlement status (`isPremium`, `hasPaid`, `trialRemaining`).
- Financial parameters (prices, discounts, tax rates, checkout totals).
- Security posture assertions (device root/jailbreak status, integrity checks, biometric pass booleans).
- Device clock for time-sensitive trials or token expirations.

---

## 8. Verification & Test Checklist

- [ ] Unauthenticated requests to protected endpoints return `401 Unauthorized`.
- [ ] Authenticated low-privilege users accessing admin routes receive `403 Forbidden`.
- [ ] User A accessing User B's resource ID returns `404 Not Found` or `403 Forbidden` across read, update, delete, and export actions.
- [ ] Tampered JWTs (modified signature, changed `sub`, `alg: none`, forged `kid`) are rejected.
- [ ] Replaying a revoked or logged-out token fails.
- [ ] Passing unexpected fields (`role`, `is_admin`, `balance`) in POST/PUT payloads does not mutate unauthorized attributes.
- [ ] Mobile logout clears all local tokens and revokes them on the server.
- [ ] Mobile app deep links cannot bypass login screens to access authenticated UI.
