# Reporting and remediation

## Contents
1. Finding format
2. Evidence rules
3. Remediation guidance
4. Regression tests
5. Verification and retest
6. Responsible disclosure
7. Incident support (mode I)

## 1. Finding format
```
ID: WAS-001
Title: <specific, e.g. "Invoice endpoint allows cross-tenant read (BOLA)">
Severity: High   Confidence: Confirmed | Likely | Possible   Status: Open
Component: <file:line, route, config key>
Weakness: CWE-639 (and CWE-862 where fitting)
Mapping: OWASP Top 10:2025 A01; ASVS 5.0.0 <chapter/requirement, confirmed>; API1:2023 (if API)
Description: <what is wrong and why, 2-4 sentences>
Impact: <who can do what to which data/function>
Evidence: <code excerpt (redacted), test output summary, safe request/response summary>
Reproduction (safe): <steps with test accounts / local environment>
Remediation: <specific fix, with minimal diff or pattern>
Regression test: <test name/location and what it asserts>
References: <official docs with edition>
```

## 2. Evidence rules
- Redact secrets and personal data in all excerpts. Use placeholders (`<redacted>`), never real values.
- Include enough to let a developer find and verify the issue; leave out weaponized payload chains, bulk data, and anything that works as a ready-made attack kit against third parties.
- Say how the evidence was obtained (static reading, local test, staging request). Include tool and version for automated results.
- Negative results are results: list controls that were checked and held.

## 3. Remediation guidance
- Root cause first; prevent the class (shared helper, framework setting, lint/Semgrep rule, base class with tenant scoping).
- Smallest change that meets the requirement and fits project style.
- Prefer deletion or reduction of attack surface (remove unused endpoints, disable debug) over adding checks.
- Backward compatibility: flag breaking changes (cookie flags, CORS, CSP, token formats, session invalidation) and propose staged rollout (report-only CSP first).
- Non-code actions to list explicitly: rotate secrets, revoke tokens, invalidate sessions, patch/upgrade, change cloud/IAM settings, notify affected parties per legal obligations (route to the user's security/legal contacts).
- Do not claim a fix works until a test or check shows it.

## 4. Regression tests
Use `templates/security-regression-plan.md`. Principles: test the security property, not the exact payload; include a negative test (attack denied) and a positive test (legitimate use still works); keep fixtures synthetic; run in CI; name tests so a future failure explains the risk (`test_user_cannot_read_other_tenants_invoice`).

## 5. Verification and retest
Re-run the original check against the fix, the full test suite, relevant scanners, and a search for sibling instances. Record before/after status. A finding is **Closed** only with evidence; otherwise **Fixed (unverified)**.

## 6. Responsible disclosure
For third-party or open-source vulnerabilities, follow the project's `SECURITY.md`/security contact; do not publish details before a fix is available; for the user's own product, recommend a `SECURITY.md` and `/.well-known/security.txt`.

## 7. Incident support (mode I)
Defensive and authorized only: analyze code, logs, and artifacts the user provides to identify likely entry point, scope, and affected data; recommend containment (rotate credentials, revoke sessions/tokens, isolate hosts, preserve logs and evidence before cleanup), eradication, recovery, and hardening. Do not access systems beyond the provided evidence, do not "hack back", and do not destroy evidence. Recommend engaging the organization's incident-response and legal contacts for notification duties. Timeline format: timestamp (UTC), source, event, confidence.
