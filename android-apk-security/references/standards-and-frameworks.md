# Standards and frameworks

Verified from public sources on 2026-10-15. **Re-verify before citing in a report.** Distinguish stable, deprecated, beta, and draft.

## Contents
1. Version table
2. MASVS v2.1.0 categories and controls
3. How MASVS, MASWE, MASTG fit together
4. Android platform and Play requirements
5. Other references
6. Citation and compliance rules

## 1. Version table
| Standard | Edition | Status / note |
|---|---|---|
| OWASP MASVS | v2.1.0 (adds MASVS-PRIVACY, Jan 2024) | Stable. 8 categories, 24 controls. Levels (L1/L2/R) were removed from MASVS in v2.0.0; scoping is done via MASTG profiles/context |
| OWASP MASWE | v1.0.0 | Stable. MASWE-0001..MASWE-0078, consecutive and grouped by MASVS category. Earlier IDs from the beta may differ |
| OWASP MASTG | v2.0.0 (June 2026) | Stable. Modular: tests, demos, best practices, techniques, tools, knowledge. v2 tests are canonical. v1 tests are deprecated/legacy; do not cite v1 IDs as current |
| MITRE CWE Top 25 | 2025 | Useful for prioritizing weakness classes; MASWE also cross-references CWEs |
| NIST SSDF SP 800-218 | v1.1 final; Rev. 1 (v1.2) was a draft in Dec 2025 | Check status before citing as final |
| OWASP Mobile Top 10 | check project page | Awareness list, not a testing standard |

## 2. MASVS v2.1.0 (paraphrased; confirm exact wording on mas.owasp.org)
- **STORAGE**: -1 secure storage of sensitive data; -2 prevent leakage of sensitive data.
- **CRYPTO**: -1 current strong cryptography used correctly; -2 key management done well.
- **AUTH**: -1 secure authentication/authorization protocols; -2 secure local authentication; -3 extra authentication for sensitive operations.
- **NETWORK**: -1 secure all network traffic; -2 identity pinning for endpoints under the developer's control.
- **PLATFORM**: -1 secure IPC; -2 secure WebViews; -3 secure UI use.
- **CODE**: -1 up-to-date platform version required; -2 mechanism to enforce app updates; -3 no components with known vulnerabilities; -4 validate and sanitize untrusted input.
- **RESILIENCE**: -1 platform integrity validation; -2 anti-tampering; -3 anti-static analysis; -4 anti-dynamic analysis.
- **PRIVACY**: -1 minimize access to sensitive data/resources; -2 prevent user identification; -3 transparency about data collection/usage; -4 user control over data.
RESILIENCE controls are defense in depth; apply by threat model (finance, DRM, game integrity), not by default.

## 3. Chain
MASVS control -> MASWE weakness -> MASTG test -> MASTG demo. Use MASVS to state the requirement, MASWE to name how it fails, MASTG to choose the test. Identify the test by its current ID from the MASTG site; never invent or reconstruct IDs (for example do not guess "MASTG-TEST-xxxx"). If you cannot look up an ID, cite the MASVS control and the weakness in words and write "MASTG test ID: not looked up".

## 4. Android platform and Play requirements (verify current)
- Google Play (as of Aug 31, 2026): new apps and updates must target Android 16 / API 36 or higher (Wear OS and Automotive: API 35; TV and XR: API 34). Existing apps need API 35+ to remain available to new users on newer Android versions. Not applicable to apps outside Play (sideload, EMM, private enterprise). Source: Play Console Help "Target API level requirements" and developer.android.com target-sdk page.
- Low `targetSdkVersion` means behavior protections (scoped storage, exported-component rules, background limits, cleartext default, PendingIntent mutability rules) may not apply. Treat low target SDK as a finding with context, and check minSdk against the supported-device rationale.
- Android 16 behavior changes, 16 KB page-size support for native libraries, Photo Picker, `dataExtractionRules`, predictive back: read the current Android developer docs for the target API level.
- Official security pages to consult: Android security best practices, security risks and mitigations, Network Security Configuration, app signing, Play Integrity API, Play App Signing, Play Data safety and User Data policies.
- Also verify versions of Android Gradle Plugin, Gradle, Kotlin, and detected SDKs from their official release notes.

## 5. Other references
Android Keystore docs, BiometricPrompt docs, Jetpack Security / Tink status, WebView security docs, Android App Links docs, OWASP ASVS and the `web-app-security` skill for backend, OWASP API Security Top 10, vendor SDK security notes.

## 6. Citation and compliance rules
- Record edition, scope, controls covered, exclusions, and evidence.
- "Assessed against MASVS v2.1.0 (STORAGE, NETWORK, PLATFORM) via MASTG v2.0.0 tests X, Y; RESILIENCE and PRIVACY not assessed."
- Never claim MASVS, GDPR, DPDP, PCI, or Play-policy compliance or approval. Technical controls may "support" a requirement; recommend legal/policy review for those questions.
