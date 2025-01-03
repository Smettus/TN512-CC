import time
import asyncio
import requests
from API_c2c import ShipAPI
import json
import os
import logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO # debug is too verbose
)


# Django server URL (replace with your actual Django server URL)
#DJANGO_SERVER_URL = 'http://127.0.0.1:8080/api/tutorials'
#DJANGO_SERVER_URL = 'http://django_app:8080/api/tutorials'

DJANGO_SERVER_URL = os.environ.get('DJANGO_URL')
ENTRIES = int(os.environ.get("SHIP_ENTRY"))
SHIP_API = ShipAPI()

def send_to_django(data):
    """
    Send ship data to Django server via a POST request.
    """
    # Convert JSON string to dictionary if necessary
    #if isinstance(data, str):
    #    data = json.loads(data)  # Parse JSON string into dictionary

    # Add the entry ID to the data
    # data['Properties']["entry_id"] = entry_id
    print(f"Found {len(data)} ships")
    logging.info(f"Found {len(data)} ships")
    json_data = {
        'Type': "Ship",
        'Ships': json.dumps(data,indent=4),
    }
    #logging.info(json_data)
    try:
        # Send POST request to Django server
        response = requests.post(DJANGO_SERVER_URL, json=json_data)
        if response.status_code == 201:
            logging.info("Data sent to DB.")
            print("Data successfully sent to Django server.")
            pass
        else:
            logging.info(f"Failed to send data. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.info(f"Error connecting to Django server: {e}")

async def process_ships():
    """
    Fetch ship data asynchronously and send it to the Django server.
    """
    
    ship_api = ShipAPI()
    
    while True:
        global ENTRIES
        ENTRIES += 1
        
        os.environ["SHIP_ENTRY"] = str(ENTRIES)
        
        ships = await ship_api.connect_ais_stream(timeout=6)
        for s in ships:
            s["Properties"]["entry_id"] = ENTRIES
           
        
        send_to_django(ships)


def main():
    """
    Start the asynchronous process for fetching and sending ship data.
    """
    asyncio.run(process_ships())

if __name__ == '__main__':
    main()