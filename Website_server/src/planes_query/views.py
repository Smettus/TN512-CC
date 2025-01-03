from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from .queries import fetch_planes_in_bbox
import os

DJANGO_URL = os.environ.get('DJANGO_URL')

@csrf_exempt  # Temporarily disable CSRF protection for simplicity
def planes_within_bbox(request):
    
    # phoah. we get a post request, but then do a get request to the backend, fix this
    if request.method =='POST':
        body = json.loads(request.body.decode('utf-8'))
        coordinates_array = [
            body['southwest']['lat'], body['southwest']['lng'],  # Southwest
            body['northeast']['lat'], body['northeast']['lng']   # Northeast
        ]
        data_get = {
            "Type": "bbox",
            "sw_lat": coordinates_array[0],
            "sw_lng": coordinates_array[1],
            "ne_lat": coordinates_array[2],
            "ne_lng": coordinates_array[3]
        }
        
        try:
            response = requests.get(DJANGO_URL, params=data_get)  # POST request with JSON payload
            if response.status_code == 200:
                print("Data successfully retrieved from the Django server.")
                return JsonResponse(response.text,safe=False)
               
            else:
                print(f"Failed to send data. Status code: {response.status_code}")
                print(f"Failed to send data. Status code: {response.text}")
        except Exception as e:
            print(f"Error connecting to Django server: {e}")
    print("Not good")
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

