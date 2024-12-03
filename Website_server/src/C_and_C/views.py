from django.shortcuts import render

# Create your views here.

def flight_map(request):
    return render(request, "C_and_C/flight_map.html")