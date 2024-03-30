from constants.config import NOTIFICATION_URL
from mixin.common import SingletonMeta


class NotificationSender(SingletonMeta):
    _base_url = NOTIFICATION_URL

    def _build_request(self, endpoint, params, body):
        return
        # return

    def send(self, user_ids, messages):
        pass
