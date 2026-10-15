# API security

## Contents
1. OWASP API Security Top 10 (2023) checklist
2. REST
3. GraphQL
4. gRPC and WebSocket
5. Webhooks and callbacks
6. Inventory and versioning
7. LLM/agent tool APIs
8. Tests to add

## 1. OWASP API Security Top 10 (2023)
| ID | Risk | What to check |
|---|---|---|
| API1 | Broken Object Level Authorization | every object ID access checks ownership/tenant; list endpoints filter by caller |
| API2 | Broken Authentication | token validation, rate limits on auth, no weak/default keys, no credentials in URLs |
| API3 | Broken Object Property Level Authorization | response filtering (excessive data exposure) and write allowlists (mass assignment) |
| API4 | Unrestricted Resource Consumption | size/rate/pagination/timeouts/batching limits, cost controls for paid backends |
| API5 | Broken Function Level Authorization | admin/privileged methods and paths, HTTP method confusion (e.g. PUT/DELETE exposed) |
| API6 | Unrestricted Access to Sensitive Business Flows | bot/abuse limits on signup, purchase, reservation, referral, scraping |
| API7 | Server Side Request Forgery | any user-supplied URL fetched by the server |
| API8 | Security Misconfiguration | CORS, TLS, verbose errors, missing headers, unneeded features/methods |
| API9 | Improper Inventory Management | old versions, shadow/debug/internal endpoints, undocumented routes, stale docs |
| API10 | Unsafe Consumption of APIs | trust placed in third-party API responses; validate, limit, timeout, TLS-verify |

Check the OWASP API Security project page for a newer edition before citing.

## 2. REST
- Strict content types; reject unexpected `Content-Type`; JSON schema validation; size limits.
- Use correct HTTP methods; safe methods do not change state.
- Consistent, minimal error bodies; no stack traces, SQL, or internal hostnames.
- Pagination with max page size; filter/sort parameters allowlisted.
- Idempotency keys for payments and other retry-prone writes.
- Do not put secrets or tokens in query strings.
- CORS: explicit origin allowlist; no wildcard with credentials; limit methods/headers.

## 3. GraphQL
- Disable introspection and GraphiQL/Playground in production unless intentionally public.
- Limit query depth, complexity/cost, alias count, and batch size; set timeouts; persist/allowlist queries for high-risk apps.
- Authorization in resolvers/data layer per field and object, not only at the top-level query. Guard against N+1 data leakage via nested relations.
- Rate limit by cost, not just by request count. Disable field suggestions if they leak schema.
- Validate variables and custom scalars; beware batching used to bypass brute-force limits.

## 4. gRPC and WebSocket
- gRPC: TLS/mTLS, per-method authz interceptors, message size limits, deadlines, reflection disabled in production.
- WebSocket: authenticate at handshake, validate `Origin` (cross-site WebSocket hijacking), re-check authorization per message/subscription, limit frame size and message rate, avoid putting tokens in URLs where logging captures them.

## 5. Webhooks and callbacks
- Verify signatures (HMAC or provider-specified) with constant-time comparison; include timestamp and reject stale requests; use replay protection (event ID store).
- Fetch the authoritative state from the provider instead of trusting the payload where possible.
- Outbound webhooks (you call customer URLs): SSRF controls, timeouts, no redirects into private ranges, per-tenant secrets.
- Callback/redirect URIs allowlisted.

## 6. Inventory and versioning
- Maintain an authoritative OpenAPI/GraphQL schema or route list; diff against what is actually deployed.
- Retire old versions; apply the same authz and security fixes across versions.
- Separate internal from public APIs at the network layer.

## 7. LLM and agent tool APIs
- Treat model output as untrusted: validate tool arguments against schemas, never pass raw model text to shells, SQL, or HTML.
- Give agents least-privilege, scoped, short-lived credentials; per-user authorization applies to every tool call (the model is not an authorization boundary).
- Require human confirmation for destructive, financial, or external-communication actions.
- Separate trusted instructions from untrusted retrieved content; assume retrieved documents and web pages may carry prompt injection; block exfiltration channels (arbitrary URL rendering, markdown images to attacker hosts).
- Rate-limit and budget-limit model calls; log tool calls with user and request IDs without storing secrets.
- Consult the OWASP Top 10 for LLM Applications (check current edition).

## 8. Tests to add
- BOLA matrix: each object endpoint x (owner, other user, other tenant, anonymous).
- BFLA: low-privilege token on every admin route and method.
- Over-posting and over-fetching tests per resource.
- Oversized body, deep nesting, huge page size, expensive query rejected.
- Webhook with bad signature, stale timestamp, replayed ID rejected.
- SSRF: internal IPs, metadata IPs, redirects, DNS rebinding style hostnames rejected (use local fixtures, not real internal systems).
