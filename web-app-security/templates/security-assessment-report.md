# Security Assessment Report: <application>

| Field | Value |
|---|---|
| Date | <YYYY-MM-DD> |
| Assessor / agent | <name, model> |
| Version / commit assessed | <hash/tag> |
| Mode(s) | <A-I> |
| Environment | <local / staging / production (read-only)> |
| Authorization | <who authorized, scope statement> |

## 1. Executive summary
<3-6 sentences: overall posture, number of findings by severity, top risks, top next steps. No "secure"/"compliant" claims.>

## 2. Scope and method
- In scope: <components, repos, URLs>
- Out of scope / excluded: <list>
- Not inspected (unknown): <list>
- Methods: <code review, threat model, SAST/SCA/secrets, local dynamic tests, config review>
- Tools and versions: <list>
- Standards referenced (edition, scope): <e.g. OWASP Top 10:2025; ASVS 5.0.0 L2, chapters V6-V8; API Top 10:2023>

## 3. Architecture and attack-surface summary
<components, trust boundaries, entry points, data classes. Mark evidence-based vs assumed.>

## 4. Findings summary
| ID | Title | Severity | Confidence | Status |
|---|---|---|---|---|

## 5. Detailed findings
<one block per finding in the format from references/reporting-and-remediation.md>

## 6. Controls verified (what held up)
<checklist items marked Pass with evidence>

## 7. Checklist coverage
| Area | Pass | Fail | Partial | N/A | Unknown |
|---|---|---|---|---|---|

## 8. Fixes applied and tests added
<commit/PR refs, test names, before/after>

## 9. Residual risks and manual actions
<rotate secrets, config changes, accepted risks with owner/date>

## 10. Recommended roadmap
- Immediate (days): 
- Short term (weeks): 
- Longer term: 

## 11. Limitations
<time-boxed, partial coverage, automated-tool limits, no dynamic testing if passive mode, etc.>

## Appendix: evidence index (redacted)
