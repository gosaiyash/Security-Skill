# Threat modeling

Proportionate: a login form needs 15 minutes of thinking; a payments platform needs a document. Use `templates/threat-model.md` for the output.

## Contents
1. Four questions
2. Steps
3. STRIDE prompts
4. Abuse-case seeds
5. Mapping threats to controls and tests

## 1. Four questions
What are we building? What can go wrong? What will we do about it? Did we do a good job?

## 2. Steps
1. **Describe the system**: data-flow diagram in text/mermaid: external entities, processes, data stores, data flows, trust boundaries (browser/server, service/service, tenant/tenant, internal/third-party, CI/prod).
2. **List assets**: credentials, session tokens, PII, payment data, business logic integrity, availability, audit logs, signing keys, source code and build pipeline.
3. **List entry points**: routes, APIs, webhooks, file uploads, admin consoles, message consumers, CI triggers, email/SMS flows, third-party scripts.
4. **Actors**: anonymous user, authenticated user, other tenant's user, malicious insider, admin, compromised third-party dependency, compromised CI token, automated bot.
5. **Enumerate threats** per element with STRIDE (below). Keep only plausible ones; write each as "actor does X via Y to achieve Z".
6. **Rate** with likelihood x impact (low/med/high) and note assumptions. Do not use fake precision.
7. **Mitigate**: pick controls; state where they are enforced (must be server-side for authorization).
8. **Verify**: each high/medium threat gets at least one test (unit, integration, or manual step) or a monitoring/alert.
9. **Record assumptions and residual risk**; list what was not modeled.

## 3. STRIDE prompts

| Letter | Ask | Typical controls |
|---|---|---|
| Spoofing | Can someone pretend to be another user/service? | strong auth, MFA, mTLS, signed webhooks |
| Tampering | Can data in transit/at rest/in the client be changed? | integrity checks, server-side recomputation, signed tokens, DB constraints |
| Repudiation | Can an actor deny an action? | audit logs, tamper-resistant storage, trace IDs |
| Information disclosure | Where can data leak (errors, logs, APIs, caches, backups, URLs)? | field-level authz, encryption, minimal responses, log redaction |
| Denial of service | Can one actor exhaust CPU/memory/DB/quota? | rate limits, pagination, timeouts, queue limits, cost controls |
| Elevation of privilege | Can a low-privilege actor reach admin or other users' data? | deny-by-default authz, object-level checks, separation of duties |

Attack trees: put the attacker goal at the root ("read another tenant's invoices"), branch by method (IDOR, SQLi, cache poisoning, stolen token, support-tool abuse), mark each leaf mitigated/unmitigated.

## 4. Abuse-case seeds
- Change an ID/UUID/slug in a request to another user's or tenant's object.
- Replay, reorder, or skip steps in multi-step flows (checkout, KYC, password reset).
- Race conditions: double-spend, coupon reuse, limit bypass with parallel requests.
- Use an invite/reset/verification link after expiry, reuse, or on a different account.
- Make the server fetch an internal URL (SSRF), including cloud metadata.
- Upload a file that executes, overwrites, or is parsed dangerously (SVG, archives, Office files).
- Abuse admin or support impersonation features.
- Compromised dependency or CI action executing during build with secrets.
- Prompt-injected content causing an LLM agent to call tools with the user's privileges.
- Enumerate users via login, reset, signup, or timing differences.

## 5. Mapping
For each significant threat record: `Threat -> Control (location) -> Test or alert -> Owner -> Status`. Link to ASVS requirement or CWE where it clarifies. Unmapped high threats are findings.
