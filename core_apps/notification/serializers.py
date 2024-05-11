from rest_framework import serializers
from . import models


class RNotification(serializers.ModelSerializer):
    house = serializers.UUIDField(source="house.id", allow_null=True)
    room = serializers.UUIDField(source="room.id", allow_null=True)
    user = serializers.UUIDField(source="user.id", allow_null=True)
    device = serializers.UUIDField(source="device.id", allow_null=True)

    class Meta:
        model = models.Notification
        fields = [
            "id",
            "user",
            "house",
            "room",
            "device",
            "label",
            "description",
            "event_code",
            "is_seen",
            "created_at",
            "meta",
        ]


class MarkSeenNotification(serializers.Serializer):
    ids = serializers.ListField(child=serializers.UUIDField())

    def create(self, validated_data):
        ids = validated_data.get("ids")
        models.Notification.bulk_mark_seen(ids)

        class DumpClass:
            ids = None

        a = DumpClass()
        a.ids = ids
        return a
