import time
import requests  # To make HTTP requests
from API_c2c import Plane_API
import json
from random import randrange

# Initialize Plane_API
P_API = Plane_API()
ENTRIES = 0
# Bounding box for the area of interest
BBOX = (-31.5, 34.5, 39.5, 71.2)
# Django server URL (replace with your actual Django server URL)
DJANGO_SERVER_URL = 'http://127.0.0.1:8080/api/tutorials'  # Example URL for Django API

def send_to_django(data,id):
    """Send plane data to Django server via a POST request."""
    
    data['Properties']["entry_id"] = id 
    try:
        response = requests.post(DJANGO_SERVER_URL, json=data)  # POST request with JSON payload
        if response.status_code == 201:
            pass
            #print("Data successfully sent to Django server.")
        else:
            
            print(f"Failed to send data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error connecting to Django server: {e}")

def main(): 
    
    while True:
        # Call the Plane API and get the response with plane states
        response = P_API.get_bbox_call(BBOX)
        if response is not None:
            states = response.states
            global ENTRIES
            ENTRIES+=1
            # Generate the JSON data for the planes (up to 1000 states)
            gp1_planes = P_API.generate_multiple_json(states)
            #print("Generated plane data:", json.loads(gp1_planes))
            # Send the generated plane data to the Django server
            
            for p in json.loads(gp1_planes):
                send_to_django(p,ENTRIES)
                
            
        else:
            print("No planes found in this area.")
            time.sleep(5)  # Sleep for 5 seconds before fetching again

if __name__ == '__main__':
    main()

