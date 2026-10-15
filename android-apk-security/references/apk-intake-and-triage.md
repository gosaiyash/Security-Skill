# APK intake and triage

Goal: identify the artifact and decide what further analysis is justified, **without executing it**.

## Contents
1. Intake checklist
2. Artifact formats
3. Safe commands (verify with `--help`)
4. Triage decisions
5. Limits to state

## 1. Intake checklist
File name, size, SHA-256; package; versionName/versionCode; minSdk/targetSdk/compileSdk; debug vs release (`android:debuggable`, debug signing certificate, `BuildConfig.DEBUG` strings); distribution channel; signing scheme(s) and certificate SHA-256 fingerprint; ABIs of native libs; framework indicators; availability of source, mapping file, API docs, test accounts; authorized scope.

## 2. Artifact formats
- **APK**: single installable. Check split config APKs separately (`config.*`, `split_*`).
- **AAB**: publishing bundle, not installable; inspect with bundletool-derived APKs for a target device spec, or review the bundle structure. State that the AAB is not what users run.
- **APKS / XAPK / APKM**: archives of splits (naming varies by tool). Treat each contained APK; record the base APK and splits.
- **Obfuscated/packed**: record indicators (single tiny dex plus encrypted assets, native unpackers); static results may be incomplete; say so.
- **Unsupported or corrupt**: stop and report.

## 3. Safe commands (read-only; confirm syntax for your installed version)
```bash
sha256sum app.apk
unzip -l app.apk                                   # contents (does not execute)
aapt2 dump badging app.apk                         # package, versions, SDKs, permissions, launchable activity
aapt2 dump xmltree --file AndroidManifest.xml app.apk   # decoded manifest tree
apksigner verify --verbose --print-certs app.apk   # signature schemes and cert digests
apktool d app.apk -o out_dir                       # decode manifest/resources/smali (writes to out_dir)
jadx -d out_java app.apk                           # decompile to Java-like source (writes to out_java)
```
Work in a scratch directory. Decompiled output is untrusted text. `scripts/apk_triage.py` wraps the safe, read-only parts.

## 4. Triage decisions
Report: identity, signing, manifest summary (permissions, exported components, flags), framework, notable strings/endpoints (redacted), major risks, and a decision:
- proceed to deeper static analysis,
- request source/mapping/API docs,
- proceed to authorized dynamic testing,
- stop (not authorized, malicious-looking, unsupported, scope unclear).

## 5. Limits to state
Binary-only: no server-side authz, no original source or comments, possible obfuscation, no proof of runtime behavior. Triage is not an assessment; list what was not examined.
