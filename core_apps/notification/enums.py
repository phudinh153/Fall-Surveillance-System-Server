from django.db import models


class EventCodeChoices(models.TextChoices):
    # Devices Events
    DEVICE_FALL_DETECTED = "FALL_DETECTED", "Fall Detected"
    # House Events
    ADD_MEMBER_TO_HOUSE = "ADD_MEMBER_TO_HOUSE", "New Invite to House"
    REMOVE_MEMBER_FROM_HOUSE = "REMOVE_MEMBER_FROM_HOUSE", "Removed from House"
    UPDATE_HOUSE_METADATA = "UPDATE_HOUSE_METADATA", "House Metadata Updated"
    # Room Events
    UPDATE_ROOM_METADATA = "UPDATE_ROOM_METADATA", "Update room meta data"
    INVITE_MEMBER_TO_ROOM = "INVITE_MEMBER_TO_ROOM", "Invited to Room"

    # User Events
    IS_INVITED_TO_ROOM = "INVITED_TO_ROOM", "Invited to Room"
    IS_INVITED_TO_HOUSE = "INVITED_TO_HOUSE", "Invited to House"
    REMOVED_FROM_ROOM = "REMOVED_FROM_ROOM", "Removed from Room"
    REMOVED_FROM_HOUSE = "REMOVED_FROM_HOUSE", "Removed from House"
    NOTIFY_USER_DEVICE_FALL_DETECTED = (
        "NOTIFY_USER_DEVICE_FALL_DETECTED",
        "Fall Detected",
    )
    # ...


DEVICE_NOTIFICATION_EVENT_CODES = [
    EventCodeChoices.DEVICE_FALL_DETECTED,
]

ROOM_NOTIFICATION_EVENT_CODES = [
    EventCodeChoices.INVITE_MEMBER_TO_ROOM,
    EventCodeChoices.UPDATE_ROOM_METADATA,
]

HOUSE_NOTIFICATION_EVENT_CODES = [
    EventCodeChoices.ADD_MEMBER_TO_HOUSE,
    EventCodeChoices.REMOVE_MEMBER_FROM_HOUSE,
    EventCodeChoices.UPDATE_HOUSE_METADATA,
]

USER_NOTIFICATION_EVENT_CODES = [
    EventCodeChoices.IS_INVITED_TO_HOUSE,
    EventCodeChoices.IS_INVITED_TO_ROOM,
    EventCodeChoices.REMOVED_FROM_ROOM,
    EventCodeChoices.REMOVED_FROM_HOUSE,
    EventCodeChoices.NOTIFY_USER_DEVICE_FALL_DETECTED,
]

DEVICE_NOTIFICATION_EVENT_CODES = [EventCodeChoices.DEVICE_FALL_DETECTED]
