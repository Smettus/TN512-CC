// Initialize the map and set its view to a default location
var map = L.map('map').setView([50.8446, 4.3933], 13);

// Set up the OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Check if Geolocation is supported
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        function(position) {
            var userLat = position.coords.latitude;
            var userLng = position.coords.longitude;

            // Set the map view to the user's location
            map.setView([userLat, userLng], 13);

            // Add a marker for the user's location
            L.marker([userLat, userLng]).addTo(map)
                .bindPopup('You are here!')
                .openPopup();
        },
        function() {
            alert('Unable to retrieve your location.');
        }
    );
} else {
    alert('Geolocation is not supported by this browser.');
}

