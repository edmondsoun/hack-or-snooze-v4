from django.test import TestCase

from users.models import User
from users.factories import UserFactory

from users.auth_utils import generate_token, generate_hash, check_token, ApiKey

# Pass empty dictionary to simulate request object:
REQUEST_MOCK = {}


class ApiKeyTestCase(TestCase):
    """Tests for custom authenticate method on ApiKey class from DjangoNinja"""
    def setUp(self):
        self.user = UserFactory()
        self.user_token = generate_token(self.user.username)

        self.token_header = ApiKey()

    def test_authenticate_ok(self):
        """Test authenticate method returns User instance on success."""

        # Pass empty dictionary to simulate request object:
        user = self.token_header.authenticate(REQUEST_MOCK, self.user_token)

        self.assertIsInstance(user, User)
        self.assertEqual(user.username, self.user.username)

    def test_authenticate_fail_token_is_none(self):
        """Test authenticate method returns None when passed a None value for
        token."""

        user = self.token_header.authenticate(REQUEST_MOCK, None)

        self.assertIsNone(user)

    def test_authenticate_fail_token_is_blank(self):
        """Test authenticate method returns None when passed an empty value for
        token."""

        user = self.token_header.authenticate(REQUEST_MOCK, "")

        self.assertIsNone(user)

    def test_authenticate_fail_token_is_malformed(self):
        """Test authenticate method returns None when token is malformed
        (contains multiple colons)."""

        user = self.token_header.authenticate(REQUEST_MOCK, 'malformed::token')

        self.assertIsNone(user)

    def test_authenticate_fail_token_is_invalid(self):
        """Test authenticate method returns None when token is invalid
        (username/hash mismatch)."""

        user = self.token_header.authenticate(REQUEST_MOCK, 'user:abcdef123456')

        self.assertIsNone(user)

    def test_authenticate_fail_no_user_matching_token(self):
        """Test authenticate method returns None when token is valid, but does
        not coorespond to an existing user."""

        user = self.token_header.authenticate(REQUEST_MOCK, 'nonexistent:357f5c155c9d')

        self.assertIsNone(user)


class AuthUtilsTestCase(TestCase):
    def test_generate_token_ok(self):
        """Test conductor function responsible for formatting token string."""

        token = generate_token("username")

        self.assertEqual(token, "username:14c4b06b824e")

    def test_generate_hash_ok(self):
        """Test helper function that generates truncated hash from username."""

        hash = generate_hash("username")

        self.assertEqual(hash, "14c4b06b824e")
        self.assertEqual(type(hash), str)
        self.assertEqual(len(hash), 12)

    def test_check_token_ok(self):
        """Test helper function that checks for valid token."""

        is_valid = check_token("username:14c4b06b824e")

        self.assertTrue(is_valid)

    def test_check_token_fail_bad_username(self):
        """Test failure on username with extra colons."""

        is_valid = check_token("user:name:14c4b06b824e")

        self.assertFalse(is_valid)

    def test_check_token_fail_no_token(self):
        """Test failure when token is None."""

        is_valid = check_token(None)

        self.assertFalse(is_valid)

