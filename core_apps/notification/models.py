from django.db import models
from mixin.models import TimeStampedModel
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from core_apps.house import models as house_models
from . import enums as notification_enums, managers as notification_managers


# Create your models here.
class Notification(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
    )
    house = models.ForeignKey(
        house_models.House,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
    )
    room = models.ForeignKey(
        house_models.Room,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
    )
    label = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    event_code = models.CharField(
        choices=notification_enums.EventCodeChoices.choices, max_length=255
    )
    meta = models.JSONField(null=True, blank=False, encoder=DjangoJSONEncoder)
    is_seen = models.BooleanField(default=False)

    objects = notification_managers.NotificationManager()

    class Meta:
        db_table = "notification"
        ordering = ["-created_at"]

    # --------- Factory Methods ---------
    @classmethod
    def _create_user_notification(
        cls,
        event_code,
        user,
        label,
        description,
        meta: dict = None,
        save=True,
    ):
        noti = cls(
            user=user,
            event_code=event_code,
            label=label,
            description=description,
            meta=meta,
        )
        if save:
            noti.save()
        return noti

    @classmethod
    def _create_house_notification(
        cls,
        event_code,
        house,
        label,
        description,
        meta: dict = None,
        save=True,
    ):
        noti = cls(
            house=house,
            event_code=event_code,
            label=label,
            description=description,
            meta=meta,
        )
        if save:
            noti.save()
        return noti

    @classmethod
    def create_add_house_member_notification(cls, house, invitor, new_members):
        from core_apps.user.serializers import ReadBasicUserProfile
        from core_apps.house.serializers import RHouseBasic

        invitor_json = ReadBasicUserProfile(invitor).data

        cls._create_house_notification(
            house=house,
            event_code=notification_enums.EventCodeChoices.ADD_MEMBER_TO_HOUSE,
            label="New member joined",
            description="",
            meta={
                "invitor": invitor_json,
                "description": f"{invitor.username} has joined the house",
                "member": ReadBasicUserProfile(new_members, many=True).data,
            },
        )

        # Notify member on there Inbox
        member_notify = [
            cls._create_user_notification(
                event_code=notification_enums.EventCodeChoices.IS_INVITED_TO_HOUSE,
                user=user,
                label="You have been invited to a house",
                description="",
                meta={
                    "invitor": invitor_json,
                    "description": f"{invitor.username} invited you to house {house.name}",
                    "house": RHouseBasic(house).data,
                },
                save=False,
            )
            for user in new_members
        ]

        cls.objects.bulk_create(member_notify, ignore_conflicts=True)

    @classmethod
    def create_update_house_metadata_notification(
        cls,
        house,
        updator,
        update_field_names,
        old_values,
    ):
        assert len(update_field_names) == len(old_values)
        from core_apps.user.serializers import ReadBasicUserProfile
        from core_apps.house.serializers import RHouseBasic

        cls._create_house_notification(
            house=house,
            event_code=notification_enums.EventCodeChoices.UPDATE_HOUSE_METADATA,
            label="House info updated",
            description="",
            meta={
                "updator": ReadBasicUserProfile(updator).data,
                "house": RHouseBasic(house).data,
                "update_fields": update_field_names,
                "old_values": old_values,
            },
        )

    @classmethod
    def _create_room_notification(
        cls,
        event_code,
        room,
        label,
        description,
        meta: dict = None,
        save=True,
    ):
        noti = cls(
            room=room,
            event_code=event_code,
            label=label,
            description=description,
            meta=meta,
        )
        if save:
            noti.save()
        return noti

    @classmethod
    def create_add_room_member_notification(cls, room, invitor, new_members):
        from core_apps.user.serializers import ReadBasicUserProfile
        from core_apps.house.serializers import RRoomBasic
        from . import enums

        invitor_json = ReadBasicUserProfile(invitor).data

        cls._create_room_notification(
            room=room,
            event_code=enums.EventCodeChoices.INVITE_MEMBER_TO_ROOM,
            label="Add members to room",
            description="",
            meta={
                "invitor": invitor_json,
                "description": f"{invitor.username} invited new members to room {room.name}",
                "new_members": ReadBasicUserProfile(
                    new_members, many=True
                ).data,
            },
        )

        # Notify User On there Inbox
        user_notify = [
            cls._create_user_notification(
                event_code=enums.EventCodeChoices.IS_INVITED_TO_ROOM,
                user=user,
                label="You have been invited to a room",
                description="",
                meta={
                    "invitor": invitor_json,
                    "description": f"{invitor.username} invited you to room {room.name}",
                    "room": RRoomBasic(room).data,
                },
                save=False,
            )
            for user in new_members
        ]
        cls.objects.bulk_create(user_notify, ignore_conflicts=True)

    @classmethod
    def create_update_room_metadata_notification(
        cls,
        updator,
        room,
        update_field_names,
        old_values,
    ):
        assert len(update_field_names) == len(
            old_values
        ), "Should be equal len"
        from core_apps.user.serializers import ReadBasicUserProfile
        from core_apps.house.serializers import RRoomBasic

        notification = cls._create_room_notification(
            room=room,
            event_code=notification_enums.EventCodeChoices.UPDATE_ROOM_METADATA,
            label="Room info updated",
            description="",
            meta={
                "updator": ReadBasicUserProfile(updator).data,
                "room": RRoomBasic(room).data,
                "update_fields": update_field_names,
                "old_values": old_values,
            },
        )

        return notification

    # --------- Queries ---------
    @classmethod
    def get_house_notifications(cls, house):
        return cls.objects.filter(
            house=house,
            event_code__in=notification_enums.HOUSE_NOTIFICATION_EVENT_CODES,
        ).order_by("is_seen", "-created_at")

    @classmethod
    def get_room_notifications(cls, room):
        return cls.objects.filter(
            room=room,
            event_code__in=notification_enums.ROOM_NOTIFICATION_EVENT_CODES,
        ).order_by(
            "is_seen",
            "-created_at",
        )

    @classmethod
    def get_user_notifications(cls, user):
        return cls.objects.filter(
            user=user,
            event_code__in=notification_enums.USER_NOTIFICATION_EVENT_CODES,
        ).order_by("is_seen", "-created_at")

    # --------- Mutators ---------
    @classmethod
    def bulk_mark_seen(cls, ids):
        notifications = cls.objects.filter(id__in=ids)
        for noti in notifications:
            noti.mark_seen(save=False)
        cls.objects.bulk_update(
            notifications,
            ["is_seen"],
        )

    def mark_seen(self, save=True):
        self.is_seen = True
        if save:
            self.save()
