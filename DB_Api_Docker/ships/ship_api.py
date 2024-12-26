import time
import asyncio
import requests
from API_c2c import ShipAPI
import json

# Django server URL (replace with your actual Django server URL)
DJANGO_SERVER_URL = 'http://127.0.0.1:8080/api/tutorials'
ENTRIES = 0
SHIP_API = ShipAPI()

def send_to_django(data, entry_id):
    """
    Send ship data to Django server via a POST request.
    """
    # Convert JSON string to dictionary if necessary
    if isinstance(data, str):
        data = json.loads(data)  # Parse JSON string into dictionary

    # Add the entry ID to the data
    data['Properties']["entry_id"] = entry_id

    try:
        # Send POST request to Django server
        response = requests.post(DJANGO_SERVER_URL, json=data)
        if response.status_code == 201:
            pass
        else:
            print(f"Failed to send data. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error connecting to Django server: {e}")

async def process_ships():
    """
    Fetch ship data asynchronously and send it to the Django server.
    """
    global ENTRIES
    ship_api = ShipAPI()
    while True:
        ships = await ship_api.connect_ais_stream(timeout=6)
        print(f"Found {len(ships)} ships")
        
        # un_val = len(list(set([ship['Properties']['entity_id'] for ship in ships])))
        # print("     Amount of unique values in here: " + str(un_val))
        ENTRIES += 1
        for ship in ships:
            send_to_django(ship, ENTRIES)
    """async for ship_data in ship_api.connect_ais_stream():
        
        print(ship_data)
        # send_to_django(ship_data, ENTRIES)
        # print(ship_data) # to test output of jsons
        await asyncio.sleep(5)"""


def main():
    """
    Start the asynchronous process for fetching and sending ship data.
    """
    asyncio.run(process_ships())

if __name__ == '__main__':
    main()