# Manifest, components, and platform exposure

MASVS-PLATFORM mostly. Treat the Android client as an attack surface for other apps on the device and for crafted links/files.

## Contents
1. Manifest flags
2. Permissions
3. Exported components
4. Intents, deep links, App Links
5. PendingIntent and intent redirection
6. Content providers and files
7. WebView
8. Services, receivers, tasks, UI
9. What to report

## 1. Manifest flags (each: where, risk, fix)
| Flag / element | Concern | Guidance |
|---|---|---|
| `android:debuggable="true"` | debugger attach, `run-as` data access | never in release; check merged manifest and build types |
| `android:testOnly` | test artifact in distribution | remove |
| `android:allowBackup` / `dataExtractionRules` / `fullBackupContent` | sensitive data in backups/transfer | exclude sensitive files or disable per threat model; API 31+ uses `dataExtractionRules` |
| `android:usesCleartextTraffic`, `networkSecurityConfig` | HTTP allowed | see network reference |
| `android:requestLegacyExternalStorage` and broad storage permissions | wide file access | prefer scoped storage, MediaStore, photo picker |
| `android:exported` | missing explicit value on components with intent filters fails to install on target 31+, but verify on older targets | set explicitly |
| `android:taskAffinity`, `launchMode` | task hijack/overlay phishing on older platforms | review for sensitive activities |
| `targetSdkVersion`/`minSdkVersion` | missing platform protections | see standards file |
| `android:enableOnBackInvokedCallback` etc. | functional, not security | ignore unless relevant |

Use the **merged** manifest (after library manifests and build variants), not just `src/main`.

## 2. Permissions
For each requested permission: which feature needs it, is it dangerous/special, is it requested in context at runtime, is denial handled, can it be narrower (approximate location, photo picker instead of storage, foreground-only), and is it contributed by a library the app does not need. Flag over-broad ones: `READ_SMS`, `READ_CONTACTS`, `MANAGE_EXTERNAL_STORAGE`, `QUERY_ALL_PACKAGES`, accessibility service use, `SYSTEM_ALERT_WINDOW`, install-packages, background location. Play restricts several of these; verify policy text.

## 3. Exported components
A component is exported if `exported=true` or it has an intent filter on older targets. Ask: (1) what does it do, (2) can another app or a web page trigger it, (3) does it touch sensitive data/actions/auth state, (4) what caller control exists (`android:permission` with signature protection level, caller UID/package checks, explicit allowlist), (5) is input validated. Exported launcher activities and intentionally public receivers are normal; document the reasoning.
Typical issues: exported activity that skips authentication when launched directly; exported service performing privileged work; receiver acting on unvalidated broadcast data; "debug" activities; activities that take a `Intent` extra and launch it (redirection).

## 4. Intents, deep links, App Links
- Treat every extra, URI, and `getIntent()` data as attacker-controlled; validate type, length, and allowlist values; do not build file paths, SQL, WebView URLs, or intents from them unchecked.
- Custom schemes can be claimed by other apps; use verified App Links (`autoVerify`, `assetlinks.json` on the domain) for sensitive flows and never treat a deep link as proof of identity.
- OAuth callbacks: validate `state`, use PKCE, use the system browser/Custom Tabs; ensure only your app handles the redirect.
- Implicit intents with sensitive extras can leak to any receiver; use explicit intents or restrict with `setPackage`.

## 5. PendingIntent and redirection
`FLAG_IMMUTABLE` unless mutability is truly needed (required choice on API 31+); explicit base intent; no empty/implicit base intent in notifications and widgets. Intent redirection: never `startActivity()` an Intent taken from an untrusted extra; if unavoidable, validate the target component and strip grant flags.

## 6. Content providers and files
Set `exported=false` unless needed; use `readPermission`/`writePermission`, `<path-permission>`, and `grantUriPermissions` narrowly; sanitize `selection` parameters (SQL injection) and path segments (traversal in `openFile`); `FileProvider` paths scoped to specific directories (not `root-path` or broad `external-path`); validate files received through share intents; never expose internal files by URI grant with persistent permission unless required.

## 7. WebView (MASVS-PLATFORM-2)
Check each: JavaScript enabled? `addJavascriptInterface` exposed, to which origins, and what the bridge can do (assume any loaded page can call it); `setAllowFileAccess`, `setAllowFileAccessFromFileURLs`, `setAllowUniversalAccessFromFileURLs`, `setAllowContentAccess`; mixed content mode; `shouldOverrideUrlLoading` allowlist; loading `http://` or user-supplied URLs; `loadDataWithBaseURL` base origin; `setWebContentsDebuggingEnabled` in release; `WebViewAssetLoader` for local content; message channels with origin checks (`WebViewCompat.addWebMessageListener` with allowed origin rules); Safe Browsing; cookie handling and storage; SSL error handler that proceeds (`onReceivedSslError` calling `proceed()`) is a finding. Hybrid frameworks (Cordova, Capacitor, React Native WebView, Flutter webview) have their own bridge configs: review them.

## 8. Services, receivers, tasks, UI
Bound services: authenticate callers; dynamic receivers registered with `RECEIVER_NOT_EXPORTED` where applicable; sticky/ordered broadcasts with sensitive data; overlay and tapjacking protection on sensitive buttons (`filterTouchesWhenObscured`); `FLAG_SECURE`; notification content visibility on lock screen; clipboard use for secrets.

## 9. What to report
Component, exposure condition, what an attacker app/page can do, preconditions, evidence (manifest excerpt, code path, or authorized runtime observation), severity with context, fix, and a regression test (instrumented test sending a crafted intent from a test harness app or `ActivityScenario`).
