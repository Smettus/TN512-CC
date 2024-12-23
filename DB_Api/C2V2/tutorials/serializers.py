from rest_framework import serializers 
from tutorials.models import Plane, Ship
 
 
class PlaneSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Plane
        fields = ('entry_id',
                'entity_id',
                'latitude',
                'longitude',
                'enemy',
                'time_position',
                'geo_altitude',
                'velocity',
                'true_track',
                'call_sign',
                'origin_country',
                'on_ground',
                'category',
                'size')

class ShipSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ship
        fields = ('entry_id',
                  'entity_id',
                  'latitude',
                  'longitude',
                  'enemy',
                  'time_position',
                  'SOG',
                  'COG')