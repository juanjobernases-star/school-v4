#!/usr/bin/env python3
# apply_update.py - Adds splash, collapsible cards, reset button
import base64, os, shutil, datetime

print("=" * 55)
print("  School v4 - Update: Splash + Collapsible + Reset")
print("=" * 55)

# Backup
for f in ["styles.css","index.html","app.js"]:
    if os.path.exists(f):
        shutil.copy2(f, f+".bak_"+datetime.datetime.now().strftime("%H%M%S"))
        print("  Backup:", f)

# 1. Append new CSS
new_css=base64.b64decode("Ci8qIOKVkOKVkCBTUExBU0ggU0NSRUVOIOKVkOKVkCAqLwouc3BsYXNoe3Bvc2l0aW9uOmZpeGVkO3RvcDowO2xlZnQ6MDt3aWR0aDoxMDAlO2hlaWdodDoxMDAlO3otaW5kZXg6OTk5OTsKICBiYWNrZ3JvdW5kOmxpbmVhci1ncmFkaWVudCgxMzVkZWcsIzdjM2FlZCwjYTg1NWY3IDMwJSwjYzAyNmQzIDYwJSwjZTkxZTYzIDg1JSwjZjQzZjVlKTsKICBkaXNwbGF5OmZsZXg7ZmxleC1kaXJlY3Rpb246Y29sdW1uO2FsaWduLWl0ZW1zOmNlbnRlcjtqdXN0aWZ5LWNvbnRlbnQ6Y2VudGVyOwogIHRyYW5zaXRpb246b3BhY2l0eSAuNnMgZWFzZSx2aXNpYmlsaXR5IC42cyBlYXNlfQouc3BsYXNoLmZhZGUtb3V0e29wYWNpdHk6MDt2aXNpYmlsaXR5OmhpZGRlbn0KLnNwbGFzaC1pY29ue2ZvbnQtc2l6ZTo1cmVtO21hcmdpbi1ib3R0b206MTZweDthbmltYXRpb246c3BsYXNoQm91bmNlIDEuNXMgZWFzZS1pbi1vdXQgaW5maW5pdGV9CkBrZXlmcmFtZXMgc3BsYXNoQm91bmNlezAlLDEwMCV7dHJhbnNmb3JtOnRyYW5zbGF0ZVkoMCl9NTAle3RyYW5zZm9ybTp0cmFuc2xhdGVZKC0xOHB4KX19Ci5zcGxhc2gtdGl0bGV7Zm9udC1zaXplOjIuNHJlbTtmb250LXdlaWdodDo4MDA7Y29sb3I6I2ZmZjtsZXR0ZXItc3BhY2luZzotMXB4O21hcmdpbi1ib3R0b206NnB4fQouc3BsYXNoLXN1Yntmb250LXNpemU6MS4xcmVtO2NvbG9yOnJnYmEoMjU1LDI1NSwyNTUsLjgpO21hcmdpbi1ib3R0b206MzJweDtmb250LXdlaWdodDo0MDB9Ci5zcGxhc2gtbG9hZGVye2NvbG9yOnJnYmEoMjU1LDI1NSwyNTUsLjcpO2ZvbnQtc2l6ZTouOTVyZW07Zm9udC13ZWlnaHQ6NTAwfQouc3BsYXNoLWRvdHN7ZGlzcGxheTppbmxpbmUtYmxvY2s7YW5pbWF0aW9uOmRvdHMgMS40cyBzdGVwcyg0LGVuZCkgaW5maW5pdGV9CkBrZXlmcmFtZXMgZG90c3swJXtjb250ZW50OicnfTI1JXtjb250ZW50OicuJ301MCV7Y29udGVudDonLi4nfTc1JXtjb250ZW50OicuLi4nfX0KLnNwbGFzaC1kb3RzOjphZnRlcntjb250ZW50OicnO2FuaW1hdGlvbjpkb3RzIDEuNHMgc3RlcHMoNCxlbmQpIGluZmluaXRlfQpAa2V5ZnJhbWVzIGRvdHN7MCV7d2lkdGg6MH0xMDAle3dpZHRoOjEuMmVtfX0KLnNwbGFzaC1iYXJ7d2lkdGg6MTgwcHg7aGVpZ2h0OjRweDtiYWNrZ3JvdW5kOnJnYmEoMjU1LDI1NSwyNTUsLjIpO2JvcmRlci1yYWRpdXM6MnB4O21hcmdpbi10b3A6MTRweDtvdmVyZmxvdzpoaWRkZW59Ci5zcGxhc2gtYmFyLWZpbGx7aGVpZ2h0OjEwMCU7d2lkdGg6MDtiYWNrZ3JvdW5kOiNmZmY7Ym9yZGVyLXJhZGl1czoycHg7YW5pbWF0aW9uOnNwbGFzaExvYWQgMi4ycyBlYXNlLWluLW91dCBmb3J3YXJkc30KQGtleWZyYW1lcyBzcGxhc2hMb2FkezAle3dpZHRoOjB9MTAwJXt3aWR0aDoxMDAlfX0KCi8qIOKVkOKVkCBDT0xMQVBTSUJMRSBTRUNUSU9OUyDilZDilZAgKi8KLnNlY3Rpb24tdG9nZ2xle2N1cnNvcjpwb2ludGVyO2Rpc3BsYXk6ZmxleDthbGlnbi1pdGVtczpjZW50ZXI7Z2FwOjhweDt1c2VyLXNlbGVjdDpub25lOy13ZWJraXQtdXNlci1zZWxlY3Q6bm9uZX0KLnNlY3Rpb24tdG9nZ2xlOmhvdmVye29wYWNpdHk6Ljh9Ci50b2dnbGUtYXJyb3d7ZGlzcGxheTppbmxpbmUtYmxvY2s7dHJhbnNpdGlvbjp0cmFuc2Zvcm0gLjNzIGVhc2U7Zm9udC1zaXplOi44cmVtO2NvbG9yOiM4ZThlOTN9Ci50b2dnbGUtYXJyb3cuY29sbGFwc2Vke3RyYW5zZm9ybTpyb3RhdGUoLTkwZGVnKX0KLmNvbGxhcHNpYmxle21heC1oZWlnaHQ6MjAwMHB4O29wYWNpdHk6MTtvdmVyZmxvdzpoaWRkZW47dHJhbnNpdGlvbjptYXgtaGVpZ2h0IC40cyBlYXNlLG9wYWNpdHkgLjNzIGVhc2UsbWFyZ2luIC4zcyBlYXNlfQouY29sbGFwc2libGUuY29sbGFwc2Vke21heC1oZWlnaHQ6MDtvcGFjaXR5OjA7bWFyZ2luLXRvcDowO21hcmdpbi1ib3R0b206MH0KCi8qIOKVkOKVkCBSRVNFVCBCVVRUT04g4pWQ4pWQICovCi5yZXNldC1zZWN0aW9ue3RleHQtYWxpZ246Y2VudGVyO21hcmdpbjoyNHB4IDAgMTBweDtwYWRkaW5nOjE4cHggMCA4cHg7Ym9yZGVyLXRvcDoxcHggc29saWQgI2YyZjJmN30KLmJ0bi1yZXNldHtwYWRkaW5nOjEycHggMjhweDtiYWNrZ3JvdW5kOnRyYW5zcGFyZW50O2NvbG9yOiNmZjNiMzA7Ym9yZGVyOjEuNXB4IHNvbGlkICNmZjNiMzA7CiAgYm9yZGVyLXJhZGl1czoxNHB4O2N1cnNvcjpwb2ludGVyO2ZvbnQtc2l6ZTouOTVyZW07Zm9udC13ZWlnaHQ6NjAwO3RyYW5zaXRpb246YWxsIC4xNXN9Ci5idG4tcmVzZXQ6aG92ZXJ7YmFja2dyb3VuZDpyZ2JhKDI1NSw1OSw0OCwuMDYpfQouYnRuLXJlc2V0OmFjdGl2ZXt0cmFuc2Zvcm06c2NhbGUoLjk2KTtiYWNrZ3JvdW5kOnJnYmEoMjU1LDU5LDQ4LC4xMil9Cg==").decode("utf-8")
with open("styles.css","r",encoding="utf-8") as f:
    css=f.read()
