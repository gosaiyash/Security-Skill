# Authentication and session security

MASVS-AUTH. The client is untrusted; the server is the authority.

## Contents
1. Principles
2. Login, registration, recovery
3. OAuth/OIDC
4. Tokens and sessions
5. Local authentication and biometrics
6. Client-controlled trust
7. Abuse resistance
8. Backend items to mark unverified
9. Tests

## 1. Principles
Any permission check, role check, feature gate, price, or "verified" flag that exists only in the APK can be bypassed. Server-side enforcement is required for anything protecting server-side resources. Local checks are UX.

## 2. Login, registration, recovery
Uniform error messages and timing (no account enumeration), rate limiting and lockout/backoff (server), MFA support for sensitive accounts, secure recovery (no weak security questions, single-use short-lived tokens), re-authentication for sensitive actions, session termination on password change. Client tasks: never log credentials, mark password fields correctly, avoid caching credentials, support password managers/autofill and passkeys (Credential Manager) where the product allows.

## 3. OAuth/OIDC
Authorization Code with PKCE; system browser or Custom Tabs (not embedded WebView); exact-match redirect URIs, preferably verified App Links; validate `state` and `nonce`; no client secret in the app (public client); validate ID tokens server-side or with the library; minimal scopes; handle revoked consent. Third-party sign-in SDKs: review permissions and data flows.

## 4. Tokens and sessions
Short-lived access tokens; refresh tokens rotated and revocable; storage per data-storage reference; logout calls the server to revoke and clears local state; handle 401 by re-auth, not by silently retrying forever; no long-lived bearer tokens in prefs; consider token binding/DPoP-like mechanisms only when threat model warrants, and verify current standards before recommending. Session expiry behavior across process death, account switching, and backup/restore.

## 5. Local authentication and biometrics
`BiometricPrompt` with the appropriate authenticator strength; for protecting secrets or authorizing sensitive operations use a `CryptoObject` bound to a Keystore key with user-auth requirements, and have the server accept the operation only with proof (signed challenge or fresh server-issued token). A client `if (biometricSucceeded)` branch followed by an unauthenticated API call is not a security control. App PIN/lock screens: rate limit, store only hashed/derived verifiers, handle app backgrounding, protect against brute force and clock manipulation.

## 6. Client-controlled trust
Look for: user ID, role, tenant, `isPremium`, price, quantity, discount, `isVerified`, jailbreak/root result, or purchase receipt sent by the client and trusted by the server; license/entitlement decided locally; purchase verification skipping server-side validation with the store; time-based trials using device clock. Each is a client-to-server finding to be confirmed on the backend.

## 7. Abuse resistance
Signup/OTP/SMS/reset flows are abusable (cost, enumeration, spam); client throttling is cosmetic; require server-side limits, bot signals, and (for Play-distributed apps where useful) Play Integrity verdicts evaluated on the server. Do not promise that attestation stops determined attackers.

## 8. Backend items to mark "not verified from the APK"
Authorization rules, rate limits, token validation, session invalidation, input validation, logging, tenant isolation, data retention, infrastructure hardening.

## 9. Tests
Instrumented/unit: logout clears tokens and calls revoke; expired token handled; deep link cannot bypass login; recents/background hides sensitive screens; refresh failure forces re-auth. Backend (authorized): cross-user access denied with two test accounts, tampered role/price ignored, replayed token after logout rejected.
