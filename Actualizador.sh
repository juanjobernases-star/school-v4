#!/bin/bash
set -euo pipefail
R='\033[0;31m';G='\033[0;32m';Y='\033[0;33m';B='\033[0;34m'
M='\033[0;35m';C='\033[0;36m';W='\033[1;37m';N='\033[0m'
BASE="$(cd "$(dirname "$0")" && pwd)"; cd "$BASE"
info(){ echo -e "${G}[OK]${N} $1"; }
warn(){ echo -e "${Y}[AVISO]${N} $1"; }
err(){ echo -e "${R}[ERROR]${N} $1"; }

check_deps(){
  for cmd in node npm; do
    command -v "$cmd" >/dev/null 2>&1 && info "$cmd OK" || { err "$cmd no encontrado"; return 1; }
  done
  if command -v ollama >/dev/null 2>&1; then
    curl -s http://localhost:11434 >/dev/null 2>&1 || { nohup ollama serve >/tmp/ollama.log 2>&1 & sleep 3; }
    ollama list 2>/dev/null | grep -q 'gemma2:2b' || ollama pull gemma2:2b
    info "Ollama + gemma2:2b OK"
  else warn "Ollama no instalado"; fi
}

prep_electron(){
  [ -f package.json ] || cat > package.json << 'PJ'
{"name":"school-v4","version":"4.3.0","main":"main.js","scripts":{"start":"electron .","build:linux":"electron-builder --linux deb AppImage","build:win":"electron-builder --win --x64"},"build":{"appId":"com.school.v4","productName":"School v4","directories":{"output":"dist"},"files":["index.html","app.js","styles.css","main.js","preload.js","manifest.json","sw.js"],"linux":{"target":["deb","AppImage"],"category":"Education"},"win":{"target":["nsis"]}},"devDependencies":{"electron":"^33.0.0","electron-builder":"^25.0.0"}}
PJ
  [ -f main.js ] || cat > main.js << 'MJ'
const{app,BrowserWindow,session}=require("electron");const path=require("path");
app.on("web-contents-created",(e,c)=>{c.on("will-navigate",e=>e.preventDefault());c.setWindowOpenHandler(()=>({action:"deny"}))});
function createWindow(){const w=new BrowserWindow({width:1200,height:800,title:"School v4",webPreferences:{preload:path.join(__dirname,"preload.js"),contextIsolation:true,sandbox:true,nodeIntegration:false,webSecurity:true}});
session.defaultSession.webRequest.onHeadersReceived((d,cb)=>{cb({responseHeaders:{...d.responseHeaders,"Content-Security-Policy":["default-src 'self';script-src 'self';style-src 'self';img-src 'self' data:;connect-src 'self' http://localhost:11434;object-src 'none'"]}})});
w.loadFile("index.html");w.setMenuBarVisibility(false)}
app.whenReady().then(createWindow);app.on("window-all-closed",()=>{if(process.platform!=="darwin")app.quit()});
MJ
  [ -f preload.js ] || echo 'const{contextBridge}=require("electron");contextBridge.exposeInMainWorld("schoolAPI",{version:"4.3.0"});' > preload.js
  [ -d node_modules ] || npm install --save-dev electron electron-builder
  info "Electron listo"
}

launch_web(){
  pkill -f "python3 -m http.server 8080" 2>/dev/null || true; sleep 1
  python3 -m http.server 8080 &
  sleep 1; info "Servidor en http://localhost:8080"
  xdg-open http://localhost:8080 2>/dev/null
  echo -e "${C}Enter para detener...${N}"; read -r
  pkill -f "python3 -m http.server 8080" 2>/dev/null; info "Detenido"
}

github_push(){
  command -v git >/dev/null || { err "git no instalado"; return 1; }
  [ -f .gitignore ] || printf 'node_modules/\ndist/\n*.bak*\n*.log\n' > .gitignore
  [ -d .git ] || git init
  git add -A
  read -rp "Commit msg (Enter=Actualizacion): " MSG
  git commit -m "${MSG:-Actualizacion School v4}" || warn "Nada que commitear"
  git remote get-url origin >/dev/null 2>&1 || { read -rp "URL repo GitHub: " URL; [ -n "$URL" ] && git remote add origin "$URL"; }
  git branch -M main 2>/dev/null; git push -u origin main; info "Subido"
}

