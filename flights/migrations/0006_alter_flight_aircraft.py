# Generated by Django 5.0.9 on 2024-11-07 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0005_alter_flight_aircraft'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='aircraft',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flights.aircfaft'),
        ),
    ]
