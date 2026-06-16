# 🔐 GUÍA DE REMEDIOS - Seguridad school-v4

## Paso 1: Auditar Vulnerabilidades Actuales

```bash
cd /ruta/al/repositorio/school-v4

# Ver todas las vulnerabilidades
npm audit

# Ver con detalles
npm audit --json > audit-report.json

# Contar por severidad
npm audit 2>/dev/null | grep -E "(critical|high|medium)"
```

---

## Paso 2: Actualizar Dependencias Críticas

### Electron (¡¡CRÍTICO!!)

**Actual:** v31.0.0 (Junio 2024 - OBSOLETO)  
**Recomendado:** v33+ (2026)

```bash
# Ver versión actual
npm list electron

# Actualizar a latest
npm install electron@latest --save-dev

# Verificar compatible con node-gyp (compilaciones nativas)
npm install --save-dev electron-builder@latest

# Test de construcción
npm run build:linux
```

**Impacto:** Parcheará 20+ CVEs de Chromium

---

### Capacitor para iOS/Android

**Actual:** v8.4.0 (EOL - Fin de Soporte)  
**Recomendado:** v6 LTS o v7

```bash
# Verificar capacitor versión
npm list @capacitor/core

# Migración (REQUIERE CAMBIOS DE CÓDIGO)
npm install @capacitor/core@latest
npm install @capacitor/cli@latest
npm install @capacitor/android@latest
npm install @capacitor/ios@latest

# Ejecutar setup
npx cap doctor  # Verifica configuración
```

