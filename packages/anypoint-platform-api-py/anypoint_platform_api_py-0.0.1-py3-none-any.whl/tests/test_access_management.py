import unittest
from anypoint.settings import Settings
from anypoint.auth import AuthenticationUsernamePassword
from anypoint.access_management import AccessManagement


class TestAccessManagement(unittest.TestCase):
    setting = None

    @classmethod
    def setUpClass(cls):
        TestAccessManagement.setting = Settings()
        TestAccessManagement.setting.logger.info("Test Started")
        AuthenticationUsernamePassword(TestAccessManagement.setting)

    def test_auth(self):
        self.assertIsNot(TestAccessManagement.setting.token, None)

    def test_list_business_groups(self):
        access_management = AccessManagement(TestAccessManagement.setting)
        root_org_id = None
        for group in access_management.list_business_groups():
            if group['parentId'] is None:
                root_org_id = group['id']
        self.assertIsNot(root_org_id, None)

    def test_list_environments(self):
        access_management = AccessManagement(TestAccessManagement.setting)
        for group in access_management.list_business_groups():
            environments = access_management.list_environments(group['id'])
            for environment in environments:
                self.assertIsNot(environment['id'], None)

    def test_list_users(self):
        access_management = AccessManagement(TestAccessManagement.setting)
        root_org_id = None
        for group in access_management.list_business_groups():
            if group['parentId'] is None:
                root_org_id = group['id']
        self.assertIsNot(root_org_id, None)
        for user in access_management.list_users(root_org_id):
            self.assertIsNot(user['username'], None)
            self.assertIsNot(user['email'], None)

    @classmethod
    def tearDownClass(cls):
        TestAccessManagement.setting.logger.info("Test Finished")


if __name__ == "__main__":
    unittest.main()
