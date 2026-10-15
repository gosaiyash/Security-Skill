#!/usr/bin/env bash
# Read-only Android source discovery. No network, no execution of project code, no secret values printed.
# Usage: scripts/source_inventory.sh [project_dir]
set -u
ROOT="${1:-.}"
cd "$ROOT" || { echo "cannot cd to $ROOT" >&2; exit 1; }
X='-not -path */build/* -not -path */.git/* -not -path */.gradle/* -not -path */node_modules/*'
section() { printf '\n== %s ==\n' "$1"; }
found() { find . -type f $X \( "$@" \) 2>/dev/null | head -60; }
count() { n=$(grep -rEIl --exclude-dir=build --exclude-dir=.git --exclude-dir=.gradle --exclude-dir=node_modules -e "$2" . 2>/dev/null | wc -l); printf '%-38s %s file(s)\n' "$1" "$n"; }

section "Build and config files"
found -name 'build.gradle*' -o -name 'settings.gradle*' -o -name 'gradle.properties' -o -name 'libs.versions.toml' -o -name 'proguard*.pro' -o -name 'pubspec.yaml' -o -name 'package.json'
section "Manifests (check merged manifest per variant too)"
found -name AndroidManifest.xml
section "Network security config / backup rules / file provider paths"
found -path '*/res/xml/*' \( -name '*network*security*' -o -name '*backup*' -o -name '*data_extraction*' -o -name '*file_paths*' -o -name '*provider_paths*' \)
section "Signing, keystores, secrets-like files (names only)"
found -name '*.jks' -o -name '*.keystore' -o -name 'keystore.properties' -o -name 'google-services.json' -o -name '.env*' -o -name '*.pem' -o -name '*.p12'
section "Tests and security tooling present"
found -path '*/androidTest/*' -o -path '*/src/test/*' -o -name 'lint.xml' -o -name '.semgrep*' -o -name '.gitleaks*' -o -name 'dependabot.yml' -o -name 'renovate.json' | head -20

section "Manifest-level indicators (file counts)"
count "debuggable true"               'android:debuggable="true"'
count "allowBackup true"              'android:allowBackup="true"'
count "usesCleartextTraffic true"     'usesCleartextTraffic="true"'
count "exported true"                 'android:exported="true"'
count "intent-filter (deep links etc)" '<intent-filter'
count "testOnly"                      'android:testOnly'
count "dangerous perms (SMS/contacts/loc)" 'READ_SMS|READ_CONTACTS|ACCESS_FINE_LOCATION|MANAGE_EXTERNAL_STORAGE|QUERY_ALL_PACKAGES|SYSTEM_ALERT_WINDOW'

section "Code-level leads (file counts; confirm manually)"
count "WebView JS / bridge"           'setJavaScriptEnabled|addJavascriptInterface|setAllowUniversalAccessFromFileURLs|setAllowFileAccess'
count "SSL/trust bypass patterns"     'onReceivedSslError|X509TrustManager|HostnameVerifier|checkServerTrusted|badCertificateCallback|CURLOPT_SSL_VERIFYPEER'
count "PendingIntent (check IMMUTABLE)" 'PendingIntent\.get'
count "SharedPreferences/DataStore use" 'getSharedPreferences|PreferenceManager|DataStore'
count "Keystore/crypto APIs"          'AndroidKeyStore|KeyGenParameterSpec|Cipher\.getInstance|SecureRandom|Tink'
count "Weak crypto leads"             'MessageDigest\.getInstance\("(MD5|SHA-?1)"\)|"AES/ECB|DES|java\.util\.Random|Math\.random'
count "Logging calls"                 'Log\.[dviwe]\(|Timber\.'
count "Raw SQL / provider query"      'rawQuery|execSQL|SQLiteDatabase|ContentProvider'
count "Reflection / dynamic loading"  'Class\.forName|DexClassLoader|PathClassLoader|System\.loadLibrary|Runtime\.exec'
count "External storage"              'getExternalStorage|getExternalFilesDir|MediaStore|WRITE_EXTERNAL_STORAGE'
count "HTTP URLs"                     'http://'
count "Possible hard-coded secrets"   '(api[_-]?key|secret|passwd|password|token)[\"'\'' ]*[:=][\"'\'' ]*[A-Za-z0-9/+_-]{12,}'
printf '\nDone. Counts are leads, not findings. Mark uninspected areas as NOT TESTED.\n'