if "splash" not in css:
    css+=new_css
    with open("styles.css","w",encoding="utf-8") as f:
        f.write(css)
    print("[OK] styles.css: splash + collapsible + reset CSS added")
else:
    print("[OK] styles.css: already has splash styles")

# 2. Patch index.html
splash_html=base64.b64decode("PGRpdiBpZD0ic3BsYXNoIiBjbGFzcz0ic3BsYXNoIj4KICAgIDxkaXYgY2xhc3M9InNwbGFzaC1pY29uIj7wn46TPC9kaXY+CiAgICA8ZGl2IGNsYXNzPSJzcGxhc2gtdGl0bGUiPlNjaG9vbCB2NDwvZGl2PgogICAgPGRpdiBjbGFzcz0ic3BsYXNoLXN1YiI+RXhwbG9yYWRvcmVzIGRlIDbCujwvZGl2PgogICAgPGRpdiBjbGFzcz0ic3BsYXNoLWxvYWRlciI+Q2FyZ2FuZG88c3BhbiBjbGFzcz0ic3BsYXNoLWRvdHMiPi4uLjwvc3Bhbj48L2Rpdj4KICAgIDxkaXYgY2xhc3M9InNwbGFzaC1iYXIiPjxkaXYgY2xhc3M9InNwbGFzaC1iYXItZmlsbCI+PC9kaXY+PC9kaXY+CiAgPC9kaXY+").decode("utf-8")
reset_html=base64.b64decode("PGRpdiBjbGFzcz0icmVzZXQtc2VjdGlvbiI+PGJ1dHRvbiBpZD0icmVzZXRBbGwiIGNsYXNzPSJidG4tcmVzZXQiPvCflIQgUmVpbmljaWFyIHRvZG8gZWwgcHJvZ3Jlc288L2J1dHRvbj48L2Rpdj4=").decode("utf-8")
with open("index.html","r",encoding="utf-8") as f:
    html=f.read()

