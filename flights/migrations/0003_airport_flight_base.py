# Generated by Django 5.0.9 on 2024-12-04 11:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_flight_air_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='flight',
            name='base',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='flights.airport'),
        ),
    ]
