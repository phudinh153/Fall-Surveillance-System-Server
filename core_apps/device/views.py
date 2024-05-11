from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from schema import paginators
from . import serializers
from . import models
from . import permissions as device_permissions

# Create your views here.


class RoomDeviceViewset(
    viewsets.ViewSet,
    generics.ListAPIView,
    generics.CreateAPIView,
    generics.UpdateAPIView,
    generics.RetrieveAPIView,
    generics.DestroyAPIView,
):
    lookup_field = "id"
    serializer_class = serializers.CRUDevice
    permission_classes = [
        permissions.IsAuthenticated,
        device_permissions.HasUpdateRoomPermission,
    ]

    def get_queryset(self):
        room = self.get_room()
        return models.Device.get_room_devices(room=room)

    def get_object(self):
        return models.Device.objects.get(id=self.kwargs["id"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["room"] = self.get_room()
        return context

    def get_room(self):
        from core_apps.house import models as house_models

        if not hasattr(self, "room"):
            self.room = get_object_or_404(
                house_models.Room, id=self.kwargs["room_id"]
            )
            return self.room
        else:
            return self.room


class DeviceSpecViewset(
    viewsets.ViewSet,
    generics.ListAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    lookup_field = "id"
    serializer_class = serializers.RDeiviceSpecDetail
    filter_backends = []
    queryset = models.DeviceSpec.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
        "series_name",
        "gpu",
        "gpu_max_fre",
        "cpu",
        "cpu_max_fre",
        "vision_acceleration",
        "storage",
        "memory",
        "power",
    ]
    pagination_class = paginators.SmallSizePagination


class RetrieveDeviceDetailView(generics.RetrieveAPIView):
    lookup_field = "id"
    serializer_class = serializers.RDeviceDetail
    permission_classes = [
        permissions.IsAuthenticated,
        device_permissions.HasUpdateRoomPermission,
    ]
    queryset = models.Device.objects.all()

    def get_object(self):
        return self.get_device()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["room"] = self.device.room
        return context

    def get_device(self):
        if not hasattr(self, "device"):
            self.device = models.Device.objects.get(id=self.kwargs["id"])
        return self.device

    def get_room(self):
        return self.get_device().room


class NewFallDetectedDeviceNotification(APIView):
    def post(self, request, *args, **kwargs):
        from core_apps.notification import models as notification_models

        device = get_object_or_404(models.Device, id=kwargs["device_id"])
        notification = notification_models.Notification.create_fall_detected_device_notification(
            device=device, fall_image=request.data.get("fall_image", "")
        )
        noticible_users = device.get_notinable_users()
        notification_models.Notification.create_users_notified_fall(
            users=noticible_users, device=device
        )

        return Response(
            {"notification_id": notification.id},
            status=status.HTTP_201_CREATED,
        )


class DeviceInfoFromSerialNumber(APIView):
    def get(self, request, *args, **kwargs):
        from core_apps.user import serializers as user_serializers
        from core_apps.house import serializers as house_serializers

        device = models.Device.objects.filter(
            serial_number=kwargs["serial"]
        ).first()
        if device is None:
            return Response()

        return Response(
            {
                "device": serializers.RDeviceDetail(device).data,
                "members": user_serializers.ReadBasicUserProfile(
                    device.get_notinable_users(), many=True
                ).data,
                "room": house_serializers.RRoomBasic(device.room).data,
            },
            status=status.HTTP_200_OK,
        )
