// ... (keep all your existing map setup, layer controls, and geocoder code the same until the layer groups) ...
// Setup the map - leaflet stuff
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

const addressSearchResults = new L.LayerGroup().addTo(map);

// Data layers
var airportLayerGroup = new L.LayerGroup().addTo(map);
var portLayerGroup = new L.LayerGroup().addTo(map);
var shipLayerGroup = new L.LayerGroup().addTo(map);
var planeLayerGroup = new L.LayerGroup().addTo(map);
var abstractIncidentLayerGroup = new L.LayerGroup().addTo(map);

// Replace the Markers array with MarkerMap
let MarkerMap = new Map();

// Fetching status flags
let isFetchingAirports = false;
let isFetchingPorts = false;
let isFetchingPlanes = false;
let isFetching = false;

// Keep your existing icon definitions and helper functions
const abstractIncident_icon = L.icon({
    iconUrl: staticUrl + 'icons/AbstractIncident_icon.svg',
    iconSize: [16, 16],
    iconAnchor: [20, 40],
    popupAnchor: [0, -40]
});

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

function getColorForAltitude(altitude) {
    if (isNaN(altitude)) return "green";
    if (altitude < 1000) return "#00ff00";
    if (altitude < 5000) return "#00bfff";
    if (altitude < 10000) return "#0000ff";
    if (altitude < 20000) return "#ff4500";
    return "#ff0000";
}

// Modify the airport update function to use MarkerMap
function updateAirportMarkers(airports, bbox) {
    const processedIds = new Set();

    airports.forEach(function(airport) {
        if (airport.latitude_deg && airport.longitude_deg && airport.type !== 'closed') {
            const lat = parseFloat(airport.latitude_deg);
            const lng = parseFloat(airport.longitude_deg);

            if (lat >= bbox.southwest.lat && lat <= bbox.northeast.lat &&
                lng >= bbox.southwest.lng && lng <= bbox.northeast.lng) {
                
                const airportId = `airport-${airport.iata_code || airport.gps_code}`;
                processedIds.add(airportId);

                let markerColor = 'blue';
                let markerSize = airport.type === 'large_airport' ? 30 :
                                airport.type === 'medium_airport' ? 20 :
                                airport.type === 'heliport' ? 10 :
                                airport.type === 'seaplane_base' ? 10 : 10;

                if (airport.type === 'heliport') markerColor = 'red';
                if (airport.type === 'seaplane_base') markerColor = 'green';

                const popupContent = `
                    <b>${airport.name}</b><br>
                    Code IATA : ${airport.iata_code}<br>
                    Code ICAO : ${airport.gps_code}<br>
                    Country : ${airport.country_name}<br>
                    City : ${airport.municipality}
                `;

                if (MarkerMap.has(airportId)) {
                    // Update existing marker
                    const marker = MarkerMap.get(airportId);
                    marker.setLatLng([lat, lng]);
                    marker.getPopup().setContent(popupContent);
                } else {
                    // Create new marker
                    const airportMarker = L.marker([lat, lng], {
                        icon: L.divIcon({
                            className: 'airport-marker',
                            html: `<div style="width: ${markerSize}px; height: ${markerSize}px; background-color: ${markerColor}; border-radius: 50%; border: 2px solid white;"></div>`,
                            iconSize: [markerSize, markerSize],
                            iconAnchor: [markerSize / 2, markerSize / 2],
                            popupAnchor: [0, -markerSize / 2]
                        })
                    }).addTo(airportLayerGroup).bindPopup(popupContent);

                    MarkerMap.set(airportId, airportMarker);
                }
            }
        }
    });

    // Remove airports that are no longer in view
    for (const [id, marker] of MarkerMap) {
        if (id.startsWith('airport-') && !processedIds.has(id)) {
            marker.remove();
            MarkerMap.delete(id);
        }
    }
}

// Similar modification for port markers
function updatePortMarkers(ports, bbox) {
    const processedIds = new Set();

    ports.forEach(function(port) {
        if (port.latitude && port.longitude) {
            const lat = parseFloat(port.latitude.toString().replace(',', '.'));
            const lng = parseFloat(port.longitude.toString().replace(',', '.'));

            if (lat >= bbox.southwest.lat && lat <= bbox.northeast.lat &&
                lng >= bbox.southwest.lng && lng <= bbox.northeast.lng) {
                
                const portId = `port-${port.code}`;
                processedIds.add(portId);

                const popupContent = `
                    <b>${port.portname}</b><br>
                    Code : ${port.code}<br>
                    Country : ${port.country}<br>
                `;

                if (MarkerMap.has(portId)) {
                    // Update existing marker
                    const marker = MarkerMap.get(portId);
                    marker.setLatLng([lat, lng]);
                    marker.getPopup().setContent(popupContent);
                } else {
                    // Create new marker
                    const portMarker = L.marker([lat, lng], {
                        icon: L.divIcon({
                            className: 'port-icon',
                            html: '<div style="background-color: blue; width: 20px; height: 20px; border-radius: 0%; border: 2px solid #fff;"></div>',
                            iconSize: [20, 20],
                            iconAnchor: [10, 10],
                            popupAnchor: [0, -10]
                        })
                    }).addTo(portLayerGroup).bindPopup(popupContent);

                    MarkerMap.set(portId, portMarker);
                }
            }
        }
    });

    // Remove ports that are no longer in view
    for (const [id, marker] of MarkerMap) {
        if (id.startsWith('port-') && !processedIds.has(id)) {
            marker.remove();
            MarkerMap.delete(id);
        }
    }
}

