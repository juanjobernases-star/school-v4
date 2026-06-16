#!/usr/bin/env python3
# fix_ios.py - Fix app.js for iOS design
import os, re, base64

print("=" * 50)
print("  School v4 - Fix iOS Design")
print("=" * 50)

if not os.path.exists("app.js"):
    print("[ERROR] app.js no encontrado");exit(1)

with open("app.js","r",encoding="utf-8") as f:
    js=f.read()

print("app.js:",len(js),"bytes")
fixes=0

# Fix 1: Colors
color_map=[
  ("matematicas","purple"),("lengua","pink"),("naturales","green"),
  ("sociales","blue"),("ingles","navy"),("artistica","orange"),("valores","teal")
]
for key,color in color_map:
    pat='key:"'+key+'",name:'
    idx=js.find(pat)
    if idx>=0:
        # Find the closing } of this object entry
        end=js.find("}",idx)
        chunk=js[idx:end]
        if "color:" not in chunk:
            # Insert color before the }
            js=js[:end]+',color:"'+color+'"'+js[end:]
            fixes+=1
print("[OK] Colors:",fixes,"added")

# Fix 2: renderSubjects
RS=base64.b64decode("ZnVuY3Rpb24gcmVuZGVyU3ViamVjdHMoKXsKICB2YXIgZ3JpZD0kKCJzdWJqZWN0cyIpO2lmKCFncmlkKXJldHVybjtncmlkLmlubmVySFRNTD0iIjsKICBmb3IodmFyIHM9MDtzPFNVQkpFQ1RTLmxlbmd0aDtzKyspewogICAgdmFyIHN1Ymo9U1VCSkVDVFNbc107CiAgICB2YXIgY291bnQ9UFJFR1VOVEFTW3N1Ymoua2V5XT9QUkVHVU5UQVNbc3Viai5rZXldLmxlbmd0aDowOwogICAgdmFyIGNhcmQ9ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgiZGl2Iik7CiAgICBjYXJkLmNsYXNzTmFtZT0ic3ViamVjdC1jYXJkIjsKICAgIGNhcmQuc2V0QXR0cmlidXRlKCJkYXRhLWNvbG9yIixzdWJqLmNvbG9yfHwicHVycGxlIik7CiAgICBjYXJkLnNldEF0dHJpYnV0ZSgiZGF0YS1rZXkiLHN1Ymoua2V5KTsKICAgIGNhcmQuaW5uZXJIVE1MPSc8ZGl2IGNsYXNzPSJzdWJqZWN0LWVtb2ppIj4nK3N1YmouZW1vamkrJzwvZGl2PicrCiAgICAgICAgICAgICAgICAgICAnPGRpdiBjbGFzcz0ic3ViamVjdC1uYW1lIj4nK3N1YmoubmFtZSsnPC9kaXY+JysKICAgICAgICAgICAgICAgICAgICc8ZGl2IGNsYXNzPSJzdWJqZWN0LWNvdW50Ij4nK2NvdW50KycgcHJlZ3VudGFzPC9kaXY+JysKICAgICAgICAgICAgICAgICAgICc8YnV0dG9uIGNsYXNzPSJzdWJqZWN0LWJ0biI+UHJhY3RpY2FyPC9idXR0b24+JzsKICAgIGNhcmQuYWRkRXZlbnRMaXN0ZW5lcigiY2xpY2siLGZ1bmN0aW9uKCl7c3RhcnRRdWl6KHRoaXMuZ2V0QXR0cmlidXRlKCJkYXRhLWtleSIpKTt9KTsKICAgIGdyaWQuYXBwZW5kQ2hpbGQoY2FyZCk7CiAgfQp9").decode()
m=re.search(r"function renderSubjects\(\)\{.+?\n\}",js,re.DOTALL)
if m:
    js=js[:m.start()]+RS+js[m.end():]
    fixes+=1
    print("[OK] renderSubjects replaced")
else:
    print("[WARN] renderSubjects not found")

# Fix 3: renderProgress
RP=base64.b64decode("ZnVuY3Rpb24gcmVuZGVyUHJvZ3Jlc3MoKXsKICB2YXIgZGl2PSQoInByb2dyZXNzIik7aWYoIWRpdilyZXR1cm47CiAgdmFyIGRhdGE9bG9hZFByb2dyZXNzKCk7dmFyIGh0bWw9IiI7CiAgZm9yKHZhciBzPTA7czxTVUJKRUNUUy5sZW5ndGg7cysrKXsKICAgIHZhciBzdWJqPVNVQkpFQ1RTW3NdOwogICAgdmFyIGQ9ZGF0YVtzdWJqLmtleV18fHt0b3RhbDowLGhpdHM6MH07CiAgICB2YXIgcGN0PWQudG90YWw+MD9NYXRoLnJvdW5kKChkLmhpdHMvZC50b3RhbCkqMTAwKTowOwogICAgaHRtbCs9JzxkaXYgY2xhc3M9InByb2dyZXNzLWl0ZW0iPicrCiAgICAgICAgICAnPHNwYW4+JytzdWJqLmVtb2ppKycgJytzdWJqLm5hbWUrJzwvc3Bhbj4nKwogICAgICAgICAgJzxkaXYgY2xhc3M9InBiYXIiPjxkaXYgY2xhc3M9InBiYXItZmlsbCBjLScrKHN1YmouY29sb3J8fCJwdXJwbGUiKSsnIiBzdHlsZT0id2lkdGg6JytwY3QrJyUiPjwvZGl2PjwvZGl2PicrCiAgICAgICAgICAnPHNwYW4+JytwY3QrJyUgKCcrZC5oaXRzKycvJytkLnRvdGFsKycpPC9zcGFuPjwvZGl2Pic7CiAgfQogIGlmKCFodG1sKWh0bWw9IjxwPkF1biBubyBoYXMgcmVzcG9uZGlkbyBwcmVndW50YXMuPC9wPiI7CiAgZGl2LmlubmVySFRNTD1odG1sOwp9").decode()
m=re.search(r"function renderProgress\(\)\{.+?\n\}",js,re.DOTALL)
if m:
    js=js[:m.start()]+RP+js[m.end():]
    fixes+=1
    print("[OK] renderProgress replaced")
