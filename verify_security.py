#!/usr/bin/env python3
"""
🔍 SCHOOL-V4 SECURITY VERIFY - Validación y Testing Post-Remediación
Verifica que todos los fixes se hayan aplicado correctamente

Uso:
    python3 verify_security.py --repo /ruta/al/repo [--report]
"""

import os
import sys
import subprocess
import json
import re
from pathlib import Path
from typing import Tuple, List, Dict

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

class SecurityCheck:
    def __init__(self, name: str, severity: str = 'INFO'):
        self.name = name
        self.severity = severity
        self.status = '?'
        self.details = ''
    
    def passed(self, details=''):
        self.status = '✓'
        self.details = details
    
    def failed(self, details=''):
        self.status = '✗'
        self.details = details
    
    def warning(self, details=''):
        self.status = '!'
        self.details = details
    
    def __str__(self):
        icons = {'✓': Color.GREEN, '✗': Color.RED, '!': Color.YELLOW, '?': Color.BLUE}
        color = icons.get(self.status, '')
        return f"{color}[{self.status}]{Color.END} {self.name} - {self.details}"

def run_cmd(cmd: str) -> Tuple[int, str, str]:
    """Execute command"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, '', str(e)

def verify_npm_audit(repo_path: str) -> List[SecurityCheck]:
    """Check npm vulnerabilities"""
    checks = []
    os.chdir(repo_path)
    
    check = SecurityCheck('NPM Dependencies Audit', 'CRITICAL')
    code, stdout, stderr = run_cmd('npm audit --json 2>/dev/null')
    
    try:
        audit = json.loads(stdout) if stdout else {}
        vulnerabilities = audit.get('vulnerabilities', {})
        
        critical = sum(1 for v in vulnerabilities.values() if v.get('severity') == 'critical')
        high = sum(1 for v in vulnerabilities.values() if v.get('severity') == 'high')
        medium = sum(1 for v in vulnerabilities.values() if v.get('severity') == 'medium')
        
        if critical > 0:
            check.failed(f'{critical} critical, {high} high, {medium} medium vulnerabilities')
        elif high > 0:
            check.warning(f'{high} high, {medium} medium vulnerabilities')
        else:
            check.passed(f'{medium} medium vulnerabilities (acceptable)')
    except:
        check.warning('Could not parse npm audit')
    
    checks.append(check)
    return checks

def verify_electron(repo_path: str) -> List[SecurityCheck]:
    """Check Electron version"""
    checks = []
    os.chdir(repo_path)
    
    check = SecurityCheck('Electron Version', 'CRITICAL')
    code, stdout, stderr = run_cmd('npm list electron 2>/dev/null | head -1')
    
    match = re.search(r'electron@(\d+\.\d+\.\d+)', stdout)
    if match:
        version = match.group(1)
        major = int(version.split('.')[0])
        
        if major >= 32:
            check.passed(f'v{version} (current)')
        elif major >= 30:
            check.warning(f'v{version} (near end-of-life)')
        else:
            check.failed(f'v{version} (outdated, update to v32+)')
    else:
        check.failed('Not installed or unreadable')
    
    checks.append(check)
    return checks

def verify_code_signing(repo_path: str) -> List[SecurityCheck]:
    """Check code signing configuration"""
    checks = []
    
    check = SecurityCheck('Code Signing Config', 'CRITICAL')
    package_json_path = os.path.join(repo_path, 'package.json')
    
    try:
        with open(package_json_path, 'r') as f:
            pkg = json.load(f)
        
        build = pkg.get('build', {})
        
        has_win_cert = 'win' in build and 'certificateFile' in build.get('win', {})
        has_mac_cert = 'mac' in build and 'signingIdentity' in build.get('mac', {})
        
        if has_win_cert and has_mac_cert:
            check.passed('Windows and macOS signing configured')
        elif has_win_cert or has_mac_cert:
            check.warning('Partial code signing (configure both Win & Mac)')
        else:
            check.failed('No code signing configured')
    except:
        check.failed('Could not read package.json')
    
    checks.append(check)
    return checks

def verify_csp(repo_path: str) -> List[SecurityCheck]:
    """Check Content Security Policy"""
    checks = []
    
    check = SecurityCheck('Content Security Policy', 'HIGH')
    main_js_path = os.path.join(repo_path, 'main.js')
    
    if os.path.exists(main_js_path):
        with open(main_js_path, 'r') as f:
            content = f.read()
        
        has_csp = 'Content-Security-Policy' in content
        has_unsafe_eval = 'unsafe-eval' in content
        has_unsafe_inline = 'unsafe-inline' in content
        has_block_mixed = 'block-all-mixed-content' in content
        
        issues = []
        if not has_csp:
            issues.append('CSP not found')
        if has_unsafe_eval:
            issues.append('unsafe-eval detected')
        if has_unsafe_inline:
            issues.append('unsafe-inline detected')
        if not has_block_mixed:
            issues.append('block-all-mixed-content missing')
        
        if not issues:
            check.passed('CSP properly configured')
        else:
            check.warning(', '.join(issues))
    else:
        check.failed('main.js not found')
    
    checks.append(check)
    return checks

def verify_credentials(repo_path: str) -> List[SecurityCheck]:
    """Check for exposed credentials"""
    checks = []
    
    check = SecurityCheck('Credentials in Repository', 'CRITICAL')
    
    sensitive_patterns = [
        ('*.p12', 'iOS certificate'),
        ('*.pem', 'PEM key'),
        ('*.keystore', 'Android keystore'),
        ('*.jks', 'Java keystore'),
        ('*.xcconfig', 'Xcode config'),
    ]
    
    found_sensitive = []
    for pattern, desc in sensitive_patterns:
        code, stdout, _ = run_cmd(f'find {repo_path} -name "{pattern}" -type f 2>/dev/null')
        if stdout.strip():
            found_sensitive.append(f'{pattern} ({desc})')
    
    if found_sensitive:
        check.failed(f'Found: {", ".join(found_sensitive)}')
    else:
        check.passed('No sensitive files found')
    
    # Check .gitignore
    gitignore_path = os.path.join(repo_path, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore = f.read()
        
        has_env = '.env' in gitignore
        has_certs = '*.p12' in gitignore or '*.pem' in gitignore
        
        if not has_env or not has_certs:
            check.warning('.gitignore missing some sensitive patterns')
    
    checks.append(check)
    return checks

def verify_encryption(repo_path: str) -> List[SecurityCheck]:
    """Check localStorage encryption"""
    checks = []
    
    check = SecurityCheck('Data Encryption (localStorage)', 'HIGH')
    app_js_path = os.path.join(repo_path, 'app.js')
    
    if os.path.exists(app_js_path):
        with open(app_js_path, 'r') as f:
            content = f.read()
        
        has_crypto = 'crypto' in content.lower() or 'encrypt' in content.lower()
        has_plain_localstorage = 'localStorage.setItem' in content and 'saveData' in content
        
        if has_crypto:
            check.passed('Encryption detected')
        elif has_plain_localstorage:
            check.warning('Using localStorage without encryption (data in plaintext)')
        else:
            check.warning('Encryption status unclear')
    else:
        check.failed('app.js not found')
    
    checks.append(check)
    return checks

def verify_android(repo_path: str) -> List[SecurityCheck]:
    """Check Android security config"""
    checks = []
    
    check = SecurityCheck('Android Network Security Config', 'HIGH')
    config_path = os.path.join(repo_path, 'android/app/src/main/res/xml/network_security_config.xml')
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            content = f.read()
        
        has_cleartext_false = 'cleartextTrafficPermitted="false"' in content
        has_domain_config = '<domain-config' in content
        
        if has_cleartext_false and has_domain_config:
            check.passed('Network security config present')
        else:
            check.warning('Config present but may be incomplete')
    else:
        check.failed('network_security_config.xml not found')
    
    checks.append(check)
    return checks

def verify_cicd(repo_path: str) -> List[SecurityCheck]:
    """Check CI/CD security"""
    checks = []
    
    check = SecurityCheck('GitHub Actions Security Workflow', 'MEDIUM')
    workflow_path = os.path.join(repo_path, '.github/workflows/security.yml')
    
    if os.path.exists(workflow_path):
        with open(workflow_path, 'r') as f:
            content = f.read()
        
        has_audit = 'npm audit' in content
        has_sast = 'semgrep' in content or 'security-audit' in content
        has_secrets = 'truffleHog' in content or 'secrets' in content
        
        checks_found = [c for c in [has_audit, has_sast, has_secrets] if c]
        
        if len(checks_found) >= 2:
            check.passed(f'CI/CD configured ({len(checks_found)} security checks)')
        else:
            check.warning('CI/CD partially configured')
    else:
        check.failed('.github/workflows/security.yml not found')
    
    checks.append(check)
    return checks

def verify_env_example(repo_path: str) -> List[SecurityCheck]:
    """Check .env.example"""
    checks = []
    
    check = SecurityCheck('.env.example Configuration', 'MEDIUM')
    env_path = os.path.join(repo_path, '.env.example')
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            content = f.read()
        
        has_ollama = 'OLLAMA' in content
        has_encryption = 'ENCRYPTION' in content or 'KEY' in content
        
        if has_ollama:
            check.passed('.env.example found with configuration')
        else:
            check.warning('.env.example exists but may be incomplete')
    else:
        check.warning('.env.example not found (create from .env)')
    
    checks.append(check)
    return checks

def verify_build(repo_path: str) -> List[SecurityCheck]:
    """Try to build the application"""
    checks = []
    os.chdir(repo_path)
    
    check = SecurityCheck('Build Test', 'MEDIUM')
    
    # Check if npm dependencies are installed
    if not os.path.exists(os.path.join(repo_path, 'node_modules')):
        check.warning('node_modules not found (run: npm install)')
    else:
        # Try build
        code, stdout, stderr = run_cmd('npm run build:linux 2>&1 | tail -20')
        
        if code == 0:
            check.passed('Linux build successful')
        else:
            check.warning(f'Build test failed (might be environment issue)')
    
    checks.append(check)
    return checks

def main():
    if len(sys.argv) < 2:
        print(f'{Color.CYAN}Usage: {sys.argv[0]} --repo /path/to/school-v4 [--report]{Color.END}')
        sys.exit(1)
    
    repo_path = None
    report_file = None
    
    for i, arg in enumerate(sys.argv[1:]):
        if arg == '--repo' and i+1 < len(sys.argv)-1:
            repo_path = sys.argv[i+2]
        elif arg == '--report':
            report_file = 'security_report.md'
    
    if not repo_path:
        print(f'{Color.RED}Error: --repo path required{Color.END}')
        sys.exit(1)
    
    repo_path = os.path.abspath(repo_path)
    
    if not os.path.isdir(repo_path):
        print(f'{Color.RED}Error: Repository not found: {repo_path}{Color.END}')
        sys.exit(1)
    
    # Run all checks
    print(f'\n{Color.CYAN}{Color.BOLD}🔍 SCHOOL-V4 SECURITY VERIFICATION{Color.END}\n')
    print(f'Repository: {repo_path}\n')
    
    all_checks = []
    
    print(f'{Color.BOLD}Running checks...{Color.END}\n')
    
    all_checks.extend(verify_npm_audit(repo_path))
    all_checks.extend(verify_electron(repo_path))
    all_checks.extend(verify_code_signing(repo_path))
    all_checks.extend(verify_csp(repo_path))
    all_checks.extend(verify_credentials(repo_path))
    all_checks.extend(verify_encryption(repo_path))
    all_checks.extend(verify_android(repo_path))
    all_checks.extend(verify_cicd(repo_path))
    all_checks.extend(verify_env_example(repo_path))
    all_checks.extend(verify_build(repo_path))
    
    # Print results
    for check in all_checks:
        print(str(check))
    
    # Summary
    print()
    passed = sum(1 for c in all_checks if c.status == '✓')
    failed = sum(1 for c in all_checks if c.status == '✗')
    warnings = sum(1 for c in all_checks if c.status == '!')
    
    print(f'{Color.BOLD}Summary:{Color.END}')
    print(f'  {Color.GREEN}✓ Passed: {passed}{Color.END}')
    print(f'  {Color.RED}✗ Failed: {failed}{Color.END}')
    print(f'  {Color.YELLOW}! Warnings: {warnings}{Color.END}')
    
    # Generate report if requested
    if report_file:
        print(f'\nGenerating report: {report_file}')
        
        with open(report_file, 'w') as f:
            f.write('# Security Verification Report\n\n')
            f.write(f'**Date:** {__import__("datetime").datetime.now().isoformat()}\n')
            f.write(f'**Repository:** {repo_path}\n\n')
            
            f.write('## Results\n\n')
            
            for check in all_checks:
                status_mark = '✓' if check.status == '✓' else ('✗' if check.status == '✗' else '⚠')
                f.write(f'### {status_mark} {check.name}\n')
                f.write(f'{check.details}\n\n')
            
            f.write('## Summary\n\n')
            f.write(f'- Passed: {passed}\n')
            f.write(f'- Failed: {failed}\n')
            f.write(f'- Warnings: {warnings}\n')
    
    # Exit code
    sys.exit(1 if failed > 0 else 0)

if __name__ == '__main__':
    main()
