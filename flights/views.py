from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Flight
from .forms import FlightCreationForm
from django.contrib.auth.decorators import login_required


def home(request):
    context = {"flights": Flight.objects.all()}
    return render(request, "flights/home.html", context=context)


@login_required
def create_flight(request):
    if request.method == "POST":
        form = FlightCreationForm(request.POST)
        form.instance.pilot = request.user
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {"form": FlightCreationForm()}
    return render(request, "flights/flight_form.html", context=context)


class FlightListView(ListView):
    model = Flight
    template_name = "flights/home.html"
    context_object_name = "flights"
    ordering = ["-pk"]