changed=False

# Add splash after <body>
if "splash" not in html:
    html=html.replace('<div class="app">', splash_html + '\n<div class="app">')
    changed=True
    print("  [OK] Splash screen added")

# Make subject header collapsible
if "section-toggle" not in html:
    html=html.replace(
        '<div class="section-header"><h2>\U0001f4da Elige una materia para practicar</h2></div>',
        '<div class="section-header section-toggle"><h2>\U0001f4da Elige una materia para practicar</h2><span class="toggle-arrow">\u25bc</span></div>')
    html=html.replace(
        '<div id="subjects" class="subjects-grid">',
        '<div id="subjects" class="subjects-grid collapsible">')
    changed=True
    print("  [OK] Subject cards made collapsible")

# Make progress header collapsible
if "section-toggle" not in html and "progress-anchor" in html:
    html=html.replace(
        '<div class="section-header" id="progress-anchor"><h2>\U0001f4ca Tu progreso por materia</h2></div>',
        '<div class="section-header section-toggle" id="progress-anchor"><h2>\U0001f4ca Tu progreso por materia</h2><span class="toggle-arrow">\u25bc</span></div>')
    # Wrap card in collapsible
    old_prog='<div class="card"><div id="progress"'
    new_prog='<div class="card collapsible"><div id="progress"'
    html=html.replace(old_prog, new_prog)
    changed=True
    print("  [OK] Progress section made collapsible")

# Add reset button before closing home section
if "resetAll" not in html:
    html=html.replace('</section>\n    <section id="quiz"', reset_html + '\n    </section>\n    <section id="quiz"')
    changed=True
    print("  [OK] Reset button added")

# Cache bust
import time
ts=str(int(time.time()))
html=html.replace("styles.css?v=99","styles.css?v="+ts).replace("app.js?v=99","app.js?v="+ts)
html=html.replace("styles.css?v=","styles.css?v="+ts+"&x=").replace("app.js?v=","app.js?v="+ts+"&x=") if "?v="+ts not in html else html
# Fallback: if no ?v= at all
if "?v=" not in html:
    html=html.replace("styles.css\"","styles.css?v="+ts+"\"").replace("app.js\"","app.js?v="+ts+"\"").replace("app.js\">","app.js?v="+ts+"\">")

if changed:
    with open("index.html","w",encoding="utf-8") as f:
        f.write(html)
    print("[OK] index.html updated")
else:
    print("[OK] index.html: already has all features")

