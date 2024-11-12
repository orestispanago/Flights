from django.shortcuts import render
from .models import Flight

flights = [
    {
        "date": "01-01-2024",
        "pilot": "pilot name",
        "aircraft": "ab123",
        "mission": "seed",
        "engine_on": "12:00",
        "take_off": "12:02",
        "landing": "13:00",
        "engine_off": "13:02",
        "ej": 1,
        "ebip": 3,
        "hygro": 0,
    },
    {
        "date": "01-01-2024",
        "pilot": "pilot name 2",
        "aircraft": "cd456",
        "mission": "recon",
        "engine_on": "14:00",
        "take_off": "14:02",
        "landing": "15:00",
        "engine_off": "15:02",
        "ej": 1,
        "ebip": 3,
        "hygro": 0,
    },
]


def home(request):
    context = {"flights": Flight.objects.all()}
    return render(request, "flights/home.html", context=context)
