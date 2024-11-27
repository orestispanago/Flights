from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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


class Flight(models.Model):
    date = models.DateField(default=timezone.now)
    plane = models.ForeignKey(Plane, on_delete=models.PROTECT)
    engine_on = models.TimeField(default=timezone.now)
    takeoff = models.TimeField(default=timezone.now)
    landing = models.TimeField(default=timezone.now)
    engine_off = models.TimeField(default=timezone.now)
    ej_attempted = models.PositiveSmallIntegerField(default=0)
    ej_fired = models.PositiveSmallIntegerField(default=0)
    bip_attempted = models.PositiveSmallIntegerField(default=0)
    bip_fired = models.PositiveSmallIntegerField(default=0)
    hygro_attempted = models.PositiveSmallIntegerField(default=0)
    hygro_fired = models.PositiveSmallIntegerField(default=0)
    mission_type = models.ForeignKey(Mission, on_delete=models.PROTECT)
    pilot = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"ID: {self.pk}, Plane: {self.plane}, Takeoff: {self.date} {self.takeoff}"
