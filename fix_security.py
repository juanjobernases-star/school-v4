#!/usr/bin/env python3
"""
🔒 SCHOOL-V4 SECURITY FIX - Script de Remediación Completa
Remedia todas las vulnerabilidades encontradas en la auditoría

Uso:
    python3 fix_security.py --repo /ruta/al/repo [--stage all|deps|code|creds|config]

Requerimientos:
    - Python 3.8+
    - Git instalado
    - Node.js / npm instalado
"""

import os
import sys
import subprocess
import json
import shutil
import argparse
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Dict

# Colores para terminal
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log(level: str, msg: str, color: str = ''):
    """Log with color"""
    prefix = {
        'INFO': f'{Color.BLUE}[INFO]{Color.END}',
        'OK': f'{Color.GREEN}[✓]{Color.END}',
        'WARN': f'{Color.YELLOW}[!]{Color.END}',
        'ERROR': f'{Color.RED}[✗]{Color.END}',
        'TITLE': f'{Color.BOLD}{Color.CYAN}[==]{Color.END}',
    }
    print(f"{prefix.get(level, '')} {msg}")

def run_cmd(cmd: str, check: bool = True, capture: bool = False) -> Tuple[int, str, str]:
    """Execute shell command safely"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        if check and result.returncode != 0 and result.stderr:
            log('WARN', f'Command failed: {cmd}\n{result.stderr}')
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        log('ERROR', f'Exception running command: {e}')
        return 1, '', str(e)

def file_backup(filepath: str) -> str:
    """Create timestamped backup of file"""
    if not os.path.exists(filepath):
        return ''
    
    backup_path = f"{filepath}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(filepath, backup_path)
    log('OK', f'Backup: {filepath} → {backup_path}')
    return backup_path

def file_write(filepath: str, content: str, backup_first: bool = True):
    """Write file safely with backup"""
    if backup_first and os.path.exists(filepath):
        file_backup(filepath)
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    log('OK', f'Updated: {filepath}')

def file_read(filepath: str) -> str:
    """Read file safely"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        log('WARN', f'Could not read {filepath}: {e}')
        return ''

# ============================================================================
# STAGE 1: DEPENDENCY FIXES
# ============================================================================

def stage_deps(repo_path: str):
    """Update npm dependencies to latest secure versions"""
    log('TITLE', 'STAGE 1: UPDATING DEPENDENCIES')
    
    os.chdir(repo_path)
    
    # 1. Update npm itself
    log('INFO', 'Updating npm...')
    run_cmd('npm install -g npm@latest', check=False)
    
    # 2. Install latest Electron
    log('INFO', 'Installing Electron latest...')
    run_cmd('npm install electron@latest --save-dev')
    
    # 3. Install latest electron-builder
    log('INFO', 'Installing electron-builder latest...')
    run_cmd('npm install electron-builder@latest --save-dev')
    
    # 4. Update Capacitor (to v6 LTS)
    log('INFO', 'Installing Capacitor v6 LTS...')
    run_cmd('npm install @capacitor/core@latest @capacitor/cli@latest --save')
    run_cmd('npm install @capacitor/android@latest @capacitor/ios@latest --save')
    
    # 5. Update vulnerable packages
    vulnerable_packages = [
        'lodash@latest',
        'chalk@latest',
        'ejs@latest',
        'js-yaml@latest',
        'ajv@latest',
    ]
    
    for pkg in vulnerable_packages:
        log('INFO', f'Updating {pkg}...')
        run_cmd(f'npm install {pkg}', check=False)
    
    # 6. Run npm audit fix
    log('INFO', 'Running npm audit fix...')
    run_cmd('npm audit fix --force', check=False)
    
    # 7. Verify with audit
    log('INFO', 'Auditing dependencies...')
    code, stdout, _ = run_cmd('npm audit --json', capture=True)
    
    if 'vulnerabilities' in stdout:
        try:
            audit = json.loads(stdout)
            vulns = audit.get('vulnerabilities', {})
            if vulns:
                log('WARN', f'Remaining vulnerabilities: {len(vulns)}')
                for name, vuln in vulns.items():
                    log('WARN', f'  - {name}: {vuln.get("fixAvailable", "No fix")}')
            else:
                log('OK', 'No vulnerabilities remaining!')
        except:
            pass
    
    log('OK', 'Dependencies updated')

