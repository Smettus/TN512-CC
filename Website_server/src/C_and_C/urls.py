from django.urls import path
from C_and_C.views import flight_map

urlpatterns = [
    path('flight_map', flight_map, name="flight_map")
]