else:
    print("[WARN] renderProgress not found")

# Fix 4: progress-scroll
if "progress-scroll" not in js:
    js=js.replace("function showPage(id){","function showPage(id){if(id===\"progress-scroll\"){showPage(\"home\");setTimeout(function(){var el=document.getElementById(\"progress-anchor\");if(el)el.scrollIntoView({behavior:\"smooth\"});},100);return;}")
    fixes+=1
    print("[OK] progress-scroll added")

# Fix 5: Extra functions
EF=base64.b64decode("CmZ1bmN0aW9uIGluaXROYXYoKXt2YXIgbmI9ZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgiLm5hdi1idG5bZGF0YS1wYWdlXSIpO2Zvcih2YXIgaT0wO2k8bmIubGVuZ3RoO2krKyl7bmJbaV0uYWRkRXZlbnRMaXN0ZW5lcigiY2xpY2siLGZ1bmN0aW9uKCl7c2hvd1BhZ2UodGhpcy5nZXRBdHRyaWJ1dGUoImRhdGEtcGFnZSIpKTt9KTt9fQpmdW5jdGlvbiBjaGVja09sbGFtYVN0YXR1cygpe3ZhciBkPWRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoIi5zdGF0dXMtZG90Iik7aWYoIWQpcmV0dXJuO2ZldGNoKCJodHRwOi8vbG9jYWxob3N0OjExNDM0IikudGhlbihmdW5jdGlvbigpe2QuY2xhc3NMaXN0LnJlbW92ZSgicmVkIik7ZC5jbGFzc0xpc3QuYWRkKCJncmVlbiIpO3ZhciB0PWRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoIi5zdGF0dXMtdGV4dCIpO2lmKHQpdC50ZXh0Q29udGVudD0iSUEgbG9jYWw6IENvbmVjdGFkYSI7fSkuY2F0Y2goZnVuY3Rpb24oKXtkLmNsYXNzTGlzdC5yZW1vdmUoImdyZWVuIik7ZC5jbGFzc0xpc3QuYWRkKCJyZWQiKTt2YXIgdD1kb2N1bWVudC5xdWVyeVNlbGVjdG9yKCIuc3RhdHVzLXRleHQiKTtpZih0KXQudGV4dENvbnRlbnQ9IklBIGxvY2FsOiBEZXNjb25lY3RhZGEiO30pO30KZnVuY3Rpb24gaW5pdFNldHRpbmdzKCl7dmFyIHM9ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoInF1aXpDb3VudCIpO2lmKHMpcy5hZGRFdmVudExpc3RlbmVyKCJjaGFuZ2UiLGZ1bmN0aW9uKCl7cXVpelNpemU9cGFyc2VJbnQodGhpcy52YWx1ZSl8fDEwO30pO3ZhciBjPWRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJjbGVhclByb2dyZXNzIik7aWYoYyljLmFkZEV2ZW50TGlzdGVuZXIoImNsaWNrIixmdW5jdGlvbigpe2lmKGNvbmZpcm0oIkJvcnJhciB0b2RvIGVsIHByb2dyZXNvPyIpKXtsb2NhbFN0b3JhZ2UucmVtb3ZlSXRlbSgic3Y0X3Byb2dyZXNzIik7bG9jYWxTdG9yYWdlLnJlbW92ZUl0ZW0oInN2NF9leGFtcyIpO3JlbmRlclByb2dyZXNzKCk7YWxlcnQoIlByb2dyZXNvIGJvcnJhZG8uIik7fX0pO30K").decode()
if "initNav" not in js:
    js=js.replace('document.addEventListener("DOMContentLoaded",function(){',EF+'\ndocument.addEventListener("DOMContentLoaded",function(){')
    if "initNav();" not in js:
        js=js.replace('showPage("home");','initNav();initSettings();checkOllamaStatus();setInterval(checkOllamaStatus,30000);showPage("home");')
    if "backSettings" not in js:
        js=js.replace('backData:"home"','backData:"home",backSettings:"home"')
    fixes+=1
    print("[OK] initNav+checkOllama+initSettings added")

# Fix 6: quizSize
if "quizSize" not in js:
    js=js.replace('"use strict";','"use strict";\nvar quizSize=10;')
    js=js.replace("Math.min(10,bank.length)","Math.min(quizSize||10,bank.length)")
    fixes+=1
    print("[OK] quizSize added")

# Fix 7: Remove old renderNav
if "function renderNav" in js and "nav.innerHTML" in js:
    m=re.search(r"function renderNav\(\)\{.+?\n\}",js,re.DOTALL)
    if m:
        js=js[:m.start()]+"// renderNav removed"+js[m.end():]
    js=js.replace("renderNav();","// nav removed;")
    fixes+=1
    print("[OK] old renderNav removed")

with open("app.js","w",encoding="utf-8") as f:
    f.write(js)

print()
print("=" * 50)
print(f"  {fixes} fixes aplicados")
print(f"  app.js: {len(js)} bytes")
print("=" * 50)
print("Recarga el navegador (Ctrl+Shift+R)")