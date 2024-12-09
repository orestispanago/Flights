from django.contrib import admin
from .models import Flight, Plane, Mission, Airport
from django.http import HttpResponse
import csv
import datetime


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        "attachment;" f"filename={opts.verbose_name}s.csv"
    )
    writer = csv.writer(response)
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d/%m/%Y")
            data_row.append(value)
        writer.writerow(data_row)

    return response


class FlightsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Flight._meta.get_fields()]
    # exclude = ["base"]
    readonly_fields = ["air_time", "ej_dud", "bip_dud", "hbip_dud"]
    list_filter = (("date", admin.DateFieldListFilter), "plane", "base")
    actions = [export_to_csv]


class PlanesAdmin(admin.ModelAdmin):
    list_display = ["callsign", "type", "equipment"]


class MissionAdmin(admin.ModelAdmin):
    list_display = ["type", "description"]


admin.site.register(Flight, FlightsAdmin)
admin.site.register(Plane, PlanesAdmin)
admin.site.register(Mission, MissionAdmin)
admin.site.register(Airport)
