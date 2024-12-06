from .models import Flight

from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime, date


class DatePickerInput(forms.DateInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({"input_type": "date", "class": "datepicker"})


class TimePickerInput(forms.TimeInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({"input_type": "time", "class": "timepicker"})


def calc_duration(start, end):
    """Calculates timedelta between datetime.time objects"""
    return datetime.combine(date.min, end) - datetime.combine(date.min, start)


class FlightCreationForm(forms.ModelForm):

    # ej_attempted = forms.IntegerField(initial=0, min_value=0, max_value=306)
    # ej_fired = forms.IntegerField(initial=0, min_value=0, max_value=306)
    # bip_attempted = forms.IntegerField(initial=0, min_value=0, max_value=10)
    # bip_fired = forms.IntegerField(initial=0, min_value=0, max_value=10)
    # hygro_attempted = forms.IntegerField(initial=0, min_value=0, max_value=10)
    # hygro_fired = forms.IntegerField(initial=0, min_value=0, max_value=10)

    class Meta:
        model = Flight
        fields = "__all__"
        exclude = ("pilot", "air_time")
        widgets = {
            "date": DatePickerInput(),
            "engine_on": TimePickerInput(),
            "takeoff": TimePickerInput(),
            "engine_off": TimePickerInput(),
            "landing": TimePickerInput(),
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     on = cleaned_data.get("engine_on")
    #     takeoff = cleaned_data.get("takeoff")
    #     landing = cleaned_data.get("landing")
    #     off = cleaned_data.get("engine_off")
    #     air_time = calc_duration(takeoff, landing)
    #     print(air_time, "================================================")

    #     times = [on, takeoff, landing, off]
    #     sorted_times = sorted(times)
    #     if on != sorted_times[0]:
    #         self.add_error(
    #             "engine_on",
    #             "'Engine On' time must be the earliest.",
    #         )
    #     if takeoff != sorted_times[1]:
    #         self.add_error(
    #             "takeoff",
    #             "'Takeoff' time should come after 'Engine On' and before 'Landing'.",
    #         )
    #     if landing != sorted_times[2]:
    #         self.add_error(
    #             "landing",
    #             "'Landing' time should come after 'Takeoff' and before 'Engine Off'.",
    #         )
    #     if off != sorted_times[3]:
    #         self.add_error(
    #             "engine_off",
    #             "'Engine Off' time must be the latest.",
    #         )
    #     return cleaned_data

    # def clean_ej_attempted(self):
    #     ej_attempted = self.cleaned_data.get("ej_attempted")
    #     if ej_attempted > 3:
    #         raise ValidationError("ej_attempted >3")
    #     return ej_attempted

    # def clean_ej_fired(self):
    #     ej_attempted = self.cleaned_data.get("ej_attempted")
    #     ej_fired = self.cleaned_data.get("ej_fired")
    #     if ej_fired > ej_attempted:
    #         raise (ValidationError("Fired cannot be more than attempted"))

    # def clean_bip_fired(self):
    #     bip_attempted = self.data.get("bip_attempted")
    #     bip_fired = self.data.get("bip_fired")
    #     if bip_fired > bip_attempted:
    #         raise (ValidationError("Fired cannot be more than attempted"))
