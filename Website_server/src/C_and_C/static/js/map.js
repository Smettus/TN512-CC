// Setup the map
var map = L.map('map', {
    center: [50.8446, 4.3933],
    zoom: 13,
    zoomcontrol: true
});

var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});
osmLayer.addTo(map);

var satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '&copy; <a href="https://www.esri.com/en-us/home">Esri</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
});

var darkmodeLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: ['a', 'b', 'c'],
    maxZoom: 19
});

// Layer control
var baseLayers = {
    "OpenStreetMap": osmLayer,
    "OSM - Dark": darkmodeLayer,
    "Satellite": satelliteLayer,
};

var planeLayerGroup = new L.LayerGroup().addTo(map);
var shipLayerGroup = new L.LayerGroup().addTo(map);
const addressSearchResults = new L.LayerGroup().addTo(map);

var airportLayerGroup = new L.LayerGroup().addTo(map); // Group for airport markers
var portLayerGroup = new L.LayerGroup().addTo(map); // Group for airport markers

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
   const coords = [e.geocode.center.lat, e.geocode.center.lng];
   map.setView(coords, 16);
   const resultMarker = L.marker(coords).addTo(map);
   resultMarker.bindPopup(e.geocode.name).openPopup();
});

let Markers = [];

// Get bounding box of current map view
function getBoundingBox() {
    var bounds = map.getBounds();
    return {
        southwest: bounds.getSouthWest(),
        northwest: { lat: bounds.getNorthEast().lat, lng: bounds.getSouthWest().lng },
        northeast: bounds.getNorthEast(),
        southeast: { lat: bounds.getSouthWest().lat, lng: bounds.getNorthEast().lng }
    };
}

let isFetchingAirports = false;
let isFetchingPorts = false;
let isFetchingPlanes = false;

// Fetch airport data based on bounding box
async function fetchAirportData() {
    var bbox = getBoundingBox();

    var payload = {
        southwest: { lat: bbox.southwest.lat, lng: bbox.southwest.lng },
        northeast: { lat: bbox.northeast.lat, lng: bbox.northeast.lng }
    };

    if (isFetchingAirports) return; // Prevent overlapping calls
    isFetchingAirports = true;

    try {
        const response = await fetch('http://localhost:8000/static/js/world-airports.csv'); // fix this... hardcoded
        const text = await response.text();

        Papa.parse(text, {
            header: true,
            dynamicTyping: true,
            complete: function(results) {
                updateAirportMarkers(results.data, payload);
            },
            error: function(error) {
                console.error("Erreur lors du chargement du CSV des aéroports : ", error);
            }
        });
    } catch (error) {
        console.error('Erreur de récupération des aéroports:', error);
    } finally {
        isFetchingAirports = false;
    }
}

// Update airport markers based on the fetched data and bounding box
function updateAirportMarkers(airports, bbox) {
    airportLayerGroup.clearLayers();  // Clear previous markers

    airports.forEach(function(airport) {
        // Check if the airport is within the bounding box and has valid coordinates
        if (airport.latitude_deg && airport.longitude_deg && airport.type !== 'closed') {
            const lat = parseFloat(airport.latitude_deg);
            const lng = parseFloat(airport.longitude_deg);

            // Check if the airport is within the bounding box
            if (
                lat >= bbox.southwest.lat && lat <= bbox.northeast.lat &&
                lng >= bbox.southwest.lng && lng <= bbox.northeast.lng
            ) {
                const popupContent = `
                    <b>${airport.name}</b><br>
                    Code IATA : ${airport.iata_code}<br>
                    Code ICAO : ${airport.gps_code}<br>
                    Country : ${airport.country_name}<br>
                    City : ${airport.municipality}
                `;

                // Define the color and size based on airport attributes
                let markerColor = 'blue';  // Default color for airports
                let markerSize = 20;  // Default size for airports

                if (airport.type === 'large_airport') {
                    markerSize = 30;  
                } else if (airport.type === 'medium_airport') {
                    markerSize = 20; 
                } else if (airport.type === 'small_airport') {
                    markerSize = 10; 
                } else if (airport.type === 'heliport') {
                    markerColor = 'red';
                    markerSize = 10;  
                } else if (airport.type === 'seaplane_base') {
                    markerColor = 'green';
                    markerSize = 10; 
                }

                // Create a base Leaflet marker with a custom style (circle with color)
                const airportMarker = L.marker([lat, lng], {
                    icon: L.divIcon({
                        className: 'airport-marker',  // Custom class for styling
                        html: `<div style="width: ${markerSize}px; height: ${markerSize}px; background-color: ${markerColor}; border-radius: 50%; border: 2px solid white;"></div>`, 
                        iconSize: [markerSize, markerSize],  // Dynamically set the size
                        iconAnchor: [markerSize / 2, markerSize / 2],  // Center the circle
                        popupAnchor: [0, -markerSize / 2]  // Position the popup above the marker
                    })
                });

                // Add the marker to the map and bind the popup
                airportMarker.addTo(airportLayerGroup)
                    .bindPopup(popupContent);
            }
        }
    });
}

