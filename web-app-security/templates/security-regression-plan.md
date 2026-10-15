# Security Regression Plan: <application / change>

Goal: ensure each fixed or prevented vulnerability stays fixed.

| Finding / Threat | Security property | Negative test (attack denied) | Positive test (legit use works) | Test location | Runs in CI |
|---|---|---|---|---|---|
| WAS-001 cross-tenant read | User of tenant A cannot read tenant B invoice | A requests B's invoice ID -> 404/403 | A reads own invoice -> 200 | tests/security/test_invoices_authz.py | Yes |

## Test data rules
Synthetic users/tenants only; no real secrets; deterministic fixtures; cleanup after run.

## Standing suites to keep
- Authz matrix (role x endpoint x object ownership)
- Input validation boundaries (type, length, unknown fields)
- Auth/session (expiry, fixation, logout, reset token reuse)
- Headers/CORS/cookie flags on key responses
- SSRF/path traversal fixtures (local only)
- Dependency and secret scans in CI with fail thresholds
- Custom Semgrep/lint rules for repeated bug classes

## Exit criteria
All new tests pass; existing suite passes; scanners show no new high/critical; suppressions justified in code.
