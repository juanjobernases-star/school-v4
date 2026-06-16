#!/usr/bin/env python3
"""
🔍 DIAGNÓSTICO DE NPM INSTALL - Resolver problemas
Identifica y soluciona problemas comunes con npm
"""

import subprocess
import sys
import json
from pathlib import Path

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

def log(level, msg):
    icons = {
        'INFO': f'{Color.BLUE}[i]{Color.END}',
        'OK': f'{Color.GREEN}[✓]{Color.END}',
        'WARN': f'{Color.YELLOW}[!]{Color.END}',
        'ERROR': f'{Color.RED}[✗]{Color.END}',
    }
    print(f"{icons.get(level, '')} {msg}")

def run_cmd(cmd):
    """Execute command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def diagnose():
    print(f'\n{Color.CYAN}{Color.BOLD}🔍 DIAGNÓSTICO NPM INSTALL{Color.END}\n')
    
    # 1. Verificar Node/npm
    print(f'{Color.BOLD}1. Verificando Node.js y npm{Color.END}')
    print('─' * 60)
    
    code, node_ver, _ = run_cmd('node --version')
    if code == 0:
        log('OK', f'Node.js: {node_ver.strip()}')
    else:
        log('ERROR', 'Node.js no instalado')
        return False
    
    code, npm_ver, _ = run_cmd('npm --version')
    if code == 0:
        log('OK', f'npm: {npm_ver.strip()}')
    else:
        log('ERROR', 'npm no instalado')
        return False
    
    # 2. Verificar package.json
    print(f'\n{Color.BOLD}2. Verificando package.json{Color.END}')
    print('─' * 60)
    
    if Path('package.json').exists():
        log('OK', 'package.json existe')
        
        try:
            with open('package.json', 'r') as f:
                pkg = json.load(f)
            
            deps_count = len(pkg.get('dependencies', {}))
            devdeps_count = len(pkg.get('devDependencies', {}))
            log('OK', f'{deps_count} dependencies, {devdeps_count} devDependencies')
        except Exception as e:
            log('ERROR', f'package.json corrupto: {e}')
            return False
    else:
        log('ERROR', 'package.json no encontrado')
        return False
    
    # 3. Limpiar caché
    print(f'\n{Color.BOLD}3. Limpiando caché de npm{Color.END}')
    print('─' * 60)
    
    log('INFO', 'Ejecutando: npm cache clean --force')
    code, _, _ = run_cmd('npm cache clean --force')
    
    if code == 0:
        log('OK', 'Caché limpiado')
    else:
        log('WARN', 'Error limpiando caché (continuando...)')
    
    # 4. Intentar instalar con diferentes opciones
    print(f'\n{Color.BOLD}4. Intentando npm install{Color.END}')
    print('─' * 60)
    
    # Opción 1: npm install normal
    log('INFO', 'Intento 1: npm install')
    code, stdout, stderr = run_cmd('npm install 2>&1')
    
    if code == 0:
        log('OK', 'npm install exitoso')
        return True
    
    # Opción 2: npm install --legacy-peer-deps
    log('WARN', 'npm install falló, intentando con --legacy-peer-deps')
    code, stdout, stderr = run_cmd('npm install --legacy-peer-deps 2>&1')
    
    if code == 0:
        log('OK', 'npm install --legacy-peer-deps exitoso')
        return True
    
    # Opción 3: npm install --force
    log('WARN', 'Intentando con --force')
    code, stdout, stderr = run_cmd('npm install --force 2>&1')
    
    if code == 0:
        log('OK', 'npm install --force exitoso')
        return True
    
    # Mostrar error
    print(f'\n{Color.RED}{Color.BOLD}❌ ERRORES:{Color.END}')
    if stderr:
        print(f'\nSTDERR:\n{stderr[-1000:]}')  # Últimas 1000 chars
    if stdout:
        print(f'\nSTDOUT:\n{stdout[-1000:]}')
    
    return False

def solutions():
    """Mostrar soluciones alternativas"""
    print(f'\n{Color.BOLD}💡 SOLUCIONES ALTERNATIVAS{Color.END}')
    print('─' * 60)
    
    print('''
Si npm install sigue fallando, intenta:

1. Limpiar todo:
   rm -rf node_modules package-lock.json
   npm cache clean --force
   npm install

2. Usar npm legacy:
   npm install --legacy-peer-deps

3. Usar yarn en lugar de npm:
   npm install -g yarn
   yarn install

4. Verificar versión de Node:
   node --version  # Debe ser v16+
   npm --version   # Debe ser v7+
   
   Si es muy antigua, actualiza:
   nvm install node  # Si tienes nvm
   o descargar desde nodejs.org

5. Verificar package.json:
   cat package.json | head -20
   
   Si está corrupto, restaurar desde git:
   git checkout package.json

6. En Kali Linux específicamente:
   sudo apt update
   sudo apt install npm nodejs
   node --version
    ''')

def main():
    success = diagnose()
    
    if not success:
        solutions()
        
        print(f'\n{Color.BOLD}¿Qué deseas hacer?{Color.END}')
        print('1. Intentar npm install --legacy-peer-deps')
        print('2. Limpiar todo y reintentar')
        print('3. Ver soluciones detalladas')
        print('4. Salir')
        
        try:
            choice = input('\nOpción (1-4): ').strip()
            
            if choice == '1':
                log('INFO', 'Ejecutando: npm install --legacy-peer-deps')
                code, _, _ = run_cmd('npm install --legacy-peer-deps')
                if code == 0:
                    log('OK', 'Éxito!')
                else:
                    log('ERROR', 'Aún falla')
                    
            elif choice == '2':
                log('INFO', 'Limpiando...')
                run_cmd('rm -rf node_modules package-lock.json')
                run_cmd('npm cache clean --force')
                log('INFO', 'Intentando de nuevo...')
                code, _, _ = run_cmd('npm install')
                if code == 0:
                    log('OK', 'Éxito!')
                else:
                    log('ERROR', 'Aún falla')
                    
            elif choice == '3':
                solutions()
                
        except KeyboardInterrupt:
            print('\nAbortado por usuario')
    else:
        print(f'\n{Color.GREEN}{Color.BOLD}✅ npm install completado exitosamente{Color.END}\n')

if __name__ == '__main__':
    main()
