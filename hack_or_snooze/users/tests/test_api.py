import json

from django.test import TestCase

# from django.db.utils import IntegrityError
# from django.core.exceptions import ValidationError, ObjectDoesNotExist

# from ninja.errors import AuthenticationError

# from users.models import User
from users.factories import UserFactory, FACTORY_USER_DEFAULT_PASSWORD
# NOTE: do we want to use AUTH_KEY constant or hardcode string "token" in tests?
from users.auth_utils import generate_token, AUTH_KEY
# from users.schemas import SignupInput, LoginInput

from stories.factories import StoryFactory


EMPTY_TOKEN_VALUE = ''
MALFORMED_TOKEN_VALUE = 'malformed::token'
INVALID_TOKEN_VALUE = 'user:abcdef123456'


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
                AUTH_KEY: "test:098f6bcd4621",
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

    def test_signup_fail_unprocessable_extra_fields(self):
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

    def test_signup_fail_username_must_be_alphanumeric(self):
        """Test username only contains alphanumeric characters, otherwise token
        generation/validation may break."""

        invalid_data = {
            **self.valid_signup_data,
            "username": "test:username"
        }

        response = self.client.post(
            '/api/users/signup',
            data=json.dumps(invalid_data),
            content_type="application/json"
        )

        # FIXME: this needs to have its response updated to match new approach
        # to validation:
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
                AUTH_KEY: "user:ee11cbb19052",
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

    def test_login_fail_unprocessable_extra_fields(self):
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
            "username": "nonexistent",
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


