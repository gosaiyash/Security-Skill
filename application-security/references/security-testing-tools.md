# Security Testing Tools (Web, API, and Mobile)

**Mandatory Rule**: Never guess command-line flags. Always execute `<tool> --help` or review official documentation before running. Prefer tools already installed or configured in the repository. Redact secrets from scan outputs before sharing.

---

## 1. Tool Selection by Target and Artifact

| Security Domain | Artifact / Target | Recommended Tooling |
|---|---|---|
| **SAST (Static Analysis)** | Web / API Source (JS, TS, Python, Go, Java, Ruby) | **Semgrep** (custom rule packs), **CodeQL**, **Bandit** (Python), **gosec** (Go), **Brakeman** (Rails), **ESLint Security Plugins**. |
| **Mobile SAST** | Android Source (Kotlin / Java) | **Android Lint** (`./gradlew lint`), **mobsfscan**, **detekt**, **ktlint**, **Semgrep** (Android rules). |
| **Secrets Scanning** | Git Repositories, commits, files | **Gitleaks** (`gitleaks detect`), **TruffleHog** (`trufflehog git file://.`). |
| **SCA & Dependencies** | Lockfiles (`package-lock.json`, `pom.xml`, `Pipfile.lock`, `Cargo.lock`) | **Trivy** (`trivy fs`), **OSV-Scanner**, `npm audit`, `pip-audit`, `cargo audit`, **OWASP Dependency-Check**. |
| **SBOM Generation** | Containers & Filesystems | **Syft** (`syft dir:. -o cyclonedx-json`), **CycloneDX CLI**. |
| **Containers & IaC** | Dockerfiles, K8s manifests, Terraform | **Hadolint** (Dockerfile lint), **Trivy** (image & misconfig scan), **Checkov**, **KICS**, **tflint**. |
| **APK / AAB Binary Triage** | Compiled Android artifacts | **aapt2**, **apksigner**, **apkanalyzer** (Android SDK), **apktool** (resource decode), **jadx** (Java/Kotlin decompiler), **bundletool** (AAB). |
| **DAST (Authorized Web Targets)** | Running Web apps, REST/GraphQL APIs | **OWASP ZAP** (baseline/active scans), **Nuclei** (vulnerability templates), **Schemathesis** (API property-based fuzzing), **Burp Suite**. |
| **Dynamic Mobile Testing** | Controlled emulator & test device | **Android Emulator**, `adb`, `logcat`, **mitmproxy** / **Burp Suite** (intercepting proxy), **Frida** / **objection** (runtime instrumentation). |
| **Reverse Engineering & Native** | Native libraries (`.so`), binaries | **Ghidra**, **radare2**, `readelf`, `objdump`, `strings`. |

---

## 2. Safe-Use Rules & Guardrails

1. **Explicit Authorization**: Run active DAST scanners, fuzzers, and dynamic mobile hooks **only** against systems, backends, accounts, and emulators explicitly authorized by the user.
2. **Offline & Passive First**: Prioritize static code review, manifest inspection, lockfile analysis, and read-only triage scripts before engaging active scanners.
3. **No External Artifact Uploads**: Never upload proprietary source code, binaries, customer APKs, or environment logs to third-party cloud scanners (e.g., public MobSF or VirusTotal) without explicit written user approval.
4. **Sandboxed Execution**: Execute build-based scanners (CodeQL builds, Gradle dependency tasks) in disposable containers or sandbox environments to prevent executing untrusted build hooks.
5. **Redact Sensitive Data**: Use `--redact` flags with secret scanners; never echo raw credentials, tokens, or private keys to terminal logs or reports.

---

## 3. Standard Invocations (Always verify syntax with `--help`)

```bash
# Secrets Scanning
gitleaks detect --source . --redact
trufflehog filesystem . --json

# Software Composition Analysis (SCA)
trivy fs . --scanners vuln,secret,misconfig
npm audit
pip-audit

# Static Code Analysis (SAST)
semgrep scan --config auto .
bandit -r app/ -ll -ii

# Mobile Source & Artifact Triage
./gradlew lint
python scripts/apk_triage.py path/to/app.apk
jadx -d out_decompiled/ path/to/app.apk
apkanalyzer -h manifest print path/to/app.apk

# Web DAST Baseline (Passive)
zap-baseline.py -t https://staging-authorized.example.com
```

---

## 4. Triage & False-Positive Elimination

Automated scanner output represents **leads**, not verified vulnerabilities. Every alert must be triaged:
1. **Trace Reachability**: Determine if the vulnerable code path or dependency function is actually reachable by untrusted input.
2. **Context & Compensating Controls**: Check if an input is already validated by middleware, sanitized, or gated behind strong authentication.
3. **Deduplicate**: Group identical findings reported by multiple tools (e.g., SAST + Lint + Secrets).
4. **Targeted Suppressions**: If a finding is a confirmed false positive, suppress it narrowly (e.g., specific rule, specific file, line number, reason, date, and author) in configuration files (`.gitleaksignore`, `semgrep.yml`). Never disable security categories globally.

---

## 5. CI/CD Security Integration Architecture

- **Pull Requests (Fast Gate)**:
  - Secrets detection (Gitleaks).
  - Incremental SAST (Semgrep on changed files).
  - Dependency diff & vulnerability scan (`npm audit` / `pip-audit`).
  - Mobile: Manifest diff check (flags newly introduced permissions or exported components).
  - *Gate*: Block merge on confirmed High or Critical findings.
- **Nightly / Main Branch (Deep Scan)**:
  - Full codebase SAST (CodeQL / SonarQube).
  - Comprehensive container & filesystem SCA (Trivy).
  - SBOM generation (Syft) and artifact archiving.
  - Scheduled passive DAST against disposable staging environments.
- **Release Pipeline**:
  - Verify release build configuration (`debuggable="false"`).
  - Check Network Security Configuration (`cleartextTrafficPermitted="false"`).
  - Ensure signing keys are stored exclusively in KMS / HSM / CI Secrets.
