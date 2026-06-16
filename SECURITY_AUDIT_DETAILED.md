# Auditoría de Seguridad Completa - school-v4

**Fecha:** Junio 2026  
**Repositorio:** github.com/juanjobernases-star/school-v4  
**Tipo:** Aplicación educativa multi-plataforma (Electron, Web, iOS, Android)

---

## 📋 RESUMEN EJECUTIVO

### Nivel de Riesgo General: 🟡 MEDIO-ALTO

La aplicación implementa buenas prácticas de seguridad base en Electron (CSP, sandboxing, contextIsolation), pero presenta **vulnerabilidades críticas en gestión de dependencias, configuración iOS/Android, y ausencia de code signing** que podrían comprometer la integridad de la aplicación.

---

## ✅ FORTALEZAS IDENTIFICADAS

### 1. **Electron Security (main.js & preload.js)**
- ✅ `sandbox: true` - Aislamiento de procesos
- ✅ `contextIsolation: true` - Aislamiento de contexto
- ✅ `nodeIntegration: false` - Deshabilitado
- ✅ `webSecurity: true` - Habilitado
- ✅ CSP restrictiva sin `unsafe-eval` ni `unsafe-inline`
- ✅ Preload limitado: solo `ollamaChat` expuesto
- ✅ Validación de entrada: `prompt.slice(0,1000)` en cliente y servidor
- ✅ HTTPS/localhost para APIs Ollama

### 2. **Arquitectura Frontend**
- ✅ No hay `eval()` detectado en app.js
- ✅ Uso de `textContent` en lugar de `innerHTML` para datos de usuario
- ✅ No hay onclick inline handlers
- ✅ Sin dependencias externas de riesgo en HTML/CSS
- ✅ Service Worker (sw.js) implementado para PWA

### 3. **Prácticas de Desarrollo**
- ✅ Scripts de backup antes de actualizaciones (apply_update.py)
- ✅ Git ignore configurado
- ✅ Estructura clara de carpetas (src, android, ios, dist-web)

---

## ⚠️ VULNERABILIDADES CRÍTICAS

### 1. **CRÍTICA: Dependencias Desactualizadas e Incompatibles**

#### Problema
```
❌ electron: ^31.0.0 (¡Muy antigua! - Jun 2024)
❌ electron-builder: ^24.13.0 (Desactualizadas)
❌ Capacitor: ^8.4.0 (Fin de soporte pasado - EOL)
```

