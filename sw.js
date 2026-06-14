var C="school-v4-v3";var A=["/index.html","/app.js","/styles.css"];
self.addEventListener("install",function(e){e.waitUntil(caches.open(C).then(function(c){return c.addAll(A)}))});
self.addEventListener("fetch",function(e){if(e.request.url.includes("11434"))return;e.respondWith(caches.match(e.request).then(function(r){return r||fetch(e.request)}))});
self.addEventListener("activate",function(e){e.waitUntil(caches.keys().then(function(n){return Promise.all(n.filter(function(k){return k!==C}).map(function(k){return caches.delete(k)}))}))});
