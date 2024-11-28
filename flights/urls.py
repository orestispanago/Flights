from django.urls import path
from .views import FlightListView, FlightCreationFormView

urlpatterns = [
    # path("", home, name="flights-home"),
    path("", FlightListView.as_view(), name="flights-home"),
    # path("flights/new/", create_flight, name="flight-create"),
    path(
        "flights/new/", FlightCreationFormView.as_view(), name="flight-create"
    ),
]