**Nota:** La migración de v8→v6/v7 requiere actualizar algunos APIs. Ver [Capacitor Migration Guide](https://capacitorjs.com/docs/getting-started/upgrading-to-v6)

---

## Paso 3: Remediar Vulnerabilidades de Dependencias

```bash
# Ejecutar fix automático (CUIDADO: puede cambiar API)
npm audit fix

# Si falla, hacer manual para cada una:
npm install lodash@latest
npm install chalk@latest
npm install ejs@latest

# Verificar que no quebró nada
npm test
npm run build:linux
```

---

## Paso 4: CRÍTICO - Remover Credenciales del Repo

### 1. Identificar archivos sensibles

```bash
# Archivos que NUNCA deben estar en Git
git log --all --name-only --oneline | grep -i "xcconfig\|plist\|keystore\|certificate\|p12\|pem\|key\|secret"

# Verificar qué está ahora
git ls-tree -r HEAD | grep -i "xcconfig\|cert\|key\|secret"
```

### 2. Remover archivos sensibles (si existen)

```bash
# Remover del historio (requiere git reset duro)
git filter-repo --path ios/debug.xcconfig --invert-paths
git filter-repo --path android/app.keystore --invert-paths

# MEJOR: Usar BFG para repositorios grandes
brew install bfg  # macOS
bfg --delete-files ios/debug.xcconfig

# Forzar push (CUIDADO: afecta a todos)
git push origin --force --all
```

### 3. Crear archivos de configuración SEGUROS

**android/.env.example:**
```bash
# NUNCA commitear .env
ANDROID_KEYSTORE_PATH=path/to/keystore.jks
ANDROID_KEYSTORE_PASSWORD=***
ANDROID_KEY_ALIAS=***
ANDROID_KEY_PASSWORD=***
```

**ios/.env.example:**
```bash
# NUNCA commitear certificados
APPLE_CERTIFICATE_FILE=path/to/cert.p12
APPLE_CERTIFICATE_PASSWORD=***
APPLE_TEAM_ID=***
```

**.gitignore (actualizar):**
```gitignore
# Credenciales
.env
.env.local
.env.*.local
*.p12
*.pem
*.key
*.jks
*.xcconfig
ios/Certificates/
ios/Profiles/
android/keystore/

# Otros
node_modules/
dist/
build/
*.deb
*.AppImage
*.dmg
*.exe
```

---

## Paso 5: Implementar Code Signing

### Para Linux (DEB/AppImage)

**En package.json:**
```json
{
  "build": {
    "linux": {
      "target": ["deb", "AppImage"],
      "category": "Education"
    },
    "deb": {
      "maintainer": "Juanjo <email@example.com>"
    }
  }
}
```

```bash
# Crear GPG key si no tienes
gpg --gen-key
gpg --list-keys

# Exportar public key
gpg --export-armor tu@email.com > public-key.asc

# En CI/CD (GitHub Actions):
# Usar secrets para private key
```

### Para Windows (MSIX/NSIS + Authenticode)

```json
{
  "build": {
    "win": {
      "certificateFile": "${env.CERT_FILE}",
      "certificatePassword": "${env.CERT_PASSWORD}",
      "signingHashAlgorithms": ["sha256"],
      "sign": "./customSign.js"
    }
  }
}
```

**Obtener certificado:**
- [DigiCert](https://www.digicert.com/code-signing/buy-code-signing-certificate)
- [Sectigo](https://sectigo.com/ssl-certificates-tls/code-signing)
- [Automate con GH Actions](https://docs.microsoft.com/es-es/windows/msix/package/sign-app-package-using-signtool)

### Para macOS (Developer ID)

**Requisito:** Suscripción Apple Developer ($99/año)

```json
{
  "build": {
    "mac": {
      "signingIdentity": "Developer ID Application: Tu Nombre (XXXXX)",
      "notarize": {
        "teamId": "XXXXXX",
        "ascProvider": "Provider Short Name"
      }
    }
  }
}
```

---

## Paso 6: Encriptar Datos Locales

### Instalar dependencia de encriptación

```bash
npm install crypto-js
# O más seguro: libsodium.js o tweetnacl.js
npm install libsodium.js
```

### Reemplazar localStorage en app.js

**ANTES (INSEGURO):**
```javascript
function saveData(k,v){
  try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}
}
```

**DESPUÉS (SEGURO):**
```javascript
const sodium = require('libsodium.js');

async function saveDataSecure(k,v){
  try {
    // Generar key única (una sola vez)
    if(!window.encryptionKey) {
      window.encryptionKey = sodium.crypto_secretbox_keygen();
      // GUARDAR: window.encryptionKey en IndexedDB sin acceso JS
    }
    
    const plaintext = new TextEncoder().encode(JSON.stringify(v));
    const nonce = sodium.randombytes_buf(sodium.crypto_secretbox_NONCEBYTES);
    const ciphertext = sodium.crypto_secretbox_easy(plaintext, nonce, window.encryptionKey);
    
    const combined = sodium.randombytes_buf(nonce.byteLength + ciphertext.byteLength);
    new Uint8Array(combined).set(new Uint8Array(nonce), 0);
    new Uint8Array(combined).set(new Uint8Array(ciphertext), nonce.byteLength);
    
    localStorage.setItem(k, sodium.to_base64(combined));
  } catch(e){console.error('Encrypt error:', e);}
}

async function loadDataSecure(k) {
  try {
    const combined = sodium.from_base64(localStorage.getItem(k));
    if(!combined) return null;
    
    const nonce = combined.slice(0, sodium.crypto_secretbox_NONCEBYTES);
    const ciphertext = combined.slice(sodium.crypto_secretbox_NONCEBYTES);
    
    const plaintext = sodium.crypto_secretbox_open_easy(ciphertext, nonce, window.encryptionKey);
    return JSON.parse(new TextDecoder().decode(plaintext));
  } catch(e){console.error('Decrypt error:', e); return null;}
}
```

**Uso:**
```javascript
// En lugar de: saveData('sv4_progress', progress)
await saveDataSecure('sv4_progress', progress);

// En lugar de: loadData('sv4_progress', {})
const progress = await loadDataSecure('sv4_progress') || {};
```

---

## Paso 7: Asegurar API Ollama

### Actualizar main.js

**ANTES (SIN AUTH):**
```javascript
ipcMain.handle('ollama-chat', async(e, prompt) =>
  new Promise(resolve=>{
    const r = http.request({
      hostname: 'localhost',
      port: 11434,
      path: '/api/generate',
      method: 'POST'
    }, ...);
  })
);
```

**DESPUÉS (CON AUTH):**
```javascript
const OLLAMA_API_KEY = process.env.OLLAMA_API_KEY || '';
const OLLAMA_HOST = process.env.OLLAMA_HOST || 'localhost';
const OLLAMA_PORT = process.env.OLLAMA_PORT || 11434;

ipcMain.handle('ollama-chat', async(e, prompt) =>
  new Promise(resolve=>{
    const b = JSON.stringify({
      model: 'gemma2:2b',
      prompt: String(prompt).slice(0, 1000),
      stream: false
    });
    
    const headers = {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(b)
    };
    
    // Agregar autenticación si existe
    if(OLLAMA_API_KEY) {
      headers['Authorization'] = `Bearer ${OLLAMA_API_KEY}`;
    }
    
    const r = http.request({
      hostname: OLLAMA_HOST,
      port: OLLAMA_PORT,
      path: '/api/generate',
      method: 'POST',
      headers: headers,
      timeout: 60000
    }, res=>{
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          resolve({
            success: true,
            response: response.response || 'Sin respuesta'
          });
        } catch(e) {
          resolve({success: false, error: 'JSON inválido'});
        }
      });
    });
    
    r.on('error', err => resolve({success: false, error: err.message}));
    r.on('timeout', () => {r.destroy(); resolve({success: false, error: 'Timeout'});});
    r.write(b);
    r.end();
  })
);
```

### Configurar Ollama con autenticación

```bash
# En servidor Ollama (si soporta)
# Actualmente Ollama no tiene auth nativa, opciones:
# 1. Usar reverse proxy (nginx) con autenticación
# 2. Usar API gateway (Kong, AWS API Gateway)
# 3. Local-only binding (solo localhost)

# Opción más segura: Bind a localhost solamente
export OLLAMA_HOST=127.0.0.1:11434

# O en Docker:
docker run -p 127.0.0.1:11434:11434 ollama/ollama
```

---

## Paso 8: Fortalecer CSP Headers

**En main.js (currentar)**
```javascript
w.webContents.session.webRequest.onHeadersReceived((d, cb) => cb({
  responseHeaders: {
    ...d.responseHeaders,
    'Content-Security-Policy': [
      "default-src 'self'",
      "script-src 'self'",
      "style-src 'self'",
      "img-src 'self' data:",
      "connect-src 'self' http://localhost:11434",
      "font-src 'self'",
      "object-src 'none'",
      "base-uri 'self'",
      "frame-ancestors 'none'",
      "form-action 'self'",
      "upgrade-insecure-requests",
      "block-all-mixed-content"
    ].join('; ')
  }
}));
```

---

## Paso 9: Secure Temporary Files

**En apply_update.py:**

```python
import tempfile
import os

# ANTES (INSEGURO)
# shutil.copy2(f, f+".bak_"+datetime.datetime.now().strftime("%H%M%S"))

# DESPUÉS (SEGURO)
def secure_backup(filepath):
    """Crear backup seguro en directorio temporal"""
    with tempfile.TemporaryDirectory(prefix='schoolv4_', suffix='_bak') as tmpdir:
        backup_path = os.path.join(tmpdir, os.path.basename(filepath))
        shutil.copy2(filepath, backup_path)
        
        # Permisos restrictivos (owner solo)
        os.chmod(backup_path, 0o600)
        
        # Copiar a ubicación final segura
        final_backup = filepath + '.backup'
        shutil.copy2(backup_path, final_backup)
        os.chmod(final_backup, 0o600)
        
        return final_backup

# Uso
for f in ["styles.css", "index.html", "app.js"]:
    if os.path.exists(f):
        backup = secure_backup(f)
        print(f"Backup seguro: {backup}")
```

---

## Paso 10: Configurar CI/CD Seguro (GitHub Actions)

Crear **.github/workflows/security.yml:**

```yaml
name: Security Checks

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  audit:
    runs-on: ubuntu-latest
    name: Dependency Audit
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm ci
      - run: npm audit --audit-level=high
      - run: npm audit --json > audit-report.json
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: npm-audit-report
          path: audit-report.json

  sast:
    runs-on: ubuntu-latest
    name: Static Analysis (Semgrep)
    steps:
      - uses: actions/checkout@v4
      - uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten
            p/cwe-top-25

  secrets:
    runs-on: ubuntu-latest
    name: Secret Detection
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: TruffleHog Secret Scanning
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

  build:
    runs-on: ubuntu-latest
    needs: [audit, sast, secrets]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build:linux
      - name: Upload Build
        uses: actions/upload-artifact@v3
        with:
          name: builds
          path: dist/
```

---

## Paso 11: Android Network Security

Crear **android/app/src/main/res/xml/network_security_config.xml:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <!-- Rechazar conexiones inseguras en producción -->
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">127.0.0.1</domain>
        
        <!-- Permitir cleartext SOLO para localhost (Ollama local) -->
        <domain-config cleartextTrafficPermitted="true">
            <domain includeSubdomains="true">localhost</domain>
            <domain includeSubdomains="true">127.0.0.1</domain>
        </domain-config>
    </domain-config>
    
    <!-- Pin certificados para HTTPS externo -->
    <domain-config>
        <domain includeSubdomains="true">school-gemini-proxy.pechicolo.workers.dev</domain>
        <pin-set expiration="2026-06-15">
            <pin digest="SHA-256"><!-- certificado public key pin --></pin>
        </pin-set>
    </domain-config>
    
    <!-- HPKP para dominios críticos -->
    <domain-config>
        <domain includeSubdomains="true">api.example.com</domain>
        <public-key-pins>
            <pin digest="SHA-256"><!-- key pin --></pin>
        </public-key-pins>
    </domain-config>
</network-security-config>
```

**Actualizar AndroidManifest.xml:**
```xml
<application
    android:networkSecurityConfig="@xml/network_security_config"
    ...>
</application>
```

---

## Paso 12: Verificación Final

```bash
# Ejecutar todos los controles
echo "=== NPM AUDIT ===" && npm audit
echo "=== BUILD LINUX ===" && npm run build:linux
echo "=== VERIFICAR GIT ===" && git log --all --name-only | grep -i "key\|secret\|cert" || echo "✅ Sin credenciales en historio"
echo "=== REVISAR CSP ===" && grep -i "content-security-policy" main.js
echo "=== COMPROBAR CODE SIGNING ===" && grep -i "certificate\|sign" package.json

# Escanear directorios sensibles
echo "=== ARCHIVOS SENSIBLES ===" && find . -name "*.p12" -o -name "*.pem" -o -name "*.key" -o -name "*.keystore"
```

---

## Resumen de Cambios

| Paso | Archivo | Cambio | Prioridad |
|---|---|---|---|
| 2 | package.json | Actualizar electron/capacitor | 🔴 |
| 3 | package.json + node_modules | Ejecutar npm audit fix | 🔴 |
| 4 | .gitignore + git history | Remover credenciales | 🔴 |
| 5 | build section | Agregar code signing | 🔴 |
| 6 | app.js | Encriptar localStorage | 🟠 |
| 7 | main.js | Agregar autenticación Ollama | 🟠 |
| 8 | main.js | Fortalecer CSP | 🟠 |
| 9 | apply_update.py | Usar tempfile seguro | 🟡 |
| 10 | .github/workflows/ | CI/CD seguro | 🟡 |
| 11 | android/res/xml | Network security config | 🟡 |
| 12 | Todo | Verificación final | 🟢 |

---

## Soporte y Referencias

- 📖 [Electron Security](https://www.electronjs.org/docs/tutorial/security)
- 📖 [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- 🔗 [npm audit docs](https://docs.npmjs.com/cli/v9/commands/npm-audit)
- 🔐 [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)

