from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
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

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

