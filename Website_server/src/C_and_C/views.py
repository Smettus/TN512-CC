from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def home_view(request):
    # Check if user is authenticated
    return render(request, 'my_project/home.html')


@login_required
def flight_map(request):
    return render(request, "C_and_C/flight_map.html")