from django.core import management
from django.contrib.auth import get_user_model
from django.core.management.base import CommandParser
from django.db.models import Count
from core_apps.permission.enums import PermissionTypeChoices
from core_apps.permission.models import Permission

User = get_user_model()

total_user_permissions = len(PermissionTypeChoices.choices)


class Command(management.BaseCommand):
    help = """
    Create all permssision instance for users.
    """

    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)

    def handle(self, *args, **options) -> str | None:
        to_fix_users = User.objects.annotate(
            permission_count=Count("permissions")
        ).filter(permission_count=total_user_permissions)
        Permission.initialize_users_permissions(*to_fix_users)
        self.stdout.write(
            self.style.SUCCESS(
                "Done! All user have corresponding Permission table"
            )
        )
