from django.urls import path
from .views import AircraftListView, home, create_flight

urlpatterns = [
    path("", home, name="flights-home"),
    path("flights/new/", create_flight, name="flight-create"),
    path("aircraft", AircraftListView.as_view(), name="flights-aircraft"),
]
