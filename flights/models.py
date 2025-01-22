from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from datetime import timedelta, datetime, date
from .validators import (
    TimeOrderValidatorMixin,
    AttemptedFiredValidatorMixin,
    PilotValidatorMixin,
)


class MissionType(models.Model):
    type = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.type


class Plane(models.Model):
    callsign = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=20, null=True, blank=True)

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
    iata = models.CharField(
        max_length=3,
        unique=True,
        null=True,
        blank=True,
        verbose_name="IATA code",
    )
    icao = models.CharField(
        max_length=4,
        unique=True,
        null=True,
        blank=True,
        verbose_name="ICAO code",
    )

    def __str__(self):
        return self.name


class Target(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


def calc_duration(start, end):
    """Calculates timedelta between datetime.time objects"""
    return datetime.combine(date.min, end) - datetime.combine(date.min, start)


class Pilot(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.first_name[0].upper()}. {self.last_name.upper()}"


class Flight(
    models.Model,
    TimeOrderValidatorMixin,
    AttemptedFiredValidatorMixin,
    PilotValidatorMixin,
):
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
    mission_type = models.ForeignKey(MissionType, on_delete=models.PROTECT)
    pilot = models.ForeignKey(
        Pilot,
        on_delete=models.PROTECT,
        related_name="flights_as_pilot",
        null=False,
        blank=True,
    )
    copilot = models.ForeignKey(
        Pilot,
        on_delete=models.PROTECT,
        related_name="flights_as_copilot",
        null=False,
        blank=True,
    )
    base = models.ForeignKey(
        Airport, on_delete=models.PROTECT, related_name="base"
    )
    dest = models.ForeignKey(
        Airport, on_delete=models.PROTECT, related_name="dest"
    )
    targets = models.ManyToManyField(
        "Target", blank=True, related_name="flights"
    )
    ej_mis = models.PositiveSmallIntegerField(null=True, blank=True)
    ej_dud = models.PositiveSmallIntegerField(null=True, blank=True)
    bip_mis = models.PositiveSmallIntegerField(null=True, blank=True)
    bip_dud = models.PositiveSmallIntegerField(null=True, blank=True)
    hbip_mis = models.PositiveSmallIntegerField(null=True, blank=True)
    hbip_dud = models.PositiveSmallIntegerField(null=True, blank=True)

    def clean(self):
        super().clean()
        TimeOrderValidatorMixin.clean(self)
        AttemptedFiredValidatorMixin.clean(self)
        PilotValidatorMixin.validate_pilot_copilot_different(self)

    def save(self, *args, **kwargs):
        self.air_time = calc_duration(self.takeoff, self.landing)
        super(Flight, self).save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.pk}, Plane: {self.plane}, Takeoff: {self.date} {self.takeoff}"
