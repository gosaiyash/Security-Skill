# Application Security Assessment Report: <application_name>

| Metadata Field | Assessment Record |
|---|---|
| **Date** | YYYY-MM-DD |
| **Assessor / Agent** | <name, agent model> |
| **Target Application** | <web repo / API base URL / APK package & SHA-256> |
| **Commit / Version** | <git commit hash / versionName (versionCode)> |
| **Assessment Mode(s)** | <Mode A-I, e.g., Source Audit + API Assessment + Mobile Triage> |
| **Environment** | <local / disposable staging / authorized emulator> |
| **Authorization Scope** | <Authorized by, authorized endpoints/devices, prohibited actions> |

---

## 1. Executive Summary
*(3–6 sentences summarizing overall security posture, finding counts by severity, primary risk drivers, and critical immediate actions. Never make absolute claims such as "secure" or "100% compliant".)*

---

## 2. Assessment Scope and Methodology

- **In Scope**: <Repositories, API endpoints, microservices, mobile APK/AAB packages>
- **Excluded / Out of Scope**: <Third-party integrations, DDoS testing, production systems>
- **Not Inspected (Unknowns)**: <Backend database queries, closed-source dependencies>
- **Methodology**: Static source analysis (SAST), manual code inspection, threat modeling, architecture review, and controlled dynamic testing.
- **Tooling Used**: <e.g., Semgrep, Gitleaks, Trivy, jadx, apksigner, ZAP>
- **Standards Referenced**:
  - OWASP Top 10:2025
  - OWASP ASVS 5.0.0 (Level: <L1/L2/L3>, Chapters: <V...>)
  - OWASP API Security Top 10 (2023)
  - OWASP MASVS v2.1.0 & MASTG v2.0.0 (Categories: <...>)
  - MITRE CWE Top 25 (2025)

---

## 3. Architecture & Attack Surface Summary
*(Data flows, trust boundaries, entry points, sensitive data assets, and multi-tenant boundaries. Contrast evidence-based observations against unverified assumptions.)*

---

## 4. Findings Summary Table

| ID | Finding Title | Severity | Confidence | Standards / CWE | Status |
|---|---|---|---|---|---|
| SEC-001 | Cross-tenant invoice access (BOLA) | High | Confirmed | ASVS V4.1.1 / CWE-639 | Open |
| SEC-002 | Exported activity allows intent redirection | High | Confirmed | MASVS-PLATFORM-1 / CWE-926 | Open |
| SEC-003 | Hardcoded test credential in repository | Critical | Confirmed | CWE-798 | Remediated |

---

## 5. Detailed Vulnerability Findings
*(One standardized block per finding formatted according to `references/remediation-and-reporting.md`)*

---

## 6. Controls Verified & Defense-in-Depth Highlights
*(Document areas where robust controls were verified through evidence: e.g., parameterized queries universally enforced, Android Keystore correctly bound to StrongBox, HSTS and CSP strictly configured.)*

---

## 7. Standards Verification Matrix

### Web & Backend (ASVS 5.0.0 & API Top 10)
| Domain | Assessed Scope | Result (Pass / Fail / Partial / N/A / Unknown) |
|---|---|---|
| V2 Authentication | Login, reset, token lifecycle | |
| V3 Session Management | Cookies, JWT invalidation | |
| V4 Access Control | Object & function level authorization | |
| V5 Input Validation | Boundary schemas, type checking | |
| V6 Cryptography | AEAD, Key management | |
| V8 Data Protection | Secrets, logging, PII masking | |
| V9 Communications | TLS configuration, HSTS | |

### Mobile Client (MASVS v2.1.0)
| Category | Controls Assessed | Result & Evidence Summary |
|---|---|---|
| MASVS-STORAGE | -1 Sensitive storage, -2 Leakage prevention | |
| MASVS-CRYPTO | -1 Strong crypto, -2 Keystore management | |
| MASVS-AUTH | -1 Auth protocols, -2 Biometrics | |
| MASVS-NETWORK | -1 Transport security, -2 Pinning | |
| MASVS-PLATFORM | -1 IPC security, -2 WebViews | |
| MASVS-CODE | -1 Target SDK, -4 Input validation | |
| MASVS-RESILIENCE | -1 Integrity, -2 Anti-tamper | |
| MASVS-PRIVACY | -1 Data minimization, -2 Permissions | |

---

## 8. Applied Remediations and Verification Tests
*(List PR/commit diffs applied during the assessment, accompanying automated regression tests, and before/after verification evidence.)*

---

## 9. Residual Risk and Non-Code Action Items
- [ ] Rotate compromised credentials, API keys, or certificates immediately.
- [ ] Invalidate active session tokens on authorization server.
- [ ] Update Google Play Data Safety declaration or privacy notices.
- [ ] Configure production secrets management and rate limiting.

---

## 10. Prioritized Security Roadmap
- **Immediate (0–7 days)**: Remediate Critical and High severity findings.
- **Short-Term (30 days)**: Address Medium findings, deploy automated PR security gates.
- **Medium-Term (60–90 days)**: Implement architecture hardening, defense-in-depth, and periodic penetration testing.

---

## Appendix: Sanitized Evidence & Tool Outputs
*(Include sanitized scanner logs, decompiler outputs, or redacted HTTP transcripts demonstrating findings.)*
