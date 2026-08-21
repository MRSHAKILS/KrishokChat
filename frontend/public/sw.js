/* =========================================================================
   KrishokChat Service Worker (PWA Offline Shell — P6 hardening)
   
   Strategies (P6 / W7 — shell-only, per PRODUCTION_ROLLOUT_PLAN.md):
   1. Static Assets & Fonts: Cache-first
   2. Library & Dataset JSON: Stale-while-revalidate (offline fallback)
   3. App Pages: Network-first with Cache fallback
   Hard invariants:
   - NEVER cache `/sw.js` itself (would freeze updates)
   - NEVER cache `/api/*` or `/health` / POST streams (backend-dependent;
     offline chat is explicitly NOT supported — chat shows offline banner)
   - Precache shell only; chat/detect POSTs always go to network.
   Future: migrate to Serwist (@serwist/next 9.5.12, Next 16 official
   guidance 2026-07 — https://nextjs.org/docs/app/guides/progressive-web-apps
   + https://serwist.pages.dev/docs/next). Current worker is a minimal
   shell-only shim that satisfies W7 without the Serwist build step; the
   Serwist migration is a TODO tracked in frontend/README or inline below.
   ========================================================================= */

const CACHE_NAME = "krishokchat-cache-v1";

// P6: bump this when shell assets change so `activate` cleans old caches.
const STATIC_PRECACHE = [
  "/",
  "/favicon.ico",
  "/manifest.webmanifest",
  "/library",
  "/detect",
  "/chat",
  "/soil",
  "/library/catalog.json",
  "/library/datasets.json"
];

// Install: precache core shell & library JSON
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_PRECACHE).catch(() => {
        // Continue even if some individual resources fail
      });
    })
  );
  self.skipWaiting();
});

// Activate: clean up older caches
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

// Fetch: route-aware caching strategies
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  // P6 invariant: never cache the worker script itself and never cache API.
  if (
    url.pathname === "/sw.js" ||
    url.pathname.startsWith("/api/") ||
    url.pathname === "/health" ||
    url.pathname === "/readyz"
  ) {
    return;
  }

  // Ignore non-GET requests or chrome-extension / analytics
  if (event.request.method !== "GET" || !url.protocol.startsWith("http")) {
    return;
  }

  // Strategy A: Library JSON datasets (Stale-While-Revalidate)
  if (url.pathname.startsWith("/library/") && url.pathname.endsWith(".json")) {
    event.respondWith(
      caches.open(CACHE_NAME).then(async (cache) => {
        const cachedResponse = await cache.match(event.request);
        const fetchPromise = fetch(event.request)
          .then((networkResponse) => {
            if (networkResponse.ok) {
              cache.put(event.request, networkResponse.clone());
            }
            return networkResponse;
          })
          .catch(() => cachedResponse);

        return cachedResponse || fetchPromise;
      })
    );
    return;
  }

  // Strategy B: Static assets (fonts, images, icons) -> Cache-first
  if (
    url.pathname.startsWith("/_next/static/") ||
    url.pathname.match(/\.(woff2?|ttf|png|jpe?g|svg|ico|webp)$/)
  ) {
    event.respondWith(
      caches.match(event.request).then((cached) => {
        if (cached) return cached;
        return fetch(event.request).then((response) => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        });
      })
    );
    return;
  }

  // Strategy C: HTML Navigation & other pages -> Network-first with Cache fallback
  if (event.request.mode === "navigate") {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        })
        .catch(async () => {
          const cached = await caches.match(event.request);
          if (cached) return cached;
          const fallbackHome = await caches.match("/");
          return fallbackHome;
        })
    );
    return;
  }

  // Default: Network with Cache fallback
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});
