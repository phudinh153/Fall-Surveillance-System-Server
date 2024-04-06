import urllib.parse as urlparse
import requests


class SingletonMeta(type):
    """
    Single thread level singleton meta class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BaseHttpService:
    _base_url = None
    headers = {
        "Content-Type": "application/json",
    }
    auth_token = None

    def __init__(self) -> None:
        pass

    @classmethod
    def new_service(cls, base_url):
        service = cls()
        service._base_url = base_url
        return service

    def get_headers(self):
        return self.headers

    def reset_headers(self, headers={}):
        self.headers = headers

    def set_auth_token(self, token):
        self.auth_token = token

    def _get_bearer_token_header(self):
        assert self.auth_token, "Auth token is not set"
        return {"Authorization:": f"Bearer {self.auth_token}"}

    def _send(self, endpoint, method, params, body, auth=False, headers={}):
        assert method in ["get", "post", "put", "delete"], "Invalid method"

        url = urlparse.urljoin(self._base_url, endpoint)
        fetcher = getattr(requests, method)
        headers = (
            headers.update(self._get_bearer_token_header())
            if auth
            else headers
        )
        response = fetcher(url, json=body, params=params, headers=headers)
        return response
