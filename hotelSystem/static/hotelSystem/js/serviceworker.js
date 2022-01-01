// Base Service Worker implementation. To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py
var staticCacheName = "django-pwa-v" + new Date().getTime();
// Cache on install
self.addEventListener("install", (event) => {
    console.log("ServiceWorker Installed");
});

// Clear cache on activate
self.addEventListener("activate", (event) => {
    console.log("ServiceWorker Activated");
    event.waitUntil(
        caches.keys().then((cacheNames) => Promise.all(
            cacheNames.map((cache) => {
                if (cache !== staticCacheName) {
                    console.log("ServiceWorker Removing Cached Files from Cache - ", cache);
                    return caches.delete(cache);
                }
            })
        ))
    );
});

// Serve from Cache
self.addEventListener("fetch", (event) => {
    console.log("ServiceWorker Fetching");
    event.respondWith(
        fetch(event.request)
        .then((response) =>{
            const data = response.clone();
            caches
                .open(staticCacheName)
                .then((cache) => {
                    cache.put(event.request, data);
                })
            return response;
        })
        .catch(
            error => {
                console.log("ServiceWorker Network Request Failed. Serving from Cache - ", error);
                caches.match(event.request)
                .then(response => response)
            }
        )
    )
});