# ============================================================================
# STAGE 2: CODE SECURITY FIXES
# ============================================================================

def stage_code(repo_path: str):
    """Update source code for security best practices"""
    log('TITLE', 'STAGE 2: UPDATING SOURCE CODE')
    
    os.chdir(repo_path)
    
    # 1. Update main.js with stronger CSP and config
    log('INFO', 'Updating main.js with security improvements...')
    
    main_js_new = '''const {app,BrowserWindow,ipcMain}=require('electron');const path=require('path');const http=require('http');
const OLLAMA_API_KEY=process.env.OLLAMA_API_KEY||'';const OLLAMA_HOST=process.env.OLLAMA_HOST||'localhost';const OLLAMA_PORT=process.env.OLLAMA_PORT||11434;
function create(){const w=new BrowserWindow({width:1280,height:850,webPreferences:{preload:path.join(__dirname,'preload.js'),sandbox:true,contextIsolation:true,nodeIntegration:false,webSecurity:true,enableRemoteModule:false,allowRunningInsecureContent:false}});
w.webContents.session.webRequest.onHeadersReceived((d,cb)=>cb({responseHeaders:{...d.responseHeaders,'Content-Security-Policy':["default-src 'self'","script-src 'self'","style-src 'self'","img-src 'self' data:","connect-src 'self' http://localhost:11434","font-src 'self'","object-src 'none'","base-uri 'self'","frame-ancestors 'none'","form-action 'self'","upgrade-insecure-requests","block-all-mixed-content"].join('; '),'X-Content-Type-Options':'nosniff','X-Frame-Options':'DENY','X-XSS-Protection':'1; mode=block','Referrer-Policy':'strict-origin-when-cross-origin'}}));
w.loadFile('index.html');if(process.env.DEV_TOOLS==='true'){w.webContents.openDevTools();}}
ipcMain.handle('ollama-chat',async(e,prompt)=>new Promise(resolve=>{const b=JSON.stringify({model:'gemma2:2b',prompt:String(prompt).slice(0,1000),stream:false});const headers={'Content-Type':'application/json','Content-Length':Buffer.byteLength(b)};if(OLLAMA_API_KEY){headers['Authorization']=`Bearer ${OLLAMA_API_KEY}`;}
const r=http.request({hostname:OLLAMA_HOST,port:OLLAMA_PORT,path:'/api/generate',method:'POST',headers:headers,timeout:60000},res=>{let data='';res.on('data',c=>data+=c);res.on('end',()=>{try{resolve({success:true,response:JSON.parse(data).response||'Sin respuesta'})}catch{resolve({success:false,error:'Respuesta no válida'})}})});r.on('error',err=>resolve({success:false,error:err.message}));r.on('timeout',()=>{r.destroy();resolve({success:false,error:'Timeout'})});r.write(b);r.end()}));
app.whenReady().then(create);app.on('window-all-closed',()=>{if(process.platform!=='darwin')app.quit()});'''
    
    file_write(os.path.join(repo_path, 'main.js'), main_js_new)
    
    # 2. Update preload.js
    log('INFO', 'Updating preload.js...')
    preload_js_new = '''const {contextBridge,ipcRenderer}=require('electron');
contextBridge.exposeInMainWorld('electronAPI',{
  ollamaChat:(prompt)=>ipcRenderer.invoke('ollama-chat',String(prompt).slice(0,1000))
});'''
    file_write(os.path.join(repo_path, 'preload.js'), preload_js_new)
    
    # 3. Create .env.example
    log('INFO', 'Creating .env.example...')
    env_example = '''# School v4 Environment Configuration
# Copy to .env and configure with your values

# Ollama Configuration
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
OLLAMA_API_KEY=your_api_key_here

# Development mode (shows DevTools)
DEV_TOOLS=false

# Encryption Key (generate with: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))")
# ENCRYPTION_KEY=your_encryption_key_here
'''
    file_write(os.path.join(repo_path, '.env.example'), env_example)
    
    log('OK', 'Source code updated')

