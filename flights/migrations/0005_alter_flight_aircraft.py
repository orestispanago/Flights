# Generated by Django 5.0.9 on 2024-11-07 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0004_aircfaft_mission_alter_flight_pilot_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='aircraft',
            field=models.SmallIntegerField(default=1),
        ),
    ]
