# Data Storage and Cryptography (Server, Cloud, and Mobile Client)

Governed by **ASVS Chapter V6 / V7 / V8** and **MASVS-STORAGE / MASVS-CRYPTO**.
Base decisions on threat modeling: classify data sensitivity, determine who has access (internal services, DB admins, rogue apps, physical device possessors, root users), and define the data retention lifecycle.

---

## 1. Sensitive Data Classification & Lifecycle

| Data Tier | Examples | Storage Location | Protection Controls |
|---|---|---|---|
| **Tier 1: Master Secrets** | Database passwords, signing private keys, API secrets, JWT signing keys. | Cloud Secrets Manager (AWS/GCP/Vault) or Hardware Keystore. | Never in code/git; hardware-backed or KMS-encrypted; rotated regularly; access audited. |
| **Tier 2: User Auth & PII** | Passwords, refresh tokens, SSNs, credit cards, health records. | Database (encrypted columns), App-Private Storage (`no_backup`). | Passwords hashed with Argon2id; tokens/PII encrypted with AEAD; excluded from backups; cleared on logout. |
| **Tier 3: Session State & Cache** | Short-lived access tokens, cached user profile, cart state. | Memory / Redis (TLS), App Cache / SQLite. | Scoped TTL; encrypted in transit; wiped on logout/session expiry. |
| **Tier 4: Public Data** | Static assets, public catalog, Maps API key (restricted). | Public CDN, Client assets, Scoped Storage. | Domain or app-signature restrictions applied on cloud console. |

---

## 2. Server-Side Data Storage & Secrets Management

- **No Secrets in Source**: Never hardcode API keys, database credentials, encryption keys, or private keys in source code, configuration files, Dockerfiles, or CI workflows.
- **Environment & Secrets Managers**: Inject secrets at runtime via environment variables loaded from dedicated secret stores (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, HashiCorp Vault). Ensure `.env` is listed in `.gitignore`.
- **Database Encryption**:
  - *At Rest*: Enable transparent data encryption (TDE) or cloud volume encryption (AWS KMS / GCP CMEK).
  - *In Use / Column-Level*: Encrypt highly sensitive PII (credit cards, tax IDs) at the application layer using AEAD before writing to the database.
- **Backups & Dumps**: Restrict access to database dumps; encrypt backups with dedicated KMS keys; apply automated retention and deletion policies.

---

## 3. Mobile Client Storage & Android Keystore

### Storage Locations on Android
- **App-Private Storage** (`/data/data/<package>/`): Private to the app UID on non-rooted devices. Contains SQLite/Room databases, SharedPreferences, DataStore, and internal cache.
- **The Backup Hazard**: Android auto-backup (`android:allowBackup="true"`) copies internal app data to Google Drive or ADB backup unless explicitly configured.
  - Implement `res/xml/data_extraction_rules.xml` (API 31+) and `res/xml/backup_rules.xml` to explicitly `<exclude>` databases, shared prefs, and keys from cloud and device-to-device transfers.
  - Store transient secrets in `context.noBackupFilesDir`.
- **Scoped Storage**: Apps must use Scoped Storage, the MediaStore API, or the Android Photo Picker rather than requesting broad `READ_EXTERNAL_STORAGE` / `MANAGE_EXTERNAL_STORAGE` permissions.

### Secrets in the APK: Public vs True Secrets
- **Public Identifiers**: Google Maps keys, Firebase App IDs, and OAuth Client IDs embedded in the APK are readable by anyone decompiling the app. Apply restrictions on the provider console (restrict by package name + SHA-256 certificate fingerprint).
- **True Secrets**: Server API keys, payment provider private keys, database connection strings, and symmetric encryption keys must **never** be included in an APK/AAB. Obfuscation (R8/ProGuard), string encryption, and NDK C++ hiding do **not** protect secrets against reverse engineering. Move the secret to the backend.

### Android Keystore System
- Store local cryptographic keys in the **Android Keystore** provider (`AndroidKeyStore`). Key material never enters application memory and cannot be extracted from hardware.
- Utilize StrongBox (`setIsStrongBoxBacked(true)`) where available for hardware-isolated cryptographic operations.
- Key parameters: Enforce `KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT`, explicit block modes (`BLOCK_MODE_GCM`), and padding (`ENCRYPTION_PADDING_NONE`).
- User authentication binding: For sensitive actions, configure `setUserAuthenticationRequired(true)` to require biometric or lock-screen authentication before the key can be used.

---

## 4. Cryptographic Standards & Safe Primitives

### Approved Cryptographic Primitives
- **Symmetric Encryption**: Authenticated Encryption with Associated Data (**AEAD**) exclusively:
  - **AES-256-GCM** or **AES-128-GCM**
  - **ChaCha20-Poly1305**
- **Nonces / IVs**: Must be unique for every encryption invocation. Generate using a cryptographically secure pseudo-random number generator (**CSPRNG**):
  - Java/Kotlin: `SecureRandom` (never `java.util.Random` or `Math.random()`).
  - Node.js: `crypto.randomBytes()`.
  - Python: `secrets.token_bytes()`.
- **Asymmetric Cryptography**: RSA (minimum 2048-bit, preferred 3072/4096-bit with OAEP padding) or Elliptic Curve (**ECDSA / Ed25519**).
- **Hashing & Signatures**: SHA-256, SHA-384, SHA-512, HMAC-SHA256. (Never MD5 or SHA-1 for security integrity).
- **Password Hashing**: Argon2id (recommended), scrypt, or bcrypt. (Never SHA-256 or MD5 for passwords).
- **Vetted High-Level Libraries**: Prefer Google Tink or platform primitives over low-level manual cipher building.

### Banned Insecure Patterns
- **ECB Mode**: `AES/ECB/PKCS5Padding` (preserves plaintext patterns; strictly prohibited).
- **Static / Hardcoded IVs**: Reusing an IV with GCM mode completely compromises message confidentiality and authentication integrity.
- **Custom Encryption Schemes**: Never implement custom encryption algorithms, proprietary XOR obfuscation, or homemade hashing schemes.
- **Timing Attacks**: Use constant-time comparison functions (`MessageDigest.isEqual` / `crypto.timingSafeEqual`) when validating tokens, signatures, or HMACs.

---

## 5. Verification & Testing Checklist

- [ ] Repository and APK contain no hardcoded secrets, private keys, or database credentials (verified via TruffleHog / Gitleaks / Semgrep).
- [ ] Passwords stored using Argon2id or bcrypt with appropriate salt and work factor.
- [ ] Symmetric encryption uses AES-GCM or ChaCha20-Poly1305 with fresh random nonces per operation.
- [ ] Android backup configuration excludes sensitive tokens and databases (`dataExtractionRules`).
- [ ] Logging frameworks (Logcat, SLF4J, Winston) redact tokens, passwords, and sensitive PII from release logs.
- [ ] Mobile app clears tokens, cached user data, and local databases upon user logout.
