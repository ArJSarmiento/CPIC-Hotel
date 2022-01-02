var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/static/hotelSystem/css/styles.css',
    '/static/hotelSystem/css/reserve_success.css',
    '/static/hotelSystem/img/CPIC.png',
    '/static/hotelSystem/img/error.png',
    '/offline',
    '/static/hotelSystem/fonts/Lato-Regular.ttf',
    '/static/hotelSystem/fonts/Poppins-Bold.ttf',
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
            .catch(err => console.log(err))
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request, { ignoreSearch: true })
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('offline');
            })
    )
});