import json

from django.test import TestCase

# from django.db.utils import IntegrityError
# from django.core.exceptions import ValidationError, ObjectDoesNotExist

# from ninja.errors import AuthenticationError

# from users.models import User
from users.factories import UserFactory
# from users.schemas import SignupInput, LoginInput


class UserAPIAuthTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "username": "test",
            "password": "password",
            "first_name": "first",
            "last_name": "last"
        }

    def test_signup_ok(self):
        response = self.client.post(
            '/api/users/signup',
            data=json.dumps(self.valid_data),
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
            **self.valid_data,
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
        existing_user = UserFactory()

        dupe_user_data = {
            **self.valid_data,
            "username": existing_user.username
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
            **self.valid_data,
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

# TODO:
# AUTH ROUTES
# - POST /api/users/signup
#   - signup success✅
#   - signup failure (missing required data) 422 - from ninja✅
#       - obj.detail[0].msg
#   - signup failure (extra fields included) 422 - from ninja✅
#   - signup failure (username already exists) 422✅
#       - obj.error
#   - signup failure (malformed username) 422 - from ninja✅
#   - (IE, a username including special characters
#       in particular ':')

# - POST /api/users/login
#   - login success
#   - login failure (missing required data) 422 - from ninja
#       - obj.detail[0].msg
#   - login failure (extra fields included) 422 - from ninja
#   - login failure (non-existant username) 401
#       - obj.error
#   - login failure (username exists; wrong password) 401
#       - obj.error
# USERS ROUTES
# FAVORITES ROUTES
