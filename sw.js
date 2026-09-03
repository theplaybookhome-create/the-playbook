/* THE PLAYBOOK — service worker v52b */
const CACHE = "playbook-v52b";
const PRECACHE = [
  "./",
  "./index.html",
  "./app.html",
  "./privacy.html",
  "./terms.html",
  "./support.html",
  "./school.html",
  "./offline.html",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png",
  "./icon-180.png",
  "./favicon.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await Promise.all(PRECACHE.map((url) => cache.add(url).catch(() => null)));
    // No skipWaiting — iPad Chrome + old app.html reloads to a white screen.
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)));
  })());
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (url.hostname.indexOf("supabase") >= 0) return;

  const isHTML = req.mode === "navigate" || url.pathname.endsWith(".html") || url.pathname === "/" || url.pathname.endsWith("/");

  if (isHTML) {
    event.respondWith(
      fetch(req)
        .then((res) => {
          if (res && res.status === 200) {
            const copy = res.clone();
            caches.open(CACHE).then((cache) => cache.put(req, copy));
          }
          return res;
        })
        .catch(() => caches.match(req).then((cached) => cached || caches.match("./offline.html")))
    );
    return;
  }

  event.respondWith(
    caches.match(req).then((cached) => {
      const network = fetch(req)
        .then((res) => {
          if (res && res.status === 200) {
            const copy = res.clone();
            caches.open(CACHE).then((cache) => cache.put(req, copy));
          }
          return res;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
});
