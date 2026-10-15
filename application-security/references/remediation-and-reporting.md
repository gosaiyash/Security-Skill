# Remediation, Reporting, and Verification (Web, API, and Mobile)

Standardized finding format, severity scoring, evidence handling, safe remediation workflows, and regression test requirements.

---

## 1. Unified Finding Format

Every finding documented in an assessment or audit must follow this schema:

```text
ID: SEC-001 (e.g., WEB-001, APK-001, API-001)
Title: [Actionable & Specific, e.g., "Invoice endpoint allows cross-tenant read (BOLA)"]
Severity: Critical | High | Medium | Low | Informational
Confidence: Confirmed | Likely | Possible
Status: Open | Remediated | Risk Accepted | False Positive
Target Artifact: [Repository / Endpoint / APK package name & SHA-256]
Component: [File path and line number, Route, Manifest entry, Config key]
Weakness: CWE-[ID] (e.g., CWE-862, CWE-639, CWE-926)
Standards Mapping: 
  - OWASP Top 10:2025 [Category, e.g., A01 Broken Access Control]
  - OWASP ASVS 5.0.0 [Chapter & Requirement, e.g., V4.1.1] (if Web/API)
  - OWASP MASVS v2.1.0 [Control, e.g., MASVS-STORAGE-1] (if Mobile)
  - OWASP MASTG v2.0.0 [Test ID or description] (if Mobile)
Preconditions: [Attacker position: anonymous, authenticated user, malicious installed app]
Expected vs. Observed: [Expected authorization check vs observed unauthenticated access]
Impact: [Realistic business, privacy, or technical impact]
Evidence: [Sanitized code excerpt, redacted request/response, or test output summary]
Reproduction (Safe): [Step-by-step reproduction using synthetic data / test accounts]
Root Cause: [Underlying architectural or coding omission]
Remediation: [Smallest correct fix, framework control reference, minimal diff]
Regression Test: [Test file, method name, and assertion verifying the fix]
Retest Result: Closed with Evidence | Fixed (Unverified) | Not Retested (reason)
Residual Risk / Limitations: [Non-code actions, manual secret rotation, platform review]
```

Categorize findings into distinct sections:
1. **Confirmed Vulnerabilities** (proven with code-path trace, failing unit test, or authorized reproduction).
2. **Suspected Issues** (code patterns suggesting risk, pending environmental validation).
3. **Hardening & Best Practices** (defense-in-depth opportunities without immediate exploitability).
4. **Not Tested** (areas out of scope or lacking test environments; never claim Pass).

---

## 2. Severity Rating Matrix

Severity is calculated as:
$$\text{Severity} = \text{Realistic Impact} \times \text{Realistic Likelihood}$$

| Severity | Criteria (Web & API) | Criteria (Mobile / Android) |
|---|---|---|
| **Critical** | Remote unauthenticated RCE, unauthenticated DB dump (SQLi), mass cross-tenant account takeover, hardcoded server master private keys or admin secrets. | Production signing keystore private keys embedded in APK, remote code execution via WebView, client-trusted auth allowing mass unauthorized cloud access. |
| **High** | BOLA/IDOR on sensitive PII/financial data, SSRF to cloud metadata (AWS IMDS), stored XSS in admin console, auth bypass via JWT `alg: none`. | Exported components leaking credentials/PII to other apps, TLS validation disabled in release (`TrustManager` stub), auth bypass via deep link, plaintext tokens with backup exposure. |
| **Medium** | Missing rate limits on login/OTP, CSRF on non-critical actions, mass assignment on non-privileged fields, cleartext HTTP on internal services. | Missing `FLAG_IMMUTABLE` with redirect risk, sensitive data logged to Logcat in release, over-broad runtime permissions, vulnerable third-party SDK with reachable path. |
| **Low** | Verbose error stack traces, missing security headers (`X-Content-Type-Options`), public API keys without domain restrictions. | Unrestricted public Google Maps key in APK, lack of `FLAG_SECURE` on non-financial screens, debug code in test builds. |
| **Informational** | Architectural observations, missing code documentation, defense-in-depth suggestions. | Resilience/obfuscation gaps (R8 disabled) where threat model does not strictly require anti-tamper. |

---

## 3. Evidence Handling & Sanitization Rules

1. **Redact All Secrets**: Never paste full API keys, passwords, bearer tokens, private keys, or PII into reports or terminal output. Use fingerprints (e.g., `sk_live_...4a9f`) or `<redacted>`.
2. **Proportionate Demonstration**: Prove vulnerabilities with the smallest safe indicator (e.g., querying your own secondary test account's record, reading a harmless config parameter). Never extract bulk database rows or target third-party accounts.
3. **No Weaponized Kits**: Provide clear reproduction steps for developers, but omit weaponized exploit scripts or automated wormable payloads.

---

## 4. Remediation Workflow & Quality Gate

1. **Fix Root Causes**: Address the architectural flaw using platform/framework-vetted controls (parameterized queries, framework CSRF, Android Keystore, proper DTO schemas) rather than ad-hoc sanitization regexes.
2. **Minimize Diff Size**: Keep code modifications focused and surgical to reduce the risk of unintended side effects.
3. **Never Weaken Protections**: Never disable linting, CSRF protection, TLS validation, or authentication checks to make a test pass.
4. **Non-Code Remediation Actions**:
   - Immediately rotate compromised secrets, database credentials, and API keys.
   - Revoke active user sessions and refresh tokens on the identity provider.
   - Update cloud IAM policies, S3 bucket permissions, and firewall rules.
   - For mobile apps: Update Google Play Data Safety forms and deploy mandatory app updates.

---

## 5. Security Regression Testing Architecture

Every security remediation must be accompanied by an automated regression test:
- **Negative Test Case**: Validates that malicious or unauthorized input is explicitly rejected (returns `401`, `403`, or validation error).
- **Positive Test Case**: Validates that legitimate business workflows and valid user requests continue to function uninterrupted.
- **Test Placement**: Integrate tests directly into the project's standard CI test suite (`npm test`, `pytest`, `./gradlew test`).
- Refer to `templates/security-regression-plan.md` (Web) and `templates/mobile-regression-plan.md` (Mobile).

---

## 6. Responsible Disclosure & Reporting Language

- **Honest Claims**: Never write "the system is 100% secure" or "compliant with ASVS/MASVS". State precisely what was evaluated, with what tools, against which versions, and enumerate what remained uninspected.
- **Third-Party Disclosures**: Disclose vulnerabilities discovered in third-party libraries or open-source packages privately to the maintainers via `SECURITY.md` or coordinated disclosure programs before public discussion.
