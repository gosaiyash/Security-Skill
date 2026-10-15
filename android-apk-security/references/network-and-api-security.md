# Network and API security (client view)

MASVS-NETWORK. HTTPS working does not prove authorization, token safety, or request integrity.

## Contents
1. Transport and cleartext
2. Network Security Configuration
3. Trust and validation code
4. Pinning
5. Sensitive data in traffic
6. Request integrity, replay, redirects
7. Other protocols
8. Environments
9. Client-side API review
10. Tests

## 1. Transport and cleartext
All sensitive traffic over TLS. Search code for `http://`, `usesCleartextTraffic`, OkHttp `ConnectionSpec.CLEARTEXT`, `HttpURLConnection` with `http`, WebView loads, and hardcoded IPs. Apps targeting API 28+ default to cleartext blocked; verify the effective config rather than assuming.

## 2. Network Security Configuration (`res/xml/network_security_config.xml`, referenced by `android:networkSecurityConfig`)
Review: `<base-config cleartextTrafficPermitted>`, `<domain-config>` exceptions (justify each), `<trust-anchors>` (user-added CAs trusted? by default apps targeting 24+ do not trust user CAs; adding `<certificates src="user"/>` in release weakens this), `<debug-overrides>` (acceptable only for debug builds; confirm it does not apply to release; the element is ignored when the app is not debuggable but still flag leakage of test CAs in resources), `<pin-set>` with expiration and backup pins, `<certificateTransparency>` if used. Check the merged resources per build variant.

## 3. Trust and validation code (findings if present in release)
Custom `X509TrustManager` whose `checkServerTrusted` does nothing or catches/ignores exceptions; `HostnameVerifier` returning true; `SSLSocketFactory` using an "all trusting" context; OkHttp `.hostnameVerifier { _, _ -> true }`; `WebViewClient.onReceivedSslError` calling `handler.proceed()`; disabling certificate checks in Flutter (`badCertificateCallback` returning true), React Native/Cordova plugins, Xamarin handlers, and native/NDK code (curl `CURLOPT_SSL_VERIFYPEER=0`). Many of these exist only in debug/test code: confirm what ships in the release artifact.

## 4. Pinning
Optional defense in depth (MASVS-NETWORK-2 for endpoints you control). Recommend only with: pin to a public key/intermediate rather than a leaf where feasible, backup pins, expiry handling, remote kill-switch/recovery plan, and testing of rotation. Never present pinning as a substitute for server-side authz. Pinning bypass in your own authorized test build is acceptable for testing; do not do it to third-party apps.

## 5. Sensitive data in traffic
Tokens/secrets in query strings, URLs in logs/analytics, PII in headers, verbose request logging interceptors (`HttpLoggingInterceptor` at BODY level in release), crash reports with request bodies, third-party SDK endpoints receiving identifiers. Establish by evidence (code, or authorized runtime capture with test data).

## 6. Request integrity, replay, redirects
Tokens in `Authorization` headers; short expiry; nonce/timestamp for sensitive requests where replay matters; request signing keyed by a secret embedded in the APK is not a strong control (key extractable); redirect handling (follow only to allowlisted hosts; no downgrade from https to http); hostname allowlists for configurable base URLs; reject attacker-controlled endpoint overrides via intents/deep links.

## 7. Other protocols
WebSockets (`wss://`, auth at connect and per message), file downloads/uploads (type and size checks, path traversal on filenames, storage location), gRPC (TLS, per-call credentials), MQTT/BLE/local network (auth, encryption, pairing), push notification payloads (no secrets), third-party payment/social SDK endpoints.

## 8. Environments
Staging/test endpoints, debug flags, mock servers, and test credentials must not appear in release builds. Check `BuildConfig`, flavor resources, remote-config defaults, and hardcoded URLs. Dev menus gated only by a client flag are findings if they expose privileged behavior.

## 9. Client-side API review (when no backend access)
List endpoints, methods, auth schemes, ID parameters (user/account/order IDs), role/price/amount fields set by the client, and hidden/admin endpoints referenced in code. Record "server-side authorization not verified" for each. With authorization and two test accounts you control, test object-level and function-level access using the `web-app-security` skill's API checklist; never touch other users' real data.

## 10. Tests
Unit/instrumented tests asserting NSC cleartext blocked, release variant has no debug overrides, trust manager is the platform default, no tokens in URLs, and that a mock server with an untrusted certificate causes the app to fail the connection.
