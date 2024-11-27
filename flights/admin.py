from django.contrib import admin
from .models import Flight, Plane, Mission


class FlightsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Flight._meta.get_fields()]


class PlanesAdmin(admin.ModelAdmin):
    list_display = ["callsign", "type", "equipment"]


class MissionAdmin(admin.ModelAdmin):
    list_display = ["type", "description"]


admin.site.register(Flight, FlightsAdmin)
admin.site.register(Plane, PlanesAdmin)
admin.site.register(Mission, MissionAdmin)
