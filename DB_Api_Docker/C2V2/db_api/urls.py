from django.urls import re_path
from db_api import views

urlpatterns = [
    re_path(r'^api/db_api$', views.db_list),
    #re_path(r'^api/db_api/(?P<pk>[0-9]+)$', views.tutorial_detail),
]
