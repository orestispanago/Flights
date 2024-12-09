# Generated by Django 5.0.9 on 2024-12-09 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0010_flight_bip_dud_flight_bip_mis_flight_ej_dud_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='bip_dud',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='flight',
            name='bip_mis',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='flight',
            name='ej_dud',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='flight',
            name='ej_mis',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='flight',
            name='hbip_dud',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='flight',
            name='hbip_mis',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
