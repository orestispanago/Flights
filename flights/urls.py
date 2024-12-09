from django.urls import path
from .views import FlightListView, FlightCreationFormView

urlpatterns = [
    path("", FlightListView.as_view(), name="flights-home"),
    path(
        "flights/new/", FlightCreationFormView.as_view(), name="flight-create"
    ),
]
