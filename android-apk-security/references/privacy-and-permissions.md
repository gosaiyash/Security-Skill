# Privacy, permissions, and third-party SDKs

MASVS-PRIVACY and parts of PLATFORM/CODE. Technical findings here are separate from legal or store-policy conclusions.

## Contents
1. Data minimization and permissions
2. SDK review
3. Identifiers and tracking
4. Consent, transparency, user control
5. Policy and legal boundary
6. Evidence methods
7. Tests

## 1. Data minimization and permissions
For each permission and each data collection point: purpose, necessity, timing (in-context request), alternatives (photo picker, approximate location, one-time grant, foreground-only), behavior when denied or revoked, and retention. Remove unused permissions contributed by libraries via manifest merge rules (`tools:node="remove"`), with testing.

## 2. SDK review
Inventory SDKs from Gradle dependency reports, manifests, and decompiled packages: analytics, crash reporting, ads, attribution, social login, payments, maps, push, A/B testing, customer support chat. For each: what data it can access (permissions, device IDs, location, contacts), what it transmits (evidence: SDK docs, code, or authorized network capture with test data), retention/sharing per the vendor's documentation, version and known vulnerabilities, default settings (for example advertising ID collection, auto-collection toggles), and whether it can be disabled or limited. State uncertainty when only inferred.

## 3. Identifiers and tracking
Advertising ID, Android ID, instance IDs, hardware/serial identifiers, IMEI-like data (restricted on modern Android), fingerprinting via device properties, persistent identifiers surviving reinstall, linking pseudonymous and real identity. Prefer resettable, app-scoped identifiers.

## 4. Consent, transparency, user control
Consent before collection where required, accurate in-app disclosures and store listings, working opt-out/delete flows (including server-side deletion), account deletion path, children's data handling where relevant. Compare actual behavior with the Play Data safety declaration and privacy policy; report mismatches as factual discrepancies for the owner to resolve.

## 5. Policy and legal boundary
Google Play policy (User Data, Permissions, Data safety, Target API) changes often: fetch the current official text before stating a requirement. Do not state legal compliance (GDPR, India DPDP Act, CCPA, COPPA, HIPAA) or guarantee Play approval. Flag items for legal/policy review.

## 6. Evidence methods
Static: manifest merge, dependency list, string/endpoint search, SDK config files. Dynamic (authorized, test data only): capture traffic metadata on an emulator and list destinations and field names, not real values. Never inspect real user traffic.

## 7. Tests
Manifest test that disallowed permissions are absent; CI check that new dependencies trigger SDK review; instrumented test for permission-denied paths; checks that analytics are disabled before consent where required.
