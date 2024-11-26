from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Mission(models.Model):
    type = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=120)

    def __str__(self):
        return self.type


class Aircraft(models.Model):
    callsign = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.callsign


class Flight(models.Model):
    date = models.DateField(default=timezone.now)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.PROTECT)
    engine_on = models.TimeField(default=timezone.now)
    take_off = models.TimeField(default=timezone.now)
    landing = models.TimeField(default=timezone.now)
    engine_off = models.TimeField(default=timezone.now)
    ej_fired = models.PositiveSmallIntegerField(default=0)
    ej_attempted = models.PositiveSmallIntegerField(default=0)
    bip_fired = models.PositiveSmallIntegerField(default=0)
    bip_attempted = models.PositiveSmallIntegerField(default=0)
    hygro_fired = models.PositiveSmallIntegerField(default=0)
    hygro_attempted = models.PositiveSmallIntegerField(default=0)
    mission_type = models.ForeignKey(Mission, on_delete=models.PROTECT)
    pilot = models.ForeignKey(User, on_delete=models.PROTECT)
