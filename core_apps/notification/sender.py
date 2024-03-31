from constants.config import NOTIFICATION_URL
import urllib.parse as urlparse
from mixin.common import SingletonMeta
import requests


class NotificationSender(SingletonMeta):
    _base_url = NOTIFICATION_URL

    def _build_request(self, endpoint, params, body):
        return
        # return

    def send(self, endpoint, method, params, body, headers={}):
        assert method in ["get", "post", "put", "delete"], "Invalid method"

        url = urlparse.urljoin(self._base_url, endpoint)
        fetcher = getattr(requests, method)
        return fetcher(url, json=body, params=params, headers=headers)
