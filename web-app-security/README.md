# web-app-security

A portable Agent Skill that makes an AI coding agent build web applications securely and assess, fix, and regression-test existing ones. It follows the open `SKILL.md` convention (YAML frontmatter + Markdown instructions + on-demand references), so it works in Claude Code and in other agents that read `SKILL.md` skills.

## What it does
- **Secure development**: applies server-side authorization, injection-safe patterns, safe auth/session/crypto/secrets handling by default whenever web code is written.
- **Security assessment**: scoped discovery, proportionate threat modeling, checklist-driven review, safe validation, evidence-graded findings (Confirmed / Likely / Possible).
- **Remediation**: root-cause fixes plus regression tests, retest, and professional reports.
- **Safety**: authorization gate, passive-mode fallback, no secret leakage, prompt-injection resistance, no destructive testing, no compliance overclaiming.

## Layout
```
web-app-security/
├── SKILL.md                      entry point: rules, modes, workflow, secure-by-default rules
├── references/                   loaded on demand (standards, checklist, auth, API, patterns, infra, tools, severity, reporting)
├── templates/                    report, threat model, regression plan
├── scripts/inventory.sh          read-only repo discovery (no network, no secret values)
├── scripts/validate_skill.py     package self-check (stdlib only)
└── evals/behavior-evals.json     prompts + pass/fail expectations for testing the skill
```

## Install
**Claude Code (personal, all projects):**
```bash
mkdir -p ~/.claude/skills && cp -r web-app-security ~/.claude/skills/
```
**Claude Code (one project, shared via git):** copy to `<repo>/.claude/skills/web-app-security/`.
**Claude.ai / Claude apps:** upload the `.zip` through the Skills settings if your plan allows custom skills.
**Other agents** (Google Antigravity, Codex-style agents, etc.): place the folder where that agent loads skills, or point its instructions at `SKILL.md`. Check that agent's docs for the exact skills directory, since locations differ and change.

## Use
Invoke by describing the task; the description triggers on security-related work. Examples:
- "Do a security audit of this repo, local only."
- "Review this PR for security issues."
- "Add login and password reset with secure defaults."
- "Threat model the new file-upload feature."
- "Fix the findings in report.md and add regression tests."
For Claude Code you can also say "use the web-app-security skill".

## Validate
```bash
python3 scripts/validate_skill.py
bash scripts/inventory.sh /path/to/project
```
Then run the prompts in `evals/behavior-evals.json` with the skill installed and grade the answers.

## Maintenance
Standards change. Re-verify `references/standards-and-frameworks.md` (editions, drafts vs final) at least twice a year and before any formal report. Tool flags in `security-testing-tools.md` are examples; the skill instructs agents to confirm flags with `--help`.

## Limits
This skill guides an AI agent; it does not replace a qualified security review, penetration test, or compliance audit for high-risk systems. It never certifies compliance.
