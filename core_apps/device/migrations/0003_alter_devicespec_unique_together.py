# Generated by Django 4.2.5 on 2024-01-29 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("device", "0002_devicespec_remove_device_firmware_version_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="devicespec",
            unique_together={("name", "series_name")},
        ),
    ]
