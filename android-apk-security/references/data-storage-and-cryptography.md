# Data storage and cryptography

MASVS-STORAGE and MASVS-CRYPTO. Base decisions on a threat model: who can read the data (other apps, a lost/unlocked device, a rooted device, backups, malware with accessibility, a forensic examiner) and how sensitive it is. Do not require encryption of every value.

## Contents
1. Data inventory
2. Where data lives
3. Leakage channels
4. Secrets in the package
5. Keystore and cryptography
6. Safe patterns
7. Tests

## 1. Data inventory
List sensitive data classes: credentials, access/refresh tokens, session cookies, PII, financial/health data, keys, business records, cached API responses, images/documents. For each: why stored, where, protection, lifetime, deletion trigger.

## 2. Where data lives
App-private (`/data/data/<pkg>`: databases, shared_prefs, files, cache, no_backup); SQLite/Room; SharedPreferences/DataStore; files and caches; WebView storage and cookies; external storage and shared collections (MediaStore, SAF); temp files and share URIs; clipboard; backups and device transfer; Keystore-held keys (key material not extractable, but usage can be abused by code running in the app).
Private storage protects against other non-root apps, not against a rooted device, a debuggable build, backup extraction, or the app's own bugs.

## 3. Leakage channels
Logs (`Log.*`, Timber, Logcat in release), crash reporters and analytics payloads, URL query strings, screenshots and recents thumbnails, notifications, keyboard cache/autofill, clipboard, third-party SDKs, WebView cache, backup archives, world-readable files, external storage, shared preferences mode, content-provider exposure.

## 4. Secrets in the package
Search source, `strings.xml`, `BuildConfig`, assets, native libs, Firebase/Google config files, and decompiled code for credential-like values (redact in output). Classify:
- **Public identifiers** (Google Maps key with restrictions, Firebase API key identifiers, OAuth client IDs, analytics keys): not secret, but should be restricted (package name + SHA-1 restriction, quotas) where the provider allows; report missing restriction as Low/Informational with context.
- **True secrets** (server API secrets, private keys, signing keystore, DB credentials, admin tokens, symmetric keys protecting server data): any presence in the APK is a finding. Obfuscation, string encryption, and NDK hiding do not make them safe; fix by moving the secret server-side or using per-user, short-lived, scoped tokens.
Check version control history and build artifacts too; rotate on exposure.

## 5. Keystore and cryptography
- Prefer Android Keystore for keys that guard local data; consider hardware-backed and StrongBox availability checks via the documented APIs; set purposes, block modes, paddings, digests explicitly; `setUserAuthenticationRequired` and validity parameters when keys should be gated by user presence; handle `KeyPermanentlyInvalidatedException` and key rotation/deletion.
- Use vetted libraries (for example Google Tink) over hand-assembled primitives. `androidx.security:security-crypto` (EncryptedSharedPreferences/EncryptedFile): check its current maintenance status and recommended alternatives in official docs before recommending it.
- AEAD (AES-GCM, ChaCha20-Poly1305), fresh random nonce per encryption, authenticated associated data where useful; `SecureRandom`, never `java.util.Random` or `Math.random` for security values; no ECB, no static/zero IVs, no MD5/SHA-1 for security, no hardcoded or derived-from-package-name keys; password-based keys via a modern KDF with proper parameters; constant-time comparisons for MACs/tokens.
- Do not recommend algorithms or parameters from memory for a specific API level; check the current Android crypto docs and provider support for the target minSdk.
- Local authentication: biometric success is a local signal. For sensitive operations tie it to a Keystore key (`BiometricPrompt.CryptoObject` with a user-auth-bound key) and have the server verify a signed challenge or fresh token; a boolean `if (authenticated)` in client code is bypassable.
- Long-lived credentials stored locally increase theft impact; prefer short-lived access tokens, rotating refresh tokens, device binding where justified, and server-side revocation.

## 6. Safe patterns
Store tokens in app-private storage encrypted with a Keystore-protected key (via Tink/AEAD); keep sensitive caches in `noBackupFilesDir` or exclude via backup rules; clear sensitive data on logout, account removal, and (where appropriate) on token expiry; avoid writing secrets to files at all when memory-only suffices; zero sensitive byte arrays after use where practical (best-effort on the JVM).

## 7. Tests
- Instrumented test asserting that after login the prefs/files directory contains no plaintext token (search for a known synthetic token).
- Backup test: exclusion rules cover sensitive paths.
- Logout test: data and keys removed.
- Lint/Semgrep rule for `Log.*` with sensitive variables; secret scan in CI (see testing-tools.md).
