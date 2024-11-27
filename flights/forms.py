from .models import Flight
from django.forms import ModelForm, DateInput
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"
    input_class = "datepicker"


class TimePickerInput(forms.TimeInput):
    input_type = "time"


class FlightCreationForm(ModelForm):
    class Meta:
        model = Flight
        fields = "__all__"
        exclude = ("pilot",)
        widgets = {
            "date": DateInput(),
            "engine_on": TimePickerInput(),
            "takeoff": TimePickerInput(),
            "engine_off": TimePickerInput(),
            "landing": TimePickerInput(),
        }
