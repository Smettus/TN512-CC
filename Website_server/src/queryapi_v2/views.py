from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import os
import logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO # debug is too verbose
)

DJANGO_URL = os.environ.get('DJANGO_URL')

@csrf_exempt
def objects_within_bbox(request):
    if request.method == 'GET':
        # Retrieve query parameters from the URL
        objecttypes = request.GET.getlist('objecttypes')
        southwest_lat = request.GET.get('southwest_lat')
        southwest_lng = request.GET.get('southwest_lng')
        northeast_lat = request.GET.get('northeast_lat')
        northeast_lng = request.GET.get('northeast_lng')

        # Optional: Convert string values to float for coordinates
        try:
            southwest_lat = float(southwest_lat)
            southwest_lng = float(southwest_lng)
            northeast_lat = float(northeast_lat)
            northeast_lng = float(northeast_lng)
        except ValueError:
            return JsonResponse({'error': 'Invalid coordinate values'}, status=400)

        # Log the received query parameters for debugging
        logging.info(f"Received objecttypes: {objecttypes}")
        logging.info(f"Bounding box: ({southwest_lat}, {southwest_lng}), ({northeast_lat}, {northeast_lng})")


        # Prepare the data to be sent to the Django server
        request_data = {
            'apiversion': 'queryapi_v2',
            'objecttypes': objecttypes,
            'sw_lat': southwest_lat,
            'sw_lng': southwest_lng,
            'ne_lat': northeast_lat,
            'ne_lng': northeast_lng,
        }

        try:
            response = requests.get(DJANGO_URL, params=request_data)
            if response.status_code == 200:
                logging.info("Data successfully retrieved from DB api.")
                return JsonResponse(response.text,safe=False)
               
            else:
                print(f"Failed to send data. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            logging.info(f"Error connecting to DB api: {e}")


        # Fetch the data based on objecttypes and bounding box (implement logic to query your database)
        # Here you'd query the database based on objecttypes and bounding box coordinates

        # Simulated response for now (replace with actual database query)
        response_data = {
            'ships': [],
            'planes': [],
            'incidents': [],
        }
        return JsonResponse(response_data)
    
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

