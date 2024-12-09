from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from datetime import timedelta, datetime, date
from django.core.exceptions import ValidationError


class Mission(models.Model):
    type = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=120)

    def __str__(self):
        return self.type


class Plane(models.Model):
    callsign = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=20, null=True)

    class Equipment(models.TextChoices):
        SEEDING = "S"
        RESEARCH = "R"

    equipment = models.CharField(
        max_length=1,
        choices=Equipment,
        default=Equipment.SEEDING,
    )

    def is_upperclass(self):
        return self.equipment in {
            self.Equipment.SEEDING,
            self.Equipment.RESEARCH,
        }

    def __str__(self):
        return self.callsign


class Airport(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


def calc_duration(start, end):
    """Calculates timedelta between datetime.time objects"""
    return datetime.combine(date.min, end) - datetime.combine(date.min, start)


class Flight(models.Model):
    date = models.DateField(default=timezone.now)
    plane = models.ForeignKey(Plane, on_delete=models.PROTECT)
    engine_on = models.TimeField(default=timezone.now)
    takeoff = models.TimeField(default=timezone.now)
    landing = models.TimeField(default=timezone.now)
    engine_off = models.TimeField(default=timezone.now)
    air_time = models.DurationField(default=timedelta(minutes=0))
    ej_att = models.PositiveSmallIntegerField(
        default=0, validators=[MaxValueValidator(306)]
    )
    ej_fired = models.PositiveSmallIntegerField(default=0)
    bip_att = models.PositiveSmallIntegerField(default=0)
    bip_fired = models.PositiveSmallIntegerField(default=0)
    hbip_att = models.PositiveSmallIntegerField(default=0)
    hbip_fired = models.PositiveSmallIntegerField(default=0)
    mission_type = models.ForeignKey(Mission, on_delete=models.PROTECT)
    pilot = models.ForeignKey(User, on_delete=models.PROTECT)
    base = models.ForeignKey(
        Airport, on_delete=models.PROTECT, related_name="base"
    )
    dest = models.ForeignKey(Airport, on_delete=models.PROTECT)
    ej_mis = models.PositiveSmallIntegerField(null=True, blank=True)
    ej_dud = models.PositiveSmallIntegerField(null=True, blank=True)
    bip_mis = models.PositiveSmallIntegerField(null=True, blank=True)
    bip_dud = models.PositiveSmallIntegerField(null=True, blank=True)
    hbip_mis = models.PositiveSmallIntegerField(null=True, blank=True)
    hbip_dud = models.PositiveSmallIntegerField(null=True, blank=True)

    def clean_engine_on(self, expected):
        if self.engine_on != expected:
            raise ValidationError(
                {"engine_on": "'Engine on' time must be the earliest."}
            )

    def clean_takeoff(self, expected):
        if self.takeoff != expected:
            raise ValidationError(
                {
                    "takeoff": "'Takeoff' time should come after 'Engine on' and before 'Landing'."
                }
            )

    def clean_landing(self, expected):
        if self.landing != expected:
            raise ValidationError(
                {
                    "landing": "'Landing' time should come after 'Takeoff' and before 'Engine Off'."
                }
            )

    def clean_engine_off(self, expected):
        if self.engine_off != expected:
            raise ValidationError(
                {"engine_off": "'Engine Off' time must be the latest."}
            )

    def clean_ej_fired(self):
        if self.ej_fired > self.ej_att:
            raise ValidationError(
                {"ej_fired": "'EJ fired' cannot be more than 'EJ attempted'."}
            )

    def clean_bip_fired(self):
        if self.bip_fired > self.bip_att:
            raise ValidationError(
                {
                    "bip_fired": "'BIP fired' cannot be more than 'BIP attempted'."
                }
            )

    def clean_hbip_fired(self):
        if self.hbip_fired > self.hbip_att:
            raise ValidationError(
                {
                    "hbip_fired": "'HBIP fired' cannot be more than 'HBIP attempted'."
                }
            )

    def clean(self):
        times = [self.engine_on, self.takeoff, self.landing, self.engine_off]
        sorted_times = sorted(times)

        self.clean_engine_on(sorted_times[0])
        self.clean_takeoff(sorted_times[1])
        self.clean_landing(sorted_times[2])
        self.clean_engine_off(sorted_times[3])

        # Check for distinct times
        seen = set()
        for idx, time in enumerate(times):
            field_name = ["engine_on", "takeoff", "landing", "engine_off"][idx]
            if time in seen:
                pretty_name = field_name.replace("_", " ").capitalize()
                raise ValidationError(
                    {
                        field_name: f"'{pretty_name}' time is duplicated. Please provide distinct times."
                    }
                )
            seen.add(time)
        self.clean_ej_fired()
        self.clean_bip_fired()
        self.clean_hbip_fired()

    def save(self, *args, **kwargs):
        self.air_time = calc_duration(self.takeoff, self.landing)
        super(Flight, self).save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.pk}, Plane: {self.plane}, Takeoff: {self.date} {self.takeoff}"
