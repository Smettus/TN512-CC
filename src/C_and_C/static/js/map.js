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

// Function to initially connect to the back end server
// Tableau pour stocker les marqueurs d'avion
let planeMarkers = [];

/*
 function connectSocket(s) {
    s.addEventListener('open', function (event) {
        console.log('Connected to the WebSocket server');
        s.send('Hello from JavaScript Client!');
    });

    s.addEventListener('message', function (event) {
        try {
            // Parse the incoming JSON data
            const planes_string = JSON.parse(event.data);
            const planes = JSON.parse(planes_string); // double encoding when data is received so need to parse it twice

            // Supprimer les anciens marqueurs de la carte
            planeMarkers.forEach(marker => {
                map.removeLayer(marker);
            });

            // Vider le tableau des marqueurs
            planeMarkers = [];

            // Loop through the planes and add markers for each one
            planes.forEach(plane => {
                const { lat, lon } = plane.Coordinates;
                const { Call_sign, Velocity, Origin_country, True_track, Geo_altitude } = plane.Properties;

                // Définir la couleur en fonction de l'altitude
               // Détermine la couleur de l'icône en fonction de l'altitude
               function getColorForAltitude(altitude) {
                if (isNaN(altitude)) {
                    return "green"; // Vert pour les avions au sol
                }
                else if (altitude < 1000) {
                    return "#00ff00"; // Vert clair pour les basses altitudes
                }
                else if (altitude < 5000) {
                    return "#00bfff"; // Bleu clair pour altitudes moyennes
                }
                else if (altitude < 10000) {
                    return "#0000ff"; // Bleu pour altitudes intermédiaires
                }
                else if (altitude < 20000) {
                    return "#ff4500"; // Orange pour hautes altitudes
                }
                else {
                    return "#ff0000"; // Rouge pour très hautes altitudes
                }
            }

            let planeColor = getColorForAltitude(parseFloat(Geo_altitude));
            let iconOpacity = 1; // Set to 1 for full opacity or adjust as needed

            var planeIcon = L.divIcon({
                className: 'plane-icon', // Custom class for the icon
                html: `
                    <svg width="25" height="125" viewBox="0 0 512 512" style="transform: rotate(${True_track}deg); display: block;">
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

            // CSS to remove the default box
            const style = document.createElement('style');
            style.innerHTML = `
                .plane-icon {
                    background: none; //Remove background
                    border: none; // Remove border
                }
            `;
            document.head.appendChild(style);


                // Ajouter le marqueur avec le nouvel icon coloré
                if (lat && lon) {
                    const marker = L.marker([lat, lon], { icon: planeIcon })
                        .addTo(map)
                        .bindPopup(`
                            <div style="text-align: center;">
                                <img src="plane_icon.png" style="width: 100px; height: auto; border: none;" />
                                <p><b>Latitude:</b> ${lat}°</p>
                                <p><b>Longitude:</b> ${lon}°</p>
                                <p><b>Altitude:</b> ${Geo_altitude}</p>
                                <p><b>Call Sign:</b> ${Call_sign}</p>
                                <p><b>Velocity:</b> ${Velocity} m/s</p>
                                <p><b>Origin:</b> ${Origin_country}</p>
                            </div>
                        `);

                    // Ajouter le marqueur au tableau pour suppression ultérieure
                    planeMarkers.push(marker);
                } else {
                    console.error("Invalid coordinates:", plane);
                }
            });

        } catch (error) {
            console.error("Error parsing data or adding markers:", error);
        }
    });
}
*/

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

// Function to convert the bbox to with command to a json
function createJson(data_input, command = 'GET') {
    const result = {
        command: command,
        data: data_input
    };

    return JSON.stringify(result);
}

/*
// Create a WebSocket client
const socket = new WebSocket('ws://localhost:65432');
// Connect client to server and check if connected on server!
connectSocket(socket)
*/

/*
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
*/

/*
// Call fetchPositions each time the map is moved
map.on('moveend', fetchPositions);
// Call fetchPositions every 5 seconds
setInterval(fetchPositions, 500);
*/