async function fetchPortData() {
    var bbox = getBoundingBox();

    var payload = {
        southwest: { lat: bbox.southwest.lat, lng: bbox.southwest.lng },
        northeast: { lat: bbox.northeast.lat, lng: bbox.northeast.lng }
    };

    if (isFetchingPorts) return; // Prevent overlapping calls
    isFetchingPorts = true;

    try {
        const response = await fetch('http://localhost:8000/static/js/GLOBAL_Ports.csv');  // Mettez à jour le chemin du fichier CSV des ports xx fix this, hardcoded
        const text = await response.text();

        Papa.parse(text, {
            header: true,
            dynamicTyping: true,
            complete: function(results) {
                updatePortMarkers(results.data, payload);  // Appel à une fonction qui met à jour les marqueurs des ports
            },
            error: function(error) {
                console.error("Erreur lors du chargement du CSV des ports : ", error);
            }
        });
    } catch (error) {
        console.error('Erreur de récupération des ports:', error);
    } finally {
        isFetchingPorts = false;
    }
}

function updatePortMarkers(ports, bbox) {
    portLayerGroup.clearLayers();  // Clear previous markers

    ports.forEach(function(port) {
        // Assurez-vous que le port a des coordonnées valides et qu'il est dans la boîte de délimitation
        if (port.latitude && port.longitude) {
            // Assurez-vous que les coordonnées sont des chaînes et que les virgules sont remplacées par des points
            const lat = parseFloat(port.latitude.toString().replace(',', '.'));  // Remplace la virgule par un point
            const lng = parseFloat(port.longitude.toString().replace(',', '.'));  // Idem pour la longitude

            // Check if the port is within the bounding box
            if (
                lat >= bbox.southwest.lat && lat <= bbox.northeast.lat &&
                lng >= bbox.southwest.lng && lng <= bbox.northeast.lng
            ) {
                const popupContent = `
                    <b>${port.portname}</b><br>
                    Code : ${port.code}<br>
                    Country : ${port.country}<br>
                `;

                // Définir la couleur et la taille du marqueur en fonction des données du port
                let iconColor = 'blue';  // Couleur par défaut
                let markerSize = 20;  // Taille par défaut


                // Créer un icône personnalisé pour le port
                const portIcon = L.divIcon({
                    className: 'port-icon',  // Classe CSS pour styliser l'icône
                    html: `<div style="background-color: ${iconColor}; width: ${markerSize}px; height: ${markerSize}px; border-radius: 0%; border: 2px solid #fff;"></div>`, 
                    iconSize: [markerSize, markerSize],
                    iconAnchor: [markerSize / 2, markerSize / 2],
                    popupAnchor: [0, -markerSize / 2]
                });

                // Créer le marqueur avec l'icône personnalisé et l'ajouter au groupe de calques
                L.marker([lat, lng], { icon: portIcon })
                    .addTo(portLayerGroup)
                    .bindPopup(popupContent);
            }
        }
    });
}
// UGLY - fix this. There should be an option for the user to select which data he wants to see;
// if only planes, then only request the planes...
// Fetch plane data from the backend
async function fetchPlaneData() {
    var bbox = getBoundingBox();

    var payload = {
        southwest: { lat: bbox.southwest.lat, lng: bbox.southwest.lng },
        northeast: { lat: bbox.northeast.lat, lng: bbox.northeast.lng }
    };

    if (isFetchingPlanes) return; // Prevent overlapping calls
    isFetchingPlanes = true;

    try {
        const response = await fetch('/planes_query/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            console.error('Failed to fetch plane data:', response.status, response.text);
            return;
        }

        const Objects = await response.json();
        updatePlaneMarkers(JSON.parse(Objects));
    } catch (error) {
        console.error('Error fetching plane data:', error);
    } finally {
        isFetchingPlanes = false;
    }
}
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

