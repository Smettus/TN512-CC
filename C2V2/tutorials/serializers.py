from rest_framework import serializers 
from tutorials.models import Tutorial
 
 
class TutorialSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Tutorial
        fields = ('entity_id',
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
