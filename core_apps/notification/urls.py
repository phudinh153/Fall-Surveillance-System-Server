from django.urls import path
from . import views as notification_views


urlpatterns = [
    # House notifications
    path(
        "room/<uuid:room_id>/",
        notification_views.RoomNotification.as_view(),
    ),
    # Room notifications
    path(
        "house/<uuid:house_id>/",
        notification_views.HouseNotification.as_view(),
    ),
    path(
        "device/<uuid:device_id>/",
        notification_views.DeviceNotification.as_view(),
    ),
    path(
        "<uuid:id>/mark-seen/",
        notification_views.MarkSeenNotification.as_view(),
    ),
    path(
        "private/",
        notification_views.UserNotification.as_view(),
    ),
    path(
        "event-code/all/", notification_views.EventCodeNotification.as_view()
    ),
]
