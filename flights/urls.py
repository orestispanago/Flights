from django.urls import path
from .views import home, create_flight, FlightListView

urlpatterns = [
    # path("", home, name="flights-home"),
    path("", FlightListView.as_view(), name="flights-home"),
    path("flights/new/", create_flight, name="flight-create"),
]
