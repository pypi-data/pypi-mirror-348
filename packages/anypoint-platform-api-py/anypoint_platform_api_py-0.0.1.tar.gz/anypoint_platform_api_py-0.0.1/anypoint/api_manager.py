import json
import time
import enum

from anypoint.anypoint_exchange import AnypointExchange
from anypoint.http_client import HttpVerbs
from anypoint.settings import Settings
from anypoint.platform import Anypoint

import traceback
import logging


class ApiManager(Anypoint):
    # *********************** Internal methods *********************** #
    def __init__(self, setting: Settings, exchange: AnypointExchange):
        super().__init__()
        self.setting: Settings = setting
        self.exchange = exchange
        self.base_url = setting.anypoint_base_url
        self.logger: logging.Logger = self.setting.logger

    # *********************** Class Interface method starts below *********************** #

    def create_api_instance(self, org_id: str, env_id: str, exchange_asset_name: str) -> dict | None:
        """Create an API instance with the name and asset version.
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
            exchange_asset_name (str): A name of the API. This has to follow naming convention

        Returns:
            dict: This function returns the response in case of success. Return None in case of any error.
        """
        url: str = f"{self.base_url}/apimanager/xapi/v1/organizations/{org_id}/environments/{env_id}/apis"
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id,
            "content-type": "application/json"
        }
        try:
            exchange_asset = self.exchange.get_exchange_asset(org_id, exchange_asset_name)
            if exchange_asset is None:
                self.logger.error(f"Unable to query the exchange asset by {exchange_asset_name}")
                return None
            dict_payload: dict = {
                "technology": "mule4",
                "endpointUri": None,
                "endpoint": {
                    "muleVersion4OrAbove": True,
                    "uri": None,
                    "type": "http",
                    "isCloudHub": None,
                    "proxyUri": None,
                    "referencesUserDomain": None,
                    "responseTimeout": None
                },
                "spec": {
                    "assetId": exchange_asset_name,
                    "groupId": org_id,
                    "version": exchange_asset['version']
                }
            }
            start = time.time()
            response = self.setting.http_client.call(url=url, http_verbs=HttpVerbs.POST,
                                                     headers=headers, payload=json.dumps(dict_payload))
            self.logger.debug(f"time=> {time.time() - start}")
            if response.status_code == 200 or response.status_code == 201:
                return response.json()
            else:
                traceback.print_exc()
                self.setting.error(f"[{response.status_code}] Unable to create API instance")

        except Exception as exp:
            traceback.print_exc()
            self.setting.error(f"{exp} - Unable to create API instance")

        return None

    def list_apis(self, org_id: str, env_id: str) -> list | None:
        """List all the API instances from a particular environment.
        This API will call the API once, so may not be able to return all the API instances.
        if your objective is to list all the APIs then call @list_apis_all

        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID

        Returns:
            list: This function returns all the API instances. Return None in case of any error. An example is below:
            [
            {
            "audit": {
                "created": {
                    "date": "2023-10-27T12:13:55.625Z"
                },
                "updated": {}
            },
            "masterOrganizationId": "c6d5cc03-f9f9-48ef-a64a-2d4e278710b9",
            "organizationId": "75dbd05f-1b06-4cf7-b3be-b8bfbc18afc9",
            "id": 213091936,
            "name": "groupId:75dbd05f-1b06-4cf7-b3be-b8bfbc18afc9:assetId:secret-manager-utility-api",
            "exchangeAssetName": "Secret Manager Utility API",
            "groupId": "75dbd05f-1b06-4cf7-b3be-b8bfbc18afc9",
            "assetId": "secret-manager-utility-api",
            "apis": [
                        {
                            "audit": {
                                "created": {
                                    "date": "2024-03-26T18:27:16.774Z"
                                },
                                "updated": {}
                            },
                            "masterOrganizationId": "xxx-xxxx",
                            "organizationId": "xxx-xxxx",
                            "id": 1298320, # This is API Instance Id
                            "instanceLabel": "bel-eu-gbl-secretmanager-sys-v1-dev",
                            "groupId": "xxx-xxxx",
                            "assetId": "secret-manager-utility-api",
                            "assetVersion": "1.0.2",
                            "productVersion": "v1",
                            "description": null,
                            "tags": [],
                            "order": 1,
                            "providerId": "xxx-xxxx",
                            "deprecated": false,
                            "lastActiveDate": "2025-05-12T08:28:35.544Z",
                            "endpointUri": null,
                            "environmentId": "xxx-xxxx",
                            "isPublic": false,
                            "stage": "release",
                            "technology": "mule4",
                            "status": "active",
                            "approvalMethod": null,
                            "deployment": null,
                            "lastActiveDelta": 33,
                            "pinned": false,
                            "activeContractsCount": 0,
                            "autodiscoveryInstanceName": "v1:1298320"
                        }
                    ],
                    "totalApis": 1,
                    "autodiscoveryApiName": "groupId:xxx-xxx-xxx:assetId:secret-manager-utility-api"
                }
            ]
        """
        url: str = f"{self.base_url}/apimanager/api/v1/organizations/{org_id}/environments/{env_id}/apis"
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id
        }
        try:
            response = self.setting.http_client.call(url, HttpVerbs.GET, headers)
            if response.status_code == 200:
                instances = response.json()
                return instances['assets']
            else:
                self.logger.error(
                    f"{org_id}:{env_id} - [Error Response=> {response.content} "
                    f"StatusCode=> {response.status_code}] "
                    f"Unable to query API Manager instances")
        except Exception as exp:
            traceback.print_exc()
            self.logger.error(f"{exp} - {org_id}:{env_id} Unable to query API Manager instances")
        return None

    def list_apis_all(self, org_id: str, env_id: str) -> list | None:
        """List all the API instances from a particular environment.
        This function will return entire API instances from an environment

        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID

        Returns:
            list: This function returns all the API instances. Return None in case of any error. An example given below:
            [
                {
                    "audit": {
                        "created": {
                            "date": "2024-03-26T18:27:16.774Z"
                        },
                        "updated": {}
                    },
                    "masterOrganizationId": "xxx-xxxx"",
                    "organizationId": "xxx-xxxx"",
                    "id": 234567,
                    "instanceLabel": "bel-eu-gbl-secretmanager-sys-v1-dev",
                    "groupId": "xxx-xxxx",
                    "assetId": "secret-manager-utility-api",
                    "assetVersion": "1.0.2",
                    "productVersion": "v1",
                    "description": null,
                    "tags": [],
                    "order": 1,
                    "providerId": "xxx-xxxx",
                    "deprecated": false,
                    "lastActiveDate": "2025-05-12T08:25:34.649Z",
                    "endpointUri": null,
                    "environmentId": "xxx-xxxx",
                    "isPublic": false,
                    "stage": "release",
                    "technology": "mule4",
                    "status": "active",
                    "approvalMethod": null,
                    "deployment": null,
                    "lastActiveDelta": 51,
                    "pinned": false,
                    "activeContractsCount": 0,
                    "asset": {
                        "name": "groupId:xxx-xxxx:assetId:secret-manager-utility-api",
                        "exchangeAssetName": "Secret Manager Utility API",
                        "groupId": "xxx-xxxx",
                        "assetId": "secret-manager-utility-api"
                    },
                    "autodiscoveryInstanceName": "v1:234567"
                }
            ]
        """
        apis = None
        pageSize = 250
        page = 0
        totalReceived = 0
        while True:
            url = (f"https://anypoint.mulesoft.com/apimanager/xapi/v1/organizations/{org_id}/environments/{env_id}/" +
                   f"apis?pinnedFirst=true&sort=name&ascending=false&limit={str(pageSize)}&offset={str(page)}")
            headers: dict = {
                "Authorization": f"Bearer {self.setting.token}",
                "x-anypnt-env-id": env_id,
                "x-anypnt-org-id": org_id
            }
            try:
                response = self.setting.http_client.call(url, HttpVerbs.GET, headers)
                apiList = response.json()
                if response.status_code == 200:
                    if apis is None:
                        apis = []
                    if apiList.get('instances'):
                        count = 0
                        for apiInstance in apiList.get('instances'):
                            apis.append(apiInstance)
                            count = count + 1

                        totalReceived = totalReceived + count
                        page = page + totalReceived

                        if totalReceived >= apiList['total'] or count == 0:
                            break
                        else:
                            self.logger.info(f"{org_id} {env_id} Query next page...")
                    else:
                        break
                else:
                    self.logger.error(
                        f"{org_id}:{env_id} - [Error Response=> {response.content} "
                        f"StatusCode=> {response.status_code}] "
                        f"Unable to query API Manager instances")
            except Exception as exp:
                self.logger.error(f"{exp} - Unable to query APIs orgId=> {org_id} env=> {env_id}")
                break
        return apis

    def policy_template_by_asset_id(self, org_id: str, asset_id: str) -> dict | None:
        """Retrieve policy template by ord_id and asset_id.
           This method will be useful while managing API policy (apply or update).

        Args:
            org_id (str): Business Group id. Normally this is a GUID
            asset_id (str): Policy template asset_id. Normally this is the name of the policy.

        Returns:
            dict: This function returns the full details of the policy template. Return None in case of any error.
            An example given below:
            {
                    "audit": {
                        "created": {
                            "date": "2022-05-26T19:23:00.651Z"
                        },
                        "updated": {}
                    },
                    "id": 341467,
                    "groupId": "68ef9520-24e9-4cf2-b2f5-620025690913",
                    "assetId": "spike-control",
                    "version": "1.2.1",
                    "name": "Spike Control",
                    "description": "Control spikes in traffic by limiting the number of messages processed by an API. If the number is exceeded, the request will be queued for retry according to configuration.\nUses a sliding window algorithm, ensuring that no more than the configured maximum requests are processed in the last X milliseconds (X being the configured time period).\nApplies spike control to all API calls, regardless of the source.",
                    "type": "policy",
                    "isOOTB": true,
                    "stage": "release",
                    "status": "published",
                    "yamlMd5": "3b338490af8abc53c26bb3cbff71ec63",
                    "jarMd5": null,
                    "orgId": "68ef9520-24e9-4cf2-b2f5-620025690913",
                    "minMuleVersion": null,
                    "schemaId": "18fd025f-31fa-41c1-834e-e6e18767947c",
                    "category": "Quality of service",
                    "providedCharacteristics": [],
                    "requiredCharacteristics": [],
                    "interfaceScope": [
                        "api",
                        "resource"
                    ],
                    "violationCategory": "qos",
                    "interfaceTransformation": [],
                    "applicable": true
            }

        """
        url = (f"https://anypoint.mulesoft.com/apimanager/xapi/v1/organizations/{org_id}/"
               f"exchange-policy-templates?latest=true")
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-org-id": org_id
        }
        try:
            response = self.setting.http_client.call(url, HttpVerbs.GET, headers)
            if response.status_code == 200:
                templates = response.json()
                for template in templates:
                    if template.get('assetId') and template.get('assetId') == asset_id:
                        return template
            else:
                self.logger.error(
                    f"{response.status_code} - Unable to query exchange policy template - {asset_id}")
        except Exception as exp:
            self.logger.error(f"{exp} - Unable to query exchange policy template - {asset_id}")

        return None

    def list_policies(self, org_id: str, env_id, api_instance_id: str) -> list | None:
        """List all the policies applied to an API

        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
            api_instance_id (str): API Instance Id.

        Returns:
            list: This function returns all the policies. Return None in case of any error. An example below:
            [
                {
                    "audit": {
                        "created": {
                            "date": "2025-02-24T02:50:40.635Z"
                        },
                        "updated": {}
                    },
                    "masterOrganizationId": "xxxxx-xxxx-xxxx",
                    "organizationId": "xxxxx-xxxxxx",
                    "id": 1231424,
                    "policyTemplateId": "12123",
                    "configurationData": {
                        "maximumRequests": 250,
                        "timePeriodInMilliseconds": 5000,
                        "delayTimeInMillis": 300,
                        "delayAttempts": 1,
                        "queuingLimit": 5,
                        "exposeHeaders": true
                    },
                    "order": 1,
                    "disabled": false,
                    "pointcutData": null,
                    "groupId": "68ef9520-24e9-4cf2-b2f5-620025690913",
                    "assetId": "spike-control",
                    "assetVersion": "1.2.1",
                    "type": "system",
                    "apiId": 12312342
                }
            ]
        """
        url = (f"https://anypoint.mulesoft.com/apimanager/api/v1/organizations/{org_id}/"
               f"environments/{env_id}/apis/{str(api_instance_id)}/policies?fullInfo=false")
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id
        }
        try:
            response = self.setting.http_client.call(url, HttpVerbs.GET, headers)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(
                    f"{response.status_code} - Unable to query policies for the following API {api_instance_id}")
        except Exception as exp:
            self.logger.error(f"{exp} - Unable to query policies for the following API {api_instance_id}")

        return None

    def list_sla_tiers(self, org_id: str, env_id, api_instance_id: str) -> list | None:
        """List all the SLA tiers created against an API
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
            api_instance_id (str): API Instance Id.
        Returns:
            list: This function returns all the SLA tiers. Return None in case of any error. An example below:
            [
                {
                    "audit": {
                        "created": {
                            "date": "2025-02-24T02:50:39.691Z"
                        },
                        "updated": {}
                    },
                    "masterOrganizationId": "xxx-xxxxx",
                    "organizationId": "xxxx-xxx-xxx",
                    "id": 123123,
                    "name": "Gold",
                    "description": "This is a standard SLA Tier for most Belron API",
                    "limits": [
                        {
                            "maximumRequests": 1800,
                            "timePeriodInMilliseconds": 60000,
                            "visible": true
                            }
                        ],
                    "status": "ACTIVE",
                    "autoApprove": false,
                    "applicationCount": 0,
                    "apiId": 235232
                }
            ]
        """
        url = (f"https://anypoint.mulesoft.com/apimanager/api/v1/organizations/{org_id}/"
               f"environments/{env_id}/apis/{api_instance_id}/tiers?limit=200&offset=0")
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id
        }
        try:
            response = self.setting.http_client.call(url, HttpVerbs.GET, headers)
            if response.status_code == 200:
                return response.json()['tiers']
            else:
                self.logger.error(
                    f"{response.status_code} - Unable to query SLA tiers for the following API {api_instance_id}")
        except Exception as exp:
            self.logger.error(f"{exp} - Unable to query SLA tiers  for the following API {api_instance_id}")

        return None

    def list_contracts(self, org_id: str, env_id, api_instance_id: str) -> list | None:
        """List all the contracts of an API
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
            api_instance_id (str): API Instance Id.
        Returns:
            list: This function returns all the contracts of an API. Return None in case of any error. An example below
            [
                {
                    "audit": {
                        "created": {
                            "date": "2024-07-01T12:07:28.444Z"
                        },
                        "updated": {}
                    },
                    "masterOrganizationId": "xxxx-xxx-xxxx",
                    "organizationId": "xxxx-xxxx-xxx",
                    "id": 423474383,
                    "status": "APPROVED",
                    "approvedDate": "2024-07-01T12:07:28.488Z",
                    "rejectedDate": null,
                    "revokedDate": null,
                    "applicationId": 1422343232,
                    "application": {
                        "audit": {
                            "created": {
                                "date": "2022-12-20T13:51:47.861Z"
                            },
                            "updated": {}
                        },
                        "id": 1422343232,
                        "name": "api-client-gbl-ewp-exp-dev",
                        "description": "EWP Experience API",
                        "clientProvider": {},
                        "coreServicesId": "xxxxxxxx",
                        "url": null
                    }
                }
            ]
        """
        url = (f"https://anypoint.mulesoft.com/apimanager/api/v1/organizations/{org_id}/"
               f"environments/{env_id}/apis/{api_instance_id}/contracts?limit=200&offset=0&sort=name&ascending=true")
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id
        }
        limit = 20
        offset = 0
        count = 1
        contracts = None
        while True:
            url = (f"https://anypoint.mulesoft.com/apimanager/api/v1/organizations/{org_id}/"
                   f"environments/{env_id}/apis/{api_instance_id}/contracts?limit={limit}&offset={offset}"
                   f"&sort=name&ascending=true")
            try:
                start = time.time()
                response = self.setting.http_client.call(url, HttpVerbs.GET, headers)
                self.logger.debug(f"{count}: time=> {time.time() - start}, offset=> {offset}")
                count = count + 1
                if response.status_code == 200:
                    if contracts is None:
                        contracts = []
                    response_object = response.json()
                    total = response_object['total']
                    if (response_object is not None) and len(response_object['contracts']) > 0:
                        for item in response_object['contracts']:
                            contracts.append(item)
                        if total == len(contracts):
                            break
                        else:
                            offset = offset + limit
                            continue
                    else:
                        break
                else:
                    self.logger.error(
                        f"{response.status_code} - Unable to query contracts for the following API {api_instance_id}")
                    break
            except Exception as exp:
                self.logger.error(f"{exp} - Unable to query contracts for the following API {api_instance_id}")
                break

        return contracts

    def api_settings(self, org_id: str, env_id, api_instance_id: str) -> dict | None:
        """Return the API settings based on API instance Id
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
            api_instance_id (str): API Instance Id.
        Returns:
            dict: This function returns the API settings. Return None in case of any error. An example below
            {
                "audit": {
                    "created": {
                        "date": "2023-03-21T20:09:06.665Z"
                    },
                    "updated": {
                        "date": "2023-12-09T21:18:32.952Z"
                    }
                },
                "masterOrganizationId": "xxxx-xxx-xxxx",
                "organizationId": "xxxx-xxx-xxxx",
                "id": 24223122,
                "instanceLabel": "bel-eu-gbl-amq-console-exp-v1-dev",
                "groupId": "xxxx-xxx-xxxx",
                "assetId": "bel-all-gbl-amq-console-exp",
                "assetVersion": "1.0.0",
                "productVersion": "v1",
                "description": null,
                "tags": [
                    "unknown",
                    "experience-api"
                ],
                "order": 1,
                "providerId": "xxxx-xxx-xxxx",
                "deprecated": false,
                "lastActiveDate": "2025-05-12T09:06:27.038Z",
                "endpointUri": null,
                "environmentId": "xxxx-xxx-xxxx",
                "isPublic": false,
                "stage": "release",
                "technology": "mule4",
                "status": "active",
                "approvalMethod": null,
                "endpoint": {
                    "audit": {
                        "created": {},
                        "updated": {}
                    },
                    "id": 21342123,
                    "type": "raml",
                    "uri": "https://{env}.{region}.api.belron.com/gbl/amq-console/v1",
                    "apiGatewayVersion": "4.6.15",
                    "proxyUri": null,
                    "proxyRegistrationUri": null,
                    "lastActiveDate": null,
                    "isCloudHub": true,
                    "deploymentType": "CH",
                    "policiesVersion": null,
                    "referencesUserDomain": null,
                    "responseTimeout": null,
                    "wsdlConfig": null,
                    "runtimeMetadata": {
                        "javaVersion": "8"
                    },
                    "muleVersion4OrAbove": true
                },
                "deployment": null,
                "lastActiveDelta": 37,
                "autodiscoveryInstanceName": "v1:24223122"
            }
        """
        url = (f"https://anypoint.mulesoft.com/apimanager/api/v1/organizations/{org_id}/"
               f"environments/{env_id}/apis/{api_instance_id}?includeProxyConfiguration=true&includeTlsContexts=true")
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id
        }
        try:
            response = self.setting.http_client.call(url, HttpVerbs.GET, headers)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(
                    f"{response.status_code} - Unable to query the settings for the API {api_instance_id}")
        except Exception as exp:
            self.logger.error(f"{exp} - Unable to query the settings for the API {api_instance_id}")

        return None

    def list_client_application(self, org_id: str, env_id) -> list | None:
        """Returns all the client applications of an Anypoint Organisation
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
        Returns:
            dict: This function returns an array of client applications. Return None in case of any error.
            An example below:
            [
                {
                    "audit": {
                        "created": {
                            "date": "2021-02-26T20:43:11.392Z"
                        },
                        "updated": {}
                    },
                    "masterOrganizationId": "xxx-xxxx",
                    "id": 24233423,
                    "name": "Account Non-Prod",
                    "description": "Safelite for Agents",
                    "clientProvider": {
                        "name": "Anypoint",
                        "providerId": null,
                        "type": null
                    },
                    "coreServicesId": "xxx-xxxx",
                    "url": null,
                    "clientId": "xxx-xxxx",
                    "clientSecret": "xxx-xxxx",
                    "grantTypes": [],
                    "redirectUri": [],
                    "owner": "N/A",
                    "email": "N/A",
                    "owners": [
                        {
                            "id": "xxx-xxxx",
                            "organizationId": "xxx-xxxx",
                            "firstName": "Joel",
                            "lastName": "Subash",
                            "email": "xxx@xxxx",
                            "username": "xxx-xxxx",
                            "entityType": "user"
                        }
                    ]
                }
            ]

        """
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id
        }
        limit = 100
        offset = 0
        client_apps = None
        count = 1
        while True:

            try:
                url: str = ("https://anypoint.mulesoft.com/apiplatform/"
                            f"repository/v2/organizations/{org_id}/applications"
                            f"?ascending=true&filter=all&limit={limit}&"
                            f"literalMatch=true&offset={offset}&sort=name&targetAdminSite=true")
                start = time.time()
                response = self.setting.http_client.call(url, HttpVerbs.GET, headers)
                self.logger.debug(f"{count}: time=> {time.time() - start}, offset=> {offset}")
                count = count + 1
                if response.status_code == 200:
                    if client_apps is None:
                        client_apps = []
                    response_object = response.json()
                    total = response_object.get('total')
                    if (response_object is not None) and len(response_object['applications']) > 0:
                        for app in response_object['applications']:
                            client_apps.append(app)
                            offset = offset + 1
                    if offset >= total:
                        break
                else:
                    self.logger.error(
                        f"{response.status_code} - Unable to query client applications. ")
                    break
            except Exception as exp:
                self.logger.error(f"{exp} - Unable to query client applications. ")
                break
        return client_apps

    def list_automated_policies(self, org_id: str, env_id) -> list | None:
        """Returns all the automated policies applied to a particular environment
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
        Returns:
            list: This function returns an array of automated policies. Return None in case of any error.
            An example below:
            [
                {
                    "audit": {
                        "created": {
                            "date": "2025-05-13T10:23:21.062Z"
                        },
                        "updated": {
                            "date": "2025-05-13T10:23:21.062Z"
                        }
                    },
                    "id": 125754,
                    "ruleOfApplication": {
                        "range": {
                            "from": "4.6.0"
                        },
                        "javaVersions": [
                            "8",
                            "11",
                            "17"
                        ],
                        "technologies": [
                            "mule4"
                        ],
                        "environmentId": "xxx-xxxx",
                        "organizationId": "xxx-xxxx"
                    },
                    "groupId": "xxx-xxxx",
                    "assetId": "header-injection",
                    "assetVersion": "1.3.1",
                    "configurationData": {
                        "inboundHeaders": [
                            {
                                "key": "nam",
                                "value": "value"
                            }
                        ],
                        "outboundHeaders": [
                            {
                                "key": "name_key",
                                "value": "value"
                            }
                        ]
                    },
                    "configuration": {
                        "id": "xxx-xxxx",
                        "version": "1"
                    },
                    "pointcutData": null,
                    "order": 2,
                    "disabled": false,
                    "implementationAssets": [
                        {
                            "name": "Header Injection - Flex",
                            "assetId": "header-injection-flex",
                            "groupId": "xxx-xxxx",
                            "version": "1.2.0",
                            "technology": "flexGateway",
                            "releaseNotes": "* Handling non-utf8 headers\n",
                            "organizationId": "xxx-xxxx",
                            "minRuntimeVersion": "1.0.0"
                        },
                        {
                            "name": "Header Injection - Mule4",
                            "assetId": "header-injection-mule",
                            "groupId": "xxx-xxxx",
                            "version": "1.4.0",
                            "technology": "mule4",
                            "releaseNotes": "* Java 17 compatibility.\n",
                            "organizationId": "xxx-xxxx",
                            "minRuntimeVersion": "4.1.0",
                            "supportedJavaVersions": [
                                "17",
                                "11",
                                "8"
                            ]
                        },
                        {
                            "name": "Header Injection - Mule4",
                            "assetId": "header-injection-mule",
                            "groupId": "xxx-xxxx",
                            "version": "1.3.0",
                            "technology": "mule4",
                            "releaseNotes": "* Separated Policy Definition from Policy Implementation.\n",
                            "organizationId": "xxx-xxxx",
                            "minRuntimeVersion": "4.1.0"
                        }
                    ]
                }
            ]
        """
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id
        }
        url = (f"https://anypoint.mulesoft.com/apimanager/xapi/v1/organizations/"
               f"{org_id}/automated-policies?environmentId={env_id}")

        try:
            start = time.time()
            response = self.setting.http_client.call(url, HttpVerbs.GET, headers)
            self.logger.debug(f"time=> {time.time() - start}")
            if response.status_code == 200:
                policies = response.json()
                if policies and policies.get('automatedPolicies'):
                    return policies.get('automatedPolicies')
                else:
                    return []
            else:
                self.logger.error(f"{response.status_code} Exception while querying the policies. ")

        except Exception as exp:
            self.logger.error(f"{exp} - Unable to query automated policies. ")

        return None

    def apply_automated_policy(self, org_id: str, env_id: str,
                               policy_asset_id: str,
                               policy_asset_version: str,
                               mule_runtime_from_version: str,
                               policy_config_data: dict,
                               policy_asset_group_id: str,
                               mule_runtime_to_version: str = None,
                               java_17: bool = True, java_8: bool = True) -> dict | None:
        """Apply an automated policy
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
            policy_asset_id (str): Policy asset id, for example "message-logging", "spike-control" etc.
            policy_asset_version (str): This is the version of the policy asset.
                You are supposed to call self@policy_template_by_asset_id#version with the policy_asset_id.
                Which will then will provide all the these information
            mule_runtime_from_version (str): From which Mule Runtime version the automated policy will be applicable.
                Any API which is deployed with any lower Mule runtime will not be selected for this automated policy
            policy_config_data (dict):  This will needs to be build based on the policy configuration.
                It will be different for each policy
            policy_asset_group_id (str): Policy asset Group id. self@policy_template_by_asset_id#orgId
            mule_runtime_to_version (str): Default is support all the versions.
            java_17 (bool):  Java 17 support
            java_8 (bool):  Java 8 support

        Returns:
            dict: Return the success object when success. Return None in case of any error.
        """
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id,
            "content-type": "application/json"
        }
        url = f"{self.base_url}/apimanager/api/v1/organizations/{org_id}/automated-policies"
        if java_17 and java_8:
            javaVersions = ["8", "11", "17"]
        elif java_17:
            javaVersions = ["17"]
        else:
            javaVersions = ["8"]

        dictPayload = {
            "configurationData": policy_config_data,
            "pointcutData": None,
            "ruleOfApplication": {
                "organizationId": org_id,
                "environmentId": env_id,
                "technologies": [
                    "mule4"
                ],
                "range": {
                    "from": mule_runtime_from_version
                },
                "javaVersions": javaVersions
            },
            "groupId": policy_asset_group_id,
            "assetId": policy_asset_id,
            "assetVersion": policy_asset_version
        }
        if mule_runtime_to_version:
            dictPayload['ruleOfApplication']['range']['to'] = mule_runtime_to_version

        try:
            start = time.time()
            response = self.setting.http_client.call(url=url, http_verbs=HttpVerbs.POST,
                                                     headers=headers, payload=json.dumps(dictPayload))
            self.logger.debug(f"time=> {time.time() - start}")
            if response.status_code in [200, 201]:
                return response.json()
            else:
                self.logger.error(f"{response.status_code} Exception while applying the policy. ")

        except Exception as exp:
            self.logger.error(f"{exp} Unable to apply automated policies. ")

        return None

    def un_apply_automated_policy(self, org_id: str, env_id, policy_id: str) -> dict | None:
        """Un-apply an automated policy
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
            policy_id (str): This attribute can be sourced from an object from the self@list_automated_policies#id result.
                Needs to pass the policy_id of the automated policy you would like to remove
        Returns:
            dict: Return the success object when success. Return None in case of any error.
        """
        url = (f"https://anypoint.mulesoft.com/apimanager/api/v1/organizations/"
               f"{org_id}/automated-policies/{policy_id}")

        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id
        }

        try:
            start = time.time()
            response = self.setting.http_client.call(url, HttpVerbs.DELETE, headers)
            self.logger.debug(f"time=> {time.time() - start}")
            if response.status_code == 200 or response.status_code == 204:
                return response
            else:
                self.logger.error(f"{response.status_code} Exception while deleting the policy. ")

        except Exception as exp:
            self.logger.error(f"{exp} Unable to delete the automated policy")

        return None

    def update_automated_policy(self, org_id: str, env_id: str, policy_asset_id: str, policy_asset_version: str,
                                mule_runtime_from_version: str, policy_config_data: dict,
                                mule_runtime_to_version: str = None,
                                java_17: bool = True, java_8: bool = True) -> dict | None:
        """Update an existing applied automated policy
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
            policy_asset_id (str): Policy asset id, for example "message-logging", "spike-control" etc.
            policy_asset_version (str): This is the version of the policy asset.
                You are supposed to call self@policy_template_by_asset_id with the policy_asset_id.
                Which will then will provide all the these information
            mule_runtime_from_version (str): From which Mule Runtime version the automated policy will be applicable.
                Any API which is deployed with any lower Mule runtime will not be selected for this automated policy
            policy_config_data (dict):  This will needs to be build based on the policy configuration.
                It will be different for each policy. An example config for message-logging policy:
                ```{
                    "loggingConfiguration": [{
                        "itemName": "Default configuration",
                        "itemData": {
                            "message": "#[attributes.headers['correlationId']]",
                            "level": "INFO",
                            "firstSection": true,
                            "secondSection": false
                        }
                    }]
                }```
            mule_runtime_to_version (str): Default is support all the versions.
            java_17 (bool):  Default is True. Java 17 support
            java_8 (bool):  Default is True. Java 8 support
        Returns:
            dict: Return the success object when success. Return None in case of any error.
        """
        policies = self.list_automated_policies(org_id, env_id)
        policy = None
        if policies:
            for p in policies:
                if p['assetId'] == policy_asset_id:
                    policy = p
                    break
        else:
            self.logger.error(f"There are no such policy [{policy_asset_id}] applied already ")
            return []

        url = (f"https://anypoint.mulesoft.com/apimanager/api/v1/organizations/"
               f"{org_id}/automated-policies/{policy['id']}")
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id,
            "content-type": "application/json"
        }

        if java_17 and java_8:
            policy['ruleOfApplication']['javaVersions'] = ["8", "11", "17"]
        elif java_17:
            policy['ruleOfApplication']['javaVersions'] = ["17"]
        else:
            policy['ruleOfApplication']['javaVersions'] = ["8"]

        if policy_asset_version:
            policy['assetVersion'] = policy_asset_version
        if mule_runtime_from_version:
            policy['ruleOfApplication']['range']['from'] = mule_runtime_from_version
        if mule_runtime_to_version:
            policy['ruleOfApplication']['range']['to'] = mule_runtime_to_version
        if policy_config_data:
            policy['configurationData'] = policy_config_data

        try:
            start = time.time()
            response = self.setting.http_client.call(url, HttpVerbs.PATCH, headers, json.dumps(policy))
            self.logger.debug(f"time=> {time.time() - start}")
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"{response.status_code} Exception while updating the policy")

        except Exception as exp:
            self.logger.error(f"{exp} Unable to update automated policies")

        return None

    def add_api_instance_tag(self, org_id: str, env_id: str, api_instance_id: str, tag: str) -> dict | None:
        """Add API instance tag based on an tag Id
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
            api_instance_id (str): API Instance Id.
            tag (str): A string value for the tag
        Returns:
            dict: Return the success object when success. Return None in case of any error.
        """

        url = (f"https://anypoint.mulesoft.com/apimanager/api/v1/organizations/{org_id}/environments/{env_id}/"
               f"apis/{api_instance_id}/tags/{tag}")
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id
        }
        try:
            start = time.time()
            response = self.setting.http_client.call(url, HttpVerbs.PUT, headers)
            self.logger.debug(f"time=> {time.time() - start}")
            if response.status_code in [200, 201, 209]:
                return response
            else:
                self.logger.error(f"{response.status_code} Exception while adding instance tag")

        except Exception as exp:
            self.logger.error(f"{exp} Exception while adding instance tag")

        return None

    def remove_api_instance_tag(self, org_id: str, env_id: str, api_instance_id: str, tag: str) -> dict | None:
        """Remove API instance tag based on an tag Id
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
            api_instance_id (str): API Instance Id.
            tag (str): The tag you want to remove
        Returns:
            dict: Return the success object when success. Return None in case of any error.
        """

        url = (f"https://anypoint.mulesoft.com/apimanager/api/v1/organizations/{org_id}/environments/{env_id}/"
               f"apis/{api_instance_id}/tags/{tag}")
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id
        }
        try:
            start = time.time()
            response = self.setting.http_client.call(url, HttpVerbs.DELETE, headers)
            self.logger.debug(f"time=> {time.time() - start}")
            if response.status_code in [200, 204]:
                return response
            else:
                self.logger.error(f"{response.status_code} Exception while removing instance tag")

        except Exception as exp:
            self.logger.error(f"{exp} Exception while removing instance tag")

        return None

    def apply_policy(self, org_id: str, env_id: str,
                     policy_asset_id: str,
                     api_instance_id: str,
                     policy_config_data: dict,
                     policy_asset_version: str = None) -> dict | None:
        """This method will help applying an API gateway policy to an API
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
            policy_asset_id (str): Policy asset id, for example "message-logging", "spike-control" etc.
            api_instance_id (str): API Instance Id.
            policy_config_data (dict): This config is going to vary between policy. Every policy has a separate
                policy config. And example of this config for message-logging policy is:
                {
                    "loggingConfiguration": [{
                        "itemName": "Default configuration",
                        "itemData": {
                            "message": "#[attributes.headers['id']]",
                            "level": "INFO",
                            "firstSection": True,
                            "secondSection": False
                        }
                    }]
                }
            policy_asset_version (str): This is the version of the policy asset.
                You are supposed to call self@policy_template_by_asset_id#version with the policy_asset_id.
                Which will then will provide all the these information
        Returns:
            dict: Return the success object when success. Return None in case of any error.
        """

        template = self.policy_template_by_asset_id(org_id=org_id, asset_id=policy_asset_id)
        if template is None:
            return None

        policy_config = {
            "configurationData": policy_config_data,
            "apiVersionId": api_instance_id,
            "pointcutData": None,
            "policyTemplateId": template['id'],
            "groupId": template['groupId'],
            "assetId": policy_asset_id,
            "assetVersion": template['version']
        }
        if policy_asset_version:
            policy_config['assetVersion'] = policy_asset_version

        url = (f"https://anypoint.mulesoft.com/apimanager/api/v1/organizations/{org_id}/environments/"
               f"{env_id}/apis/{api_instance_id}/policies")
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id,
            "content-type": "application/json"
        }
        try:
            start = time.time()
            response = self.setting.http_client.call(url, HttpVerbs.POST, headers,
                                                     payload=json.dumps(policy_config))
            self.logger.debug(f"time=> {time.time() - start}")
            if response.status_code == 201:
                return response.json()
            else:
                self.logger.error(f"{response.status_code} Exception while applying policy")

        except Exception as exp:
            self.logger.error(f"{exp} Exception while applying policy")

        return None

    def update_policy(self, org_id: str, env_id: str,
                      policy_asset_id: str,
                      api_instance_id: str,
                      policy_config_data: dict,
                      policy: dict,
                      policy_asset_version: str = None) -> dict | None:
        """This method will help updating an existing applied an API gateway policy
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
            policy_asset_id (str): Policy asset id, for example "message-logging", "spike-control" etc.
            api_instance_id (str): API Instance Id.
            policy_config_data (dict): This config is going to vary between policy. Every policy has a separate
                policy config. And example of this config for message-logging policy is:
                {
                    "loggingConfiguration": [{
                        "itemName": "Default configuration",
                        "itemData": {
                            "message": "#[attributes.headers['id']]",
                            "level": "INFO",
                            "firstSection": True,
                            "secondSection": False
                        }
                    }]
                }
            policy (dict): Existing policy instance from self@list_policies response
            policy_asset_version (str): This is the version of the policy asset.
                You are supposed to call self@policy_template_by_asset_id#version with the policy_asset_id.
                Which will then will provide all the these information
        Returns:
            dict: Return the success object when success. Return None in case of any error.
        """

        template = self.policy_template_by_asset_id(org_id=org_id, asset_id=policy_asset_id)
        if template is None:
            return None

        if policy_config_data:
            policy['configurationData'] = policy_config_data
        if policy_asset_version:
            policy['assetVersion'] = policy_asset_version

        url = (f"https://anypoint.mulesoft.com/apimanager/api/v1/organizations/{org_id}/environments/"
               f"{env_id}/apis/{api_instance_id}/policies/{policy['id']}")

        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id,
            "content-type": "application/json"
        }

        try:
            start = time.time()
            response = self.setting.http_client.call(url, HttpVerbs.PATCH, headers,
                                                     payload=json.dumps(policy))
            self.logger.debug(f"time=> {time.time() - start}")
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"{response.status_code} Exception while updating a policy")

        except Exception as exp:
            self.logger.error(f"{exp} Exception while updating a policy")

        return None

    def un_apply_policy(self, org_id: str, env_id: str, api_instance_id: str, policy_id: str) -> dict | None:
        """This method will help removing a policy from an API
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
            api_instance_id (str): API Instance Id.
            policy_id (str): This attribute can be sourced from an object from the self@list_automated_policies#id result.
                Needs to pass the policy_id of the automated policy you would like to remove
        Returns:
            dict: Return the success object when success. Return None in case of any error.
        """
        url = (f"{self.base_url}/apimanager/api/v1/organizations/{org_id}/environments/"
               f"{env_id}/apis/{api_instance_id}/policies/{policy_id}")
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id
        }
        try:
            start = time.time()
            response = self.setting.http_client.call(url, HttpVerbs.DELETE, headers)
            self.logger.debug(f"time=> {time.time() - start}")
            if response.status_code in [204, 200]:
                return response
            else:
                self.logger.error(f"{response.status_code} Exception while unapplying a policy")

        except Exception as exp:
            self.logger.error(f"{exp} Exception while unapplying a policy")

        return None

    def delete_api_instance(self, org_id: str, env_id: str, api_instance_id: str) -> dict | None:
        """This method will help removing a policy from an API
        Args:
            org_id (str): Business Group id. Normally this is a GUID
            env_id (str): Environment Id. Normally this is a GUID
            api_instance_id (str): API Instance Id.
        Returns:
            dict: Return the success object when success. Return None in case of any error.
        """
        url = (f"{self.base_url}/apimanager/api/v1/organizations/{org_id}/environments/"
               f"{env_id}/apis/{api_instance_id}/policies/{policy_id}")
        headers: dict = {
            "Authorization": f"Bearer {self.setting.token}",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": org_id
        }
        try:
            start = time.time()
            response = self.setting.http_client.call(url, HttpVerbs.DELETE, headers)
            self.logger.debug(f"time=> {time.time() - start}")
            if response.status_code in [204, 200]:
                return response
            else:
                self.logger.error(f"{response.status_code} Exception while unapplying a policy")

        except Exception as exp:
            self.logger.error(f"{exp} Exception while unapplying a policy")

        return None
