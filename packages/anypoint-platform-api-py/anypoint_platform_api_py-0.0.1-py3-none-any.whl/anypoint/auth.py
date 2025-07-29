from anypoint.http_client import HttpVerbs
from anypoint.settings import Settings
from abc import ABC, abstractmethod

import json
import traceback


class Authentication(ABC):
    def __init__(self, setting):
        super().__init__()
        self.setting: Settings = setting
        self.logger = setting.logger
        self.__authenticate()

    def __authenticate(self):
        try:
            data = self.setting.http_client.call(self.url(),
                                                 HttpVerbs.POST,
                                                 self.headers(),
                                                 json.dumps(self.payload()))
            self.setting.token = data.json()['access_token']
            self.logger.info(f"Authentication done!")
        except Exception as exp:
            traceback.print_exc()
            self.logger.error(f"ERROR: {exp}: Something went wrong")
            raise exp

    def recycle_token(self):
        self._authenticate()

    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    def headers(self):
        pass

    @abstractmethod
    def payload(self) -> dict:
        pass


class AuthenticationConnectedApp(Authentication):
    def __init__(self, setting: Settings):
        super().__init__(setting)
        setting.auth = self
        if (setting.client_id is None) or (setting.client_secret is None):
            setting.logger.error(f"Please set the client_id/client_secret in the Configuration object")
            raise Exception("Please set the client_id/client_secret in the Configuration object")

    def url(self):
        return "https://anypoint.mulesoft.com/accounts/api/v2/oauth2/token"

    def headers(self):
        return {"content-type": "application/x-www-form-urlencoded"}

    def payload(self) -> dict:
        return {
            "grant_type": "client_credentials",
            "client_id": self.setting.client_id,
            "client_secret": self.setting.client_secret
        }


class AuthenticationUsernamePassword(Authentication):
    def __init__(self, setting: Settings):
        super().__init__(setting)
        setting.auth = self
        if (setting.user_name is None) or (setting.password is None):
            setting.logger.error(f"Please set the user_name/password in the Configuration object")
            raise Exception("Please set the user_name/password in the Configuration object")

    def url(self):
        return "https://anypoint.mulesoft.com/accounts/login"

    def headers(self):
        return {"content-type": "application/json"}

    def payload(self) -> dict:
        return {
            "username": self.setting.user_name,
            "password": self.setting.password
        }


class AuthenticationRefreshToken(Authentication):
    def __init__(self, setting: Settings):
        super().__init__(setting)
        setting.auth = self
        if setting.refresh_token is None:
            setting.logger.error(f"Please set the refresh_token in the Configuration object")
            raise Exception("Please set the refresh_token in the Configuration object")
        if (setting.client_id is None) or (setting.client_secret is None):
            setting.logger.error(f"Please set the client_id/client_secret in the Configuration object")
            raise Exception("Please set the client_id/client_secret in the Configuration object")

    def url(self):
        return "https://anypoint.mulesoft.com/accounts/api/v2/oauth2/token"

    def headers(self):
        return {"content-type": "application/x-www-form-urlencoded"}

    def payload(self) -> dict:
        return {
            "grant_type": "refresh_token",
            "refresh_token": self.setting.refresh_token,
            "client_id": self.setting.client_id,
            "client_secret": self.setting.client_secret
        }
