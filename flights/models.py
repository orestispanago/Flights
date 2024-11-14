from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Mission(models.Model):
    type = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=120)


class Aircfaft(models.Model):
    callsign = models.CharField(max_length=10, unique=True)


class Flight(models.Model):
    date = models.DateField(default=timezone.now)
    aircraft = models.ForeignKey(Aircfaft, on_delete=models.PROTECT)
    engine_on = models.TimeField(default=timezone.now)
    take_off = models.TimeField(default=timezone.now)
    landing = models.TimeField(default=timezone.now)
    engine_off = models.TimeField(default=timezone.now)
    ej = models.PositiveSmallIntegerField(default=0)
    bip = models.PositiveSmallIntegerField(default=0)
    hygro = models.PositiveSmallIntegerField(default=0)
    mission_type = models.ForeignKey(Mission, on_delete=models.PROTECT)
    pilot = models.ForeignKey(User, on_delete=models.PROTECT)
