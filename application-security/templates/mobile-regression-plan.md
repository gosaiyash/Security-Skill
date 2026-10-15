# Mobile Security Regression Plan: <app / change>

| Finding | Security property | Negative test | Positive test | Type | Location | In CI |
|---|---|---|---|---|---|---|
| APK-001 | exported activity rejects crafted intent | harness sends malicious extra -> no privileged action | valid internal launch works | instrumented | androidTest/... | yes |

## Standing checks
- Merged-manifest diff: new permissions, exported components, debuggable/allowBackup changes require review.
- Release config: `debuggable=false`, NSC cleartext blocked, no debug overrides, R8 enabled.
- Storage: no plaintext synthetic token after login; logout clears data; backup rules exclude sensitive paths.
- WebView: JS/bridge/file-access settings asserted; navigation allowlist tested.
- Deep links: unauthenticated launch cannot reach protected screens; parameters validated.
- Dependencies and secrets: scans in CI with fail thresholds.
- Backend (authorized): cross-user access denied, tampered client values ignored.

## Rules
Synthetic data only; deterministic fixtures; no real secrets; tests must fail before the fix and pass after.

## Exit criteria
All new tests pass; existing suite passes; no new High/Critical from scanners; retest evidence recorded.
