# Security testing tools

**Rule: never guess flags.** Run `<tool> --help` (or the official docs) first. Prefer tools already configured in the repo. Ask before installing. Pin versions, install from official sources, and verify checksums where provided. Output often contains secrets; redact before sharing.

## Contents
1. Selection by purpose
2. Safe-use rules
3. Typical invocations (verify first)
4. Triage rules
5. CI integration pattern

## 1. Selection by purpose
| Purpose | Tools (all real, pick what fits the stack) |
|---|---|
| SAST | Semgrep, CodeQL, Bandit (Python), gosec (Go), Brakeman (Rails), SpotBugs + Find Security Bugs (Java), ESLint security plugins (JS/TS), language linters |
| Secrets | Gitleaks, TruffleHog, GitHub secret scanning |
| SCA / dependencies | OSV-Scanner, Trivy, Grype, `npm audit`, `pip-audit`, `cargo audit`, OWASP Dependency-Check, Dependabot/Renovate |
| SBOM | Syft, CycloneDX tools |
| Containers | Trivy, Grype, Hadolint (Dockerfile lint), Docker Scout |
| IaC | Checkov, Trivy config scanning, KICS, tflint |
| DAST (authorized targets only) | OWASP ZAP (baseline/full scans), Nuclei (templates), Burp Suite (commercial), Schemathesis/Dredd for API contract fuzzing |
| TLS | testssl.sh, SSL Labs for public hosts |
| Supply-chain posture | OpenSSF Scorecard, Sigstore cosign for verification |
| Specialized, high-risk | sqlmap and similar exploit tools: only with explicit authorization, in staging, never against production by default |

## 2. Safe-use rules
- DAST/fuzzers only against authorized targets, with rate limits, a test account, and a stop condition. ZAP "baseline" (passive) is the default; active scans need explicit approval.
- Do not point scanners at third-party hosts discovered during testing.
- Scanners that execute project code (some build-based SCA, CodeQL builds) run in a sandbox/CI container, not on a workstation with secrets.
- Network-using SAST rules or "auto" configs may fetch rule packs; make sure that is acceptable.
- Do not upload proprietary code to third-party services without user approval.

## 3. Typical invocations (examples; confirm with `--help` for the installed version)
```bash
gitleaks detect --source . --redact          # secrets in repo history
trivy fs .                                   # vulns, secrets, misconfig in filesystem
trivy image <image>                          # container image scan
semgrep scan --config <ruleset-or-path> .    # SAST; choose rules deliberately
bandit -r <package_dir>                      # Python SAST
pip-audit                                    # Python dependencies
npm audit                                    # Node dependencies
osv-scanner --help                           # CLI syntax changed between major versions; read help
syft dir:. -o cyclonedx-json                 # SBOM
checkov -d <iac_dir>                         # IaC scan
hadolint Dockerfile                          # Dockerfile lint
zap-baseline.py -t <authorized_url>          # passive ZAP baseline (via ZAP Docker/packaged scripts)
```
Add `--redact` or equivalent where available so secrets are not echoed.

## 4. Triage rules
1. Reproduce or trace each finding to reachable code. 2. Mark false positives with the reason; suppress narrowly (rule + line + justification + date), never globally. 3. Map confirmed findings to CWE and severity. 4. Deduplicate across tools. 5. For dependency CVEs: check whether the vulnerable function is reachable, whether a fixed version exists, exploit evidence (CISA KEV, EPSS), and exposure.
Do not report raw scanner output as findings.

## 5. CI integration pattern
- Pull requests: fast checks (secrets, SAST diff, dependency diff, lint, IaC). Block on high-confidence high/critical.
- Nightly/main: full SCA, container scans, SBOM, scheduled DAST baseline against staging.
- Release: SBOM and signatures attached; provenance recorded.
- Run scanners with read-only tokens; upload results as SARIF where the platform supports it; track suppressions in version control; measure time-to-fix.
- Start with warn-only for noisy tools, then ratchet to blocking.
