// Setup the map
// todo get user location
var map = L.map('map', {
    center: [50.8446, 4.3933],
    zoom: 13,
    zoomcontrol: true
}) //.setView([50.8446, 4.3933], 13);
var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});
osmLayer.addTo(map); // be sure to load some layer
var satelliteLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
});
var darkmodeLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: ['a', 'b', 'c'],
    maxZoom: 19
})

//      - Layer control
var baseLayers = {
    "OpenStreetMap": osmLayer,
    "OSM - Dark": darkmodeLayer,
    "Satellite": satelliteLayer,
};
L.control.layers(baseLayers).addTo(map);


// container for address search results
const addressSearchResults = new L.LayerGroup().addTo(map);

/*** Geocoder ***/
// OSM Geocoder
const osmGeocoder = new L.Control.geocoder({
    collapsed: false,
    position: 'topright',
    text: 'Address Search',
    placeholder: 'Enter street address',
   defaultMarkGeocode: false
}).addTo(map);    

// handle geocoding result event
osmGeocoder.on('markgeocode', e => {
   // to review result object
   console.log(e);
   // coordinates for result
   const coords = [e.geocode.center.lat, e.geocode.center.lng];
   // center map on result
   map.setView(coords, 16);
   // popup for location
   // todo: use custom icon
   const resultMarker = L.marker(coords).addTo(map);
   // add popup to marker with result text
   resultMarker.bindPopup(e.geocode.name).openPopup();
});

let Markers = [];

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

let isFetching = false;

// Fetch plane data from the backend
async function fetchPlaneData() {
    var bbox = getBoundingBox();

    // Prepare the request payload
    var payload = {
        southwest: { lat: bbox.southwest.lat, lng: bbox.southwest.lng },
        northeast: { lat: bbox.northeast.lat, lng: bbox.northeast.lng }
    };

    if (isFetching) return; // Prevent overlapping calls
    isFetching = true;

    try {
        // Send POST request to the backend
        const response = await fetch('/planes_query/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Specify JSON format
            },
            body: JSON.stringify(payload) // Include payload as body
        });
    
        // Check the response status
        if (!response.ok) {
            console.error('Failed to fetch plane data:', response.status, response.statusText);
            return; // Stop execution here to avoid further processing
        }
    
        // Ensure the response body is read only once
        
        const Objects = await response.json();

        // Process the data (update map markers)
        updatePlaneMarkers(JSON.parse(Objects));
    } catch (error) {
        console.error('Error fetching plane data:', error);
    } finally {
        isFetching = false; // Allow new requests
    }
    
}

