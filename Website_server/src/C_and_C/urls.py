from django.urls import path
from C_and_C.views import flight_map
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('flight_map', flight_map, name="flight_map")
]