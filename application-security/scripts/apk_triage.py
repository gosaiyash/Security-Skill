#!/usr/bin/env python3
"""Read-only APK/AAB intake. NEVER executes the artifact.
Standard library only; optionally calls `aapt2` and `apksigner` (argument lists, no shell) if on PATH.
Usage: python3 scripts/apk_triage.py <file.apk|file.aab|file.apks|file.xapk>
Prints identity, container layout, framework indicators, and tool output. Values are leads, not findings.
"""
import hashlib, re, shutil, subprocess, sys, zipfile
from pathlib import Path

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def run(cmd, limit=60):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        lines = (out.stdout or out.stderr).splitlines()
        return lines[:limit] + ([f"... ({len(lines)-limit} more lines)"] if len(lines) > limit else [])
    except Exception as e:  # tool missing or failed
        return [f"(failed: {e})"]

def main():
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(2)
    p = Path(sys.argv[1])
    if not p.is_file():
        print(f"not a file: {p}"); sys.exit(1)
    print(f"File: {p.name}\nSize: {p.stat().st_size} bytes\nSHA-256: {sha256(p)}")
    if not zipfile.is_zipfile(p):
        print("Not a ZIP container: unsupported or corrupt. Stop and report."); sys.exit(1)
    z = zipfile.ZipFile(p)
    names = z.namelist()
    ext = p.suffix.lower()
    print(f"Extension: {ext}  Entries: {len(names)}")

    inner = [n for n in names if n.lower().endswith(".apk")]
    if ext in (".apks", ".xapk", ".apkm") or inner:
        print(f"Split/bundle archive; contained APKs ({len(inner)}):")
        for n in inner[:40]: print("  -", n)
        print("Triage each APK separately (extract to a scratch dir). Not executed.")
    if ext == ".aab" or "BundleConfig.pb" in names:
        print("Android App Bundle: publishing format, not installable. Analyze device-specific APKs or the bundle structure.")

    dex = sorted(n for n in names if re.fullmatch(r"(base/dex/)?classes\d*\.dex", n))
    abis = sorted({n.split("/")[1] for n in names if n.startswith("lib/") and n.count("/") >= 2})
    sigs = [n for n in names if n.startswith("META-INF/") and n.lower().endswith((".rsa", ".dsa", ".ec", ".sf", ".mf"))]
    print(f"\nManifest present: {'AndroidManifest.xml' in names or 'base/manifest/AndroidManifest.xml' in names}")
    print(f"DEX files: {len(dex)}  Native ABIs: {abis or 'none'}")
    print(f"v1 signature files in META-INF: {len(sigs)} (v2+ signatures live in the signing block; use apksigner)")

    ind = {
        "Kotlin": any(n.startswith("kotlin/") or n.endswith(".kotlin_module") for n in names),
        "Flutter": any("libflutter.so" in n or "flutter_assets" in n for n in names),
        "React Native": any("libreactnativejni.so" in n or "index.android.bundle" in n for n in names),
        "Xamarin/.NET MAUI": any("libmonodroid.so" in n or "assemblies/" in n for n in names),
        "Unity": any("libunity.so" in n or "unity" in n.lower() and n.startswith("assets/bin/Data") for n in names),
        "Cordova/Capacitor": any(n.startswith("assets/www/") or n.startswith("assets/public/") for n in names),
        "Native libs (JNI/NDK)": bool(abis),
    }
    print("Framework indicators:", ", ".join(k for k, v in ind.items() if v) or "none detected")
    suspicious = [n for n in names if re.search(r"(debug|test|\.keystore|\.jks|\.pem|\.p12|\.env|id_rsa|google-services\.json|firebase)", n, re.I)]
    if suspicious:
        print("\nFiles worth a look (names only; contents not read):")
        for n in suspicious[:40]: print("  -", n)

    aapt2 = shutil.which("aapt2")
    if aapt2 and ext == ".apk":
        print("\n--- aapt2 dump badging (first lines) ---")
        print("\n".join(run([aapt2, "dump", "badging", str(p)])))
    else:
        print("\n(aapt2 not used: not on PATH or not an .apk)")
    apksigner = shutil.which("apksigner")
    if apksigner and ext == ".apk":
        print("\n--- apksigner verify ---")
        print("\n".join(run([apksigner, "verify", "--verbose", "--print-certs", str(p)])))
    else:
        print("(apksigner not used: not on PATH or not an .apk)")
    print("\nNext: record scope/authorization, review manifest and components, decide on deeper analysis. Binary-only: server-side behavior is NOT verified.")

if __name__ == "__main__":
    main()
