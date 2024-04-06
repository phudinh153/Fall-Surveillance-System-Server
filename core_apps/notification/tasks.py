import celery
from constants.config import NOTIFICATION_URL
from django.contrib.auth import get_user_model
from .enums import EventCodeChoices
from .push_noti.sender import UserNotificationSender
from .push_noti.message import UserNotificationMessage

User = get_user_model()

user_service = UserNotificationSender.new_service(
    base_url=NOTIFICATION_URL,
    message_class=UserNotificationMessage,
)

DEFAULT_NOTI_IMAGE = "https://www.pushengage.com/wp-content/uploads/2022/10/How-to-Add-a-Push-Notification-Icon.png"


@celery.shared_task
def push_is_added_to_house_notification(house_id, invitor_id, invitee_ids):
    from core_apps.house.models import House

    house = House.objects.get(id=house_id)
    invitor = User.objects.get(id=invitor_id)
    user_service.push(
        event_code=EventCodeChoices.IS_INVITED_TO_HOUSE,
        receiver_ids=invitee_ids,
        message=UserNotificationMessage.create_new(
            username=invitor.get_username(),
            avatar=invitor.profile.avatar,
            des_image=DEFAULT_NOTI_IMAGE,
            des_name=house.name,
        ),
    )


@celery.shared_task
def push_is_added_to_room_notification(room_id, invitor_id, invitee_ids):
    from core_apps.house.models import Room

    room = Room.objects.get(id=room_id)
    invitor = User.objects.get(id=invitor_id)
    user_service.push(
        event_code=EventCodeChoices.IS_INVITED_TO_ROOM,
        receiver_ids=invitee_ids,
        message=UserNotificationMessage.create_new(
            username=invitor.get_username(),
            avatar=invitor.profile.avatar,
            des_image=DEFAULT_NOTI_IMAGE,
            des_name=room.name,
        ),
    )
