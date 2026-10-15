# application-security Skill Package

A unified, production-grade application security engineering skill package for Antigravity AI coding agents and security engineers. It integrates web application security, backend APIs, cloud infrastructure, and mobile client security (Android APK/AAB and source) into a single cohesive framework.

---

## Overview

Modern software applications are multi-tiered systems comprising web frontends, mobile client apps (Android/Kotlin/Java/Flutter/React Native), API gateways, microservices, databases, and CI/CD pipelines.

The `application-security` skill harmonizes:
- **Web & Backend Security**: OWASP Top 10 (2025), OWASP ASVS 5.0.0 (Levels 1–3), OWASP API Security Top 10 (2023), input validation, injection prevention, authentication, session security, CSRF, SSRF, BOLA/IDOR, secure headers, and cloud infrastructure.
- **Mobile Client Security**: OWASP MASVS v2.1.0, MASWE v1.0.0, MASTG v2.0.0, Android manifest and IPC components, Android Keystore, biometric authentication, deep links/App Links, WebViews, static APK/AAB triage (`apk_triage.py`), and dynamic testing workflows.
- **Fullstack Lifecycle**: Threat modeling (STRIDE), static analysis (SAST), software composition analysis (SCA), secrets detection, verified remediation diffs, and automated regression testing.

---

## Directory Structure

```text
application-security/
├── SKILL.md                                 # Master instruction file with frontmatter and workflow
├── README.md                                # Package documentation
├── evals/
│   └── behavior-evals.json                  # Behavioral evaluation suite (Web & Mobile test prompts)
├── references/
│   ├── api-and-network-security.md          # REST, GraphQL, gRPC, TLS, NSC, certificate pinning
│   ├── apk-intake-and-triage.md             # APK/AAB static intake, decompilation, signing
│   ├── authentication-and-authorization.md  # Web sessions, JWT, OAuth PKCE, biometrics, multi-tenancy
│   ├── data-storage-and-cryptography.md     # DB encryption, secrets, Android Keystore, Tink
│   ├── dynamic-testing-workflow.md          # Controlled emulator & API dynamic testing
│   ├── infrastructure-and-deployment.md     # Docker, K8s, CI/CD, IaC, cloud, secure headers
│   ├── mobile-manifest-and-components.md    # Android components, IPC, deep links, WebViews
│   ├── privacy-and-permissions.md           # Android permissions, SDK flows, Play Store policy
│   ├── remediation-and-reporting.md         # Unified finding schema, evidence, retesting
│   ├── reverse-engineering-and-tamper-resistance.md # R8, ProGuard, root detection, Play Integrity
│   ├── secure-coding-patterns.md            # Vulnerable vs fixed code patterns
│   ├── security-testing-tools.md            # SAST, DAST, SCA, secrets, and mobile tools
│   ├── standards-and-frameworks.md          # ASVS 5.0, Top 10 2025, MASVS v2.1, MASTG v2.0, CWE
│   ├── threat-modeling.md                   # STRIDE across web, API, and mobile architectures
│   ├── vulnerability-severity.md            # CVSS rating and severity guidelines
│   └── web-security-checklist.md            # Comprehensive web application review checklist
├── scripts/
│   ├── apk_triage.py                        # Safe, offline static APK/AAB triage script
│   ├── inventory.sh                         # Fullstack / web codebase inventory script
│   ├── source_inventory.sh                  # Mobile source code inventory script
│   └── validate_skill.py                    # Package integrity validation script
└── templates/
    ├── android-security-report.md           # Dedicated mobile assessment report template
    ├── apk-triage-report.md                 # Rapid APK triage deliverable template
    ├── application-security-report.md       # Master unified security assessment report template
    ├── mobile-regression-plan.md            # Mobile regression test plan template
    ├── security-regression-plan.md          # Web/API security regression test plan template
    └── threat-model.md                      # System threat model template
```

---

## Validation

To validate package integrity, run:

```bash
python scripts/validate_skill.py
```

This verifies frontmatter conformity, description length ($\le 1024$ chars), line counts ($\le 500$ lines for `SKILL.md`), internal reference links, and absence of hardcoded secrets.
