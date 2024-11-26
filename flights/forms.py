from django.contrib.auth.models import User
from .models import Flight, Aircraft
from django.forms import ModelForm, ModelChoiceField, DateInput
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class TimePickerInput(forms.TimeInput):
    input_type = "time"


class FlightCreationForm(ModelForm):
    class Meta:
        model = Flight
        aircraft = ModelChoiceField(queryset=Aircraft.objects)
        # fields = ["date", "engine_on", "take_off", "aircraft", "mission_type"]
        fields = "__all__"
        widgets = {
            "date": DateInput(),
            "engine_on": TimePickerInput(),
            "take_off": TimePickerInput(),
            "engine_off": TimePickerInput(),
            "landing": TimePickerInput(),
        }
