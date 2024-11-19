from django.shortcuts import render


def home(request):
    return render(request, "my_project/home.html")