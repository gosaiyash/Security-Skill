# Controlled dynamic testing

Only with explicit authorization, for the user's own app (or an app they are authorized to test), on a disposable emulator or dedicated test device, with test accounts and synthetic data.

## Contents
1. Preconditions
2. Environment setup
3. Test plan
4. Network observation
5. Storage and component checks
6. Instrumentation (Frida and similar)
7. Evidence and logging
8. Stop conditions and cleanup

## 1. Preconditions (write them down first)
Package, version, SHA-256; build type (prefer a debuggable or test build only if the release behavior is not what is being tested; state which); permitted tools; test accounts (two, for authz tests); backend environment (staging, not production, unless explicitly authorized and read-only); rate limits and test window; prohibited actions. If any is missing, do not start.

## 2. Environment setup
Use a fresh emulator image (AVD) or a dedicated device with no personal accounts or data; snapshot before install so you can reset. Verify that the APK hash matches the authorized artifact before install. Install with `adb install` (confirm syntax with `adb help`) only on that device. Do not connect personal devices. Keep the emulator network restricted to the test backend where possible.

## 3. Test plan (minimal interactions, synthetic data)
- Install/first run, permission prompts and denial handling.
- Login, logout, session expiry, account switching, process death and restart.
- Component exposure: send crafted intents/deep links from a harness app or `adb shell am start` (confirm syntax) to the app's own exported components; observe behavior.
- Storage after use: inspect app data on a debuggable test build (`adb shell run-as <package>`) or via an emulator with appropriate access; search for synthetic tokens and test PII in files, prefs, DBs, cache, logs.
- Logs: watch `adb logcat` during flows for sensitive data.
- WebView and deep-link navigation, redirects, OAuth callback handling.
- Backup/restore behavior where relevant (check configured rules; use documented tooling, since `adb backup` is deprecated/limited on modern Android).
- Network failure, airplane mode, invalid input, repeated operations (within rate limits).
- Environment handling (rooted/emulator) only if relevant to the app's threat model.

## 4. Network observation
Use an intercepting proxy only against the authorized test app and test backend. Trusting a proxy CA for a debuggable test build via a debug-only network security configuration is acceptable in the test environment; never ship it. Record destinations, methods, headers by name, and field names; use synthetic values. Look for cleartext, tokens in URLs, unexpected third-party endpoints, missing certificate validation (app should refuse a proxy CA it does not trust in release builds).

## 5. Storage and component checks
Prefer reading evidence the app produced for the test account. Never extract data of other real users. For authorization tests use your two test accounts: account A attempts to access account B's objects; stop at proof (an HTTP status or a marker string), do not enumerate.

## 6. Instrumentation (authorized test build only)
Frida and similar tools can observe or modify behavior at runtime. Use only to answer a specific question about the user's own app (for example "does the release build skip certificate validation" or "is a client-side check enforced by the server"). Confirm usage with the tool's own `--help` and docs; do not run scripts copied from the internet unread; no hooks that exfiltrate data off the device; no bypassing third-party protections. Record each script's purpose and content in the report appendix.

## 7. Evidence and logging
Keep a timestamped log: action, expected, observed, artifact version, environment. Screenshots or text excerpts with sensitive values redacted. Mark each test Pass / Fail / Not tested; a test you could not run is Not tested. Do not generalize one device/OS result to all devices.

## 8. Stop conditions and cleanup
Stop on real user data, instability, unexpected external communication, backend disruption, or scope doubt. Cleanup: revert the emulator snapshot or wipe the device, delete captured traffic/artifacts containing tokens, rotate any test credentials that appeared in logs, remove debug CAs.
