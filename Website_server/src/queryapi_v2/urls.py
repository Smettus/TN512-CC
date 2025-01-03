from django.urls import path
from . import views

urlpatterns = [
    path('', views.objects_within_bbox, name='objects_within_bbox'),
]