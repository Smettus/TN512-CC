from db_api.models import Plane,Entities, AbstractIncident
from db_api.serializers import PlaneSerializer, ShipSerializer, AbstractIncidentSerializer
from rest_framework.response import Response
from rest_framework import status

import json
import logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class Handler():
    def __init__(self) -> None:
        pass
    
    def Plane(self,req):
        planes= req.data.get('Planes', None)  # DRF automatically handles JSON parsing
        for plane_data in json.loads(planes):
            # Ensure the entity_id exists in the request data
            plane_data = plane_data.get('Properties',None)
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
            else:    
                
                # If the data is invalid, return validation errors with HTTP 400 Bad Request status
                return Response(plane_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # Return the serialized data as a response with HTTP 201 Created status
        #logging.info(f"Saved planes.")
        return Response(plane_serializer.data, status=status.HTTP_201_CREATED)
    
    def Ship(self,req):
        Ships = json.loads(req.data.get('Ships', None)) 
       
        for ship_data in Ships:
            # Ensure the entity_id exists in the request data
            ship_data = ship_data.get('Properties',None)
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
            else:
                # If the data is invalid, return validation errors
                return Response(ship_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #logging.info(f"Saved ships.")
        return Response(ship_serializer.data, status=status.HTTP_201_CREATED)
    
    
    def Ground(self,req):
        pass
    def AbstractIncident(self, req):
        # why not refactor the rest? - both ships and planes are handled the same way
        # comes from incident_generator.py, over views.py to here
        try:
            # Get the dictionary from the request
            abstractincidents = req.data.get('Incidents', None)
            if not abstractincidents:
                raise ValueError('No "Incidents" key found in the request.')
        except Exception as e:
            return Response({'error': f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)

        # Process each incident (it's already a list of dictionaries)
        for incident_data in abstractincidents:
            incident_serializer = AbstractIncidentSerializer(data=incident_data)
            if incident_serializer.is_valid():
                incident_serializer.save()
                #logging.info(f"Saved incident to DB")
            else:
                logging.error(f"Failed to save incident: {incident_serializer.errors}")
                return Response(incident_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(incident_serializer.data, status=status.HTTP_201_CREATED)


    
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
                        "COG": obj.COG,
                        "ShipName": obj.ShipName
                    }
                }
                res.append(json_object)
        
        elif type == "Ground":
            pass
        elif type == "AbstractIncident":
            for obj in objects:
                json_object = {
                    "Type": type,
                    "Properties": {
                        "lat": obj.lat,
                        "lon": obj.lon,
                        "msg": obj.msg,
                        "time": obj.time
                    }
                }
                res.append(json_object)
        return res
    
    def is_in_bbox(self,lat, lng, bbox):
        sw_lng, sw_lat, ne_lng, ne_lat = bbox
    
        # Check if the latitude and longitude are within the bounding box
        return (sw_lat <= lat <= ne_lat) and (sw_lng <= lng <= ne_lng)

    def get_in_bbox(self,model,type,bbox):
        # check if table exists aka if there are entries
        if not model.objects.exists():
            print("The table is empty.")
            return []  # Return an empty list 
        
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
    def get_incidents_in_bbox(self, bbox, model=AbstractIncident, type="AbstractIncident"):
        # For now, need a seperate function, as it does not use the parent entry id thing like plane and ship
        
        # Do a filter on the db entries:
        sw_lng, sw_lat, ne_lng, ne_lat = bbox
        filtered_incidents = model.objects.filter(
            lat__gte=sw_lat,
            lat__lte=ne_lat,
            lon__gte=sw_lng,
            lon__lte=ne_lng
        )
        jsonifyed_incidents = self.generate_jsons(filtered_incidents, type)
        return jsonifyed_incidents