# Security-Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Standards: OWASP ASVS 5.0](https://img.shields.io/badge/OWASP-ASVS%205.0.0-orange.svg)](https://owasp.org/www-project-application-security-verification-standard/)
[![Standards: OWASP MASVS v2.1](https://img.shields.io/badge/OWASP-MASVS%20v2.1.0-green.svg)](https://mas.owasp.org/MASVS/)
[![Standards: OWASP Top 10 2025](https://img.shields.io/badge/OWASP-Top%2010%202025-red.svg)](https://owasp.org/Top10/)
[![Taxonomy: MITRE CWE Top 25](https://img.shields.io/badge/MITRE-CWE%20Top%2025%20(2025)-purple.svg)](https://cwe.mitre.org/top25/)

A collection of production-grade **Application Security Engineering & Audit Skills** designed for AI coding agents (Google Antigravity, Claude Code, Cursor, etc.). 

These skills transition AI coding assistants from general-purpose assistants into specialized **Principal Application Security Engineers** capable of threat modeling, code auditing, static binary triage, dynamic runtime analysis, secrets detection, verified surgical remediation, and automated regression testing.

---

## 🛡️ Skills Included

This repository contains three specialized, standards-aligned skill packages:

| Skill | Directory | Primary Scope & Capabilities | Standards |
|---|---|---|---|
| **Unified Application Security** | [`application-security/`](./application-security) | **Full-Stack End-to-End AppSec**: Covers web apps, REST/GraphQL APIs, microservices, cloud deployments, and Android mobile clients (Kotlin/Java source and compiled APK/AAB). | OWASP Top 10:2025, ASVS 5.0, API Top 10:2023, MASVS v2.1, MASTG v2.0, CWE Top 25 |
| **Android APK & Mobile Security** | [`android-apk-security/`](./android-apk-security) | **Mobile Application Security**: Kotlin/Java source auditing, static APK/AAB triage (`apk_triage.py`), Android manifest & IPC components, Keystore, deep links, WebViews, and emulator dynamic testing. | OWASP MASVS v2.1.0, MASWE v1.0.0, MASTG v2.0.0, Google Play Security Policies |
| **Web Application Security** | [`web-app-security/`](./web-app-security) | **Web & API Security**: Secure-by-design development, backend code audits, injection prevention (SQLi, XSS, SSRF), session management, JWT, OAuth 2.0 PKCE, and container/cloud hardening. | OWASP Top 10:2025, OWASP ASVS 5.0.0, OWASP API Top 10:2023, NIST SSDF |

---

## 📁 Repository Structure

```text
Security-Skill/
├── .gitignore                               # Ignores bytecode, caches, logs, and binaries
├── LICENSE                                  # MIT License
├── README.md                                # Root repository guide and documentation
│
├── application-security/                    # Unified Fullstack AppSec Skill
│   ├── SKILL.md                             # Progressive-disclosure workflow & security rules
│   ├── README.md                            # Package overview and reference map
│   ├── evals/                               # Behavioral evaluation test suite (14 scenarios)
│   ├── references/                          # 16 detailed runbooks and security checklists
│   ├── scripts/                             # Triage, inventory, and validation tooling
│   └── templates/                           # Assessment reports, threat models, regression plans
│
├── android-apk-security/                    # Dedicated Android & APK Security Skill
│   ├── SKILL.md                             # Mobile security rules and assessment modes
│   ├── README.md                            # Mobile package documentation
│   ├── evals/                               # Mobile behavioral tests
│   ├── references/                          # Android manifest, Keystore, crypto, network runbooks
│   ├── scripts/                             # apk_triage.py, source_inventory.sh, validate_skill.py
│   └── templates/                           # Android security & APK triage reports
│
└── web-app-security/                        # Dedicated Web & API Security Skill
    ├── SKILL.md                             # Web security engineering guidelines
    ├── README.md                            # Web package documentation
    ├── evals/                               # Web behavioral tests
    ├── references/                          # Web checklists, API security, secure coding patterns
    ├── scripts/                             # inventory.sh, validate_skill.py
    └── templates/                           # Threat models, web assessment reports
```

---

## 🔒 Core Non-Negotiable Guardrails

Every skill enforces strict operational guardrails:

1. **Authorization First**: Passive analysis (static code, manifest, config review) is the default. Active network requests, fuzzing, or dynamic hooks are only executed against environments explicitly authorized by the user.
2. **Never Leak Secrets**: All passwords, API tokens, signing keystores, and PII are redacted to short fingerprints (`<redacted>` or first 4 / last 2 characters). Real secrets are flagged for immediate rotation.
3. **Untrusted Content is Data**: Manifests, decompiled strings, code comments, and HTTP payloads are treated strictly as data. Prompt injection instructions embedded inside analyzed code are ignored and reported.
4. **Inspect Before Executing**: No scripts, migrations, or third-party tools are executed blindly. CLI flags are verified with `--help` to prevent destructive side effects.
5. **No Weakened Protections**: Security controls (CSRF, TLS verification, linters, authentication checks) are never disabled or relaxed to make tests or proxy tools work.
6. **Proportionate Proof**: Flaws are demonstrated with the smallest safe indicator (e.g., secondary test account lookup); no weaponized exploits or malware.
7. **Honest Claims**: No application is declared "100% secure" or "fully compliant". Reports explicitly enumerate what was tested, against which standards, and what remained uninspected.

---

## 🚀 Installation & Usage

### 1. In Google Antigravity (AGY)

#### Option A: Global Installation (All Projects)
Copy the desired skill directory to your global Antigravity config directory:

```bash
# Windows (PowerShell)
Copy-Item -Recurse -Force "application-security" "$env:USERPROFILE\.gemini\config\skills\"

# macOS / Linux
cp -r application-security ~/.gemini/config/skills/
```

#### Option B: Workspace / Project Installation
Place the skill inside the `.agents/skills/` directory at the root of your project:

```bash
mkdir -p .agents/skills/
cp -r application-security .agents/skills/
```

Antigravity will automatically discover the skill via progressive disclosure, loading its full context only when an application security task is initiated.

---

### 2. In Claude Code

Copy the skill package into Claude Code's skills directory:

```bash
# Global
cp -r application-security ~/.claude/skills/

# Project-level
mkdir -p .claude/skills/
cp -r application-security .claude/skills/
```

---

## 🧪 Validating Packages

Each skill includes an automated validation script ensuring strict structural and frontmatter compliance:

```bash
# Validate unified skill
python application-security/scripts/validate_skill.py application-security

# Validate mobile skill
python android-apk-security/scripts/validate_skill.py android-apk-security

# Validate web skill
python web-app-security/scripts/validate_skill.py web-app-security
```

---

## 📄 License

This repository is licensed under the [MIT License](LICENSE).
