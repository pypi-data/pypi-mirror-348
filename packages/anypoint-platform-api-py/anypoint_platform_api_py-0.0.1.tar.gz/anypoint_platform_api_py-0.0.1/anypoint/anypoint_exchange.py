import json
import time
import enum

from anypoint.access_management import AccessManagement
from anypoint.http_client import HttpVerbs
from anypoint.settings import Settings
from anypoint.platform import Anypoint

import traceback
import logging


class AnypointExchange(Anypoint):
    # *********************** Internal methods *********************** #
    def __init__(self, setting: Settings, access_management: AccessManagement):
        super().__init__()
        self.setting: Settings = setting
        self.access_management = access_management
        self.base_url = setting.anypoint_base_url
        self.logger: logging.Logger = self.setting.logger

    # *********************** Class Interface method starts below *********************** #

    def exchange_asset_minor_versions(self, org_id: str, exchange_asset_name: str) -> list | None:
        """Get an exchange asset minor version number
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            exchange_asset_name (str): A name of the API. This has to follow naming convention

        Returns:
            list: A list of the minor version of an exchange asset. Return None in case of any error.
                An sample response:
            [
                {
                    "organizationId": "9d5a43ad-7dc7-475a-85b3-88f602cd9850",
                    "groupId": "9d5a43ad-7dc7-475a-85b3-88f602cd9850",
                    "assetId": "ptas-external-proxy-ntrl-dev",
                    "minorVersion": "1.0",
                    "versionGroup": "v1",
                    "isPublic": false,
                    "isSnapshot": false,
                    "statuses": [
                        "published"
                    ]
                }
            ]
        """

        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}"
        }
        url: str = (f"{self.base_url}/exchange/api/v2/assets/{org_id}/{exchange_asset_name}/"
                    f"minorVersions?status=development&status=published&status=deprecated")
        try:
            start = time.time()
            response = self.setting.http_client.call(url=url, http_verbs=HttpVerbs.GET, headers=headers)
            self.logger.debug(f"time=> {time.time() - start}")
            if response.status_code == 200:
                return response.json()
            else:
                self.setting.error(f"ERROR: [{response.status_code}] Unable to query minor versions")
        except Exception as exp:
            traceback.print_exc()
            self.setting.error(f"{exp} -Unable to query minor versions")

        return None

    def get_exchange_asset(self, org_id: str, exchange_asset_name: str) -> dict | None:
        """Get an exchange asset details
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            exchange_asset_name (str): A name of the API. This has to follow naming convention

        Returns:
            dict: Exchange asset details. Return None in case of any error.
                An sample response:
            {
                "groupId": "9d5a43ad-7dc7-475a-85b3-88f602cd9850",
                "assetId": "ptas-external-proxy-ntrl-dev",
                "version": "1.0.75",
                "minorVersion": "1.0",
                "description": "",
                "contactName": null,
                "contactEmail": null,
                "versionGroup": "v1",
                "isPublic": false,
                "name": "ptas-external-proxy-ntrl-dev",
                "type": "rest-api",
                "isSnapshot": false,
                "status": "published",
                "attributes": [],
                "externalFile": {
                    "url": null
                },
                "createdDate": "2024-10-21T20:59:03.826Z",
                "updatedDate": "2024-10-21T20:59:02.680Z",
                "originalFormat": "oas",
                "originalFormatVersion": "2.0",
                "minMuleVersion": null,
                "isMozartTemplate": false,
                "labels": [],
                "categories": [],
                "customFields": [],
                "mule3ConnectorMetadata": {
                    "fullVersion": null,
                    "featureId": null
                },
                "files": [],
                "dependencies": [],
                "generated": [],
                "rating": 0,
                "numberOfRates": 0,
                "createdBy": {
                    "id": "4232879d-c216-4117-8e0e-eaf1b97e9674",
                    "userName": "ahaque_belron",
                    "firstName": "Aminul",
                    "lastName": "Haque"
                },
                "otherVersions": [],
                "instances": [],
                "id": "9d5a43ad-7dc7-475a-85b3-88f602cd9850/ptas-external-proxy-ntrl-dev/1.0.75",
                "icon": null,
                "createdAt": "2024-10-21T20:59:03.826Z",
                "modifiedAt": "2024-10-21T20:59:02.680Z",
                "organization": [],
                "permissions": [
                    "admin",
                    "edit"
                ],
                "versions": []
            }

        """
        try:
            owner_id = self.access_management.get_organisation_owner()
            if owner_id is None:
                self.logger.error(f"Unable to query owner_id")
                return None
            headers: dict = {
                "Authorization": f"Bearer {self.setting.token}",
                "X-Anypnt-Org-Id": org_id,
                "X-Owner-Id": owner_id
            }
            exchange_minor_versions = self.exchange_asset_minor_versions(org_id, exchange_asset_name)
            if exchange_minor_versions and len(exchange_minor_versions) > 0:
                minor_version = exchange_minor_versions[0].get('minorVersion')
                url = (f"{self.base_url}/exchange/api/v2/assets/{org_id}/{exchange_asset_name}/"
                       f"minorVersions/{minor_version}?status=development&status=published&status=deprecated")
                start = time.time()
                response = self.setting.http_client.call(url=url, http_verbs=HttpVerbs.GET, headers=headers)
                self.logger.debug(f"time=> {time.time() - start}")
                if response.status_code == 200:
                    return response.json()
                else:
                    self.setting.logger.error(f"{response.status_code} Unable to query exchange asset versions")
            else:
                self.setting.logger.error(f"[call to exchange_asset_minor_versions failed] - "
                                          f"Unable to query exchange asset versions")

        except Exception as e:
            self.setting.logger.error(f"[{e}] Unable to query exchange asset versions")

        return None
