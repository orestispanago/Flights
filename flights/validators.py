from django.core.exceptions import ValidationError


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


class PilotValidatorMixin:
    def validate_pilot_copilot_different(self):
        if self.pilot_id == self.copilot_id:
            error_message = "Pilot and co-pilot cannot be the same person."
            raise ValidationError(
                {
                    "pilot": error_message,
                    "copilot": error_message,
                }
            )
