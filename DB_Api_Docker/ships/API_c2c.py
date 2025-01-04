import json
import websockets
from datetime import datetime
import asyncio
import os 

class ShipAPI:
    def __init__(self):
        self.api_key = os.environ.get("KEY_SHIP_API")
        # Fixed bounding box for Belgium's territorial waters
        self.bbox = [[51.05, 2.10], [51.60, 3.40]]
        self.ships_dict = {}

    async def connect_ais_stream(self,timeout=2):
        """
        Async function to collect ship data
        """
        try:
            async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
                # Subscribe to the stream
                subscribe_message = {"APIKey": self.api_key, "BoundingBoxes": [self.bbox]}
                await websocket.send(json.dumps(subscribe_message))
                
                # Set end time for timeout
                end_time = asyncio.get_event_loop().time() + timeout
                
                while asyncio.get_event_loop().time() < end_time:
                    try:
                        # Set timeout for each message
                        message_json = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        message = json.loads(message_json)
                        
                        if message["MessageType"] == "PositionReport":
                            ais_message = message['Message']['PositionReport']
                            mmsi = ais_message.get('UserID')
                            if mmsi:
                                self.ships_dict[mmsi] = self.generate_ship_json(ais_message)
                    
                    except asyncio.TimeoutError:
                        continue  # Continue if we timeout waiting for a message
        
        except Exception as e:
            print(f"Error in collecting ships: {e}")
        
        # Convert all JSON strings back to dictionaries
        return [json.loads(ship_data) for ship_data in self.ships_dict.values()]
    from datetime import datetime

    def generate_ship_json(self, data):
        """
        Convert AIS data into JSON format for a ship.
        """
        # Convertir le timestamp en datetime UTC
        timestamp = datetime.utcfromtimestamp(data['Timestamp'])

        # Formatage selon le format attendu
        time_position_iso = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')  # Format ISO 8601 avec 'Z' pour UTC

        # Création de l'objet JSON
        json_object = {
            "Type": "Ship",
            "Properties": {
                "entry_id": None,
                "entity_id": data.get('UserID', None),  # unique MMSI nr
                "latitude": data.get('Latitude', None),
                "longitude": data.get('Longitude', None),
                "enemy": 0,
                "time_position": time_position_iso,
                "SOG": data.get('Sog', -1),
                "COG": data.get('Cog', -1)
            },
        }
        return json.dumps(json_object, indent=4)
