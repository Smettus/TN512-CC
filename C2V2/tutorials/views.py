from django.shortcuts import render
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

import json

from tutorials.models import Tutorial,Entities
from tutorials.serializers import TutorialSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):

    
    # GET list of tutorials, POST a new tutorial, DELETE all tutorials
    if request.method == 'GET':
        tutorials = Tutorial.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        
    # 'safe=False' for objects serialization    
    elif request.method == 'POST':
        # Directly access the parsed request data using DRF's request.data
        plane_data = request.data.get('Properties', None)  # DRF automatically handles JSON parsing
        print(plane_data)
        # Ensure the entity_id exists in the request data
        entity_id = plane_data.get('entity_id')
        
        if not entity_id:
            # If entity_id is missing, return an error
            return Response({'error': 'entity_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the entity already exists in the entities table, or create it if not
        entity, created = Entities.objects.get_or_create(
            entity_id=entity_id,  # Match on the entity_id in the Entities table
            defaults={'name': plane_data.get('call_sign'), 'type': 'Plane'}  # Default values if the entity is created
        )
        
        # Update the plane_data with the correct entity_id if needed
        plane_data['entity_id'] = entity.entity_id
        
        # Serialize the incoming plane data
        tutorial_serializer = TutorialSerializer(data=plane_data)
        
        # Check if the serialized data is valid
        if tutorial_serializer.is_valid():
            # Save the valid data to the database
            tutorial_serializer.save()
            
            # Return the serialized data as a response with HTTP 201 Created status
            return Response(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        
        # If the data is invalid, return validation errors with HTTP 400 Bad Request status
        return Response(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Tutorial.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    # find tutorial by pk (id)
    try: 
        tutorial = Tutorial.objects.get(pk=pk) 
    except Tutorial.DoesNotExist: 
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    # GET / PUT / DELETE tutorial
    if request.method == 'GET': 
        tutorial_serializer = TutorialSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
   
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        
@api_view(['GET'])
def tutorial_list_published(request):
    # GET all published tutorials
    tutorials = Tutorial.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)