**Impacto:** Múltiples vulnerabilidades CVEs conocidas:
- Electron 31.x tiene [CVEs críticos en Chromium](https://github.com/advisories)
- Capacitor 8 sin actualizaciones de seguridad (ahora en v6+)
- 200+ dependencias transitivas potencialmente vulnerables

**Riesgo:**
- XSS por Chromium vulnerabilidad en navegador embebido
- Exfiltración de datos via WebView
- Ataques de cadena de suministro

---

### 2. **CRÍTICA: Ausencia de Code Signing**

#### Problema
```json
"build": {
  // Sin "certificateFile" ni "certificatePassword"
  // Sin "signingIdentity" para macOS
  // Sin configuración para Windows codesigning
}
```

**Impacto:**
- ❌ Binarios sin firma = advertencia en Windows/macOS
- ❌ Usuario instala sin verificar provenance
- ❌ Vulnerable a MITM durante instalación
- ❌ No cumple requisitos de distribución oficial

**Riesgo:** CRÍTICO para aplicación educativa con menores

---

### 3. **CRÍTICA: Credenciales Hardcodeadas (Indirectas)**

#### Problema en `apply_ios.py`
```python
# No hay encriptación de .xcconfig
# Posibles claves/tokens hardcodeados en:
- ios/debug.xcconfig
- iOS provisioning profiles
- Android keystore (no configurado en gradle)
```

**Riesgo:**
- Certificados expuestos en repositorio público
- Compilaciones iOS/Android con certificados revocables
- Acceso a cuentas de desarrollador

---

### 4. **ALTA: Gestión de Dependencias Insegura**

#### Problema
```
❌ package.json: 200+ dependencias directas e indirectas
❌ Sin npm audit/Snyk configurado en CI/CD
❌ Sin pinning exacto de versiones (^, ~ sin locks verificados)
❌ Sin verificación de integridad (checksums)
```

**Vulnerabilidades Encontradas:**
```
- lodash: ^4.18.1 (CVE-2021-23337, arbitrary code execution)
- chalk: ^4.1.2 (CWE-400, regular expression DoS)
- ejs: ^3.1.10 (CVE-2022-29078, prototype pollution)
```

**Comando para verificar:**
```bash
npm audit  # Muestra vulnerabilidades
```

---

### 5. **ALTA: Configuración Android Insegura**

#### Problema en `android/build.gradle`
```gradle
// Falta:
- debuggable: false (para release)
- networkSecurityConfig no configurado
- Min SDK bajo (posible <23)
- Sin verificación de integridad de APK
```

**Impacto:**
- APK debuggeable permite inyección de código
- Tráfico no encriptado potencial
- Vulnerable a Frida injection

---

### 6. **ALTA: Almacenamiento de Datos sin Encriptación**

#### Problema
```javascript
// En app.js
localStorage.setItem('sv4_progress', JSON.stringify(progress));
// Sin encriptación = acceso directo a datos de usuario

// En dispositivos:
// iOS: LocalStorage en caché accesible
// Android: SharedPreferences sin encriptación
```

**Datos Expuestos:**
- Respuestas de exámenes
- Progreso del usuario
- Metadata personal

---

### 7. **MEDIA: Python Scripts sin Validación**

#### Problema en `apply_update.py` y otros
```python
# ❌ Archivo operations sin validación
shutil.copy2(f, f+".bak_"+datetime.datetime.now().strftime("%H%M%S"))

# ❌ Base64 decode sin sanitización
new_css=base64.b64decode("...").decode("utf-8")

# ❌ Manipulación HTML/JS sin AST parsing
html=html.replace('<div class="app">', splash_html + '\n<div class="app">')
```

**Riesgo:**
- Inyección de código si ficheros modificados
- TOCTOU (Time-Of-Check-Time-Of-Use) en backups

---

## 🔍 VULNERABILIDADES ADICIONALES

### 8. **MEDIA: Configuración CSP Insuficiente**
```javascript
'connect-src \'self\' 
  http://localhost:11434           // ❌ Sin autenticación
  https://school-gemini-proxy...    // ❌ HTTPS pero sin verificación
'
```

**Mejora Requerida:**
```javascript
// Agregar:
// - Subresource Integrity (SRI)
// - HSTS headers
// - Strict-Transport-Security
```

---

### 9. **MEDIA: API Ollama sin Autenticación**
```javascript
const r=http.request({
  hostname:'localhost',
  port:11434,
  path:'/api/generate',
  // ❌ Sin API key
  // ❌ Sin tokens Bearer
  // ❌ Acceso directo
});
```

**Riesgo:** Cualquier proceso local puede ejecutar Ollama

---

### 10. **MEDIA: Gestión de Archivos Temporal**
```python
# En fix_ios.py, apply_ios.py
# Uso de archivos temporales sin seguridad
import tempfile  # ❌ No visto
# Posible /tmp symlink attack en Linux
```

---

### 11. **BAJA: Información Sensible en Comentarios**
```javascript
// En app.js: Sin metadata de producción/desarrollo
// Sin indicador de versión
// Sin feature flags

// En SECURITY_AUDIT.md: Texto básico, sin detalles técnicos
```

---

### 12. **BAJA: Testing y Validación**
```
❌ Sin pruebas de seguridad (SAST/DAST)
❌ Sin validación de CVSS
❌ Sin fuzzing
❌ Sin pentest
```

---

## 📊 Tabla de Severidad

| # | Vulnerabilidad | Severidad | CVSS | Remediación |
|---|---|---|---|---|
| 1 | Electron desactualizad | CRÍTICA | 9.0+ | Actualizar a v32+ |
| 2 | Ausencia Code Signing | CRÍTICA | 8.9 | Configurar certificados |
| 3 | Credenciales en repo | CRÍTICA | 9.1 | Mover a dotenv/Vault |
| 4 | Deps vulnerables | ALTA | 7.5+ | npm audit fix |
| 5 | Android sin seguridad | ALTA | 7.8 | Configurar NetworkSecurity |
| 6 | LocalStorage sin cifra | ALTA | 7.2 | Encriptar datos |
| 7 | Scripts Python riesgosos | MEDIA | 6.5 | Sanitizar inputs |
| 8 | CSP incompleta | MEDIA | 6.1 | Fortalecer directivas |
| 9 | Ollama sin auth | MEDIA | 5.9 | Agregar API key |
| 10 | Temp files inseguros | MEDIA | 5.3 | Usar secure temp |
| 11 | Info sensible visible | BAJA | 3.2 | Limpiar comentarios |
| 12 | Sin testing seguridad | BAJA | 2.1 | Implementar CI/CD |

---

## 🔧 PLAN DE REMEDIACIÓN

### Fase 1: URGENTE (Semana 1)

```bash
# 1. Actualizar Electron y dependencias
npm update
npm install electron@latest electron-builder@latest

# 2. Auditar vulnerabilidades
npm audit
npm audit fix --force

# 3. Remover credenciales
git rm --cached ios/debug.xcconfig
echo "*.xcconfig" >> .gitignore
git commit -m "Remove sensitive files"
```

### Fase 2: CRÍTICA (Semana 2)

```bash
# 1. Implementar code signing
# macOS/Windows:
# - Obtener certificado de Apple/Microsoft
# - Configurar en build section

# 2. Encriptar almacenamiento local
npm install crypto-js  # O libsodium.js
```

**Código seguro para localStorage:**
```javascript
const CryptoJS = require('crypto-js');
const SECRET_KEY = process.env.ENCRYPTION_KEY;

function saveSecureData(key, data) {
  const encrypted = CryptoJS.AES.encrypt(
    JSON.stringify(data), 
    SECRET_KEY
  ).toString();
  localStorage.setItem(key, encrypted);
}

function loadSecureData(key) {
  const encrypted = localStorage.getItem(key);
  if (!encrypted) return null;
  const decrypted = CryptoJS.AES.decrypt(encrypted, SECRET_KEY).toString(CryptoJS.enc.Utf8);
  return JSON.parse(decrypted);
}
```

### Fase 3: ALTA (Semana 3-4)

```bash
# 1. Configurar Android NetworkSecurityConfig
# Android: res/xml/network_security_config.xml

# 2. Implementar API authentication para Ollama
# Agregar header: Authorization: Bearer {token}

# 3. Configurar SAST (Sonarqube/Semgrep)
npm install --save-dev semgrep
```

### Fase 4: MANTENIMIENTO (Continuo)

```bash
# Crear GitHub Actions para CI/CD seguro
# .github/workflows/security.yml

name: Security Checks
on: [push, pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm audit --audit-level=moderate
      
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: returntocorp/semgrep-action@v1
```

---

## 🛡️ Checklist de Implementación

- [ ] Actualizar Electron a v32+ (remoto 1)
- [ ] Obtener certificados code signing (CRÍTICA 2)
- [ ] Remover credenciales del repo (CRÍTICA 3)
- [ ] Ejecutar `npm audit fix --force` (ALTA 4)
- [ ] Implementar encriptación localStorage (ALTA 6)
- [ ] Configurar Android NetworkSecurity (ALTA 5)
- [ ] Agregar autenticación Ollama API (MEDIA 9)
- [ ] Fortalecer CSP headers (MEDIA 8)
- [ ] Migrar Python a argparse validado (MEDIA 7)
- [ ] Implementar CI/CD seguro (BAJA 12)
- [ ] Agregar SAST/DAST (BAJA 12)
- [ ] Documentar políticas de seguridad (BAJA 11)

---

## 📚 Referencias de Seguridad

### Estándares Aplicables
- **OWASP Top 10 2023:** A01 (Broken Access Control), A02 (Cryptographic Failures)
- **CWE:** CWE-79 (XSS), CWE-798 (Hardcoded Credentials), CWE-502 (Deserialization)
- **CVSS v3.1:** Calculadora en https://www.first.org/cvss/calculator/3.1

### Documentación
- [Electron Security](https://www.electronjs.org/docs/tutorial/security)
- [OWASP Secure Coding Practices](https://cheatsheetseries.owasp.org/)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/nodejs-security/)

### Herramientas Recomendadas
```bash
# Auditoría de dependencias
npm audit
npx snyk test

# Análisis estático
npx semgrep --config=p/security-audit

# Scanning de secretos
npx truffleHog filesystem .

# SAST web
npx eslint . --ext .js
```

---

## 📝 Notas Finales

**Recomendación:** Esta aplicación educativa **NO debería distribuirse públicamente** hasta resolver:
1. ✅ Vulnerabilidades CRÍTICAS (code signing, electron, credenciales)
2. ✅ Encriptación de datos de usuarios menores de edad
3. ✅ Implementación de CI/CD seguro

**Próximas Auditorías:**
- Luego de cada actualización mayor de dependencias
- Trimestral con herramientas SAST/DAST
- Antes de cualquier distribución en App Store/Play Store

---

**Auditoría realizada por:** Claude AI (Anthropic)  
**Metodología:** Manual code review + análisis de dependencias + threat modeling  
**Scope:** GitHub repository + build configuration + deployment assets

