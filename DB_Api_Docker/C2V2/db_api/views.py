from django.shortcuts import render
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from db_api.models import Plane,Entities, Ship, AbstractIncident
from db_api.serializers import PlaneSerializer
from rest_framework.decorators import api_view

from .HandleConnection import Handler, Retriever
import logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


@api_view(['GET', 'POST', 'DELETE'])
def db_list(request):
    handler = Handler()
    retriever = Retriever()
    # GET list of Plane, POST a new Plane, DELETE all Plane
    if request.method == 'GET':
        # CHECK TYPE OF GET REQUEST
        if request.GET.get('Type', None) == "Latest_all":
            latest_planes = retriever.get_latest(Plane,"Plane")
            latest_ships = retriever.get_latest(Ship,"Ships")
            # latest_ground = retriever.get_latest( <Ground Model> )
            # Create list of all the sub lists
            latest_all = latest_planes
            return JsonResponse(latest_all,safe = False)
        
        if request.GET.get('Type', None) == "bbox":
            # Retrieve the coordinates from the query parameters and store them in an array
            bbox_arr = (
                float(request.GET.get('sw_lng', 0)),  # Southwest longitude
                float(request.GET.get('sw_lat', 0)),  # Southwest latitude
                float(request.GET.get('ne_lng', 0)),  # Northeast longitude
                float(request.GET.get('ne_lat', 0))   # Northeast latitude
            )
            
            latest_planes = retriever.get_in_bbox(Plane,"Plane",bbox_arr)
           
            latest_ships = retriever.get_latest(Ship,"Ship")
            # latest_ground = retriever.get_latest( <Ground Model> )
            # Create list of all the sub lists
            latest_all = latest_planes + latest_ships
            
            return JsonResponse(latest_all,safe = False)
        # NEW API - works for all object types:
        if request.GET.get('apiversion', None) == "queryapi_v2":
            #logging.info(f'queryapi_v2 reached with {request}')
            requestedobjects = request.GET.getlist('objecttypes')
            logging.info(requestedobjects)
            
            bbox_arr = (
                float(request.GET.get('sw_lng', 0)),
                float(request.GET.get('sw_lat', 0)),
                float(request.GET.get('ne_lng', 0)),
                float(request.GET.get('ne_lat', 0))
            )
            
            response_objects = []
            for object in requestedobjects:
                if object == "planes":
                    latest_planes = retriever.get_in_bbox(Plane,"Plane",bbox_arr)
                    response_objects = response_objects + latest_planes
                elif object == "ships":
                    latest_ships = retriever.get_in_bbox(Ship,"Ship",bbox_arr)
                    response_objects = response_objects + latest_ships
                elif object == "abstractincidents":
                    latest_incidents = retriever.get_incidents_in_bbox(bbox_arr)
                    response_objects = response_objects + latest_incidents
            #logging.info(f'Response objects: {response_objects}')
            logging.info(f"Returned response objects")
            return JsonResponse(response_objects,safe = False)
        
    
    elif request.method == 'POST':
        if request.data.get('Type', None) == "Plane":
            return handler.Plane(request)
        elif request.data.get('Type', None) == "Ship":
            return handler.Ship(request)
        elif request.data.get('Type', None) == "Ground":
            return handler.Ground(request)
        elif request.data.get('Type', None) == "AbstractIncident":
            #logging.info("got the request, yeeeey")
            return handler.AbstractIncident(request)
        else:
            pass # here need to handle the error if the post does not exist, tell the client that requested it
        
    elif request.method == 'DELETE':
        count = Plane.objects.all().delete()
        return JsonResponse({'message': '{} Planes were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    
'''@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    # find Plane by pk (id)
    try: 
        plane = Plane.objects.get(pk=pk) 
    except Plane.DoesNotExist: 
        return JsonResponse({'message': 'The Plane does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    # GET / PUT / DELETE Plane
    if request.method == 'GET': 
        Plane_serializer = PlaneSerializer(Plane) 
        return JsonResponse(Plane_serializer.data) 
   
    elif request.method == 'PUT': 
        plane_data = JSONParser().parse(request) 
        plane_serializer = PlaneSerializer(plane, data=plane_data) 
        if plane_serializer.is_valid(): 
            plane_serializer.save() 
            return JsonResponse(plane_serializer.data) 
        return JsonResponse(plane_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    elif request.method == 'DELETE': 
        plane.delete() 
        return JsonResponse({'message': 'Plane was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
  '''      