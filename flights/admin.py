from django.contrib import admin
from .models import Flight


class FlightsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Flight._meta.get_fields()]


admin.site.register(Flight, FlightsAdmin)
