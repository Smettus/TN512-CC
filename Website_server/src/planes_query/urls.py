from django.urls import path
from . import views

urlpatterns = [
    path('', views.planes_within_bbox, name='planes_within_bbox'),
]