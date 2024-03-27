# Generated by Django 4.2.5 on 2024-02-02 09:30
from django.db import migrations
import django


def add_default_permissions(apps, schema_editor):
    MyUser = apps.get_model("user", "MyUser")  # Replace 'your_app_name'
    PermissionType = apps.get_model("permission", "PermissionType")
    Permission = apps.get_model("permission", "Permission")
    # Replace 'your_app_name'
    users = MyUser.objects.all()
    permission_types = PermissionType.objects.all()
    Permission.objects.bulk_create(
        [
            Permission(permission_type=permission_type, user=user)
            for permission_type in permission_types
            for user in users
        ],
        ignore_conflicts=True,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("permission", "0004_permission_houses_alter_permissiontype_name")
    ]

    operations = [
        migrations.RunPython(add_default_permissions),
    ]