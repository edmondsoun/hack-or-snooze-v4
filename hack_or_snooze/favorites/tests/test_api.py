from django.test import TestCase

from users.factories import UserFactory
from users.auth_utils import generate_token
from stories.factories import StoryFactory

AUTH_KEY = 'token'
EMPTY_TOKEN_VALUE = ''
MALFORMED_TOKEN_VALUE = 'malformed::token'
INVALID_TOKEN_VALUE = 'user:abcdef123456'


class APIFavoritePostTestCase(TestCase):
    """Test POST /user/{username}/favorites endpoint."""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.user_2 = UserFactory(username="user2")
        cls.staff_user = UserFactory(username="staffUser", is_staff=True)

        # by default, a story created by StoryFactory was posted by "user":
        cls.story = StoryFactory()

        cls.user_token = generate_token(cls.user.username)
        cls.user2_token = generate_token(cls.user_2.username)
        cls.staff_user_token = generate_token(cls.staff_user.username)

    def test_add_favorite_ok_as_self(self):

        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user2/{story_id}/favorite',
            headers={AUTH_KEY: self.user2_token},
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
        """ Tests a staff user capable of adding a story to another users
        favorites"""

        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user2/{story_id}/favorite',
            headers={AUTH_KEY: self.staff_user_token},
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

    def test_add_favorite_does_not_add_same_favorite_twice(self):

        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user2/{story_id}/favorite',
            headers={AUTH_KEY: self.user2_token},
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
            f'/api/favorites/user2/{story_id}/favorite',
            headers={AUTH_KEY: self.user2_token},
        )

        self.assertEqual(add_same_favorite_response.status_code, 400)
        self.assertJSONEqual(
            add_same_favorite_response.content,
            {"detail": "Story already favorited."}
        )

    def test_add_favorite_fail_unauthorized_no_token_header(self):

        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user2/{story_id}/favorite',
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_add_favorite_fail_unauthorized_token_header_empty(self):

        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user2/{story_id}/favorite',
            headers={AUTH_KEY: EMPTY_TOKEN_VALUE},
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_add_favorite_fail_unauthorized_malformed_token(self):

        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user2/{story_id}/favorite',
            headers={AUTH_KEY: MALFORMED_TOKEN_VALUE},
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_add_favorite_fail_unauthorized_invalid_token(self):

        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user2/{story_id}/favorite',
            headers={AUTH_KEY: INVALID_TOKEN_VALUE},
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_add_favorite_fail_unauthorized_as_different_user(self):

        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user/{story_id}/favorite',
            headers={AUTH_KEY: self.user2_token},
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_add_favorite_fail_cannot_add_own_story_to_favorites(self):

        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user/{story_id}/favorite',
            headers={AUTH_KEY: self.user_token},
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'Cannot add own user stories to favorites'
            }
        )

    def test_add_favorite_fail_bad_request_nonexistent_user_as_staff(self):
        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user3/{story_id}/favorite',
            headers={AUTH_KEY: self.staff_user_token},
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'User not found.'
            }
        )

    def test_add_favorite_fail_bad_request_nonexistent_story_as_self(self):

        response = self.client.post(
            '/api/favorites/user2/nonexistent-story-id/favorite',
            headers={AUTH_KEY: self.user2_token},
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'Story not found.'
            }
        )

    def test_add_favorite_fail_bad_request_nonexistent_story_as_staff(self):

        response = self.client.post(
            '/api/favorites/user2/nonexistent-story-id/favorite',
            headers={AUTH_KEY: self.staff_user_token},
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'Story not found.'
            }
        )


class APIFavoriteDeleteTestCase(TestCase):
    """Test DELETE /user/{username}/favorites endpoint."""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.user_2 = UserFactory(username="user2")
        cls.staff_user = UserFactory(username="staffUser", is_staff=True)

        # by default, a story created by StoryFactory was posted by "user":
        cls.story = StoryFactory()

        # pre-emptively add this story to user_2's favorites:
        cls.user_2.favorites.add(cls.story)

        cls.user_token = generate_token(cls.user.username)
        cls.user2_token = generate_token(cls.user_2.username)
        cls.staff_user_token = generate_token(cls.staff_user.username)

    def test_delete_favorite_ok_as_self(self):

        # Sanity check: user_2 has at least 1 favorite currently
        self.assertTrue(self.user_2.favorites.exists())

        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user2/{story_id}/unfavorite',
            headers={AUTH_KEY: self.user2_token},
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

        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user2/{story_id}/unfavorite',
            headers={AUTH_KEY: self.staff_user_token},
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

    def test_delete_favorite_does_not_delete_same_favorite_twice(self):

        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user2/{story_id}/unfavorite',
            headers={AUTH_KEY: self.user2_token},
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

        delete_same_favorite_response = self.client.post(
            f'/api/favorites/user2/{story_id}/unfavorite',
            headers={AUTH_KEY: self.user2_token},
        )

        self.assertEqual(delete_same_favorite_response.status_code, 404)
        self.assertJSONEqual(
            delete_same_favorite_response.content,
            {
                'detail': 'Favorite not found.'
            }

        )

    def test_delete_favorite_fail_unauthorized_no_token_header(self):
        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user2/{story_id}/unfavorite',
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_delete_favorite_fail_unauthorized_token_header_empty(self):
        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user2/{story_id}/unfavorite',
            headers={AUTH_KEY: EMPTY_TOKEN_VALUE},
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_delete_favorite_fail_unauthorized_malformed_token(self):

        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user2/{story_id}/unfavorite',
            headers={AUTH_KEY: MALFORMED_TOKEN_VALUE},
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_delete_favorite_fail_unauthorized_invalid_token(self):

        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user2/{story_id}/unfavorite',
            headers={AUTH_KEY: INVALID_TOKEN_VALUE},
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_delete_favorite_fail_unauthorized_as_different_user(self):
        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/user/{story_id}/unfavorite',
            headers={AUTH_KEY: self.user2_token},
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {
                "detail": "Unauthorized"
            }
        )

    def test_delete_favorite_fail_bad_request_nonexistent_user_as_staff(self):
        story_id = self.story.id

        response = self.client.post(
            f'/api/favorites/non-existent-user-id/{story_id}/unfavorite',
            headers={AUTH_KEY: self.staff_user_token},
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'Favorite not found.'
            }
        )

    def test_delete_favorite_fail_bad_request_nonexistent_story_as_self(self):

        response = self.client.post(
            '/api/favorites/user2/non-existent-story-id/unfavorite',
            headers={AUTH_KEY: self.user2_token},
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'Favorite not found.'
            }
        )

    def test_delete_favorite_fail_bad_request_nonexistent_story_as_staff(self):
        response = self.client.post(
            '/api/favorites/user2/non-existent-story-id/unfavorite',
            headers={AUTH_KEY: self.staff_user_token},
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                'detail': 'Favorite not found.'
            }
        )
