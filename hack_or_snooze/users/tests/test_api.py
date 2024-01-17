import json

from django.test import TestCase

# from django.db.utils import IntegrityError
# from django.core.exceptions import ValidationError, ObjectDoesNotExist

# from ninja.errors import AuthenticationError

# from users.models import User
from users.factories import UserFactory, FACTORY_USER_PASSWORD
# from users.schemas import SignupInput, LoginInput


class APIAuthTestCase(TestCase):
    def setUp(self):
        # TODO: investigate why this is outside setup in SIS?
        self.existing_user = UserFactory()

        self.valid_signup_data = {
            "username": "test",
            "password": "password",
            "first_name": "first",
            "last_name": "last"
        }

        self.valid_login_data = {
            "username": self.existing_user.username,
            "password": FACTORY_USER_PASSWORD
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
                    "first_name": "first",
                    "last_name": "last",
                    "date_joined": response_date_joined
                }
            }
        )

    def test_signup_fail_missing_data(self):

        invalid_data = {
            "username": "test",
            "password": "password",
            "first_name": "first",
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
            "extra": "extra"
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
                            "extra"
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

        # TODO: can we set a timestamp on the user factory class so we don't
        # have to dynamically access here?
        response_json = json.loads(response.content)
        response_date_joined = response_json["user"]["date_joined"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "token": "factoryUser:27bbe49cbca0",
                "user": {
                    "stories": [],
                    "favorites": [],
                    "username": "factoryUser",
                    "first_name": "factory_first",
                    "last_name": "factory_last",
                    "date_joined": response_date_joined
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
            "extra": "extra"
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
                            "extra"
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

# USERS ROUTES

class APIUserTestCase(TestCase):
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

    # patch specific tests:
    # works with all fields submitted
    # works with only some fields submitted
    # 400 friendly error if first name or last name is blank
    # 400 friendly error if no fields submitted
    # 422 if extra fields submitted




class APIFavoriteTestCase(TestCase):
    # POST /{username}/favorites
    # DELETE /{username}/favorites


# FAVORITES ROUTES
