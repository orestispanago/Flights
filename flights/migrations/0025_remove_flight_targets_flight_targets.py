# Generated by Django 5.0.9 on 2025-01-22 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0024_alter_missiontype_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='targets',
        ),
        migrations.AddField(
            model_name='flight',
            name='targets',
            field=models.ManyToManyField(blank=True, related_name='flights', to='flights.target'),
        ),
    ]