class APIUserGetTestCase(TestCase):
    """Test GET /users/{username} endpoint."""

    def setUp(self):
        # FIXME: may want to move this to beforeAll (setUpTestData), otherwise
        # tokens get regenerated every time:

        self.user = UserFactory()
        self.user_2 = UserFactory(username="user2")

        self.staff_user = UserFactory(username="staffUser", is_staff=True)

        self.user_token = generate_token(self.user.username)
        self.user2_token = generate_token(self.user_2.username)
        self.staff_user_token = generate_token(self.staff_user.username)

    def test_get_user_ok_as_self(self):
        """Test that a user can get their own user information with a valid
        token."""

        response = self.client.get(
            '/api/users/user',
            headers={AUTH_KEY: self.user_token}
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

    def test_get_user_ok_as_staff(self):
        """Test that a staff user can get a different user's information with a
        valid token."""

        response = self.client.get(
            '/api/users/user',
            headers={AUTH_KEY: self.staff_user_token}
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

    def test_get_user_fail_unauthorized_no_token_header(self):

        response = self.client.get(
            '/api/users/user'
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_get_user_fail_unauthorized_token_header_empty(self):

        response = self.client.get(
            '/api/users/user',
            headers={AUTH_KEY: EMPTY_TOKEN_VALUE}
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_get_user_fail_unauthorized_malformed_token(self):

        response = self.client.get(
            '/api/users/user',
            headers={AUTH_KEY: MALFORMED_TOKEN_VALUE}
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_get_user_fail_unauthorized_invalid_token(self):

        response = self.client.get(
            '/api/users/user',
            headers={AUTH_KEY: INVALID_TOKEN_VALUE}
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_get_user_fail_unauthorized_as_different_user(self):

        response = self.client.get(
            '/api/users/user',
            headers={AUTH_KEY: self.user2_token}
        )

        self.assertEqual(response.status_code, 401)
        # FIXME: currently the "different user" checks return a slightly
        # different response than the generic Unauthorized message produced
        # during schema validation. do we want to normalize these?
        self.assertJSONEqual(
            response.content,
            {
                "error": "Unauthorized"
            }
        )

    def test_get_user_fail_bad_request_nonexistent_user_as_staff(self):

        response = self.client.get(
            '/api/users/nonexistent',
            headers={AUTH_KEY: self.staff_user_token}
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'Not Found'
            }
        )


class APIUserPatchTestCase(TestCase):
    """Test PATCH /users/{username} endpoint."""

    def setUp(self):
        # FIXME: may want to move this to beforeAll (setUpTestData), otherwise
        # tokens get regenerated every time:
        self.user = UserFactory()
        self.user_2 = UserFactory(username="user2")
        self.staff_user = UserFactory(username="staffUser", is_staff=True)

        self.user_token = generate_token(self.user.username)
        self.user2_token = generate_token(self.user_2.username)
        self.staff_user_token = generate_token(self.staff_user.username)

    def test_patch_user_ok_all_fields_as_self(self):

        response = self.client.patch(
            '/api/users/user',
            data=json.dumps({
                "password": "new_password",
                "first_name": "newFirst",
                "last_name": "newLast"
            }),
            headers={AUTH_KEY: self.user_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "user": {
                    "stories": [],
                    "favorites": [],
                    "username": "user",
                    "first_name": "newFirst",
                    "last_name": "newLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

    def test_patch_user_ok_some_fields_as_self(self):

        response = self.client.patch(
            '/api/users/user',
            data=json.dumps({
                "first_name": "newFirst",
            }),
            headers={AUTH_KEY: self.user_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "user": {
                    "stories": [],
                    "favorites": [],
                    "username": "user",
                    "first_name": "newFirst",
                    "last_name": "userLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

    def test_patch_user_ok_all_fields_as_staff(self):

        response = self.client.patch(
            '/api/users/user',
            data=json.dumps({
                "password": "new_password",
                "first_name": "newFirst",
                "last_name": "newLast"
            }),
            headers={AUTH_KEY: self.staff_user_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "user": {
                    "stories": [],
                    "favorites": [],
                    "username": "user",
                    "first_name": "newFirst",
                    "last_name": "newLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

    def test_patch_user_ok_some_fields_as_staff(self):

        response = self.client.patch(
            '/api/users/user',
            data=json.dumps({
                "first_name": "newFirst",
            }),
            headers={AUTH_KEY: self.staff_user_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "user": {
                    "stories": [],
                    "favorites": [],
                    "username": "user",
                    "first_name": "newFirst",
                    "last_name": "userLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

    # TODO: may want to simplify or remove this test once .update is unittested
    def test_patch_user_can_reauthenticate_with_patched_password(self):
        """This test is to ensure a patched password is re-hashed and stored
        correctly, such that a user can re-authenticate with the new
        password."""

        response = self.client.patch(
            '/api/users/user',
            data=json.dumps({
                "password": "new_password",
            }),
            headers={AUTH_KEY: self.user_token},
            content_type="application/json"
        )

        # Assert we receive the correct response:
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

        # Confirm we can log back in with new password:
        login_response = self.client.post(
            '/api/users/login',
            data=json.dumps({
                "username": self.user.username,
                "password": "new_password"
            }),
            content_type="application/json"
        )

        self.assertEqual(login_response.status_code, 200)
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

    def test_patch_user_fail_unauthorized_no_token_header(self):

        response = self.client.patch(
            '/api/users/user',
            data=json.dumps({
                "password": "new_password",
                "first_name": "newFirst",
                "last_name": "newLast"
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_patch_user_fail_unauthorized_token_header_empty(self):

        response = self.client.patch(
            '/api/users/user',
            data=json.dumps({
                "password": "new_password",
                "first_name": "newFirst",
                "last_name": "newLast"
            }),
            headers={AUTH_KEY: EMPTY_TOKEN_VALUE},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_patch_user_fail_unauthorized_malformed_token(self):

        response = self.client.patch(
            '/api/users/user',
            data=json.dumps({
                "password": "new_password",
                "first_name": "newFirst",
                "last_name": "newLast"
            }),
            headers={AUTH_KEY: MALFORMED_TOKEN_VALUE},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_patch_user_fail_unauthorized_invalid_token(self):

        response = self.client.patch(
            '/api/users/user',
            data=json.dumps({
                "password": "new_password",
                "first_name": "newFirst",
                "last_name": "newLast"
            }),
            headers={AUTH_KEY: INVALID_TOKEN_VALUE},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_patch_user_fail_unauthorized_as_different_user(self):

        response = self.client.patch(
            '/api/users/user',
            data=json.dumps({
                "password": "new_password",
                "first_name": "newFirst",
                "last_name": "newLast"
            }),
            headers={AUTH_KEY: self.user2_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        # FIXME: currently the "different user" checks return a slightly
        # different response than the generic Unauthorized message produced
        # during schema validation. do we want to normalize these?
        self.assertJSONEqual(
            response.content,
            {
                "error": "Unauthorized"
            }
        )

    def test_patch_user_fail_bad_request_nonexistent_user_as_staff(self):

        response = self.client.patch(
            '/api/users/nonexistent',
            data=json.dumps({
                "password": "new_password",
                "first_name": "newFirst",
                "last_name": "newLast"
            }),
            headers={AUTH_KEY: self.staff_user_token},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'Not Found'
            }
        )

    def test_patch_user_fail_unprocessable_extra_fields(self):

        response = self.client.patch(
            '/api/users/user',
            data=json.dumps({
                "password": "new_password",
                "first_name": "newFirst",
                "last_name": "newLast",
                "extra_field": "extra_value"
            }),
            headers={AUTH_KEY: self.user_token},
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

    # FIXME: test fails right now; this is intentional.
    # TODO: rename/refactor once new validators are in place:
    def test_patch_user_fail_empty_body(self):
        response = self.client.patch(
            '/api/users/user',
            data=json.dumps({}),
            headers={AUTH_KEY: self.user_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Must provide data to patch."
            }
        )

    # FIXME: test fails right now; this is intentional.
    # TODO: rename/refactor once new validators are in place.
    def test_patch_user_fail_patch_data_contains_empty_strings(self):
        response = self.client.patch(
            '/api/users/user',
            data=json.dumps({
                "password": "new_password",
                "first_name": "",
                "last_name": "",
            }),
            headers={AUTH_KEY: self.user_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Provided fields cannot be empty strings."
            }
        )


class APIFavoritePostTestCase(TestCase):
    """Test POST /user/{username}/favorites endpoint."""

    def setUp(self):
        # FIXME: may want to move this to beforeAll (setUpTestData), otherwise
        # tokens get regenerated every time:
        self.user = UserFactory()
        self.user_2 = UserFactory(username="user2")
        self.staff_user = UserFactory(username="staffUser", is_staff=True)

        # by default, a story created by StoryFactory was posted by "user":
        self.story = StoryFactory()

        self.user_token = generate_token(self.user.username)
        self.user2_token = generate_token(self.user_2.username)
        self.staff_user_token = generate_token(self.staff_user.username)

    def test_add_favorite_ok_as_self(self):

        response = self.client.post(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: self.user2_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "user": {
                    "stories": [],
                    "favorites": [{
                        'author': 'test_author',
                        'created': '2020-01-01T00:00:00Z',
                        'id': self.story.id,
                        'modified': '2020-01-01T00:00:00Z',
                        'title': 'test_title',
                        'url': 'http://test.com',
                        'username': 'user'
                    }],
                    "username": "user2",
                    "first_name": "userFirst",
                    "last_name": "userLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

    def test_add_favorite_ok_as_staff(self):

        response = self.client.post(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: self.staff_user_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "user": {
                    "stories": [],
                    "favorites": [{
                        'author': 'test_author',
                        'created': '2020-01-01T00:00:00Z',
                        'id': self.story.id,
                        'modified': '2020-01-01T00:00:00Z',
                        'title': 'test_title',
                        'url': 'http://test.com',
                        'username': 'user'
                    }],
                    "username": "user2",
                    "first_name": "userFirst",
                    "last_name": "userLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

    def test_add_favorite_fail_unauthorized_no_token_header(self):

        response = self.client.post(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_add_favorite_fail_unauthorized_token_header_empty(self):

        response = self.client.post(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: EMPTY_TOKEN_VALUE},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_add_favorite_fail_unauthorized_malformed_token(self):

        response = self.client.post(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: MALFORMED_TOKEN_VALUE},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_add_favorite_fail_unauthorized_invalid_token(self):

        response = self.client.post(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: INVALID_TOKEN_VALUE},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_add_favorite_fail_unauthorized_as_different_user(self):

        response = self.client.post(
            '/api/users/user/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: self.user2_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        # FIXME: currently the "different user" checks return a slightly
        # different response than the generic Unauthorized message produced
        # during schema validation. do we want to normalize these?
        self.assertJSONEqual(
            response.content,
            {
                "error": "Unauthorized"
            }
        )

    def test_add_favorite_fail_does_not_add_same_favorite_twice(self):
        """NOTE: this will 'silently fail' by merit of the default behavior of
        Django's ManyToManyField. Should we alter test name/find a way to make
        this more clear? """
        response = self.client.post(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: self.user2_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "user": {
                    "stories": [],
                    "favorites": [{
                        'author': 'test_author',
                        'created': '2020-01-01T00:00:00Z',
                        'id': self.story.id,
                        'modified': '2020-01-01T00:00:00Z',
                        'title': 'test_title',
                        'url': 'http://test.com',
                        'username': 'user'
                    }],
                    "username": "user2",
                    "first_name": "userFirst",
                    "last_name": "userLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

        add_same_favorite_response = self.client.post(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: self.user2_token},
            content_type="application/json"
        )

        self.assertEqual(add_same_favorite_response.status_code, 200)
        self.assertJSONEqual(
            add_same_favorite_response.content,
            {
                "user": {
                    "stories": [],
                    "favorites": [{
                        'author': 'test_author',
                        'created': '2020-01-01T00:00:00Z',
                        'id': self.story.id,
                        'modified': '2020-01-01T00:00:00Z',
                        'title': 'test_title',
                        'url': 'http://test.com',
                        'username': 'user'
                    }],
                    "username": "user2",
                    "first_name": "userFirst",
                    "last_name": "userLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

    def test_add_favorite_fail_cannot_add_own_story_to_favorites(self):

        response = self.client.post(
            '/api/users/user/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: self.user_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                'error': 'Cannot add own user stories to favorites'
            }
        )

    def test_add_favorite_fail_bad_request_nonexistent_user_as_staff(self):
        response = self.client.post(
            '/api/users/nonexistent/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: self.staff_user_token},
            content_type="application/json"
        )

        # TODO: should we try to customize this error message to make it clear
        # it's the user who isn't found?
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'Not Found'
            }
        )

    def test_add_favorite_fail_bad_request_nonexistent_story_as_self(self):
        response = self.client.post(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": "does-not-exist"
            }),
            headers={AUTH_KEY: self.user2_token},
            content_type="application/json"
        )

        # TODO: should we try to customize this error message to make it clear
        # it's the story that isn't found?
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'Not Found'
            }
        )

    def test_add_favorite_fail_bad_request_nonexistent_story_as_staff(self):
        response = self.client.post(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": "does-not-exist"
            }),
            headers={AUTH_KEY: self.staff_user_token},
            content_type="application/json"
        )

        # TODO: should we try to customize this error message to make it clear
        # it's the story that isn't found?
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'Not Found'
            }
        )


class APIFavoriteDeleteTestCase(TestCase):
    """Test DELETE /user/{username}/favorites endpoint."""

    def setUp(self):
        # FIXME: may want to move this to beforeAll (setUpTestData), otherwise
        # tokens get regenerated every time:
        self.user = UserFactory()
        self.user_2 = UserFactory(username="user2")
        self.staff_user = UserFactory(username="staffUser", is_staff=True)

        # by default, a story created by StoryFactory was posted by "user":
        self.story = StoryFactory()

        # pre-emptively add this story to user_2's favorites:
        self.user_2.favorites.add(self.story)

        self.user_token = generate_token(self.user.username)
        self.user2_token = generate_token(self.user_2.username)
        self.staff_user_token = generate_token(self.staff_user.username)

    def test_delete_favorite_ok_as_self(self):

        # Sanity check: user_2 has at least 1 favorite currently
        self.assertTrue(self.user_2.favorites.exists())

        response = self.client.delete(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: self.user2_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "user": {
                    "stories": [],
                    "favorites": [],
                    "username": "user2",
                    "first_name": "userFirst",
                    "last_name": "userLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

    def test_delete_favorite_ok_as_staff(self):

        # Sanity check: user_2 has at least 1 favorite currently
        self.assertTrue(self.user_2.favorites.exists())

        response = self.client.delete(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: self.staff_user_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "user": {
                    "stories": [],
                    "favorites": [],
                    "username": "user2",
                    "first_name": "userFirst",
                    "last_name": "userLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

    def test_delete_favorite_fail_unauthorized_no_token_header(self):

        response = self.client.delete(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_delete_favorite_fail_unauthorized_token_header_empty(self):

        response = self.client.delete(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: EMPTY_TOKEN_VALUE},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_delete_favorite_fail_unauthorized_malformed_token(self):

        response = self.client.delete(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: MALFORMED_TOKEN_VALUE},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_delete_favorite_fail_unauthorized_invalid_token(self):

        response = self.client.delete(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: INVALID_TOKEN_VALUE},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_delete_favorite_fail_unauthorized_as_different_user(self):

        response = self.client.delete(
            '/api/users/user/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: self.user2_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        # FIXME: currently the "different user" checks return a slightly
        # different response than the generic Unauthorized message produced
        # during schema validation. do we want to normalize these?
        self.assertJSONEqual(
            response.content,
            {
                "error": "Unauthorized"
            }
        )

    def test_delete_favorite_fail_does_not_delete_same_favorite_twice(self):
        """NOTE: this will 'silently fail' by merit of the default behavior of
        Django's ManyToManyField. Should we alter test name/find a way to make
        this more clear? """
        response = self.client.delete(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: self.user2_token},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "user": {
                    "stories": [],
                    "favorites": [],
                    "username": "user2",
                    "first_name": "userFirst",
                    "last_name": "userLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

        delete_same_favorite_response = self.client.delete(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: self.user2_token},
            content_type="application/json"
        )

        self.assertEqual(delete_same_favorite_response.status_code, 200)
        self.assertJSONEqual(
            delete_same_favorite_response.content,
            {
                "user": {
                    "stories": [],
                    "favorites": [],
                    "username": "user2",
                    "first_name": "userFirst",
                    "last_name": "userLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

    def test_delete_favorite_no_effect_on_story_not_in_favorites(self):

        new_story = StoryFactory()

        response = self.client.delete(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": new_story.id
            }),
            headers={AUTH_KEY: self.user2_token},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "user": {
                    "stories": [],
                    "favorites": [{
                        'author': 'test_author',
                        'created': '2020-01-01T00:00:00Z',
                        'id': self.story.id,
                        'modified': '2020-01-01T00:00:00Z',
                        'title': 'test_title',
                        'url': 'http://test.com',
                        'username': 'user'
                    }],
                    "username": "user2",
                    "first_name": "userFirst",
                    "last_name": "userLast",
                    "date_joined": "2020-01-01T00:00:00Z"
                }
            }
        )

    def test_delete_favorite_fail_bad_request_nonexistent_user_as_staff(self):
        response = self.client.delete(
            '/api/users/nonexistent/favorites',
            data=json.dumps({
                "story_id": self.story.id
            }),
            headers={AUTH_KEY: self.staff_user_token},
            content_type="application/json"
        )

        # TODO: should we try to customize this error message to make it clear
        # it's the user who isn't found?
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'Not Found'
            }
        )

    def test_delete_favorite_fail_bad_request_nonexistent_story_as_self(self):
        response = self.client.delete(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": "does-not-exist"
            }),
            headers={AUTH_KEY: self.user2_token},
            content_type="application/json"
        )

        # TODO: should we try to customize this error message to make it clear
        # it's the story that isn't found?
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'Not Found'
            }
        )

    def test_delete_favorite_fail_bad_request_nonexistent_story_as_staff(self):
        response = self.client.delete(
            '/api/users/user2/favorites',
            data=json.dumps({
                "story_id": "does-not-exist"
            }),
            headers={AUTH_KEY: self.staff_user_token},
            content_type="application/json"
        )

        # TODO: should we try to customize this error message to make it clear
        # it's the story that isn't found?
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'Not Found'
            }
        )

# DONE:

    # GET /{username}
    # works ok w/ user token ✅
    # works ok w/ staff token ✅
    # 401 unauthorized if no token header (authentication) ✅
    # 401 unauthorized if token header blank (authentication) ✅
    # 401 unauthorized if malformed token (authentication) ✅
    # 401 unauthorized if invalid token (authentication) ✅
    # 401 unauthorized if different non-staff user's token (authorization) ✅
    # 404 if user not found w/ staff token ✅

    # PATCH /{username}
    # works ok as self, all fields submitted ✅
    # works ok as self, only some fields submitted ✅
    # works ok as self, updating password re-hashes before storing ✅
    # works ok as staff, all fields submitted ✅
    # works ok as staff, only some fields submitted ✅
    # 401 unauthorized if no token (authentication) ✅
    # 401 unauthorized if malformed token (authentication) ✅``
    # 401 unauthorized if invalid token (authentication) ✅
    # 401 unauthorized if different non-staff user's token (authorization) ✅
    # 404 if user not found w/ staff token ✅
    # 422 if extra fields submitted✅
    # error if no fields submitted ⚠️ - needs validator updates to pass
    # error if fields contain blank strings as values ⚠️ - needs validator updates to pass

    # POST /{username}/favorites
    # works ok w/ user token ✅
    # works ok w/ staff token ✅
    # 401 unauthorized if no token (authentication) ✅
    # 401 unauthorized if malformed token (authentication) ✅
    # 401 unauthorized if invalid token (authentication) ✅
    # 401 unauthorized if different non-staff user's token (authorization) ✅
    # OTHER TESTS:
    # favorite record is not duplicated when added twice ✅
    # 400 user cannot add a story they posted to their favorites ✅
    # 404 if {username} not found w/ staff token ✅
    # 404 if story_id not found w/ valid user token ✅
    # 404 if story_id not found w/ staff token ✅

    # DELETE /{username}/favorites
    # works ok w/ user token ✅
    # works ok w/ staff token ✅
    # 401 unauthorized if no token (authentication) ✅
    # 401 unauthorized if malformed token (authentication) ✅
    # 401 unauthorized if invalid token (authentication) ✅
    # 401 unauthorized if different non-staff user's token (authorization) ✅
    # OTHER TESTS:
    # works ok to DELETE same story_id twice ✅
    # works ok to DELETE story not in favorites ✅
    # 404 if {username} not found w/ staff token ✅
    # 404 if story_id not found w/ valid user token ✅
    # 404 if story_id not found w/ staff token ✅