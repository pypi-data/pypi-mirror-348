import time
import unittest
import random

import requests

from anypoint.api_manager import ApiManager
from anypoint.settings import Settings
from anypoint.auth import AuthenticationUsernamePassword
from anypoint.access_management import AccessManagement


class TestApiManager(unittest.TestCase):
    setting: Settings = None
    api_manager: ApiManager = None
    org_id = None
    env_id = None
    api_instance_id = None

    @classmethod
    def setUpClass(cls):
        TestApiManager.setting = Settings()
        TestApiManager.setting.logger.info("Test suite [TestApiManager] started")
        TestApiManager.setting.logger.info("Test initialization happening")
        AuthenticationUsernamePassword(TestApiManager.setting)
        access_management = AccessManagement(TestApiManager.setting)
        TestApiManager.api_manager = ApiManager(TestApiManager.setting)
        business_groups = access_management.list_business_groups()
        if (business_groups is None) or len(business_groups) <= 0:
            raise Exception("Could not query business groups.")
        for group in business_groups:
            done = False
            environments = access_management.list_environments(group['id'])
            for environment in environments:
                TestApiManager.org_id = group['id']
                TestApiManager.env_id = environment['id']
                apis = TestApiManager.api_manager.list_apis_all(org_id=TestApiManager.org_id,
                                                                env_id=TestApiManager.env_id)
                if apis and len(apis) > 0:
                    TestApiManager.api_instance_id = apis[0]['id']
                    done = True
                    break
            if done:
                break
        TestApiManager.setting.logger.info("Test initialization finished")

    def test_auth(self):
        self.assertIsNot(TestApiManager.setting.token, None)

    def test_list_apis(self):
        self.assertIsNot(TestApiManager.org_id, None)
        self.assertIsNot(TestApiManager.env_id, None)
        apis = TestApiManager.api_manager.list_apis(org_id=TestApiManager.org_id, env_id=TestApiManager.env_id)
        self.assertIsNot(apis, None)
        for api in apis:
            self.assertIsNot(api['assetId'], None)

    def test_list_client_application(self):
        self.assertIsNot(TestApiManager.org_id, None)
        self.assertIsNot(TestApiManager.env_id, None)
        client_applications = TestApiManager.api_manager.list_client_application(org_id=TestApiManager.org_id,
                                                                                 env_id=TestApiManager.env_id)
        self.assertIsNot(client_applications, None)
        for api in client_applications:
            self.assertIsNot(api['clientId'], None)
            self.assertIsNot(api['clientSecret'], None)

    def test_api_settings(self):
        self.assertIsNot(TestApiManager.org_id, None)
        self.assertIsNot(TestApiManager.env_id, None)
        self.assertIsNot(TestApiManager.api_instance_id, None)
        api_settings = TestApiManager.api_manager.api_settings(org_id=TestApiManager.org_id,
                                                               env_id=TestApiManager.env_id,
                                                               api_instance_id=TestApiManager.api_instance_id)
        self.assertIsNot(api_settings, None)

    def test_list_contracts(self):
        self.assertIsNot(TestApiManager.org_id, None)
        self.assertIsNot(TestApiManager.env_id, None)
        self.assertIsNot(TestApiManager.api_instance_id, None)
        contracts = TestApiManager.api_manager.list_contracts(org_id=TestApiManager.org_id,
                                                              env_id=TestApiManager.env_id,
                                                              api_instance_id=TestApiManager.api_instance_id)
        self.assertIsNot(contracts, None)

    def test_list_sla_tiers(self):
        self.assertIsNot(TestApiManager.org_id, None)
        self.assertIsNot(TestApiManager.env_id, None)
        self.assertIsNot(TestApiManager.api_instance_id, None)
        sla_tiers = TestApiManager.api_manager.list_sla_tiers(org_id=TestApiManager.org_id,
                                                              env_id=TestApiManager.env_id,
                                                              api_instance_id=TestApiManager.api_instance_id)
        self.assertIsNot(sla_tiers, None)

    def test_automated_policy(self):
        policy_asset_id = "ip-blocklist"
        mule_runtime_from_version = "4.6.0"
        policy_config_data = {
            "ipExpression": "#[attributes.headers['x-forwarded-for']]",
            "ips": ["192.168.0.120/32"]
        }
        self.assertIsNot(TestApiManager.org_id, None)
        self.assertIsNot(TestApiManager.env_id, None)
        automated_policies = TestApiManager.api_manager.list_automated_policies(org_id=TestApiManager.org_id,
                                                                                env_id=TestApiManager.env_id)
        if automated_policies and len(automated_policies) > 0:
            for each_policy in automated_policies:
                if each_policy['assetId'] == policy_asset_id:
                    policy_id = each_policy['id']
                    is_un_apply_success = TestApiManager.api_manager.un_apply_automated_policy(
                        org_id=TestApiManager.org_id,
                        env_id=TestApiManager.env_id,
                        policy_id=policy_id)
                    self.assertIsNot(is_un_apply_success, None)
                    break

        template = TestApiManager.api_manager.policy_template_by_asset_id(org_id=TestApiManager.org_id,
                                                                          asset_id=policy_asset_id)
        self.assertIsNot(template, None)
        policy_asset_version = template['version']
        policy_asset_group_id = template['orgId']

        is_apply_success = TestApiManager.api_manager.apply_automated_policy(
            org_id=TestApiManager.org_id,
            env_id=TestApiManager.env_id,
            policy_asset_id=policy_asset_id,
            policy_asset_version=policy_asset_version,
            mule_runtime_from_version=mule_runtime_from_version,
            mule_runtime_to_version=None,
            policy_asset_group_id=policy_asset_group_id,
            policy_config_data=policy_config_data,
            java_17=True,
            java_8=True)
        self.assertIsNot(is_apply_success, None)

        is_update_apply_success = TestApiManager.api_manager.update_automated_policy(
            org_id=TestApiManager.org_id,
            env_id=TestApiManager.env_id,
            policy_asset_id=policy_asset_id,
            policy_asset_version=None,
            mule_runtime_from_version=None,
            mule_runtime_to_version=None,
            policy_config_data=policy_config_data,
            java_17=True,
            java_8=True)
        self.assertIsNot(is_update_apply_success, None)

        automated_policies = TestApiManager.api_manager.list_automated_policies(org_id=TestApiManager.org_id,
                                                                                env_id=TestApiManager.env_id)

        done = False
        if automated_policies and len(automated_policies) > 0:
            for each_policy in automated_policies:
                if each_policy['assetId'] == policy_asset_id:
                    policy_id = each_policy['id']
                    is_un_apply_success = TestApiManager.api_manager.un_apply_automated_policy(
                        org_id=TestApiManager.org_id,
                        env_id=TestApiManager.env_id,
                        policy_id=policy_id)
                    self.assertIsNot(is_un_apply_success, None)
                    done = True
                    break
        self.assertIsNot(done, False)

    def test_api_instance_tag(self):
        tag = "Hello world".lower()
        self.assertIsNot(TestApiManager.org_id, None)
        self.assertIsNot(TestApiManager.env_id, None)
        self.assertIsNot(TestApiManager.api_instance_id, None)
        add_tag_response = TestApiManager.api_manager.add_api_instance_tag(
            org_id=TestApiManager.org_id,
            env_id=TestApiManager.env_id,
            api_instance_id=TestApiManager.api_instance_id,
            tag=tag)

        self.assertIsNot(add_tag_response, None)

        api_settings = TestApiManager.api_manager.api_settings(
            org_id=TestApiManager.org_id,
            env_id=TestApiManager.env_id,
            api_instance_id=TestApiManager.api_instance_id)
        self.assertIsNot(api_settings, None)

        found = False
        if api_settings['tags'] and len(api_settings['tags']) > 0:
            for each_tag in api_settings['tags']:
                if tag == each_tag:
                    found = True
                    break
        self.assertIs(found, True)
        remove_tag_response = TestApiManager.api_manager.remove_api_instance_tag(
            org_id=TestApiManager.org_id,
            env_id=TestApiManager.env_id,
            api_instance_id=TestApiManager.api_instance_id,
            tag=tag)
        self.assertIsNot(remove_tag_response, None)

    def test_api_policy(self):
        policy_asset_id = "ip-blocklist"
        policy_config_data = {
            "ipExpression": "#[attributes.headers['x-forwarded-for']]",
            "ips": ["192.168.0.120/32"]
        }
        self.assertIsNot(TestApiManager.org_id, None)
        self.assertIsNot(TestApiManager.env_id, None)
        self.assertIsNot(TestApiManager.api_instance_id, None)
        policies = TestApiManager.api_manager.list_policies(
            org_id=TestApiManager.org_id,
            env_id=TestApiManager.env_id,
            api_instance_id=TestApiManager.api_instance_id)

        self.assertIsNot(policies, None)
        if len(policies) > 0:
            for p in policies:
                if p['assetId'] == policy_asset_id:
                    policy = p
                    un_apply_response = TestApiManager.api_manager.un_apply_policy(
                        org_id=TestApiManager.org_id,
                        env_id=TestApiManager.env_id,
                        api_instance_id=TestApiManager.api_instance_id,
                        policy_id=policy['id'])
                    self.assertIsNot(un_apply_response, None)
                    break

        apply_response = TestApiManager.api_manager.apply_policy(
            org_id=TestApiManager.org_id,
            env_id=TestApiManager.env_id,
            policy_asset_id=policy_asset_id,
            api_instance_id=TestApiManager.api_instance_id,
            policy_config_data=policy_config_data,
            policy_asset_version=None)
        self.assertIsNot(apply_response, None)
        policies = TestApiManager.api_manager.list_policies(
            org_id=TestApiManager.org_id,
            env_id=TestApiManager.env_id,
            api_instance_id=TestApiManager.api_instance_id)
        self.assertGreater(len(policies), 0)
        done = False
        for policy in policies:
            if policy['assetId'] == policy_asset_id:
                done = True
                policy_config_data['ips'].append("192.168.0.121/32")
                update_response = TestApiManager.api_manager.update_policy(
                    org_id=TestApiManager.org_id,
                    env_id=TestApiManager.env_id,
                    policy_asset_id=policy_asset_id,
                    api_instance_id=TestApiManager.api_instance_id,
                    policy_config_data=policy_config_data,
                    policy=policy,
                    policy_asset_version=None)
                self.assertIsNot(update_response, None)
                un_apply_response = TestApiManager.api_manager.un_apply_policy(
                    org_id=TestApiManager.org_id,
                    env_id=TestApiManager.env_id,
                    api_instance_id=TestApiManager.api_instance_id,
                    policy_id=policy['id'])
                self.assertIsNot(un_apply_response, None)
        self.assertIsNot(done, None)


    @classmethod
    def tearDownClass(cls):
        TestApiManager.setting.logger.info("Test suite [TestApiManager] Finished")


if __name__ == "__main__":
    unittest.main()
