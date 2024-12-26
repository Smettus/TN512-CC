from tutorials.models import Plane,Entities
from tutorials.serializers import PlaneSerializer, ShipSerializer
from rest_framework.response import Response
from rest_framework import status

import json

class Handler():
    def __init__(self) -> None:
        pass
    
    def Plane(self,req):
        plane_data = req.data.get('Properties', None)  # DRF automatically handles JSON parsing
      
        # Ensure the entity_id exists in the request data
        
        entity_id = plane_data.get('entity_id')
        
        if not entity_id:
            # If entity_id is missing, return an error
            return Response({'error': 'entity_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the entity already exists in the entities table, or create it if not
        entity, created = Entities.objects.get_or_create(
            entity_id = entity_id,  # Match on the entity_id in the Entities table
            defaults={'name': plane_data.get('call_sign'), 'type': 'Plane'}  # Default values if the entity is created
        )
        
        # Update the plane_data with the correct entity_id if needed
        plane_data['entity_id'] = entity.entity_id
        # Serialize the incoming plane data
        plane_serializer = PlaneSerializer(data=plane_data)
        # Check if the serialized data is valid
        if plane_serializer.is_valid():
            # Save the valid data to the database
            plane_serializer.save()
            
            # Return the serialized data as a response with HTTP 201 Created status
            return Response(plane_serializer.data, status=status.HTTP_201_CREATED)
            
        # If the data is invalid, return validation errors with HTTP 400 Bad Request status
        return Response(plane_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def Ship(self,req):
        ship_data = req.data.get('Properties', None)  # DRF automatically handles JSON parsing

            # Ensure the entity_id exists in the request data
        entity_id = ship_data.get('entity_id')
        
        if not entity_id:
            # If entity_id is missing, return an error
            return Response({'error': 'entity_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the entity already exists in the entities table, or create it if not
        entity, created = Entities.objects.get_or_create(
            entity_id=entity_id,  # Match on the entity_id in the Entities table
            defaults={'name': ship_data.get('entity_id'), 'type': 'Ship'}  # Default values if the entity is created
        )
        
        # Update the ship_data with the correct entity_id if needed
        ship_data['entity_id'] = entity.entity_id

        # Serialize the incoming ship data
        ship_serializer = ShipSerializer(data=ship_data)

        # Check if the serialized data is valid
        if ship_serializer.is_valid():
            # Save the valid data to the database
            ship_serializer.save()
            return Response(ship_serializer.data, status=status.HTTP_201_CREATED)

        # If the data is invalid, return validation errors
        return Response(ship_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def Ground(self,req):
        pass
    
class Retriever():
    def __init__(self) -> None:
        pass
    
    def generate_jsons(self,objects,type):
        res = []
        
        if type == "Plane":
            for obj in objects:
                json_object = {
                    "Type": type,  # As per the example, this is fixed Will change for other type of objects
                    "Properties": {
                        "latitude": obj.latitude,
                        "longitude": obj.longitude,
                        "enemy": obj.enemy,  # Assuming False unless there's a reason to change it
                        "time_position": str(obj.time_position),
                        "geo_altitude": obj.geo_altitude,
                        "velocity": obj.velocity,
                        "true_track": obj.true_track,
                        "call_sign": obj.call_sign,
                        "origin_country": obj.origin_country ,
                        "on_ground": obj.on_ground,
                        "category": obj.category,
                        "size": obj.size  # Size based on category
                    }
                }
                
                res.append(json_object)
        
        elif type == "Ship":
            for obj in objects:
                json_object = {
                    "Type": type,  # As per the example, this is fixed Will change for other type of objects
                    "Properties": {
                        "latitude": obj.latitude,
                        "longitude": obj.longitude,
                        "enemy": obj.enemy,  # Assuming False unless there's a reason to change it
                        "time_position": str(obj.time_position),
                        "SOG": obj.SOG,
                        "COG": obj.COG
                    }
                }
                res.append(json_object)
        
        elif type == "Ground":
            pass
        

        return res
    
    def is_in_bbox(self,lat, lng, bbox):
        sw_lng, sw_lat, ne_lng, ne_lat = bbox
    
        # Check if the latitude and longitude are within the bounding box
        return (sw_lat <= lat <= ne_lat) and (sw_lng <= lng <= ne_lng)

    def get_in_bbox(self,model,type,bbox):
        # get latest entry_id
        entries = model.objects.order_by("-entry_id")
        latest_entry_id = entries[0].entry_id
        
        # get list with all planes that have this entry id 
        filtered_entries = entries.filter(entry_id__exact = latest_entry_id)
        in_bbox = []
        
        for obj in filtered_entries:
            lat = obj.latitude
            lon = obj.longitude
            
            if self.is_in_bbox(lat,lon,bbox):
                in_bbox.append(obj)
        
        json_entries = self.generate_jsons(in_bbox,type)
        
        return json_entries
    
    def get_latest(self,model,type):
        
        # get latest entry_id
        entries = model.objects.order_by("-entry_id")
        latest_entry_id = entries[0].entry_id
        
        # get list with all planes that have this entry id 
        filtered_entries = entries.filter(entry_id__exact = latest_entry_id)
        
        json_entries = self.generate_jsons(filtered_entries,type)
        
        return json_entries
         
        