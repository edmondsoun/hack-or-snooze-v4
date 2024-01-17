import json

from django.test import TestCase

# from django.db.utils import IntegrityError
# from django.core.exceptions import ValidationError, ObjectDoesNotExist

# from ninja.errors import AuthenticationError

# from users.models import User
from users.factories import UserFactory, FACTORY_USER_DEFAULT_PASSWORD
# from users.schemas import SignupInput, LoginInput


class APIAuthTestCase(TestCase):
    def setUp(self):
        # TODO: investigate why this is outside setup in SIS?
        self.existing_user = UserFactory()

        self.valid_signup_data = {
            "username": "test",
            "password": "password",
            "first_name": "testFirst",
            "last_name": "testLast"
        }

        self.valid_login_data = {
            "username": self.existing_user.username,
            "password": FACTORY_USER_DEFAULT_PASSWORD
        }

    def test_signup_ok(self):
        response = self.client.post(
            '/api/users/signup',
            data=json.dumps(self.valid_signup_data),
            content_type="application/json"
        )

        # get date_joined from response so we don't encounter
        # issues with differing dates
        response_json = json.loads(response.content)
        response_date_joined = response_json["user"]["date_joined"]

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_json,
            {
                "token": "test:098f6bcd4621",
                "user": {
                    "stories": [],
                    "favorites": [],
                    "username": "test",
                    "first_name": "testFirst",
                    "last_name": "testLast",
                    "date_joined": response_date_joined
                }
            }
        )

    def test_signup_fail_missing_data(self):

        invalid_data = {
            "username": "test",
            "password": "password",
            "first_name": "testFirst",
        }

        response = self.client.post(
            '/api/users/signup',
            data=json.dumps(invalid_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 422)
        self.assertJSONEqual(
            response.content,
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": [
                            "body",
                            "data",
                            "last_name"
                        ],
                        "msg": "Field required"
                    }
                ]
            }
        )

    def test_signup_fail_extra_fields(self):
        invalid_data = {
            **self.valid_signup_data,
            "extra_field": "extra_value"
        }

        response = self.client.post(
            '/api/users/signup',
            data=json.dumps(invalid_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 422)
        self.assertJSONEqual(
            response.content,
            {
                "detail": [
                    {
                        "type": "extra_forbidden",
                        "loc": [
                            "body",
                            "data",
                            "extra_field"
                        ],
                        "msg": "Extra inputs are not permitted"
                    }
                ]
            }
        )

    def test_signup_fail_username_exists(self):

        dupe_user_data = {
            **self.valid_signup_data,
            "username": self.existing_user.username
        }

        response = self.client.post(
            '/api/users/signup',
            data=json.dumps(dupe_user_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 422)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Username already exists."
            }
        )

    def test_signup_fail_malformed_username(self):

        invalid_data = {
            **self.valid_signup_data,
            "username": "test:username"
        }

        response = self.client.post(
            '/api/users/signup',
            data=json.dumps(invalid_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 422)
        self.assertJSONEqual(
            response.content,
            {
                "detail": [
                    {
                        "type": "string_pattern_mismatch",
                        "loc": [
                            "body",
                            "data",
                            "username"
                        ],
                        "msg": "String should match pattern '^[0-9a-zA-Z]*$'",
                        "ctx": {
                            "pattern": "^[0-9a-zA-Z]*$"
                        }
                    }
                ]
            }
        )

    def test_login_ok(self):
        response = self.client.post(
            '/api/users/login',
            data=json.dumps(self.valid_login_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "token": "user:ee11cbb19052",
                "user": {
                    "stories": [],
                    "favorites": [],
                    "username": "user",
                    "first_name": "userFirst",
                    "last_name": "userLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

    def test_login_fail_missing_data(self):
        invalid_data = {
            "username": self.existing_user.username,
        }

        response = self.client.post(
            '/api/users/login',
            data=json.dumps(invalid_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 422)
        self.assertJSONEqual(
            response.content,
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": [
                            "body",
                            "data",
                            "password"
                        ],
                        "msg": "Field required"
                    }
                ]
            }
        )

    def test_login_fail_extra_fields(self):
        invalid_data = {
            **self.valid_login_data,
            "extra_field": "extra_value"
        }

        response = self.client.post(
            '/api/users/login',
            data=json.dumps(invalid_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 422)
        self.assertJSONEqual(
            response.content,
            {
                "detail": [
                    {
                        "type": "extra_forbidden",
                        "loc": [
                            "body",
                            "data",
                            "extra_field"
                        ],
                        "msg": "Extra inputs are not permitted"
                    }
                ]
            }
        )

    def test_login_fail_username_does_not_exist(self):
        invalid_data = {
            "username": "nonexistent_user",
            "password": "password"
        }

        response = self.client.post(
            '/api/users/login',
            data=json.dumps(invalid_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Invalid credentials."
            }
        )

    def test_login_fail_invalid_password(self):
        invalid_data = {
            "username": self.existing_user.username,
            "password": "bad_password"
        }

        response = self.client.post(
            '/api/users/login',
            data=json.dumps(invalid_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Invalid credentials."
            }
        )


class APIUserTestCase(TestCase):
    """Test /users endpoints"""

    def setUp(self):
        self.user = UserFactory()
        self.user_2 = UserFactory(username="user2")
        self.admin = UserFactory(username="admin", is_staff=True)

    def test_get_own_user_info_ok(self):
        """Test that a user can get their own user information with a valid
        token."""

        response = self.client.get(
            '/api/users/user',
            headers={'token': 'user:ee11cbb19052'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "user": {
                    "stories": [],
                    "favorites": [],
                    "username": "user",
                    "first_name": "userFirst",
                    "last_name": "userLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

    # GET /{username}
    # works ok w/ user token
    # works ok w/ staff token
    # 401 unauthorized if no token (authentication)
    # 401 unauthorized if malformed token (authentication)
    # 401 unauthorized if different non-staff user's token (authorization)
    # 404 if user not found w/ staff token

    # PATCH /{username}
    # works ok w/ user token
    # works ok w/ staff token
    # 401 unauthorized if no token (authentication)
    # 401 unauthorized if malformed token (authentication)
    # 401 unauthorized if different non-staff user's token (authorization)
    # 404 if user not found w/ staff token
    # OTHER TESTS:
    # works with all fields submitted
    # works with only some fields submitted
    # 400 friendly error if no fields submitted
    # error if some/all fields contain blank strings as values
    # 422 if extra fields submitted


class APIFavoriteTestCase(TestCase):
    """Test /user/{username}/favorites endpoints"""
    # POST /{username}/favorites
    # works ok w/ user token
    # works ok w/ staff token
    # 401 unauthorized if no token (authentication)
    # 401 unauthorized if malformed token (authentication)
    # 401 unauthorized if different non-staff user's token (authorization)
    # OTHER TESTS:
    # favorite record is not duplicated when added twice
    # 400 user cannot add a story they posted to their favorites
    # 404 if {username} not found w/ staff token
    # 404 if story_id not found w/ staff token

    # DELETE /{username}/favorites
    # works ok w/ user token
    # works ok w/ staff token
    # 401 unauthorized if no token (authentication)
    # 401 unauthorized if malformed token (authentication)
    # 401 unauthorized if different non-staff user's token (authorization)
    # OTHER TESTS:
    # works ok to DELETE same story_id twice?
    # 404 if {username} not found w/ staff token
    # 404 if story_id not found w/ staff token


