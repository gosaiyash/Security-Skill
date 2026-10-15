# android-apk-security

A portable Agent Skill for securing Android apps and running **authorized** assessments of source code, APK/AAB artifacts, controlled runtime behavior, and the client's view of its backend. It follows the open `SKILL.md` convention (YAML frontmatter + Markdown instructions + on-demand references), so it works in Claude Code and in other agents that read `SKILL.md` skills.

## What it does
- Secure Android development by default (components, PendingIntent, storage, Keystore, network, WebView, release hygiene).
- Static triage of APK/AAB without executing them; source audit; authorized emulator testing; client+backend review.
- Evidence-graded findings (Confirmed / Likely / Possible), explicit **Not tested** status, MASVS/MASWE/MASTG mapping without invented IDs.
- Safety: authorization gate, static-first, no real user data, no third-party protection bypass, no weakening release builds, prompt-injection resistance, no compliance claims.

## Layout
```
android-apk-security/
├── SKILL.md                         entry point: rules, modes, workflow, secure-by-default rules
├── references/                      11 on-demand guides (standards, intake, manifest, storage/crypto, network, auth, privacy, resilience, dynamic testing, tools, reporting)
├── templates/                       APK triage report, full assessment report, regression plan
├── scripts/apk_triage.py            read-only APK/AAB intake (never executes the artifact)
├── scripts/source_inventory.sh      read-only Android source discovery
├── scripts/validate_skill.py        package self-check
└── evals/behavior-evals.json        prompts with pass/fail expectations
```

## Install
- **Claude Code (all projects):** `mkdir -p ~/.claude/skills && cp -r android-apk-security ~/.claude/skills/`
- **Claude Code (one repo):** copy to `<repo>/.claude/skills/android-apk-security/`.
- **Claude.ai / Claude apps:** upload the zip in Skills settings if your plan allows custom skills.
- **Other agents:** place the folder where the agent loads skills or point its instructions at `SKILL.md`; check that agent's docs for the path.

## Use
Describe the task; the description triggers on Android security work. Examples:
- "Triage this APK (static only) and tell me what to look at."
- "Review this Android repo for security issues."
- "Check my AndroidManifest and network security config."
- "Is this WebView setup safe?"
- "Prepare a release-readiness security review."
- "Fix the findings and add regression tests."

## Validate
```bash
python3 scripts/validate_skill.py
python3 scripts/apk_triage.py path/to/app.apk
bash scripts/source_inventory.sh path/to/android/project
```
Then run the prompts in `evals/behavior-evals.json`.

## Maintenance
Re-verify `references/standards-and-frameworks.md` (MASVS/MASWE/MASTG editions, Play target API level, Android behavior changes) at least twice a year and before formal reports. Tool commands are examples; the skill tells agents to confirm syntax with `--help`.

## Limits
Guides an AI agent; does not replace a qualified mobile penetration test or compliance review. It never certifies compliance or Play approval. For the backend, use the companion `web-app-security` skill.
