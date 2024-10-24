// See documentation: https://leafletjs.com/reference.html


// Setup the map
var map = L.map('map', {
    center: [50.8446, 4.3933],
    zoom: 13,
    zoomcontrol: true
}) //.setView([50.8446, 4.3933], 13);

var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});

var satelliteLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
});

osmLayer.addTo(map);

//      - Layer control
var baseLayers = {
    "OpenStreetMap": osmLayer,
    "Satellite": satelliteLayer
};
L.control.layers(baseLayers).addTo(map);


//      - Component layers (Plane, Ship, Groundtroops)
// XXX TODO
// Placeholder geojson
/*
https://leafletjs.com/reference.html#geojson
var geojson_planes


var geojsonLayer = L.geoJSON(geojson_planes, {
    onEachFeature: function (feature, layer) {
        // Bind a popup to each feature
        if (feature.properties && feature.properties.name) {
            layer.bindPopup(feature.properties.name + ': ' + feature.properties.description);
        }
    }
}).addTo(map);


//https://leafletjs.com/reference.html#marker
// for adding markers
*/

// Function to initially connect to the back end server
function connectSocket(s){
    s.addEventListener('open', function (event) {
        console.log('Connected to the WebSocket server');
        s.send('Hello from JavaScript Client!');
    });
}



// Upon map move -> api call
function getBoundingBox() {
    var bounds = map.getBounds();
    return {
        southwest: bounds.getSouthWest(),
        northwest: { lat: bounds.getNorthEast().lat, lng: bounds.getSouthWest().lng },
        northeast: bounds.getNorthEast(),
        southeast: { lat: bounds.getSouthWest().lat, lng: bounds.getNorthEast().lng }
    };
}

// Function to covnert the bbox to with command to a json
function createJson(data_input, command = 'GET') {
    const result = {
        command: command,
        data: data_input
    };

    return JSON.stringify(result);
}


// Create a WebSocket client
const socket = new WebSocket('ws://localhost:65432');
// Connect client to server and check if connected on server!
connectSocket(socket)

function fetchPositions() {
    var bbox = getBoundingBox();
    var bboxString = `${bbox.southwest.lng},${bbox.southwest.lat},${bbox.northwest.lng},${bbox.northwest.lat},${bbox.northeast.lng},${bbox.northeast.lat},${bbox.southeast.lng},${bbox.southeast.lat}`;


    // TODO: how will fetchPositions talk to the backend?
    //      decide upon format
    // Make a POST request to the backend
    console.log('Bounding Box:', bbox);

    // Check if the socket is open before sending
    if (socket.readyState === WebSocket.OPEN) {
        console.log('Sending bbox to the backend server');
        const jsonBbox = createJson(bbox)

        socket.send(jsonBbox);
    } else {
        console.log('WebSocket is not open. Current state:', socket.readyState);
    }

}



map.on('moveend', fetchPositions);










// TODO: add to ask browser location
/* // Check if Geolocation is supported
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
 */
