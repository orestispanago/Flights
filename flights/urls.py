from django.urls import path
from .views import FlightListView, FlightCreationFormView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(FlightListView.as_view()), name="flights-home"),
    path(
        "flights/new/",
        FlightCreationFormView.as_view(),
        name="flight-create",
    ),
]
