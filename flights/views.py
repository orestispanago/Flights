from django.views.generic import ListView, FormView
from .models import Flight
from .forms import FlightCreationForm
from django.contrib import messages
from django.http import HttpResponse
import csv


class FlightCreationFormView(FormView):
    form_class = FlightCreationForm
    template_name = "flights/flight_form.html"

    def get_success_url(self):
        return "/"

    def form_valid(self, form):
        form.instance.pilot = self.request.user
        form.save()
        messages.success(
            self.request,
            "Flight created successfully",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        form.add_error(None, "Please correct the errors below")
        return super().form_invalid(form)


class FlightListView(ListView):
    model = Flight
    template_name = "flights/home.html"
    context_object_name = "flights"
    ordering = ["-pk"]
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        if "download" in request.GET and request.GET["download"] == "csv":
            return self.download_csv()
        return super().get(request, *args, **kwargs)

    def download_csv(self):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="flights.csv"'
        writer = csv.writer(response)
        fields = [field.name for field in self.model._meta.fields]
        writer.writerow(fields)
        for flight in self.model.objects.all().order_by(*self.ordering):
            writer.writerow([getattr(flight, field) for field in fields])
        return response


# def get_queryset(self):
#     user_info = self.request.user.info
#     self.queryset = user_info.trade_set.all()
#     return super().get_queryset()
