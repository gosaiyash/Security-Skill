# Remediation and reporting

## Contents
1. Finding format
2. Severity guidance
3. Evidence rules
4. Remediation workflow
5. Regression tests
6. Report types
7. Wording rules

## 1. Finding format
```
ID: APK-001
Title: <specific, e.g. "Exported activity launches arbitrary intents (intent redirection)">
Severity: High    Confidence: Confirmed | Likely | Possible    Status: Open
Artifact: <package> <versionName> (<versionCode>) SHA-256 <hash prefix>
Assessment type: source | binary-only | runtime | client+backend
Component: <manifest entry, class, file:line, config key>
Mappings: MASVS-<CAT>-<n>; MASWE-<id> (looked up); MASTG test <id or "not looked up">; CWE-<id>
Preconditions: <who/what is needed>
Expected vs observed: ...
Impact: <realistic>
Evidence: <sanitized excerpt / test result / authorized runtime observation>
Reproduction (safe): <steps, test accounts, synthetic data>
Root cause: ...
Remediation: <smallest correct fix, official guidance reference>
Regression test: <location and assertion>
Retest result: <Closed with evidence | Fixed (unverified) | Not retested - reason>
Limitations / residual risk: ...
```
Separate: **Confirmed vulnerabilities**, **Suspected issues**, **Hardening opportunities**, **Unverified hypotheses**. Missing test capability = **Not tested**.

## 2. Severity guidance (Critical / High / Medium / Low / Informational)
Severity = realistic impact x realistic likelihood in this app and its distribution. Use CVSS (state v4.0 or v3.1 and the vector) only if required; Android attack vectors are often "local" or "adjacent app" and user-interaction dependent, so explain context adjustments.
- Critical: true server secret or signing material in the artifact; remote unauthenticated account takeover; client-trusted authorization allowing mass data access.
- High: exported component leaking tokens/PII or enabling arbitrary file read/write to other apps; TLS validation disabled in release; auth bypass via deep link; plaintext long-lived tokens plus backup exposure; WebView bridge reachable from untrusted content.
- Medium: cleartext exceptions for sensitive domains; missing PendingIntent immutability with exploitable redirect; sensitive data in logs on release; over-broad permissions with data exposure risk; vulnerable dependency with reachable path.
- Low: unrestricted public API key, minor info leaks, missing hardening without demonstrated path.
- Informational: best-practice deviations, resilience gaps without threat-model justification.
Raise for sensitive data, easy reliable exploitation, no compensating controls; lower for needing physical access, rooted device only, unlikely user interaction, strong verified mitigations. Explain each adjustment.

## 3. Evidence rules
Sanitized test data only; redact secrets and personal data; include enough for a developer to verify; leave out weaponized exploit chains. State how evidence was obtained (static, authorized runtime, backend test) and tool versions.

## 4. Remediation workflow
1. Root cause. 2. Smallest correct fix matching project conventions and current official Android guidance. 3. Fix the class where possible (shared helper, lint rule, manifest check). 4. Add regression test. 5. Rebuild if source is available and inspect the merged manifest and release configuration. 6. Re-run relevant safe checks (and dynamic ones if authorized). 7. Record what could not be retested. Do not silently change signing keys, production endpoints, backend data, release settings, or permissions without explicit authorization. List non-code actions: rotate secrets, revoke tokens, update backend rules, update Data safety form, legal review.

## 5. Regression tests (see templates/mobile-regression-plan.md)
Test the property, not the payload: instrumented tests for exported components (crafted intents denied), storage (no plaintext token), NSC/release config (cleartext blocked, no debug overrides), WebView settings, deep-link validation, logout cleanup; unit tests for validators and token handling; CI checks for manifest diffs and secrets; backend tests for authorization. Keep fixtures synthetic.

## 6. Report types
- **APK triage report** (`templates/apk-triage-report.md`): identity, signing, manifest summary, major risks, further-analysis decision.
- **Full security assessment** (`templates/android-security-report.md`): scope, method, environment, standards, findings, evidence, remediation, limitations.
- **Release readiness**: unresolved high-priority risks, signing and configuration status, test coverage, known limitations, recommendation (go / go with conditions / no-go) with reasons.
- **Developer remediation report**: prioritized fixes, affected files/components, implementation guidance, verification tests.

## 7. Wording rules
Never write "secure", "compliant", "approved by Play", or "complete coverage". Use "no issues found in the areas tested" with the list. Distinguish what is true of the artifact from what depends on the backend. Report absences as "not observed in X" with the method.
