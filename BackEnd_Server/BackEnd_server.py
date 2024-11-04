import asyncio
import websockets
import json
from API_c2c import Plane_API

valid_commands = ["POST", "GET", "INTERACTIVE", "QUIT"] 

# Used API's
P_API = Plane_API()

def handle_command(data):
    """
        Processes incoming command data and executes the corresponding action.

        This function retrieves the command and bounding box data from the input, checks
        if the command is valid, and if it is a "GET" command, it fetches state information 
        about planes within the specified bounding box. The function then generates a 
        JSON representation of the plane data.

        Parameters:
        data (dict): A dictionary containing command and data information. It is expected to have:
                    - 'command': The command string (e.g., "GET").
                    - 'data': The bounding box data for querying plane information.

        Returns:
        Will return the requested data 
        
        =============*** TO DO ***=============
        >>> Send json with the planes to geojson part of the application
    """
    
    
    command = data['command']
    bbox = data['data']
    print(f"The received command is: {command}")
    
    if command not in valid_commands:
        print(f"ERROR: {command} is not a valid command.")
        return 0
    
    if command == "GET":
        
        response = P_API.get_bbox_call(bbox)
        if response is not None:
            states = response.states
            #gp1_planes = P_API.generate_multiple_json(states[:1000]) "We put a certain limitation --> why ? "
            gp1_planes = P_API.generate_multiple_json(states)
            print(gp1_planes)
            return gp1_planes
        else:
            print("No planes found in this area.")
            return None

async def echo(websocket, path):
    """
        Asynchronously handles incoming WebSocket messages.

        This function listens for messages from the WebSocket connection, attempts to
        parse each message as JSON, and then processes the parsed data using the 
        `handle_command` function. It then sends the resulting data back to the client.

        Parameters:
        websocket (WebSocket): The WebSocket connection object through which messages are received and sent.
        path (str): The path of the WebSocket endpoint, used for routing (not used in this implementation).

        Returns:
        None
    """
    
    
    async for message in websocket:
        # convert message to json
        try:
            json_message = json.loads(message)
            # print(f"JSON Message: {json_message}")
        except json.JSONDecodeError:
            print("Error: The message is not a valid JSON")
            continue
        
        # handle the data and get response data
        response_data = handle_command(json_message)
        
        # Send the planes data back to the frontend if response_data exists
        if response_data:
            await websocket.send(json.dumps(response_data))
        else:
            await websocket.send("No data available for the given command.")

# Start the server
start_server = websockets.serve(echo, "localhost", 65432)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server listening on ws://localhost:65432")
asyncio.get_event_loop().run_forever()