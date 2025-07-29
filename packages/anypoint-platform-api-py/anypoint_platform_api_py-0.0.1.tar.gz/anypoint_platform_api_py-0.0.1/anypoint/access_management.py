from anypoint.http_client import HttpVerbs
from anypoint.settings import Settings
from anypoint.platform import Anypoint

import traceback
import logging


class AccessManagement(Anypoint):
    # *********************** Internal methods *********************** #
    def __init__(self, setting: Settings):
        super().__init__()
        self.setting: Settings = setting
        self.base_url = setting.anypoint_base_url
        self.logger: logging.Logger = self.setting.logger

    # *********************** Class Interface method starts below *********************** #

    def list_environments(self, organisation_id: str) -> list:
        environments = None
        url: str = (f"{self.base_url}/accounts/api/"
                    f"cs/organizations/{organisation_id}/environments?limit=150&offset=0")
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}"
        }
        try:
            response = self.setting.http_client.call(url, HttpVerbs.GET, headers)
            environments = response.json()['data']
        except Exception as exp:
            traceback.print_exc()
            self.logger.exception(f"{exp}: Unable to query environments")

        return environments

    def list_business_groups(self) -> list:
        url: str = f"{self.base_url}/accounts/api/profile"
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}"
        }
        try:
            response = self.setting.http_client.call(url, HttpVerbs.GET, headers)
            profile = response.json()
            if profile.get('memberOfOrganizations'):
                return profile.get('memberOfOrganizations')
        except Exception as exp:
            self.logger.error(f"{exp}: Unable to query organisations")

        return None

    def get_organisation_owner(self) -> str | None:
        url: str = f"{self.base_url}/accounts/api/profile"
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}"
        }
        try:
            response = self.setting.http_client.call(url, HttpVerbs.GET, headers)
            profile = response.json()
            if profile:
                return profile.get('id')
        except Exception as exp:
            self.logger.error(f"{exp}: Unable to query owner Id")

        return None

    def list_users(self, root_org_id: str) -> list:
        """List all the users from your Anypoint Organisation
        This function will return entire users

        Args:
            root_org_id (str): Anypoint root business group Id.

        Returns:
            list: This function returns all the  users
        """
        logger = self.setting.logger
        users = []
        limit = 500
        offset = 0
        while True:
            try:
                url = (f"{self.base_url}/accounts/api/organizations/{root_org_id}/"
                       f"users?limit={str(limit)}&offset={str(offset)}&includeProfiles=false")
                headers: dict = {
                    "Authorization": f"Bearer {self.setting.token}"
                }
                response = self.setting.http_client.call(url, HttpVerbs.GET, headers)
                if response.status_code == 200:
                    users_response = response.json()
                    for user in users_response['data']:
                        users.append(user)
                        offset = offset + 1
                    if users_response['total'] > offset:
                        continue
                    else:
                        break
                else:
                    logger.error(f"{response.status_code} Unable to query users")
                    break
            except Exception as e:
                logger.exception(f"{e} - Exception while getting the users.")
                break
        return users

    def delete_user(self, org_id, user_id) -> bool:
        logger = self.setting.logger
        processing_status: bool = False
        try:
            url = f"{self.base_url}/accounts/api/organizations/{org_id}/members/{user_id}"
            headers: dict = {
                "Authorization": f"Bearer {self.setting.token}"
            }
            response = self.setting.http_client.call(url, HttpVerbs.DELETE, headers)
            if response.status_code == 200 or response.status_code == 204:
                processing_status = True
            else:
                logger.error(f"{response.status_code} {response.headers} Unable to delete a user. ")
                processing_status = False

        except Exception as e:
            logger.exception(f"{e} Exception while deleting a the user {user_id}.")
            processing_status = False

        return processing_status
