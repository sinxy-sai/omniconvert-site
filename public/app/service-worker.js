const CACHE = 'omniconvert-app-v1';
const SHELL = ['/app/', '/app/manifest.webmanifest', '/app/icons/icon-192.png', '/app/icons/icon-512.png'];
self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(SHELL)));
  self.skipWaiting();
});
self.addEventListener('activate', (event) => event.waitUntil(self.clients.claim()));
self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);
  const path = url.pathname;
  const isSameOrigin = url.origin === self.location.origin;
  const isStaticAsset = /\.(?:css|js|mjs|png|jpg|jpeg|webp|svg|ico|woff2?|ttf|webmanifest)$/.test(path);
  const isAppShell = path === '/app/' || path === '/app/manifest.webmanifest';
  if (request.method !== 'GET' || !isSameOrigin || path.startsWith('/api/') || path.startsWith('/uploads/') || path.startsWith('/downloads/') || (!isStaticAsset && !isAppShell)) return;
  event.respondWith(caches.match(request).then((cached) => cached || fetch(request).then((response) => {
    const copy = response.clone();
    caches.open(CACHE).then((cache) => cache.put(request, copy));
    return response;
  })));
});