// Update the plane markers on the map
function updatePlaneMarkers(Objects) {
    Markers.forEach(marker => {
        map.removeLayer(marker);
    });
    Markers = [];

    Objects.forEach(obj => {
        if (obj.Type == "Ship") {
            // Code pour gérer les navires
            const { latitude, longitude, enemy, time_position, SOG, COG } = obj.Properties;
    
            const shipColor = "#000000"; // Changez cela si nécessaire
            const track = isNaN(COG) ? 0 : parseFloat(COG);
    
            if (latitude && longitude) {
                var triangleIcon = L.divIcon({
                    className: 'triangle-icon',
                    html: `
                        <svg width="15" height="15" viewBox="0 0 100 100" style="transform: rotate(${track}deg); display: block;">
                            <polygon points="50,10 10,90 90,90" fill="${shipColor}" />
                        </svg>
                    `,
                    iconSize: [15, 15],
                    iconAnchor: [15, 15]
                });
    
                const marker = L.marker([latitude, longitude], { icon: triangleIcon })
                    .addTo(map)
                    .bindPopup(`
                        <div style="text-align: center;">
                            <p><b>Latitude:</b> ${latitude}°</p>
                            <p><b>Longitude:</b> ${longitude}°</p>
                            <p><b>Enemy:</b> ${enemy}</p>
                            <p><b>SOG:</b> ${SOG}°</p>
                            <p><b>COG:</b> ${COG}°</p>
                        </div>
                    `);
    
                Markers.push(marker);
            }
        } else if (obj.Type == "Plane") {
            const { latitude, longitude, geo_altitude, call_sign, velocity, origin_country, true_track } = obj.Properties;
    
            if (latitude && longitude) {
                let planeColor = getColorForAltitude(parseFloat(geo_altitude));
    
                // Assurez-vous que true_track est un nombre avant de l'utiliser
                const track = isNaN(true_track) ? 0 : parseFloat(true_track);
    
                var planeIcon = L.divIcon({
                    className: 'plane-icon',
                    html: `
                        <svg width="25" height="125" viewBox="0 0 512 512" style="transform: rotate(${track}deg); display: block;">
                            <path d="M488.063,283.172l-178.016-83.078V68.938C310.047,37.391,287.547,0,256,0s-54.047,37.391-54.047,68.938
                                v131.156L23.938,283.172c-3.922,2.391-7.141,8.109-7.141,12.703v56.703c0,4.609,3.563,7.172,7.922,5.703l188.219-49.188
                                v119.281c0,0-30.609,22.438-48.953,34.688c-18.344,12.219-10.203,36.688,4.078,36.688c14.266,0,68.563,0,68.563,0
                                S245.797,512,256,512s19.375-12.25,19.375-12.25s54.297,0,68.563,0c14.281,0,22.422-24.469,4.078-36.688
                                c-18.344-12.25-48.953-34.688-48.953-34.688V309.094l188.203,49.188c4.375,1.469,7.938-1.094,7.938-5.703v-56.703
                                C495.203,291.281,492,285.563,488.063,283.172z" fill="${planeColor}" opacity="1"/>
                        </svg>
                    `,
                    iconSize: [25, 25],
                    iconAnchor: [12, 13]
                });
    
                const marker = L.marker([latitude, longitude], { icon: planeIcon })
                    .addTo(planeLayerGroup)
                    .bindPopup(`
                        <div style="text-align: center;">
                            <p><b>Latitude:</b> ${latitude}°</p>
                            <p><b>Longitude:</b> ${longitude}°</p>
                            <p><b>Altitude:</b> ${geo_altitude}</p>
                            <p><b>Call Sign:</b> ${call_sign}</p>
                            <p><b>Velocity:</b> ${velocity} m/s</p>
                            <p><b>Origin:</b> ${origin_country}</p>
                        </div>
                    `);
    
                Markers.push(marker);
            }
        }
    });
    
}


// Call fetchPositions each time the map is moved
let debounceTimer;
map.on('moveend', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        //fetchAirportData();  // Fetch airports based on bounding box
        fetchPlaneData();    // Fetch plane data based on bounding box
        //fetchPortData();
    }, 500); // Prevent overlapping calls
});
L.control.layers(baseLayers).addTo(map);
// Initial fetch of airport and plane data
//fetchAirportData();
fetchPlaneData();
//fetchPortData();

setInterval(fetchPlaneData, 2000);