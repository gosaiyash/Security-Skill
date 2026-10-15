# API and Network Security (Backend, Cloud, and Mobile Client)

Governed by **ASVS Chapter V9 / V10**, **OWASP API Security Top 10 (2023)**, and **MASVS-NETWORK**.
**Core Axiom**: HTTPS encrypts the pipe in transit; it does not prove server authorization, prevent BOLA/IDOR, secure stored tokens, or validate request integrity.

---

## 1. OWASP API Security Top 10 (2023) Reference

| ID | Vulnerability | Core Verification & Mitigation |
|---|---|---|
| **API1** | **Broken Object Level Authorization (BOLA/IDOR)** | Enforce ownership and tenant checks on every object lookup. Never rely on client-supplied object IDs. |
| **API2** | **Broken Authentication** | Strict token validation, brute-force protection, lockout/backoff on auth routes, no credentials in query strings. |
| **API3** | **Broken Object Property Level Authorization (BOPLA)** | Response filtering (no excessive data exposure) and strict write allowlists/DTOs (mass assignment prevention). |
| **API4** | **Unrestricted Resource Consumption** | Strict rate limits, request payload size caps, pagination max-limits, execution timeouts, DB query complexity limits. |
| **API5** | **Broken Function Level Authorization (BFLA)** | Server-side role/permission validation on privileged functions (admin, billing, export); verify all HTTP verbs (`PUT`, `DELETE`). |
| **API6** | **Unrestricted Access to Sensitive Business Flows** | Bot detection, CAPTCHA/proof-of-work, velocity limits on signup, purchases, OTP requests, and coupon claims. |
| **API7** | **Server-Side Request Forgery (SSRF)** | Validate user-supplied URLs against strict allowlists; resolve DNS and block private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.169.254`, `::1`); disable automatic HTTP redirects. |
| **API8** | **Security Misconfiguration** | Strict CORS (no wildcard with credentials), disable unneeded HTTP methods, strip debug stack traces, enforce HSTS. |
| **API9** | **Improper Inventory Management** | Deprecate old API versions, eliminate shadow/debug/staging routes, synchronize OpenAPI/Swagger specs with code. |
| **API10** | **Unsafe Consumption of APIs** | Validate and sanitize all responses from third-party APIs/microservices; enforce timeouts; verify TLS certificates. |

---

## 2. API Architectures: REST, GraphQL, gRPC, and WebSockets

### REST APIs
- **Content Negotiation**: Enforce strict `Content-Type` matching (e.g., `application/json`). Reject unexpected media types.
- **Error Handling**: Standardize RFC 7807 problem details or minimal error bodies without stack traces or SQL snippets.
- **Idempotency**: Use `Idempotency-Key` headers for retry-prone financial writes (`POST /charges`).
- **CORS**: Explicit origin allowlist; avoid echoing the `Origin` header dynamically when credentials (`Access-Control-Allow-Credentials: true`) are enabled.

### GraphQL APIs
- **Production Hardening**: Disable GraphQL Playground and schema introspection in production.
- **DoS Protection**: Enforce maximum query depth, cost/complexity calculation, and alias limits. Set resolver timeouts.
- **Granular Authz**: Enforce authorization within individual field resolvers, not just at the top-level query. Guard against N+1 data leaks through nested relations.

### gRPC & WebSockets
- **gRPC**: Enforce TLS/mTLS, auth interceptors per RPC method, message size limits, and deadlines. Disable server reflection in production.
- **WebSockets**: Validate the `Origin` header during the initial HTTP handshake (prevents Cross-Site WebSocket Hijacking). Authenticate per-connection and re-verify authorization per message frame.

---

## 3. Webhooks & Callback Security

1. **Signature Verification**: Verify HMAC signatures using constant-time comparison (`crypto.timingSafeEqual` / `MessageDigest.isEqual`).
2. **Replay Defense**: Include and enforce timestamps ($\le 5$ minutes tolerance) and store processed webhook IDs (idempotency table).
3. **Outbound Webhooks**: Enforce SSRF defenses before dispatching webhooks to customer-supplied URLs.

---

## 4. Mobile Client Network Security (Android & Transport)

### Transport Encryption & Cleartext Prevention
- Search for and eliminate `http://` URLs in code, `usesCleartextTraffic="true"`, and raw socket connections.
- Target SDK 28+ enforces cleartext blocking by default; verify merged manifests to ensure no library has enabled it.

### Android Network Security Configuration (`res/xml/network_security_config.xml`)
- Enforce `<base-config cleartextTrafficPermitted="false">`.
- Trust anchors: Do **not** trust user certificates in release builds (`<certificates src="user" />`). User CAs allow trivial MITM on devices with user-installed root certificates.
- `<debug-overrides>`: Ensure debug overrides (used for Charles/Burp during local testing) are strictly scoped to debug variants and completely removed from release artifacts.

### Audit Insecure TrustManagers & HostnameVerifiers
Flag and eliminate dangerous patterns in code:
- Empty `checkServerTrusted()` implementations in custom `X509TrustManager`.
- `HostnameVerifier` returning `true` unconditionally.
- `WebViewClient.onReceivedSslError()` calling `handler.proceed()`.
- Disabling certificate verification in Flutter (`badCertificateCallback: (_, _, _) => true`), React Native, or cURL (`CURLOPT_SSL_VERIFYPEER = 0`).

### Certificate Pinning (MASVS-NETWORK-2)
- Optional defense-in-depth for endpoints owned by the developer.
- If implemented: pin to intermediate/public key hashes (SPKI), configure backup pins, establish expiration dates, and deploy a dynamic remote recovery/kill-switch mechanism. Pinning without a rotation plan risks bricking mobile apps upon certificate rotation.

---

## 5. LLM and AI Agent Tool APIs

- **Untrusted Output**: Treat all model outputs as untrusted input. Validate tool arguments against strict JSON schemas before invoking actions.
- **Least-Privilege Execution**: Model tools must execute with the caller's authenticated user context, never elevated service-account privileges.
- **Human Confirmation**: Require explicit human approval for destructive operations, financial transactions, or public communication.
- **Indirect Prompt Injection**: Assume data retrieved from emails, web scraping, or third-party databases may contain adversarial instructions aimed at tool invocation.

---

## 6. Verification & Test Checklist

- [ ] Cleartext HTTP requests are rejected or redirected to HTTPS with HSTS enabled.
- [ ] BOLA: Requesting `/api/v1/users/{id}/profile` with another user's ID yields `403` or `404`.
- [ ] BFLA: Low-privilege user attempting `DELETE /api/v1/users/{id}` receives `403 Forbidden`.
- [ ] SSRF: Providing `http://169.254.169.254/latest/meta-data/` to file/URL import endpoints is blocked post-DNS resolution.
- [ ] Webhook requests without valid HMAC signatures or with replayed timestamps are rejected.
- [ ] Android release builds have `android:usesCleartextTraffic="false"` and do not trust user-installed CAs.
- [ ] Custom `TrustManager` and `HostnameVerifier` stubs that bypass TLS validation are eliminated from release code.
