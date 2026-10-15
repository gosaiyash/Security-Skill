#!/usr/bin/env python3
"""Validate the structure of the web-app-security skill. Standard library only.
Usage: python3 scripts/validate_skill.py [skill_dir]
Checks: frontmatter, name/dir match, description length, SKILL.md size, referenced files exist,
required files present, internal-link targets exist, and no obvious secrets in the package.
"""
import re, sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
errors, warnings = [], []

REQUIRED = [
    "SKILL.md", "README.md",
    "references/standards-and-frameworks.md", "references/threat-modeling.md",
    "references/security-checklist.md", "references/authentication-and-authorization.md",
    "references/api-security.md", "references/secure-coding-patterns.md",
    "references/infrastructure-and-deployment.md", "references/security-testing-tools.md",
    "references/vulnerability-severity.md", "references/reporting-and-remediation.md",
    "templates/security-assessment-report.md", "templates/threat-model.md",
    "templates/security-regression-plan.md",
]
for rel in REQUIRED:
    if not (root / rel).is_file():
        errors.append(f"missing required file: {rel}")

skill = root / "SKILL.md"
if skill.is_file():
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append("SKILL.md: missing YAML frontmatter")
    else:
        fm = m.group(1)
        name = re.search(r"^name:\s*(.+)$", fm, re.M)
        desc = re.search(r"^description:\s*(.+)$", fm, re.M)
        if not name: errors.append("frontmatter: missing name")
        else:
            n = name.group(1).strip()
            if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", n) or len(n) > 64:
                errors.append(f"frontmatter: invalid name '{n}'")
            if n != root.name:
                warnings.append(f"name '{n}' differs from directory '{root.name}' (some agents require a match)")
        if not desc: errors.append("frontmatter: missing description")
        elif len(desc.group(1)) > 1024:
            errors.append(f"description is {len(desc.group(1))} chars (max 1024)")
    lines = text.count("\n")
    if lines > 500: warnings.append(f"SKILL.md has {lines} lines (>500; move detail to references)")
    for ref in set(re.findall(r"`((?:references|templates|scripts)/[A-Za-z0-9_./-]+)`", text)):
        if not (root / ref).exists():
            errors.append(f"SKILL.md references missing path: {ref}")

for md in list(root.rglob("*.md")) + list(root.rglob("*.py")) + list(root.rglob("*.sh")):
    body = md.read_text(encoding="utf-8", errors="ignore")
    if re.search(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", body) or re.search(r"AKIA[0-9A-Z]{16}", body):
        errors.append(f"possible secret in {md.relative_to(root)}")

for e in errors: print("ERROR:", e)
for w in warnings: print("WARN: ", w)
print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
