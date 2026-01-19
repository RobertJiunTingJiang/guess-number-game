self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open('guess-game-v1').then((cache) => {
            return cache.addAll(['/']);
        })
    );
});

self.addEventListener('fetch', (e) => {
    e.respondWith(
        fetch(e.request).catch(() => caches.match(e.request))
    );
});