security_check(){
  echo -e "\n${M}=== Verificacion Seguridad ===${N}\n"
  local i=0
  grep -q "onclick\|onerror\|javascript:" index.html 2>/dev/null && { err "Handlers inline"; i=$((i+1)); } || info "Sin handlers inline"
  grep -q "Content-Security-Policy" index.html 2>/dev/null && info "CSP OK" || { warn "Falta CSP"; i=$((i+1)); }
  grep -qE "eval\(|new Function\(" app.js 2>/dev/null && { err "eval() detectado"; i=$((i+1)); } || info "Sin eval()"
  grep -q "function sanitize" app.js 2>/dev/null && info "sanitize() OK" || { warn "Falta sanitize()"; i=$((i+1)); }
  grep -q "textContent" app.js 2>/dev/null && info "textContent OK" || { warn "Falta textContent"; i=$((i+1)); }
  [ -d node_modules ] && npm audit --audit-level=high 2>/dev/null || true
  echo ""; [ $i -eq 0 ] && info "SEGURIDAD: 0 problemas" || warn "SEGURIDAD: $i problemas"
}

update_questions(){
  echo -e "\n${M}=== Actualizar Preguntas ===${N}"
  curl -s http://localhost:11434 >/dev/null 2>&1 || { err "Ollama no activo"; return 1; }
  echo "1)Mates 2)Lengua 3)Naturales 4)Sociales 5)Ingles 6)Artistica 7)Valores"
  read -rp "Materia: " m
  local MAT; case $m in 1)MAT=matematicas;;2)MAT=lengua;;3)MAT=naturales;;4)MAT=sociales;;5)MAT=ingles;;6)MAT=artistica;;7)MAT=valores;;*)warn "No valida";return;;esac
  read -rp "Cuantas preguntas (5-20): " N; N="${N:-10}"
  info "Generando $N preguntas de $MAT..."
  local F="/tmp/school_preguntas_$(date +%s).json"
  curl -s http://localhost:11434/api/generate -d "{\"model\":\"gemma2:2b\",\"prompt\":\"Genera $N preguntas test 6o Primaria LOMLOE $MAT. JSON:[{\\\"p\\\":\\\"pregunta\\\",\\\"o\\\":[\\\"a\\\",\\\"b\\\",\\\"c\\\",\\\"d\\\"],\\\"c\\\":0,\\\"e\\\":\\\"explicacion\\\"}]. Solo JSON.\",\"stream\":false}" | python3 -c "import sys,json;print(json.load(sys.stdin).get('response','ERROR'))" > "$F"
  [ -s "$F" ] && { info "Guardado: $F"; cat "$F"; } || err "Fallo"
}

backup(){
  local A="$HOME/Documentos/Escuela/backups/school-v4-$(date +%Y%m%d_%H%M%S).tar.gz"
  mkdir -p "$(dirname "$A")"
  tar -czf "$A" --exclude='node_modules' --exclude='dist' --exclude='.git' -C "$BASE/.." "$(basename "$BASE")"
  info "Backup: $A"; ls -lh "$A"
}

while true; do
  clear
  echo -e "${M}========================================${N}"
  echo -e "${W}  School v4 - Build & Deploy System${N}"
  echo -e "${M}========================================${N}"
  echo -e "  ${G}1)${N} Compilar Linux    ${G}2)${N} Compilar Windows"
  echo -e "  ${G}3)${N} Web App/PWA       ${G}4)${N} Test Electron"
  echo -e "  ${B}5)${N} Subir a GitHub    ${Y}6)${N} Seguridad"
  echo -e "  ${C}7)${N} Actualizar preguntas (IA)"
  echo -e "  ${C}8)${N} Backup            ${C}9)${N} Limpiar builds"
  echo -e "  ${R}0)${N} Salir"
  echo -e "${M}========================================${N}"
  read -rp "Opcion: " op
  case $op in
    1)check_deps;prep_electron;npx electron-builder --linux deb AppImage;;
    2)check_deps;prep_electron;npx electron-builder --win --x64;;
    3)launch_web;; 4)check_deps;prep_electron;npx electron .;;
    5)github_push;; 6)security_check;; 7)update_questions;; 8)backup;;
    9)rm -rf dist/ node_modules/;info "Limpio";;
    0)echo -e "${G}Adios${N}";exit 0;; *)warn "No valida";;
  esac
  echo "";read -rp "Enter..." _
done
