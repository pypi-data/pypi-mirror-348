from anypoint.custom_logging import CustomLogging
from anypoint.http_client import HttpClient

import logging
import os


class Settings:
    def __init__(self):
        self.user_name: str = os.environ.get('ANYPOINT_USER_NAME', None)
        self.password: str = os.environ.get('ANYPOINT_PASSWORD', None)
        self.client_id: str = os.environ.get('ANYPOINT_CONN_APP_CLIENT_ID', None)
        self.client_secret: str = os.environ.get('ANYPOINT_CONN_APP_CLIENT_SECRET', None)
        self.refresh_token: str = os.environ.get('ANYPOINT_CONN_APP_REFRESH_TOKEN', None)
        self.http_retry_count = 3
        self.http_retry_wait_in_sec = 1
        self.http_timeout_in_sec = 5
        self.anypoint_base_url = "https://anypoint.mulesoft.com"
        self.http_client = HttpClient(self)
        self.logger: logging.Logger = (CustomLogging(enable_wire_logging=False)
                                       .getLogger("anypoint-platform-api-py", True))

        self.auth = None
        self.token: str = None

    def auth_username_password(self, user_name, password):
        self.user_name = user_name
        self.password = password

    def auth_connected_app(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def auth_refresh_token(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
