from requests import Response
from enum import Enum

import requests
import time


class HttpVerbs(Enum):
    GET = 1
    POST = 2
    PATCH = 3
    PUT = 4
    DELETE = 5


class HttpContentType(Enum):
    URL_ENCODE = "application/x-www-form-urlencoded"
    JSON = "application/json"
    MULTIPART_FORM_DATA = "multipart/form-data"
    ARBITRARY_CONTENT_TYPE = ""


class HttpClient:
    def __init__(self, setting):
        super().__init__()
        self.setting = setting

    def call(self, url: str,
             http_verbs: HttpVerbs,
             headers: dict[str, str],
             payload: dict = None,
             files: dict = None,
             content_type: HttpContentType = None) -> Response:
        logger = self.setting.logger
        response = None
        error = None
        for trial_count in range(0, self.setting.http_retry_count):
            error = None
            try:
                if http_verbs == HttpVerbs.GET:
                    response = requests.get(url, headers=headers, timeout=self.setting.http_timeout_in_sec)
                elif http_verbs == HttpVerbs.POST:
                    response = requests.post(url, data=payload, files=files, headers=headers, timeout=self.setting.http_timeout_in_sec)
                elif http_verbs == HttpVerbs.PATCH:
                    response = requests.patch(url, data=payload, files=files, headers=headers, timeout=self.setting.http_timeout_in_sec)
                elif http_verbs == HttpVerbs.PUT:
                    response = requests.put(url, data=payload, files=files, headers=headers, timeout=self.setting.http_timeout_in_sec)
                elif http_verbs == HttpVerbs.DELETE:
                    response = requests.delete(url, data=payload, files=files, headers=headers, timeout=self.setting.http_timeout_in_sec)
                else:
                    msg = f"Not supported method - {http_verbs}"
                    logger.error(msg)
                    raise Exception(msg)

                if 200 <= response.status_code < 400:
                    break  # Success
                elif response.status_code == 401:
                    if self.setting.auth:
                        self.setting.auth.recycle_token()
                        self.__connection_retry_message(trial_count, None)
                        continue
                    break  # Retry after renewing the token
                elif 400 <= response.status_code < 500:
                    break  # Data issue, will not be retried
                elif response.status_code >= 500:
                    self.__connection_retry_message(trial_count, None)
                    continue  # will be retried
            except requests.exceptions.ConnectionError as exp:
                self.__connection_retry_message(trial_count, exp)
                error = exp
            except requests.exceptions.Timeout as exp:
                self.__connection_retry_message(trial_count, exp)
                error = exp
            except Exception as exp:
                logger.error(f"{exp} - Something went wrong while calling the API with URL - {url}. "
                             f"This will not be retried")
                error = exp
        if error:
            raise error

        return response

    def __connection_retry_message(self, trial_count, exp=None) -> bool:
        logger = self.setting.logger
        if exp:
            if trial_count >= (self.setting.http_retry_count - 1):
                logger.error(f"{exp} - Connection error. It will not be retried anymore. ")
            else:
                logger.error(f"{exp} - Connection error. It will be retried again... ")
                time.sleep(self.setting.http_retry_wait_in_sec)
        else:
            if trial_count >= (self.setting.http_retry_count - 1):
                logger.error(f"Connection error. It will not be retried anymore. ")
            else:
                logger.error(f"Connection error. It will be retried again... ")
                time.sleep(self.setting.http_retry_wait_in_sec)