# 3. Patch app.js
js_splash=base64.b64decode("Ci8vIFNQTEFTSCBTQ1JFRU4KZnVuY3Rpb24gaW5pdFNwbGFzaCgpewogIHZhciBzcGxhc2g9ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoInNwbGFzaCIpOwogIGlmKCFzcGxhc2gpcmV0dXJuOwogIHNldFRpbWVvdXQoZnVuY3Rpb24oKXsKICAgIHNwbGFzaC5jbGFzc0xpc3QuYWRkKCJmYWRlLW91dCIpOwogICAgc2V0VGltZW91dChmdW5jdGlvbigpe3NwbGFzaC5yZW1vdmUoKTt9LDYwMCk7CiAgfSwyNTAwKTsKfQo=").decode("utf-8")
js_collapsible=base64.b64decode("Ci8vIENPTExBUFNJQkxFIFNFQ1RJT05TCmZ1bmN0aW9uIGluaXRDb2xsYXBzaWJsZSgpewogIHZhciBoZWFkZXJzPWRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoIi5zZWN0aW9uLXRvZ2dsZSIpOwogIGZvcih2YXIgaT0wO2k8aGVhZGVycy5sZW5ndGg7aSsrKXsKICAgIGhlYWRlcnNbaV0uYWRkRXZlbnRMaXN0ZW5lcigiY2xpY2siLGZ1bmN0aW9uKCl7CiAgICAgIHZhciBhcnJvdz10aGlzLnF1ZXJ5U2VsZWN0b3IoIi50b2dnbGUtYXJyb3ciKTsKICAgICAgdmFyIHRhcmdldD10aGlzLm5leHRFbGVtZW50U2libGluZzsKICAgICAgaWYodGFyZ2V0JiZ0YXJnZXQuY2xhc3NMaXN0LmNvbnRhaW5zKCJjb2xsYXBzaWJsZSIpKXsKICAgICAgICB0YXJnZXQuY2xhc3NMaXN0LnRvZ2dsZSgiY29sbGFwc2VkIik7CiAgICAgICAgaWYoYXJyb3cpYXJyb3cuY2xhc3NMaXN0LnRvZ2dsZSgiY29sbGFwc2VkIik7CiAgICAgIH0KICAgIH0pOwogIH0KfQo=").decode("utf-8")
js_reset=base64.b64decode("Ci8vIFJFU0VUIEJVVFRPTgpmdW5jdGlvbiBpbml0UmVzZXQoKXsKICB2YXIgYnRuPWRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJyZXNldEFsbCIpOwogIGlmKCFidG4pcmV0dXJuOwogIGJ0bi5hZGRFdmVudExpc3RlbmVyKCJjbGljayIsZnVuY3Rpb24oKXsKICAgIGlmKGNvbmZpcm0oIlx1MDBiZlNlZ3VybyBxdWUgcXVpZXJlcyBib3JyYXIgVE9ETyBlbCBwcm9ncmVzbz9cbkVzdGEgYWNjaVx1MDBmM24gbm8gc2UgcHVlZGUgZGVzaGFjZXIuIikpewogICAgICBsb2NhbFN0b3JhZ2UucmVtb3ZlSXRlbSgic3Y0X3Byb2dyZXNzIik7CiAgICAgIGxvY2FsU3RvcmFnZS5yZW1vdmVJdGVtKCJzdjRfZXhhbXMiKTsKICAgICAgcmVuZGVyUHJvZ3Jlc3MoKTsKICAgICAgYWxlcnQoIlx1MjcwNSBQcm9ncmVzbyByZWluaWNpYWRvIGNvcnJlY3RhbWVudGUuIik7CiAgICB9CiAgfSk7Cn0K").decode("utf-8")
with open("app.js","r",encoding="utf-8") as f:
    js=f.read()

changed_js=False

# Add splash function
if "initSplash" not in js:
    js=js.replace('document.addEventListener("DOMContentLoaded",function(){', js_splash + js_collapsible + js_reset + 'document.addEventListener("DOMContentLoaded",function(){')
    # Add init calls
    js=js.replace('showPage("home");', 'initSplash();initCollapsible();initReset();showPage("home");')
    changed_js=True
    print("  [OK] Splash, collapsible, reset functions added")

if changed_js:
    with open("app.js","w",encoding="utf-8") as f:
        f.write(js)
    print("[OK] app.js updated")
else:
    print("[OK] app.js: already has all features")

print()
print("=" * 55)
print("  LISTO! 3 nuevas funcionalidades:")
print("    1. Pantalla de bienvenida (splash 2.5s)")
print("    2. Tarjetas plegables (click en titulo)")
print("    3. Boton reiniciar progreso")
print("=" * 55)
print()
print("Ejecuta:")
print("  kill $(lsof -t -i:8080) 2>/dev/null; sleep 1")
print("  python3 -m http.server 8080 & sleep 1 && xdg-open http://localhost:8080")