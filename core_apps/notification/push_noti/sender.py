from mixin.common import SingletonMeta, BaseHttpService
from .message import NotificationMessage


class NotificationSender(BaseHttpService, metaclass=SingletonMeta):
    """
    Push Notification Service should inherit this class.
    """

    endpoint = None
    metaclass = None

    @classmethod
    def new_service(cls, base_url, message_class=None):
        service = super().new_service(base_url)
        service.set_message_class(message_class)
        return service

    def get_push_endpoint(self):
        return self.endpoint

    def set_message_class(self, message_class):
        self.metaclass = message_class

    def validate_meta(self, meta):
        return isinstance(meta, self.metaclass)

    def make_request_body(
        self, event_code, receiver_ids, message: NotificationMessage
    ):
        assert self.validate_meta(message), "Invalid message body"
        return {
            "eventCode": event_code,
            "receiverIDs": receiver_ids,
            "meta": message.to_dict(),
        }

    def push(self, event_code, receiver_ids, message: NotificationMessage):
        self._send(
            self.get_push_endpoint(),
            "post",
            {},
            body=self.make_request_body(
                event_code, receiver_ids=receiver_ids, message=message
            ),
            auth=False,
        )


class UserNotificationSender(NotificationSender):
    endpoint = "/app-notify/"
