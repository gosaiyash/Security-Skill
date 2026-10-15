# Standards and Frameworks

Verified against authoritative public sources on 2026-10-15. **Re-verify editions before citing them in a report**; standards evolve. Always distinguish *stable*, *draft*, *deprecated*, and *in development*.

---

## 1. Version Table

| Standard | Edition to Cite | Status | Domain / Notes |
|---|---|---|---|
| **OWASP Top 10** | 2025 | Stable (Nov 2025 / Jan 2026) | Web awareness. A01 Broken Access Control, A02 Security Misconfiguration, A03 Supply Chain, A04 Crypto, A05 Injection, A06 Insecure Design, A07 Auth Failures, A08 Software/Data Integrity, A09 Logging & Alerting, A10 Exceptional Conditions. |
| **OWASP ASVS** | 5.0.0 (May 2025) | Stable | Web verification standard (~350 requirements, 17 chapters, levels L1/L2/L3). Prior edition: 4.0.3. |
| **OWASP MASVS** | v2.1.0 (Jan 2024) | Stable | Mobile Application Security Verification Standard (8 categories, 24 controls). |
| **OWASP MASWE** | v1.0.0 | Stable | Mobile App Security Weakness Enumeration (MASWE-0001..MASWE-0078). |
| **OWASP MASTG** | v2.0.0 (June 2026) | Stable | Mobile Application Security Testing Guide (modular tests, demos, techniques). Legacy v1 tests are deprecated. |
| **OWASP API Security Top 10** | 2023 | Stable | API-specific vulnerability patterns (API1:BOLA, API2:Broken Auth, API3:BOPLA, API5:BFLA, etc.). |
| **OWASP WSTG** | 4.2 (Dec 2020) | Stable (5.0 in dev) | Web Security Testing Guide. Cite IDs with version (`WSTG-v42-INFO-02`). |
| **OWASP Top 10 for LLM Applications** | 2025 | Living | LLM01 Prompt Injection, LLM02 Sensitive Info Disclosure, LLM06 Excessive Agency, etc. |
| **MITRE CWE Top 25** | 2025 | Stable | Most dangerous software weaknesses (CWE-79, CWE-89, CWE-352, CWE-862, CWE-22, CWE-78, etc.). |
| **NIST SSDF SP 800-218** | v1.1 (Feb 2022) | Final | Secure Software Development Framework (PO, PS, PW, RV practice groups). |
| **NIST SP 800-218A** | Jul 2024 | Final | SSDF community profile for generative AI. |
| **CIS Benchmarks** | Per product/version | Stable | Configuration baselines for OS, databases, cloud, and Kubernetes. |
| **CVSS** | v4.0 and v3.1 | Both in use | State version used; see `references/vulnerability-severity.md`. |

---

## 2. Web Application Standards (ASVS & Top 10)

### Choosing an ASVS 5.0.0 Level
- **Level 1 (L1)**: Low-risk, early-stage apps, internal tooling without PII or sensitive business secrets. Basic automated + manual hygiene.
- **Level 2 (L2)**: **Default** for most applications handling user accounts, personal data, transactional data, business secrets, or payments. Defense in depth required.
- **Level 3 (L3)**: High-assurance / mission-critical applications (banking, healthcare, critical infrastructure, large multi-tenant platforms).

### Applying ASVS & Top 10
- **ASVS**: The primary verification benchmark. Cite exact chapter and requirement IDs (e.g., `ASVS-5.0.0-V3.2.1`).
- **Top 10**: High-level communication and prioritization tool for executive summaries.
- **CWE**: Root-cause taxonomy. Map every finding to a valid CWE identifier.

---

## 3. Mobile Application Standards (MASVS, MASWE, MASTG)

### MASVS v2.1.0 Categories
- **MASVS-STORAGE**: Secure storage of sensitive data (`-1`), prevent leakage (`-2`).
- **MASVS-CRYPTO**: Current strong cryptography (`-1`), proper key management (`-2`).
- **MASVS-AUTH**: Secure authentication/authorization protocols (`-1`), secure local auth (`-2`), step-up authentication for sensitive operations (`-3`).
- **MASVS-NETWORK**: Secure all network traffic (`-1`), identity pinning for controlled endpoints (`-2`).
- **MASVS-PLATFORM**: Secure IPC (`-1`), secure WebViews (`-2`), secure UI use (`-3`).
- **MASVS-CODE**: Up-to-date platform version required (`-1`), app update enforcement (`-2`), no vulnerable components (`-3`), input validation and sanitization (`-4`).
- **MASVS-RESILIENCE**: Platform integrity validation (`-1`), anti-tampering (`-2`), anti-static analysis (`-3`), anti-dynamic analysis (`-4`). (Defense in depth: apply by threat model, e.g., fintech, gaming, DRM).
- **MASVS-PRIVACY**: Minimize access to sensitive data/resources (`-1`), prevent user identification/tracking (`-2`), transparency about data collection (`-3`), user control over data (`-4`).

### The Mobile Mapping Chain
$$\text{MASVS Control} \longrightarrow \text{MASWE Weakness} \longrightarrow \text{MASTG Test}$$
Use MASVS to state the normative requirement, MASWE to name the specific weakness mechanism, and MASTG to cite the test procedure. If you cannot verify a current MASTG v2 test ID, cite the MASVS control and describe the test in words; never fabricate test IDs.

---

## 4. Platform & Ecosystem Security Requirements

### Android & Google Play Target API Requirements
- Target API level: New apps and updates on Google Play must target Android 16 (API 36) or higher.
- Legacy target SDK (< 34) risks disabling critical OS defenses: scoped storage, explicit exported component requirements, background execution limits, default cleartext TLS denial, and PendingIntent mutability enforcement.
- 16 KB page-size support: Mandatory for native libraries (`.so`) running on modern Android devices.

---

## 5. Compliance & Citation Rules

1. **Never claim compliance**: Never write "the app is secure", "ASVS compliant", "MASVS certified", or "Play-policy approved".
2. **State exact scope**: Write "Assessed against OWASP ASVS 5.0.0 Level 2 (Chapters V2, V3, V5) and OWASP MASVS v2.1.0 (STORAGE, NETWORK, PLATFORM); RESILIENCE was out of scope."
3. **Formal compliance is human-led**: Technical controls may *support* compliance; state that formal regulatory determinations (PCI-DSS, HIPAA, GDPR, DPDP) require certified external auditors.
4. **Authoritative sources only**: Reference official specifications and vendor hardening guides, not random blogs or forum posts.
