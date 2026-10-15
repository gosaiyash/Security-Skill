# Threat Modeling for Web and Mobile Applications

Proportionate threat modeling: a single component or endpoint needs 15 minutes of structured thinking; a multi-tier platform with mobile clients and APIs needs a dedicated model. Use `templates/threat-model.md` for formal output.

---

## 1. Core Framework: The Four Questions

1. **What are we building?** (Architecture, data-flow diagrams, entry points, trust boundaries)
2. **What can go wrong?** (STRIDE, abuse cases, threat enumeration)
3. **What will we do about it?** (Controls, mitigations, server-side enforcement)
4. **Did we do a good job?** (Verification tests, regression coverage, review)

---

## 2. Threat Modeling Steps

1. **Deconstruct the Application**:
   - Diagram data flows across trust boundaries:
     - **Browser/Mobile Client $\longleftrightarrow$ Public Internet $\longleftrightarrow$ API Gateway / Reverse Proxy**
     - **API Server $\longleftrightarrow$ Microservices / Internal Bus**
     - **Server $\longleftrightarrow$ Primary Database / Caches / Object Storage**
     - **Application $\longleftrightarrow$ External APIs / Third-Party SDKs / Payment Processors**
     - **On-Device (Android)**: App Sandbox $\longleftrightarrow$ Android OS $\longleftrightarrow$ Other Apps via IPC/Intents
2. **Catalog Assets & Data**:
   - Master credentials, session tokens, refresh tokens, signing keys, OAuth secrets, database passwords.
   - PII, payment info (cards/tokens), health data, customer financial records, proprietary IP.
   - Device keys (Android Keystore), local SQLite/DataStore databases, cached media, offline payloads.
3. **Identify Entry Points**:
   - **Web/API**: REST routes, GraphQL queries/mutations, WebSockets, webhook endpoints, admin portals.
   - **Mobile (Android)**: Exported Activities, Services, BroadcastReceivers, ContentProviders, deep links/App Links, push notifications, Bluetooth/NFC receivers.
4. **Define Threat Actors**:
   - Anonymous external attacker, authenticated malicious user, cross-tenant intruder, rogue third-party SDK, local attacker on compromised/rooted device, malicious insider.
5. **Enumerate Threats via STRIDE** (see below).
6. **Rate Plausible Threats**: Likelihood $\times$ Impact (Low / Medium / High / Critical).
7. **Mitigate with Enforceable Controls**: Sensitive authorization and validation **must be enforced server-side**; client-side controls are defense in depth.
8. **Verify with Tests**: Every High/Critical threat must map to a test (unit, integration, or automated scan).

---

## 3. STRIDE Prompts across Web and Mobile

| Letter | Threat Category | Web & API Vectors | Mobile (Android) Vectors | Primary Controls |
|---|---|---|---|---|
| **S** | **Spoofing** | Faked session cookies, forged JWTs, IP spoofing, unauthenticated webhooks. | Intent spoofing, forged caller package, fake custom URI scheme handling. | Strong auth, JWT signature validation, webhook HMAC, Android caller package verification (`CallingUid`), verified App Links (`autoVerify`). |
| **T** | **Tampering** | Parameter manipulation, mass assignment, SQLi, cache poisoning. | App repackaging, runtime Frida hooking, modifying local SQLite/prefs, PendingIntent mutability hijack. | Server-side validation, ORM bind variables, Android `FLAG_IMMUTABLE`, R8/tamper detection, integrity checks. |
| **R** | **Repudiation** | User denies performing transaction or financial action. | User denies offline actions or actions performed via compromised client. | Append-only server audit logs, cryptographic transaction signatures, trace IDs. |
| **I** | **Information Disclosure** | Verbose error stack traces, unmasked PII in API responses, SSRF to cloud metadata. | World-readable storage, SharedPreferences leaks, logcat output, snapshot thumbnails, clipboard snooping. | Scoped API responses, Scoped Storage, Keystore encryption, `FLAG_SECURE`, log stripping in release builds. |
| **D** | **Denial of Service** | Regex DoS (ReDoS), unpaginated DB queries, memory exhaustion, resource starvation. | IPC broadcast flooding, heavy parsing on UI thread, excessive battery/CPU drain. | Rate limiting, strict pagination, query depth limits, timeouts, offloading IPC to background workers. |
| **E** | **Elevation of Privilege** | BOLA/IDOR, BFLA, path traversal, role spoofing (`isAdmin: true`). | Exported ContentProvider traversal, unauthorized Intent action triggers, unvalidated deep link execution. | Strict server-side RBAC/ABAC with owner scoping, non-exported components by default, signature-level permissions. |

---

## 4. High-Priority Abuse Cases

1. **Cross-Tenant IDOR/BOLA**: Manipulating an object ID in an API request (`GET /api/v1/orders/{id}`) to access another customer's data.
2. **Client-Trust Fallacy**: Trusting client-calculated totals, discounts, user roles, or biometric success booleans without server-side verification.
3. **PendingIntent Hijacking**: Passing a mutable PendingIntent to an untrusted third-party component that overwrites the base Intent to target private components.
4. **Deep Link / Custom Scheme Hijacking**: Registering a duplicate custom scheme (`myapp://`) in a malicious app to intercept tokens or sensitive URLs.
5. **SSRF to Internal Services**: Feeding internal IP addresses (`http://169.254.169.254/` or `http://10.0.0.1/`) to server-side URL fetchers.
6. **Insecure WebView Execution**: Enabling `setJavaScriptEnabled(true)` and exposing native Java/Kotlin interfaces (`addJavascriptInterface`) to arbitrary or HTTP origins.
7. **Race Conditions**: Concurrent requests attempting double redemption of gift cards, coupon reuse, or balance overdrafts.
8. **Supply Chain / Third-Party SDK Leakage**: Analytics or ad SDKs exfiltrating clipboard content, device identifiers, or user inputs to untrusted endpoints.

---

## 5. Threat-to-Mitigation Mapping

For every identified threat in the assessment, document:
$$\text{Threat ID} \longrightarrow \text{STRIDE Category} \longrightarrow \text{Enforcement Point} \longrightarrow \text{Mitigating Control} \longrightarrow \text{Verification Test}$$
Unmitigated High or Critical threats must be logged as active findings.