// Update the markers on the map based on the fetched data
function updatePlaneMarkers(Objects) {
    // Remove old markers
    Markers.forEach(marker => {
        map.removeLayer(marker);
    });
    Markers = [];

    // Function to determine color based on altitude
    function getColorForAltitude(altitude) {
        if (isNaN(altitude)) {
            return "green"; // Green for planes on the ground
        } else if (altitude < 1000) {
            return "#00ff00"; // Light green for low altitudes
        } else if (altitude < 5000) {
            return "#00bfff"; // Light blue for medium altitudes
        } else if (altitude < 10000) {
            return "#0000ff"; // Blue for intermediate altitudes
        } else if (altitude < 20000) {
            return "#ff4500"; // Orange for high altitudes
        } else {
            return "#ff0000"; // Red for very high altitudes
        }
    }
    
    // Add new markers
    Objects.forEach(obj => {
        if (obj.Type == "Plane"){
            const { latitude, longitude, geo_altitude, call_sign, velocity, origin_country, true_track } = obj.Properties;

            if (latitude && longitude) {
                // Determine icon color based on altitude
                let planeColor = getColorForAltitude(parseFloat(geo_altitude));
                let iconOpacity = 1; // Full opacity

                // Create a custom SVG icon
                var planeIcon = L.divIcon({
                    className: 'plane-icon', // Custom class for styling
                    html: `
                        <svg width="25" height="125" viewBox="0 0 512 512" style="transform: rotate(${true_track}deg); display: block;">
                            <path d="M488.063,283.172l-178.016-83.078V68.938C310.047,37.391,287.547,0,256,0s-54.047,37.391-54.047,68.938
                                v131.156L23.938,283.172c-3.922,2.391-7.141,8.109-7.141,12.703v56.703c0,4.609,3.563,7.172,7.922,5.703l188.219-49.188
                                v119.281c0,0-30.609,22.438-48.953,34.688c-18.344,12.219-10.203,36.688,4.078,36.688c14.266,0,68.563,0,68.563,0
                                S245.797,512,256,512s19.375-12.25,19.375-12.25s54.297,0,68.563,0c14.281,0,22.422-24.469,4.078-36.688
                                c-18.344-12.25-48.953-34.688-48.953-34.688V309.094l188.203,49.188c4.375,1.469,7.938-1.094,7.938-5.703v-56.703
                                C495.203,291.281,492,285.563,488.063,283.172z" fill="${planeColor}" opacity="${iconOpacity}"/>
                        </svg>
                    `,
                    iconSize: [25, 25],
                    iconAnchor: [12, 13]
                });

                // Create a marker with the custom icon
                const marker = L.marker([latitude, longitude], { icon: planeIcon })
                    .addTo(map)
                    .bindPopup(`
                        <div style="text-align: center;">
                            <img src="plane_icon.png" style="width: 100px; height: auto; border: none;" />
                            <p><b>Latitude:</b> ${latitude}°</p>
                            <p><b>Longitude:</b> ${longitude}°</p>
                            <p><b>Altitude:</b> ${geo_altitude}</p>
                            <p><b>Call Sign:</b> ${call_sign}</p>
                            <p><b>Velocity:</b> ${velocity} m/s</p>
                            <p><b>Origin:</b> ${origin_country}</p>
                        </div>
                    `);

                // Add marker to the array for later removal
                Markers.push(marker);
            } else {
                console.error("Invalid coordinates:", obj);
            }
        }else if(obj.Type == "Ship"){
            
            const { latitude, longitude, enemy, time_position, SOG, COG} = obj.Properties;
            
            const colors = ["#FF5733", "#33FF57", "#3357FF", "#FFFF33", "#FF33FF", "#33FFFF"];
            const randomIndex = Math.floor(Math.random() * colors.length);

            if (latitude && longitude) {
                // Determine icon color based on altitude
                let shipColor = "#000000"; // colors[randomIndex];
                let iconOpacity = 1; // Full opacity

                // Create a custom SVG icon
                var triangleIcon = L.divIcon({
                    className: 'triangle-icon', // Custom class for styling
                    html: `
                        <svg width="15" height="15" viewBox="0 0 100 100" style="transform: rotate(${COG}deg); display: block;">
                            <!-- A simple triangle pointing upwards -->
                            <polygon points="50,10 10,90 90,90" fill="${shipColor}" opacity="${iconOpacity}" />
                        </svg>
                    `,
                    iconSize: [15, 15], // Adjust as needed
                    iconAnchor: [15, 15] // Adjust anchor to center the icon
                });

                // Create a marker with the custom icon
                const marker = L.marker([latitude, longitude], { icon: triangleIcon })
                    .addTo(map)
                    .bindPopup(`
                        <div style="text-align: center;">
                            <img src="plane_icon.png" style="width: 100px; height: auto; border: none;" />
                            <p><b>Latitude:</b> ${latitude}°</p>
                            <p><b>Longitude:</b> ${longitude}°</p>
                            <p><b>enemy:</b> ${enemy}</p>
                            <p><b>SOG:</b> ${SOG}°</p>
                            <p><b>COG:</b> ${COG}°</p>
                        </div>
                    `);

                // Add marker to the array for later removal
                Markers.push(marker);
            }
        }
    });
}

// Call fetchPositions each time the map is moved
let debounceTimer;
map.on('moveend', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(fetchPlaneData, 500); // Prevent overlapping calls
});
// Call fetchPositions every 5 seconds
setInterval(fetchPlaneData, 5000);