// Main updateMarkers function for dynamic objects (ships, planes, incidents)
function updateMarkers(Objects) {
    const processedIds = new Set();

    Objects.forEach(obj => {
        let markerId, lat, lng, properties;

        if (obj.Type === "Ship") {
            const { latitude, longitude, enemy, time_position, SOG, COG } = obj.Properties;
            markerId = `ship-${latitude}-${longitude}-${time_position}`;
            lat = latitude;
            lng = longitude;
            properties = { enemy, SOG, COG };

            if (lat && lng) updateShipMarker(obj, markerId, processedIds);

        } else if (obj.Type === "Plane") {
            const { latitude, longitude, call_sign } = obj.Properties;
            markerId = `plane-${call_sign}`;
            lat = latitude;
            lng = longitude;

            if (lat && lng) updatePlaneMarker(obj, markerId, processedIds);

        } else if (obj.Type === "AbstractIncident") {
            const { lat: ilat, lon: ilon, time } = obj.Properties;
            markerId = `incident-${time}-${ilat}-${ilon}`;
            lat = ilat;
            lng = ilon;

            if (lat && lng) updateIncidentMarker(obj, markerId, processedIds);
        }
    });

    // Remove markers that are no longer present
    for (const [id, marker] of MarkerMap) {
        if (!processedIds.has(id)) {
            marker.remove();
            MarkerMap.delete(id);
        }
    }
}

