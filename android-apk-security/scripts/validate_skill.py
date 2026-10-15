#!/usr/bin/env python3
"""Validate the android-apk-security skill package (stdlib only).
Usage: python3 scripts/validate_skill.py [skill_dir]"""
import re, sys
from pathlib import Path
root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
errors, warnings = [], []
REQUIRED = ["SKILL.md", "README.md"] + [f"references/{n}.md" for n in (
    "standards-and-frameworks", "apk-intake-and-triage", "android-manifest-and-components",
    "data-storage-and-cryptography", "network-and-api-security", "authentication-and-session-security",
    "privacy-and-permissions", "reverse-engineering-and-tamper-resistance", "dynamic-testing-workflow",
    "testing-tools", "remediation-and-reporting")] + [f"templates/{n}.md" for n in (
    "android-security-report", "apk-triage-report", "mobile-regression-plan")]
for rel in REQUIRED:
    if not (root / rel).is_file(): errors.append(f"missing required file: {rel}")
skill = root / "SKILL.md"
if skill.is_file():
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m: errors.append("SKILL.md: missing YAML frontmatter")
    else:
        fm = m.group(1)
        name = re.search(r"^name:\s*(.+)$", fm, re.M); desc = re.search(r"^description:\s*(.+)$", fm, re.M)
        if not name: errors.append("frontmatter: missing name")
        else:
            n = name.group(1).strip()
            if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", n) or len(n) > 64: errors.append(f"invalid name '{n}'")
            if n != root.name: warnings.append(f"name '{n}' differs from directory '{root.name}'")
        if not desc: errors.append("frontmatter: missing description")
        elif len(desc.group(1)) > 1024: errors.append(f"description {len(desc.group(1))} chars (max 1024)")
    if text.count("\n") > 500: warnings.append("SKILL.md exceeds 500 lines")
    for ref in set(re.findall(r"`((?:references|templates|scripts)/[A-Za-z0-9_./-]+)`", text)):
        if not (root / ref).exists(): errors.append(f"SKILL.md references missing path: {ref}")
for f in list(root.rglob("*.md")) + list(root.rglob("*.py")) + list(root.rglob("*.sh")):
    body = f.read_text(encoding="utf-8", errors="ignore")
    if re.search(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", body) or re.search(r"AKIA[0-9A-Z]{16}", body):
        errors.append(f"possible secret in {f.relative_to(root)}")
for e in errors: print("ERROR:", e)
for w in warnings: print("WARN: ", w)
print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
