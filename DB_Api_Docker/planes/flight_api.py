import time
import requests  # To make HTTP requests
from API_c2c import Plane_API
import json
from random import randrange
import os

# Initialize Plane_API
P_API = Plane_API()
ENTRIES = int(os.environ.get("FLIGHT_ENTRY"))
# Bounding box for the area of interest
BBOX = (47.5294835476, 53.4750237087,0.51357303225, 8.15665815596) 
"""
THIS SI HOW THE API HANDLES A BBOX
OpenSkyApi._check_lat(bbox[0])
            OpenSkyApi._check_lat(bbox[1])
            OpenSkyApi._check_lon(bbox[2])
            OpenSkyApi._check_lon(bbox[3])

            params["lamin"] = bbox[0]
            params["lamax"] = bbox[1]
            params["lomin"] = bbox[2]
            params["lomax"] = bbox[3]
            
"""



# Django server URL (replace with your actual Django server URL)
#DJANGO_SERVER_URL = 'http://django:8080/api/tutorials'
DJANGO_SERVER_URL = os.environ.get('DJANGO_URL')

def send_to_django(data):
    """Send plane data to Django server via a POST request."""
    json_data = {
        "Type": 'Plane',
        "Planes" : data,
    }
    
    try:
        response = requests.post(DJANGO_SERVER_URL, json=json_data)  # POST request with JSON payload
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")  # Afficher le corps de la réponse
        if response.status_code == 201:
            print("Data successfully sent to Django server.")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error connecting to Django server: {e}")


def main(): 
    
    while True:
        print(BBOX)
        # Call the Plane API and get the response with plane states
        response = P_API.get_bbox_call(BBOX)
        if response is not None:
            states = response.states
            global ENTRIES
            ENTRIES+=1
            os.environ["FLIGHT_ENTRY"] = str(ENTRIES)
            # Generate the JSON data for the planes (up to 1000 states)
            gp1_planes = P_API.generate_multiple_json(states,ENTRIES)
            #print("Generated plane data:", json.loads(gp1_planes))
            # Send the generated plane data to the Django server
            
            
            send_to_django(gp1_planes)
                
            
        else:
            print("No planes found in this area.")
            time.sleep(5)  # Sleep for 5 seconds before fetching again

if __name__ == '__main__':
    main()

