from rest_framework import serializers
from . import models


class RNotification(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = [
            "id",
            "user",
            "house",
            "room",
            "label",
            "description",
            "event_code",
            "is_seen",
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
