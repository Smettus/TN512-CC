from django.db import models

# Create your models here.
class Plane(models.Model):
    plane_id = models.AutoField(primary_key=True)
    entry_id = models.IntegerField()
    entity_id = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    enemy = models.IntegerField()
    time_position = models.DateTimeField(max_length=255)
    geo_altitude = models.FloatField()
    velocity = models.FloatField()
    true_track = models.FloatField()
    call_sign = models.CharField(max_length=255)
    origin_country = models.CharField(max_length=255)
    on_ground = models.IntegerField()
    category = models.IntegerField()
    size = models.CharField(max_length=50)

    class Meta:
        db_table = 'plane'  # This tells Django to use your existing table name
        

class Entities(models.Model):
    ENTITY_TYPES = [
        ('Plane', 'Plane'),
        ('Ship', 'Ship'),
        ('LandForce', 'LandForce'),
        ('User', 'User'),
    ]

    entity_id = models.AutoField(primary_key=True)  # Maps to the `entity_id` field in the table
    name = models.CharField(max_length=255)  # Maps to the `name` field
    type = models.CharField(max_length=50, choices=ENTITY_TYPES)  # Maps to the `type` field
    created_at = models.DateTimeField(auto_now_add=True)  # Maps to the `created_at` field

    class Meta:
        db_table = 'entities'  # Explicitly specifies the database table name

class Ship(models.Model):
    ship_id = models.AutoField(primary_key=True)
    entry_id = models.IntegerField()
    entity = models.ForeignKey(Entities, models.DO_NOTHING)
    ship_name = models.CharField(max_length=255, blank=True, null=True)
    ship_type = models.CharField(max_length=255, blank=True, null=True)
    displacement = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'ship'
        
class Landforce(models.Model):
    landforce_id = models.AutoField(primary_key=True)
    entry_id = models.IntegerField()
    entity = models.ForeignKey(Entities, models.DO_NOTHING)
    unit_name = models.CharField(max_length=255, blank=True, null=True)
    unit_size = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'landforce'
