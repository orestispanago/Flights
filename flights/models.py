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


def format_comparison_error(field1, relationship, field2):
    return (
        f"{field1.verbose_name.capitalize()}"
        f" {relationship} "
        f"{field2.verbose_name.capitalize()}."
    )


def add_error(errors, field, message):
    if field.name not in errors:
        errors[field.name] = message
    else:
        errors[field.name] += f" {message}"


class AttemptedFiredValidatorMixin:
    def validate_attempted_fired(self, errors, field_pairs):
        for attempted, fired in field_pairs:
            attempted_value = getattr(self, attempted.name)
            fired_value = getattr(self, fired.name)
            if fired_value > attempted_value:
                error_msg = format_comparison_error(
                    attempted, "cannot be less than", fired
                )
                add_error(errors, attempted, error_msg)
                error_msg = format_comparison_error(
                    fired, "must be greater than or equal to", attempted
                )
                add_error(errors, fired, error_msg)

    def clean(self):
        errors = {}
        field_pairs = [
            (self._meta.get_field("ej_att"), self._meta.get_field("ej_fired")),
            (
                self._meta.get_field("bip_att"),
                self._meta.get_field("bip_fired"),
            ),
            (
                self._meta.get_field("hbip_att"),
                self._meta.get_field("hbip_fired"),
            ),
        ]

        self.validate_attempted_fired(errors, field_pairs)
        if errors:
            raise ValidationError(errors)


class TimeOrderValidatorMixin:
    def validate_order(self, errors, fields):
        for current, next in zip(fields, fields[1:]):
            current_time = getattr(self, current.name)
            next_time = getattr(self, next.name)
            if current_time >= next_time:
                error_msg = format_comparison_error(
                    current, "must be earlier than", next
                )
                add_error(errors, current, error_msg)
                error_msg = format_comparison_error(
                    next, "must be later than", current
                )
                add_error(errors, next, error_msg)

    def clean(self):
        errors = {}
        fields = [
            self._meta.get_field("engine_on"),
            self._meta.get_field("takeoff"),
            self._meta.get_field("landing"),
            self._meta.get_field("engine_off"),
        ]

        self.validate_order(errors, fields)
        if errors:
            raise ValidationError(errors)


class Flight(
    models.Model, TimeOrderValidatorMixin, AttemptedFiredValidatorMixin
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

    def clean(self):
        super().clean()
        TimeOrderValidatorMixin.clean(self)
        AttemptedFiredValidatorMixin.clean(self)

    def save(self, *args, **kwargs):
        self.air_time = calc_duration(self.takeoff, self.landing)
        super(Flight, self).save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.pk}, Plane: {self.plane}, Takeoff: {self.date} {self.takeoff}"
