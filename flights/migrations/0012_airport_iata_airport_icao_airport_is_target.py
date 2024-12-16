# Generated by Django 5.0.9 on 2024-12-16 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0011_alter_flight_bip_dud_alter_flight_bip_mis_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='airport',
            name='iata',
            field=models.CharField(max_length=3, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='airport',
            name='icao',
            field=models.CharField(max_length=4, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='airport',
            name='is_target',
            field=models.BooleanField(default=False),
        ),
    ]
