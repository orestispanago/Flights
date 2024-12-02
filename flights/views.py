from django.views.generic import ListView, FormView
from .models import Flight
from .forms import FlightCreationForm


class FlightCreationFormView(FormView):
    form_class = FlightCreationForm
    template_name = "flights/flight_form.html"

    def get_success_url(self):
        return "/"

    def form_valid(self, form):
        form.instance.pilot = self.request.user
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        form.add_error(None, "Please correct the errors below")
        return super().form_invalid(form)


class FlightListView(ListView):
    model = Flight
    template_name = "flights/home.html"
    context_object_name = "flights"
    ordering = ["-pk"]
