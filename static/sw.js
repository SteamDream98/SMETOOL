// Service Worker for SME Debt Management Tool
const CACHE_NAME = 'sme-debt-tool-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/js/calculations.js',
    '/static/favicon.ico',
    '/static/manifest.json',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://cdn.jsdelivr.net/npm/chart.js'
];

// Install event - cache resources
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                // Return cached version or fetch from network
                if (response) {
                    return response;
                }
                
                // Clone the request
                const fetchRequest = event.request.clone();
                
                return fetch(fetchRequest).then(function(response) {
                    // Check if valid response
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }
                    
                    // Clone the response
                    const responseToCache = response.clone();
                    
                    caches.open(CACHE_NAME)
                        .then(function(cache) {
                            cache.put(event.request, responseToCache);
                        });
                    
                    return response;
                }).catch(function() {
                    // Return offline page for navigation requests
                    if (event.request.destination === 'document') {
                        return caches.match('/');
                    }
                });
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Background sync for offline calculations
self.addEventListener('sync', function(event) {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

function doBackgroundSync() {
    // Sync any offline calculations when back online
    return new Promise(function(resolve) {
        // Get offline calculations from IndexedDB
        const offlineCalculations = JSON.parse(localStorage.getItem('offlineCalculations') || '[]');
        
        if (offlineCalculations.length > 0) {
            // Process offline calculations
            offlineCalculations.forEach(function(calculation) {
                // Save to main calculations
                const calculations = JSON.parse(localStorage.getItem('smeCalculations') || '{}');
                if (!calculations[calculation.type]) {
                    calculations[calculation.type] = [];
                }
                calculations[calculation.type].unshift(calculation);
                localStorage.setItem('smeCalculations', JSON.stringify(calculations));
            });
            
            // Clear offline calculations
            localStorage.removeItem('offlineCalculations');
        }
        
        resolve();
    });
}

// Push notifications for important updates
self.addEventListener('push', function(event) {
    const options = {
        body: event.data ? event.data.text() : 'New calculation results available',
        icon: '/static/favicon-192x192.png',
        badge: '/static/favicon-32x32.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'View Results',
                icon: '/static/favicon-32x32.png'
            },
            {
                action: 'close',
                title: 'Close',
                icon: '/static/favicon-32x32.png'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('SME Debt Tool', options)
    );
});

// Notification click handling
self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    
    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});
