# Infrastructure and deployment

## Contents
1. HTTP security headers
2. TLS
3. Reverse proxy and server hardening
4. Docker and containers
5. Kubernetes
6. IaC and cloud
7. CI/CD and supply chain
8. Secrets management
9. Databases and storage
10. Monitoring and incident readiness

## 1. HTTP security headers (verify on real responses; see OWASP Secure Headers Project)
| Header | Recommended starting point | Notes |
|---|---|---|
| `Content-Security-Policy` | `default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'` | Tune per app; prefer nonces or hashes over `'unsafe-inline'`; use report-only first |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Add `preload` only after confirming all subdomains support HTTPS |
| `X-Content-Type-Options` | `nosniff` | |
| `Referrer-Policy` | `strict-origin-when-cross-origin` or stricter | |
| `Permissions-Policy` | disable unused features (camera, microphone, geolocation) | |
| `X-Frame-Options` | `DENY` or `SAMEORIGIN` | Legacy; prefer CSP `frame-ancestors` |
| `Cross-Origin-Opener-Policy` / `Cross-Origin-Resource-Policy` | `same-origin` where compatible | Test cross-origin features |
| `Cache-Control` | `no-store` on sensitive responses | |
Do not rely on deprecated `X-XSS-Protection`. Remove or reduce `Server`/`X-Powered-By`.

## 2. TLS
TLS 1.2+ (prefer 1.3), strong cipher suites from a current recommended profile (e.g. Mozilla's server-side TLS guidelines), valid certificates with automated renewal, redirect HTTP to HTTPS, HSTS, OCSP stapling optional. Do not disable certificate verification in clients. Internal service traffic: mTLS or service mesh where the threat model warrants.

## 3. Reverse proxy and server hardening
Terminate TLS at a hardened proxy; set request size, header size, and timeout limits; restrict methods; hide internal paths and admin consoles; rate limit; run as non-root; separate public and admin listeners; keep OS, runtime, and web server patched. Align with the matching CIS Benchmark.

## 4. Docker and containers
- Minimal, pinned base images (by digest), multi-stage builds, no build tools or secrets in the final image.
- `USER` non-root; read-only root filesystem where possible; drop capabilities; no `--privileged`; no Docker socket mounts.
- No secrets in `ENV`, `ARG`, or image layers; use runtime secret injection or BuildKit secrets.
- `.dockerignore` excludes `.git`, `.env`, keys.
- Scan images (Trivy, Grype) and regenerate on base-image updates.

## 5. Kubernetes
Pod Security Standards (restricted), NetworkPolicies default-deny, RBAC least privilege, no `cluster-admin` for workloads, service-account token automount off unless needed, secrets via external secret store or encrypted at rest, resource limits, admission policies, and image provenance checks. Follow the CIS Kubernetes Benchmark for the exact version.

## 6. IaC and cloud
Scan Terraform/CloudFormation/Helm (Checkov, Trivy config, KICS). Check: public buckets/databases, `0.0.0.0/0` on admin ports, wildcard IAM (`*:*`), unencrypted storage, missing logging (CloudTrail/Audit Logs), long-lived access keys instead of roles/workload identity, metadata service hardening, separate accounts/projects per environment.

## 7. CI/CD and supply chain
- Least-privilege tokens (e.g. read-only default `permissions:` in GitHub Actions); scoped per job.
- Pin third-party actions/plugins to full commit SHAs; review before updating; limit which workflows run on forks and untrusted PRs; never expose secrets to untrusted PR code (`pull_request_target` risks).
- Protect main branches: required reviews, status checks, signed commits where practical; CODEOWNERS on security-sensitive paths and workflow files.
- Lockfiles, `npm ci`, hash-checked installs where practical, private registry/proxy; dependency update bots with review.
- Generate an SBOM (Syft, CycloneDX/SPDX tools); sign artifacts/images (Sigstore cosign) and verify before deploy for release-critical software; consider SLSA provenance levels.
- OpenSSF Scorecard for important dependencies and for the project itself.
- Separate build and deploy credentials; short-lived OIDC federation to cloud rather than stored keys.

## 8. Secrets management
Central secret store (cloud secrets manager, Vault, or platform equivalent); per-environment, per-service secrets; rotation schedule; audit access; secret scanning pre-commit and in CI; revoke on exposure; never share via chat/email/tickets. `.env.example` has placeholders only.

## 9. Databases and storage
Network-isolated, TLS enabled, least-privilege app accounts, no default accounts, encrypted at rest and backups, tested restores, row-level security where useful, audit logging for admin access, object storage private by default with short-lived signed URLs.

## 10. Monitoring and incident readiness
Centralized logs, alerts on auth anomalies and privilege changes, uptime and error monitoring, documented incident response with contacts, key-rotation runbooks, and a `SECURITY.md` / `security.txt` with a disclosure contact.
