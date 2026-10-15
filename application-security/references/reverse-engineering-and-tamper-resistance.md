# Reverse engineering, signing, and tamper resistance

MASVS-RESILIENCE plus distribution integrity. Apply by threat model; these controls raise attacker cost, they do not provide security by themselves.

## Contents
1. Signing and key management
2. Variants and release hygiene
3. Shrinking and obfuscation (R8)
4. Anti-tamper and environment checks
5. Play Integrity API
6. Testing guidance and limits
7. Reporting language

## 1. Signing and key management
- Verify signature scheme(s) and certificate (`apksigner verify --print-certs`): v2+ present for modern installs; v3/v3.1 key rotation lineage if rotated; certificate not a debug certificate; consistent cert across APK and splits; validity period and key size/algorithm reasonable.
- Play App Signing: Google holds the app signing key; you keep an upload key. Protect the upload key and keystore (not in the repo, strong password in a secrets manager, restricted CI access, backup, documented reset procedure with Play Console).
- Without Play App Signing, losing the key can mean losing the ability to update; compromise allows malicious updates. Check CI logs and Gradle files for keystore passwords (redact).
- Do not change signing keys silently; key changes affect updates and users.

## 2. Variants and release hygiene
Debug and release separated; release non-debuggable; no `testOnly`; no debug endpoints, mock servers, test credentials, verbose logging, or leftover `BuildConfig.DEBUG` branches that expose features; no debug `network_security_config` overrides; source maps/mapping files not shipped inside the APK; mapping files stored for crash deobfuscation; Native libs stripped; for NDK apps check current page-size requirements (16 KB) in official docs.

## 3. Shrinking and obfuscation (R8)
Enable minification/shrinking/obfuscation for release; review keep rules for over-broad `-keep` that expose sensitive classes; strings and endpoints remain readable unless separately protected; reflection and serialization need keep rules; commercial hardening is optional. Never describe obfuscation as protection for secrets.

## 4. Anti-tamper and environment checks
Root/emulator/debugger/hook detection, installer-source checks, signature self-checks, and runtime integrity checks are bypassable by a capable attacker with local control. Use them for fraud/abuse risk reduction where justified, report results to the **server** (which decides), and avoid breaking legitimate users (false positives, accessibility tools, custom ROMs). Security-critical decisions must not depend only on a client-side `if (isRooted)` check.

## 5. Play Integrity API
For Play-distributed apps needing integrity signals: request a verdict with a server-generated nonce (bind to the action/request to prevent replay), send the token to **your server**, decode/verify the verdict server-side via Google's API, and apply policy server-side (allow, step-up, deny). Do not decode or trust verdicts only on the client. Check current docs for standard vs classic requests, quotas, verdict fields (app, device, account licensing, and optional signals), and for deprecation of older attestation APIs (SafetyNet Attestation is deprecated/replaced; do not recommend it). Integrity verdicts are probabilistic signals, not guarantees, and not useful outside Play-installed contexts. Do not claim Integrity makes tampering impossible.

## 6. Testing guidance and limits
Test anti-tamper behavior only on the user's own authorized build in a test environment (for example verifying the app refuses a re-signed build or that the server rejects a failed verdict). Do not weaken or bypass protections in third-party apps. Report whether protections exist and whether the server enforces outcomes, not whether you "defeated" them for sport.

## 7. Reporting language
Missing RESILIENCE controls are Informational/Low hardening unless the threat model (finance, DRM, competitive games, payments, regulated data) makes them important. State the threat model assumed. Never say an app "cannot be reverse engineered".
