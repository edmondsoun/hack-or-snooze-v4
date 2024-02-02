from django.test import TestCase
from django.contrib.auth.hashers import check_password

from users.factories import UserFactory


class UserModelTestCase(TestCase):
    def setUp(self):
        self.test_user = UserFactory()

    def test_update_some_fields_no_password(self):
        patch_data = {
            "first_name": "patch_test_first",
            "last_name": "patch_test_last",
        }

        self.test_user.update(patch_data)

        self.assertEqual(
            self.test_user.first_name,
            patch_data["first_name"]
        )
        self.assertEqual(
            self.test_user.last_name,
            patch_data["last_name"]
        )

    def test_update_all_fields_with_password(self):
        patch_data = {
            "first_name": "patch_test_first",
            "last_name": "patch_test_last",
            "password": "patch_test_password"
        }

        self.test_user.update(patch_data)

        self.assertEqual(
            self.test_user.first_name,
            patch_data["first_name"]
        )
        self.assertEqual(
            self.test_user.last_name,
            patch_data["last_name"]
        )
        self.assertTrue(check_password(
            patch_data["password"],
            self.test_user.password
        ))

        # Check that password is not plain-text
        self.assertNotEqual(
            self.test_user.password,
            patch_data["password"]
        )
