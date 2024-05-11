from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from core_apps.house.models import Room, House
from utils import list as list_utils
from . import enums

User = get_user_model()


# Create your models here.
class PermissionType(models.Model):
    name = models.CharField(
        enums.PermissionTypeChoices.choices,
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )
    description = models.TextField(null=False, blank=True)

    class Meta:
        db_table = "permission_type"

    @classmethod
    def get_permission_type(cls, permission_name):
        return cls.objects.get(name=permission_name)


class Permission(models.Model):

    permission_type = models.ForeignKey(
        PermissionType,
        on_delete=models.CASCADE,
        related_name="permissions",
        null=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="permissions",
        null=False,
    )
    # House rooms that current permission is applied to
    rooms = models.ManyToManyField(Room, related_name="permissions")
    houses = models.ManyToManyField(House, related_name="permissions")
    # Add other model permission here

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_permission"
        unique_together = ("permission_type", "user")
        # Add indexing for permission, user

    @classmethod
    def initialize_users_permissions(cls, *users):
        """
        create all permission for correspond user
        """
        permission_types = PermissionType.objects.all()
        cls.objects.bulk_create(
            [
                cls(permission_type=permission_type, user=user)
                for permission_type in permission_types
                for user in users
            ],
            ignore_conflicts=True,
        )

    # -----------------------------------
    # ----- HOUSE PERMISSION HANDLER -----
    # -----------------------------------

    # ----- Mutator -----
    @classmethod
    def grant_houses_permissions(cls, user, permission_type_names, *houses):
        permissions = cls.objects.filter(
            user=user, permission_type__name__in=permission_type_names
        )
        for p in permissions:
            p.houses.add(*houses)

    @classmethod
    def grant_houses_owner_permissions(cls, user, *houses):
        print("granting owner", flush=True)
        cls.grant_houses_permissions(user, enums.HOUSE_PERMISSIONS, *houses)

    @classmethod
    def remove_house_permissions(
        cls,
        permission_names=enums.HOUSE_PERMISSIONS,
        user=None,
        house=None,
        house_id="",
        user_id="",
    ):
        from core_apps.house.models import House

        assert bool(user) or bool(user_id), "user or user_id must be provided"
        assert bool(house) or bool(
            house_id
        ), "house or house_id must be provided"

        user_id = user_id if bool(user_id) else user.id
        house_id = house_id if bool(house_id) else house.id

        house = house if bool(house) else House.objects.get(id=house_id)

        permissions = cls.objects.filter(
            user__id=user_id,
            houses__id=house_id,
            permission_type__name__in=permission_names,
        )
        for p in permissions:
            p.houses.remove(house)

    # ----- Properties -----
    @classmethod
    def has_house_permissions(cls, user, house, *permission_names):
        """
        check if user has all house's permission in given permission_names
        """
        return cls.objects.filter(
            user=user, permission_type__name__in=permission_names, houses=house
        ).distinct().count() >= len(permission_names)

    # ----- Queries -----
    @classmethod
    def get_user_house_permissions(cls, user, house, flat=False):
        if flat:
            return cls.objects.filter(user=user, houses=house).values_list(
                "permission_type__name", flat=True
            )
        return cls.objects.filter(user=user, houses=house)

    # -----------------------------------
    # ----- ROOM PERMISSION HANDLER -----
    # -----------------------------------
    # ----- Mutator -----
    @classmethod
    def grant_all_room_permissions(cls, user, *rooms):
        cls.grant_rooms_permissions(user, enums.ROOM_PERMISSIONS, *rooms)

    @classmethod
    def remove_user_room_permissions(
        cls,
        permission_names=enums.ROOM_PERMISSIONS,
        user_id="",
        room_id="",
        user=None,
        room=None,
    ):
        assert bool(user) or bool(user_id), "user or user_id must be provided"
        assert bool(room) or bool(room_id), "room or room_id must be provided"

        user_id = user_id if bool(user_id) else user.id
        room_id = room_id if bool(room_id) else room.id

        room = room if bool(room) else Room.objects.get(id=room_id)

        permissions = cls.objects.filter(
            user__id=user_id,
            rooms__id=room_id,
            permission_type__name__in=permission_names,
        )
        for p in permissions:
            p.rooms.remove(room)

    @classmethod
    def grant_rooms_permissions(cls, user, permission_type_names, *rooms):
        """
        grants user with room's permissions to multiple room at once
        """
        assert list_utils.is_subset_list(
            enums.ROOM_PERMISSIONS, permission_type_names
        )
        permissions = cls.objects.filter(
            user=user, permission_type__name__in=permission_type_names
        )
        for p in permissions:
            p.rooms.add(*rooms)

    # ----- Queries -----
    @classmethod
    def get_room_assigned_users(cls, room_id):
        room_pers = cls.objects.select_related("user").filter(
            rooms__id=room_id,
            permission_type__name__in=enums.ROOM_PERMISSIONS,
        )
        return list(set(per.user for per in room_pers))

    @classmethod
    def get_user_room_permissions(cls, user, room, flat=False):
        if flat:
            return cls.objects.filter(user=user, rooms=room).values_list(
                "permission_type__name", flat=True
            )
        return cls.objects.filter(user=user, rooms=room)

    @classmethod
    def get_users_from_room_permission(
        cls, room_id, permission_names: list[str]
    ):
        user_ids = cls.objects.filter(
            rooms__id=room_id, permission_type__name__in=permission_names
        ).values_list("user", flat=True)
        users = User.objects.filter(pkid__in=user_ids).distinct()

        return users

    # ----- Properties

    @classmethod
    def has_room_permissions(cls, user, room, *permission_names):
        """
        check if user has all permission in given permission_names
        """
        permissions = cls.objects.filter(
            user=user, permission_type__name__in=permission_names, rooms=room
        ).distinct()
        return permissions.count() >= len(permission_names)
