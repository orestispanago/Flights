from .models import Flight

from django import forms
from django.core.exceptions import ValidationError


class DatePickerInput(forms.DateInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({"input_type": "date", "class": "datepicker"})


class TimePickerInput(forms.TimeInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({"input_type": "time", "class": "timepicker"})


class FlightCreationForm(forms.ModelForm):
    # ej_attempted = forms.IntegerField(initial=0, min_value=0, max_value=10)
    # ej_fired = forms.IntegerField(initial=0, min_value=0, max_value=10)
    # bip_attempted = forms.IntegerField(initial=0, min_value=0, max_value=10)
    # bip_fired = forms.IntegerField(initial=0, min_value=0, max_value=10)
    # hygro_attempted = forms.IntegerField(initial=0, min_value=0, max_value=10)
    # hygro_fired = forms.IntegerField(initial=0, min_value=0, max_value=10)

    class Meta:
        model = Flight
        fields = "__all__"
        exclude = ("pilot",)
        widgets = {
            "date": DatePickerInput(),
            "engine_on": TimePickerInput(),
            "takeoff": TimePickerInput(),
            "engine_off": TimePickerInput(),
            "landing": TimePickerInput(),
        }

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
