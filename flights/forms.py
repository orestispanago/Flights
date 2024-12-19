from .models import Flight, Airport

from django import forms
from datetime import datetime, date


class DatePickerInput(forms.DateInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({"input_type": "date", "class": "datepicker"})


class TimePickerInput(forms.TimeInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({"input_type": "time", "class": "timepicker"})


class MultipleSelect(forms.SelectMultiple):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({"select": "multiple"})


def calc_duration(start, end):
    """Calculates timedelta between datetime.time objects"""
    return datetime.combine(date.min, end) - datetime.combine(date.min, start)


class FlightCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pilot"].required = True
        self.fields["copilot"].required = True

    class Meta:
        model = Flight

        fields = [
            "date",
            "plane",
            "engine_on",
            "takeoff",
            "landing",
            "engine_off",
            # "air_time",
            "ej_att",
            "ej_fired",
            "bip_att",
            "bip_fired",
            "hbip_att",
            "hbip_fired",
            "mission_type",
            "pilot",
            "copilot",
            "base",
            "dest",
            "ej_mis",
        ]
        widgets = {
            "date": DatePickerInput(),
            "engine_on": TimePickerInput(),
            "takeoff": TimePickerInput(),
            "engine_off": TimePickerInput(),
            "landing": TimePickerInput(),
        }