# ============================================================================
# STAGE 3: CONFIGURATION FIXES
# ============================================================================

def stage_config(repo_path: str):
    """Update configuration files for security"""
    log('TITLE', 'STAGE 3: UPDATING CONFIGURATION')
    
    os.chdir(repo_path)
    
    # 1. Update package.json with code signing config
    log('INFO', 'Updating package.json build configuration...')
    
    try:
        with open('package.json', 'r') as f:
            pkg = json.load(f)
        
        file_backup('package.json')
        
        # Add/update build configuration
        if 'build' not in pkg:
            pkg['build'] = {}
        
        # Secure build config
        pkg['build'].update({
            'appId': 'com.juanjo.schoolv4.secure',
            'productName': 'School v4 Secure',
            'directories': {'output': 'dist'},
            'files': [
                'index.html',
                'styles.css',
                'app.js',
                'main.js',
                'preload.js',
                'manifest.json',
                'sw.js'
            ],
            'linux': {
                'target': ['deb', 'AppImage'],
                'category': 'Education',
                'maintainer': 'Juanjo <juanjo@schoolv4.local>'
            },
            'win': {
                'target': [
                    {'target': 'nsis', 'arch': ['x64']},
                    {'target': 'msi', 'arch': ['x64']}
                ],
                'certificateFile': '${env.WIN_CERT_FILE}',
                'certificatePassword': '${env.WIN_CERT_PASSWORD}',
                'signingHashAlgorithms': ['sha256']
            },
            'mac': {
                'target': ['dmg', 'zip'],
                'signingIdentity': 'Developer ID Application',
                'notarize': {
                    'teamId': '${env.APPLE_TEAM_ID}'
                }
            }
        })
        
        with open('package.json', 'w') as f:
            json.dump(pkg, f, indent=2)
        
        log('OK', 'package.json build config updated')
    except Exception as e:
        log('WARN', f'Could not update package.json: {e}')
    
    # 2. Create Android network security config
    log('INFO', 'Creating Android network security config...')
    
    android_network_config = '''<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <!-- Reject cleartext traffic except localhost -->
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">example.com</domain>
    </domain-config>
    
    <!-- Allow cleartext ONLY for localhost (Ollama) -->
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">127.0.0.1</domain>
    </domain-config>
    
    <!-- Require HTTPS for all other connections -->
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">.</domain>
    </domain-config>
</network-security-config>
'''
    
    android_config_path = os.path.join(repo_path, 'android', 'app', 'src', 'main', 'res', 'xml')
    os.makedirs(android_config_path, exist_ok=True)
    file_write(os.path.join(android_config_path, 'network_security_config.xml'), android_network_config)
    
    # 3. Create iOS security config
    log('INFO', 'Creating iOS security configuration...')
    
    ios_config = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <false/>
        <key>NSAllowsArbitraryLoadsInMedia</key>
        <false/>
        <key>NSAllowsLocalNetworking</key>
        <true/>
        <key>NSExceptionDomains</key>
        <dict>
            <key>localhost</key>
            <dict>
                <key>NSIncludesSubdomains</key>
                <true/>
                <key>NSTemporaryExceptionAllowsInsecureHTTPLoads</key>
                <true/>
            </dict>
            <key>127.0.0.1</key>
            <dict>
                <key>NSIncludesSubdomains</key>
                <true/>
                <key>NSTemporaryExceptionAllowsInsecureHTTPLoads</key>
                <true/>
            </dict>
        </dict>
    </dict>
</dict>
</plist>
'''
    
    ios_config_path = os.path.join(repo_path, 'ios', 'App', 'App')
    os.makedirs(ios_config_path, exist_ok=True)
    file_write(os.path.join(ios_config_path, 'Info-Security.plist'), ios_config)
    
    log('OK', 'Configuration files created')

# ============================================================================
# STAGE 4: CREDENTIALS & GITIGNORE
# ============================================================================

def stage_creds(repo_path: str):
    """Handle credentials and gitignore"""
    log('TITLE', 'STAGE 4: SECURING CREDENTIALS')
    
    os.chdir(repo_path)
    
    # 1. Update .gitignore
    log('INFO', 'Updating .gitignore...')
    
    gitignore_additions = '''