// Helper functions for updateMarkers
function updateShipMarker(obj, id, processedIds) {
    const { latitude, longitude, enemy, SOG, COG } = obj.Properties;
    processedIds.add(id);

    const track = isNaN(COG) ? 0 : parseFloat(COG);
    const shipColor = "#000000";

    if (MarkerMap.has(id)) {
        // Update existing marker
        const marker = MarkerMap.get(id);
        marker.setLatLng([latitude, longitude]);
        
        const icon = marker.getIcon();
        icon.options.html = `
            <svg width="15" height="15" viewBox="0 0 100 100" style="transform: rotate(${track}deg); display: block;">
                <polygon points="50,10 10,90 90,90" fill="${shipColor}" />
            </svg>
        `;
        marker.setIcon(icon);

        marker.getPopup().setContent(`
            <div style="text-align: center;">
                <p><b>Latitude:</b> ${latitude}°</p>
                <p><b>Longitude:</b> ${longitude}°</p>
                <p><b>Enemy:</b> ${enemy}</p>
                <p><b>SOG:</b> ${SOG}°</p>
                <p><b>COG:</b> ${COG}°</p>
            </div>
        `);
    } else {
        // Create new marker
        const triangleIcon = L.divIcon({
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
            .addTo(shipLayerGroup)
            .bindPopup(`
                <div style="text-align: center;">
                    <p><b>Latitude:</b> ${latitude}°</p>
                    <p><b>Longitude:</b> ${longitude}°</p>
                    <p><b>Enemy:</b> ${enemy}</p>
                    <p><b>SOG:</b> ${SOG}°</p>
                    <p><b>COG:</b> ${COG}°</p>
                </div>
            `);

        MarkerMap.set(id, marker);
    }
}

function updatePlaneMarker(obj, id, processedIds) {
    const { latitude, longitude, geo_altitude, call_sign, velocity, origin_country, true_track } = obj.Properties;
    processedIds.add(id);

    const track = isNaN(true_track) ? 0 : parseFloat(true_track);
    const planeColor = getColorForAltitude(parseFloat(geo_altitude));

    if (MarkerMap.has(id)) {
        // Update existing marker
        const marker = MarkerMap.get(id);
        marker.setLatLng([latitude, longitude]);
        
        const icon = marker.getIcon();
        icon.options.html = `
            <svg width="25" height="125" viewBox="0 0 512 512" style="transform: rotate(${track}deg); display: block;">
                <path d="M488.063,283.172l-178.016-83.078V68.938C310.047,37.391,287.547,0,256,0s-54.047,37.391-54.047,68.938
                    v131.156L23.938,283.172c-3.922,2.391-7.141,8.109-7.141,12.703v56.703c0,4.609,3.563,7.172,7.922,5.703l188.219-49.188
                    v119.281c0,0-30.609,22.438-48.953,34.688c-18.344,12.219-10.203,36.688,4.078,36.688c14.266,0,68.563,0,68.563,0
                    S245.797,512,256,512s19.375-12.25,19.375-12.25s54.297,0,68.563,0c14.281,0,22.422-24.469,4.078-36.688
                    c-18.344-12.25-48.953-34.688-48.953-34.688V309.094l188.203,49.188c4.375,1.469,7.938-1.094,7.938-5.703v-56.703
                    C495.203,291.281,492,285.563,488.063,283.172z" fill="${planeColor}" opacity="1"/>
            </svg>
        `;
        marker.setIcon(icon);

        marker.getPopup().setContent(`
            <div style="text-align: center;">
                <p><b>Latitude:</b> ${latitude}°</p>
                <p><b>Longitude:</b> ${longitude}°</p>
                <p><b>Altitude:</b> ${geo_altitude}</p>
                <p><b>Call Sign:</b> ${call_sign}</p>
                <p><b>Velocity:</b> ${velocity} m/s</p>
                <p><b>Origin:</b> ${origin_country}</p>
            </div>
        `);
    } else {
        // Create new marker
        const planeIcon = L.divIcon({
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

        MarkerMap.set(id, marker);
    }
}

function updateIncidentMarker(obj, id, processedIds) {
    const { lat, lon, msg, time } = obj.Properties;
    processedIds.add(id);

    if (MarkerMap.has(id)) {
        // Update existing marker
        const marker = MarkerMap.get(id);
        marker.setLatLng([lat, lon]);
        
        marker.getPopup().setContent(`
            <div style="text-align: center;">
                <p><b>Latitude:</b> ${lat}°</p>
                <p><b>Longitude:</b> ${lon}°</p>
                <p><b>Message:</b> ${msg}</p>
                <p><b>Time:</b> ${time}</p>
            </div>
        `);
    } else {
        // Create new marker
        const marker = L.marker([lat, lon], { icon: abstractIncident_icon })
            .addTo(abstractIncidentLayerGroup)
            .bindPopup(`
                <div style="text-align: center;">
                    <p><b>Latitude:</b> ${lat}°</p>
                    <p><b>Longitude:</b> ${lon}°</p>
                    <p><b>Message:</b> ${msg}</p>
                    <p><b>Time:</b> ${time}</p>
                </div>
            `);

        MarkerMap.set(id, marker);
    }
}

// Keep your existing fetch functions but modify their update calls
async function fetchData(objecttypes) {
    var bbox = getBoundingBox();
    var queryParams = new URLSearchParams();

    objecttypes.forEach(type => queryParams.append('objecttypes', type));
    queryParams.append('southwest_lat', bbox.southwest.lat);
    queryParams.append('southwest_lng', bbox.southwest.lng);
    queryParams.append('northeast_lat', bbox.northeast.lat);
    queryParams.append('northeast_lng', bbox.northeast.lng);

    var url = `/queryapi_v2/?${queryParams.toString()}`;

    if (isFetching) return;
    isFetching = true;

    try {
        const response = await fetch(url, {
            method: 'GET',
        });

        if (!response.ok) {
            console.error('Failed to fetch data:', response.status, response.text);
            return;
        }

        const objects = await response.json();
        updateMarkers(JSON.parse(objects));
    } catch (error) {
        console.error('Error fetching data:', error);
    } finally {
        isFetching = false;
    }
}

async function fetchAirportData() {
    var bbox = getBoundingBox();
    var payload = {
        southwest: { lat: bbox.southwest.lat, lng: bbox.southwest.lng },
        northeast: { lat: bbox.northeast.lat, lng: bbox.northeast.lng }
    };

    if (isFetchingAirports) return;
    isFetchingAirports = true;

    try {
        const response = await fetch('http://localhost:8000/static/js/world-airports.csv');
        const text = await response.text();

        Papa.parse(text, {
            header: true,
            dynamicTyping: true,
            complete: function(results) {
                updateAirportMarkers(results.data, payload);
            },
            error: function(error) {
                console.error("Error loading airport CSV: ", error);
            }
        });
    } catch (error) {
        console.error('Error fetching airports:', error);
    } finally {
        isFetchingAirports = false;
    }
}

async function fetchPortData() {
    var bbox = getBoundingBox();
    var payload = {
        southwest: { lat: bbox.southwest.lat, lng: bbox.southwest.lng },
        northeast: { lat: bbox.northeast.lat, lng: bbox.northeast.lng }
    };

    if (isFetchingPorts) return;
    isFetchingPorts = true;

    try {
        const response = await fetch('http://localhost:8000/static/js/GLOBAL_Ports.csv');
        const text = await response.text();

        Papa.parse(text, {
            header: true,
            dynamicTyping: true,
            complete: function(results) {
                updatePortMarkers(results.data, payload);
            },
            error: function(error) {
                console.error("Error loading ports CSV: ", error);
            }
        });
    } catch (error) {
        console.error('Error fetching ports:', error);
    } finally {
        isFetchingPorts = false;
    }
}

// Event handlers and initialization
let debounceTimer;
map.on('moveend', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        fetchData(["abstractincidents", "ships", "planes"]);
    }, 1000);
});

L.control.layers(baseLayers).addTo(map);

// Initial fetch
fetchData(["abstractincidents", "ships", "planes"]);

// Regular updates
setInterval(function() {
    fetchData(["abstractincidents", "ships", "planes"]);
}, 2000);