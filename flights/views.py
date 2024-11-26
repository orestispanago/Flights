from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Flight, Aircraft
from .forms import FlightCreationForm


def home(request):
    context = {"flights": Flight.objects.all()}
    return render(request, "flights/home.html", context=context)


def create_flight(request):
    if request.method == "POST":
        form = FlightCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {"form": FlightCreationForm()}
    return render(request, "flights/flight_form.html", context=context)


class AircraftListView(ListView):
    model = Aircraft
    template_name = "flights/aircraft.html"
    context_object_name = "aircrafts"


# class FlightListView(ListView):
#     model = Flight
#     template_name = "flights/home.html"
#     context_object_name = "flights"
#     ordering = ["-date"]