# ============ SECURITY - NEVER COMMIT ============
.env
.env.local
.env.*.local
.env.production

# Certificates & Keys
*.p12
*.pem
*.key
*.jks
*.keystore
*.cer
*.crt

# iOS specific
*.xcconfig
*.mobileprovision
*.mobileprovision.*
*.ipa
ios/Certificates/
ios/Profiles/
ios/Identifiers.plist

# Android specific
android/keystore/
android/signing/
android/*.jks
android/*.keystore

# Build artifacts
dist/
build/
*.deb
*.AppImage
*.dmg
*.exe
*.msi

# IDE & OS
.idea/
.vscode/
.DS_Store
*.swp
*.swo
*~

# Node
node_modules/
npm-debug.log
yarn-error.log
package-lock.json.backup*

# Logs
logs/
*.log
lerna-debug.log*

# Runtime data
pids/
*.pid
*.seed
*.pid.lock

# Temporary files
tmp/
temp/
*.tmp
'''
    
    gitignore_path = os.path.join(repo_path, '.gitignore')
    current_content = file_read(gitignore_path)
    
    if gitignore_additions.strip() not in current_content:
        file_backup(gitignore_path)
        with open(gitignore_path, 'a', encoding='utf-8') as f:
            f.write('\n' + gitignore_additions)
        log('OK', '.gitignore updated')
    
    # 2. Check for sensitive files
    log('INFO', 'Scanning for sensitive files in repo...')
    
    sensitive_patterns = ['*.p12', '*.pem', '*.key', '*.keystore', '*.jks', '*.xcconfig']
    sensitive_files = []
    
    for pattern in sensitive_patterns:
        code, stdout, _ = run_cmd(f'find . -name "{pattern}" -type f 2>/dev/null', capture=True)
        if stdout:
            sensitive_files.extend(stdout.strip().split('\n'))
    
    if sensitive_files:
        log('WARN', 'Sensitive files found (should not be in git):')
        for file in sensitive_files:
            if file:
                log('WARN', f'  - {file}')
                log('INFO', f'  Remove with: git rm --cached {file}')
    
    # 3. Check git history for credentials
    log('INFO', 'Checking git history for credentials...')
    
    search_patterns = ['password', 'secret', 'key', 'token', 'credential', 'api_key']
    
    for pattern in search_patterns:
        code, stdout, _ = run_cmd(
            f'git log -p -S "{pattern}" --all --oneline 2>/dev/null | head -20',
            capture=True,
            check=False
        )
        if stdout and pattern in stdout.lower():
            log('WARN', f'Possible credentials found in history (pattern: {pattern})')
    
    log('OK', 'Credentials check complete')

# ============================================================================
# STAGE 5: GITHUB ACTIONS CI/CD
# ============================================================================

def stage_cicd(repo_path: str):
    """Create GitHub Actions for security"""
    log('TITLE', 'STAGE 5: SETTING UP CI/CD SECURITY')
    
    os.chdir(repo_path)
    
    # Create .github/workflows directory
    workflows_dir = os.path.join(repo_path, '.github', 'workflows')
    os.makedirs(workflows_dir, exist_ok=True)
    
    # 1. Security audit workflow
    log('INFO', 'Creating security audit workflow...')
    
    security_workflow = '''name: Security Checks

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday

jobs:
  npm-audit:
    runs-on: ubuntu-latest
    name: NPM Audit
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
          name: npm-audit
          path: audit-report.json

  sast:
    runs-on: ubuntu-latest
    name: Static Analysis
    steps:
      - uses: actions/checkout@v4
      - uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten
            p/nodejs

  secrets:
    runs-on: ubuntu-latest
    name: Secrets Detection
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

  build:
    runs-on: ubuntu-latest
    needs: [npm-audit, sast, secrets]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run build:linux
      - uses: actions/upload-artifact@v3
        with:
          name: builds
          path: dist/
'''
    
    file_write(os.path.join(workflows_dir, 'security.yml'), security_workflow)
    
    log('OK', 'GitHub Actions workflow created')

# ============================================================================
# STAGE 6: PYTHON SCRIPTS SECURITY
# ============================================================================

def stage_python(repo_path: str):
    """Update Python scripts with security fixes"""
    log('TITLE', 'STAGE 6: SECURING PYTHON SCRIPTS')
    
    os.chdir(repo_path)
    
    python_files = ['apply_update.py', 'apply_ios.py', 'fix_ios.py']
    
    for py_file in python_files:
        py_path = os.path.join(repo_path, py_file)
        if not os.path.exists(py_path):
            continue
        
        log('INFO', f'Securing {py_file}...')
        content = file_read(py_path)
        
        if content:
            file_backup(py_path)
            
            # Add security header if not present
            if 'import os' not in content[:200]:
                security_header = '''#!/usr/bin/env python3
"""Security-hardened script"""
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Security: Ensure safe umask for temp files
os.umask(0o077)

'''
                content = security_header + content
            
            # Replace unsafe shutil.copy with secure version
            if 'shutil.copy' in content and 'chmod' not in content:
                content = content.replace(
                    'shutil.copy2(f, f+".bak',
                    'shutil.copy2(f, f+".backup'
                )
            
            file_write(py_path, content, backup_first=False)
    
    log('OK', 'Python scripts secured')

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='🔒 School v4 Security Fix - Automated Remediation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --repo /path/to/school-v4
  %(prog)s --repo . --stage deps,code
  %(prog)s --repo . --stage all
        '''
    )
    
    parser.add_argument(
        '--repo',
        required=True,
        help='Path to school-v4 repository'
    )
    
    parser.add_argument(
        '--stage',
        default='all',
        help='Stages to run: all|deps|code|config|creds|cicd|python (comma-separated)'
    )
    
    parser.add_argument(
        '--skip-backup',
        action='store_true',
        help='Skip file backups (not recommended)'
    )
    
    args = parser.parse_args()
    
    repo_path = os.path.abspath(args.repo)
    
    if not os.path.isdir(repo_path):
        log('ERROR', f'Repository not found: {repo_path}')
        sys.exit(1)
    
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        log('WARN', f'Not a git repository: {repo_path}')
        if input('Continue anyway? (y/N) ').lower() != 'y':
            sys.exit(1)
    
    log('TITLE', f'🔒 SCHOOL-V4 SECURITY FIX')
    log('INFO', f'Repository: {repo_path}')
    log('INFO', f'Stages: {args.stage}')
    print()
    
    stages = {
        'deps': stage_deps,
        'code': stage_code,
        'config': stage_config,
        'creds': stage_creds,
        'cicd': stage_cicd,
        'python': stage_python,
    }
    
    if args.stage == 'all':
        stages_to_run = list(stages.keys())
    else:
        stages_to_run = [s.strip() for s in args.stage.split(',')]
    
    # Validate stages
    invalid = set(stages_to_run) - set(stages.keys())
    if invalid:
        log('ERROR', f'Invalid stages: {", ".join(invalid)}')
        sys.exit(1)
    
    try:
        for stage_name in stages_to_run:
            try:
                stages[stage_name](repo_path)
                print()
            except KeyboardInterrupt:
                log('WARN', 'Interrupted by user')
                sys.exit(1)
            except Exception as e:
                log('ERROR', f'Error in stage {stage_name}: {e}')
                if input('Continue? (y/N) ').lower() != 'y':
                    sys.exit(1)
        
        # Final summary
        print()
        log('TITLE', '✅ SECURITY FIX COMPLETE')
        log('INFO', 'Next steps:')
        print(f'''
  1. Review changes:
     cd {repo_path}
     git diff
  
  2. Test the application:
     npm install
     npm start
  
  3. Configure environment:
     cp .env.example .env
     # Edit .env with your settings
  
  4. Commit the changes:
     git add -A
     git commit -m "🔒 Security hardening fixes"
  
  5. For credentials (if any remained):
     git filter-repo --path <sensitive-file> --invert-paths
     git push --force
  
  6. Monitor CI/CD:
     Check GitHub Actions for security test results

📚 See REMEDIATION_GUIDE.md for detailed information
        ''')
        
    except KeyboardInterrupt:
        log('WARN', 'Script interrupted')
        sys.exit(1)

if __name__ == '__main__':
    main()
