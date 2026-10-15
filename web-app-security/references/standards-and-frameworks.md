# Standards and frameworks

Verified against public sources on 2026-10-15. **Re-verify editions before citing them in a report**; this file can go stale. Always distinguish *stable*, *draft*, and *in development*.

## Contents
1. Version table
2. How to use each standard
3. Choosing an ASVS level
4. Compliance language rules
5. Additional sources by stack

## 1. Version table

| Standard | Edition to cite | Status | Notes |
|---|---|---|---|
| OWASP Top 10 | 2025 | Stable (announced Nov 2025, finalized Jan 2026) | Awareness document, not a checklist. Supersedes 2021 |
| OWASP ASVS | 5.0.0 (May 2025) | Stable | ~350 requirements, 17 chapters, levels L1/L2/L3. 4.0.3 is the prior edition |
| OWASP WSTG | 4.2 (Dec 2020) | Latest stable; 5.0 in development | Cite IDs with version, e.g. `WSTG-v42-INFO-02` |
| OWASP API Security Top 10 | 2023 | Stable (check project page for newer) | API1..API10 |
| OWASP Proactive Controls | check project page | Stable | Developer-oriented controls |
| OWASP Cheat Sheet Series | rolling | Living docs | Cite the sheet name and access date |
| OWASP Secure Headers Project | rolling | Living | Header recommendations |
| OWASP Top 10 for LLM Applications | check project page | Living | Only if the app uses LLMs |
| NIST SSDF SP 800-218 | v1.1 (Feb 2022) | Final | Rev. 1 (SSDF v1.2) was an initial public draft in Dec 2025; check whether finalized before citing it as final |
| NIST SP 800-218A | Jul 2024 | Final | SSDF community profile for generative AI |
| NIST CSF | 2.0 | Final | Org-level risk framework, not an AppSec standard |
| NIST SP 800-228 | 2025 | check status | Guidelines for API protection for cloud-native systems |
| MITRE CWE Top 25 | 2025 | Stable (Dec 2025) | Ranked weakness types from CVE data; for prioritizing, not compliance |
| CIS Benchmarks | per product/version | Stable per benchmark | Pick the benchmark matching the exact OS/DB/cloud/K8s version |
| OpenSSF Scorecard | tool-versioned | Tooling | Project-hygiene signals for dependencies, not proof of security |
| CVSS | v4.0 and v3.1 | Both in use | State which one; see vulnerability-severity.md |

## 2. How to use each

- **ASVS**: the verification standard. Use it to set assurance level and to cite requirement-level evidence. Confirm exact requirement IDs in the document before citing.
- **Top 10 2025**: communication and prioritization. Categories: A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions. SSRF is folded into A01 in 2025. If the project cites 2021, map both and say so.
- **WSTG**: the catalogue of how to test; use it to build dynamic test plans.
- **CWE**: root-cause taxonomy. Every finding gets a CWE where one fits. 2025 Top 25 web-relevant entries include CWE-79 (XSS), CWE-89 (SQLi), CWE-352 (CSRF), CWE-862 (Missing Authorization), CWE-22 (Path Traversal), CWE-78 (OS Command Injection), CWE-94 (Code Injection), CWE-434 (Unrestricted Upload), CWE-502 (Deserialization), CWE-863 (Incorrect Authorization), CWE-306 (Missing Authentication), CWE-20 (Improper Input Validation).
- **API Top 10**: required lens for any API (see api-security.md).
- **SSDF / CSF**: process and governance mapping for "secure SDLC" requests; map practices to what the repo actually shows (PO, PS, PW, RV practice groups in SSDF).
- **CIS / vendor hardening**: configuration baselines for the concrete platform.

## 3. Choosing an ASVS level (recommend, then confirm with the user)

- **L1**: low-risk or early-stage apps, internal tools without sensitive data.
- **L2**: default for most apps with accounts, personal data, business data, or payments.
- **L3**: high-value targets (finance, health, critical infrastructure, large multi-tenant platforms).

Levels are cumulative. ASVS 5.0 expects documented security decisions where a requirement is met in a non-obvious way; record them.

## 4. Compliance language rules

- Say "assessed against ASVS 5.0.0 L2, chapters V6, V7, V8 only", never "ASVS compliant".
- Never claim PCI DSS, SOC 2, ISO 27001, HIPAA, or GDPR compliance. A technical control may "support" a requirement; recommend a qualified assessor for formal compliance.
- Record for each standard used: edition, applicable controls, scope, exclusions, evidence, date.
- Blog posts, vendor pages, and forum answers are not standards. Prefer the owning organization's page or repository.

## 5. Additional sources by stack (discover, then verify)

Use official docs for the detected stack: the framework's security guide (Django, Rails, Spring Security, Laravel, ASP.NET Core, Express/Node.js security best practices, FastAPI/Starlette), the language's secure coding guidance, the database vendor's hardening guide, the identity provider's docs, the cloud provider's security best practices (AWS, Azure, Google Cloud), Kubernetes security docs, Docker/OCI docs. Note doc version and access date in the report.
