from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from .queries import fetch_planes_in_bbox

@csrf_exempt  # Temporarily disable CSRF protection for simplicity
def planes_within_bbox(request):
    if request.method == 'POST':
        print("Building query to the database")
        try:
            # Parse the JSON payload
            data = json.loads(request.body)
            southwest = data.get('southwest')
            northeast = data.get('northeast')

            # Validate input
            if not southwest or not northeast:
                return JsonResponse({'error': 'Invalid bounding box'}, status=400)

            # Extract coordinates
            sw_lat, sw_lng = southwest['lat'], southwest['lng']
            ne_lat, ne_lng = northeast['lat'], northeast['lng']

            # Query the database
            planes = fetch_planes_in_bbox(sw_lat, sw_lng, ne_lat, ne_lng)

            # Return the result as JSON
            return JsonResponse(planes, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    if request.method =='GET':
        DJANGO_URL = "http://127.0.0.1:8080/api/tutorials"
        data_get = {"Type": "Latest_all"}
        try:
            response = requests.get(DJANGO_URL, params=data_get)  # POST request with JSON payload
            print(response.raw)
            if response.status_code == 200:
                print("Data successfully retrieved from the Django server.")
                return JsonResponse(response.text,safe=False)
               
            else:
                print(f"Failed to send data. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error connecting to Django server: {e}")
            
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

