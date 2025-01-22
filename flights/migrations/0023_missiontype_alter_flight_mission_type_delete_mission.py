from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("flights", "0022_alter_flight_dest"),
    ]

    operations = [
        # Rename the table instead of dropping and creating it
        migrations.AlterModelTable(
            name="Mission",
            table="flights_missiontype",
        ),
        # Update the model name in Django's ORM
        migrations.RenameModel(
            old_name="Mission",
            new_name="MissionType",
        ),
    ]
