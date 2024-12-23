import base64
from opensky_api import OpenSkyApi
import json
import websockets
from datetime import datetime
import asyncio

class Plane_API():
    def __init__(self) -> None:
        pw_enc = self.get_password()
        self.api = OpenSkyApi("SaYo",base64.b64decode(pw_enc).decode("utf-8"))
    
    def get_password(self):
        file_name = 'secret.txt'

        try:
            with open(file_name, 'r') as file:
                content = file.read()
                
        except FileNotFoundError:
            print(f"The file '{file_name}' was not found.")
        except IOError:
            print(f"An error occurred while trying to read the file '{file_name}'.")
            
        return content
    
    
    def get_bbox_tuple(self,bbox):
            """
                Extracts the minimum and maximum latitude and longitude values from a geographical bounding box.

                Parameters:
                bbox (dict): A dictionary containing the geographical bounding box coordinates. The expected structure is:
                {
                    'southwest': {'lat': <latitude>, 'lng': <longitude>},
                    'northwest': {'lat': <latitude>, 'lng': <longitude>},
                    'northeast': {'lat': <latitude>, 'lng': <longitude>},
                    'southeast': {'lat': <latitude>, 'lng': <longitude>}
                }

                Returns:
                tuple: A tuple containing the minimum and maximum latitude and longitude values in the format
                    (min_latitude, max_latitude, min_longitude, max_longitude).
                
                Example:
                >>> bbox = {
                        'southwest': {'lat': 34.0522, 'lng': -118.2437},
                        'northwest': {'lat': 34.0522, 'lng': -118.1234},
                        'northeast': {'lat': 34.1922, 'lng': -118.1234},
                        'southeast': {'lat': 34.1922, 'lng': -118.2437}
                    }
                >>> get_bbox_tuple(bbox)
                (34.0522, 34.1922, -118.2437, -118.1234)
            """
            
            
            latitudes = [
                bbox['southwest']['lat'],
                bbox['northwest']['lat'],
                bbox['northeast']['lat'],
                bbox['southeast']['lat']
            ]

            longitudes = [
                bbox['southwest']['lng'],
                bbox['northwest']['lng'],
                bbox['northeast']['lng'],
                bbox['southeast']['lng']
            ]

            # Calculate min and max
            min_latitude = min(latitudes)
            max_latitude = max(latitudes)
            min_longitude = min(longitudes)
            max_longitude = max(longitudes)

            return (min_latitude, max_latitude, min_longitude, max_longitude)
        
        
    def get_bbox_call(self, bbox) -> list:
        """
            Retrieves a list of states within the specified geographical bounding box.

            This method uses the bounding box coordinates extracted from the provided
            `bbox` argument to call an API and fetch relevant state data.

            Parameters:
            bbox (dict): A dictionary containing the geographical bounding box coordinates. The expected structure is:
            {
                'southwest': {'lat': <latitude>, 'lng': <longitude>},
                'northwest': {'lat': <latitude>, 'lng': <longitude>},
                'northeast': {'lat': <latitude>, 'lng': <longitude>},
                'southeast': {'lat': <latitude>, 'lng': <longitude>}
            }

            Returns:
            list or None: A list of states within the bounding box if found; otherwise, returns None.
        """
        
        if type(bbox) == tuple:
            states = self.api.get_states(bbox=bbox)
        else:
            states = self.api.get_states(bbox=self.get_bbox_tuple(bbox))
        
        if states is None:
            return None
        else:
            return states
    
    def generate_json(self,data):
        """
            Convert an object of data received from the OpenSky API into a JSON object.

            This function extracts relevant information from the provided data object,
            formats the time in ISO 8601, and constructs a JSON-compatible dictionary
            that includes the predefined information about the plane.

            Parameters:
            data (object): An object containing the data of one plane. It is expected to have 
                        the following attributes:
                        - time_position: UNIX timestamp of the position
                        - latitude: Latitude of the plane
                        - longitude: Longitude of the plane
                        - geo_altitude: Geographical altitude of the plane
                        - velocity: Velocity of the plane
                        - true_track: True track of the plane
                        - callsign: Callsign of the plane
                        - origin_country: Country of origin
                        - on_ground: Boolean indicating if the plane is on the ground
                        - category: Category of the plane

            Returns:
            dict: A JSON-compatible dictionary containing the predefined information 
                about the plane, including coordinates, properties, and type.
        """
        
        
        # Convert UNIX time to ISO 8601 format (UTC)
        time_position_iso = datetime.utcfromtimestamp(data.time_position).isoformat('Z')
        json_object = {
            "Type": "Plane",  # As per the example, this is fixed Will change for other type of objects
            "Properties": {
                "entry_id":None,
                "entity_id": int(data.icao24,16),
                "latitude": data.latitude,
                "longitude": data.longitude,
                "enemy": 0,  # Assuming False unless there's a reason to change it
                "time_position": time_position_iso,
                "geo_altitude": data.geo_altitude if data.geo_altitude != None else -1,
                "velocity": data.velocity,
                "true_track": data.true_track,
                "call_sign": data.callsign.split()[0] if data.callsign.split() else "0", # Note that the call sign is not the call sign receiveed from the API but the ICAO24 id!!!!!!!!!!!!!!
                "origin_country": data.origin_country ,
                "on_ground": 0 if data.on_ground else 1,
                "category": data.category,
                "size": "Large" if data.category >= 1 else "Small"  # Size based on category
            }
        }
        
        # if this funciton is not used in another function then return the json.dumps(json_object, indent = 4)
        return json_object
    
    def generate_multiple_json(self, data_list, output_filename = 0):
        """
            Convert multiple data objects to a single JSON file with an array of JSON objects.

            This function processes a list of data objects, converting each to a JSON object
            using the `generate_json` method, and optionally writes the resulting array of
            JSON objects to a specified file.

            Parameters:
            data_list (list): A list of objects containing the data of multiple planes or entities. 
                            Each object is expected to have the required attributes as defined 
                            in the `generate_json` method.
            output_filename (str, optional): The name of the JSON file to write the result to. 
                                            If set to 0 (default), the function does not write 
                                            to a file.

            Returns:
            str: A JSON string containing all data entries in the predefined JSON format if 
                `output_filename` is not provided; otherwise, returns None.
        """
        
        
        json_list = []  # List to store all JSON objects
        
        for data in data_list:
            json_object = self.generate_json(data)  # Call the function for each data object
            json_list.append(json_object)      # Append the resulting JSON to the list
        
        # Write the list of JSON objects to a file
        if output_filename:
            with open(output_filename, 'w') as outfile:
                json.dump(json_list, outfile, indent=4)
            
            print(f"JSON file '{output_filename}' created successfully with {len(data_list)} entries.")
        
        return json.dumps(json_list, indent = 4)
    
class ShipAPI:
    def __init__(self):
        self.api_key = self.get_password()
        # Fixed bounding box for Belgium's territorial waters
        self.bbox = [[51.05, 2.10], [51.60, 3.40]]
        self.ships_dict = {}
        
    def get_password(self):
        file_name = 'AIS_API_key.txt'

        try:
            with open(file_name, 'r') as file:
                content = file.read().strip()
        except FileNotFoundError:
            print(f"The file '{file_name}' was not found.")
            content = None
        except IOError:
            print(f"An error occurred while trying to read the file '{file_name}'.")
            content = None
        return content

    async def connect_ais_stream(self, timeout=2):
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

    def generate_ship_json(self, data):
        """
        Convert AIS data into JSON format for a ship.
        """
        time_position_iso = datetime.utcfromtimestamp(data['Timestamp']).isoformat('Z')
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
