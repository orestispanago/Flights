# Generated by Django 5.0.9 on 2024-12-09 16:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0005_rename_hygro_attempted_flight_hbip_attempted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='dest',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='flights.airport'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='base',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='base', to='flights.airport'),
        ),
    ]