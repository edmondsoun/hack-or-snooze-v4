from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from ninja.errors import AuthenticationError

from users.models import User
from users.factories import UserFactory
from users.schemas import SignupInput, LoginInput


class UserModelTestCase(TestCase):
    def setUp(self):
        self.test_user = UserFactory()

    def test_validation_error_on_blank_first_name(self):
        """
        tests that the model throws an validation error when

        user.first_name == ""

        Note: This test is to ensure that no one changes the user model. We
        really do need these values to not be blank otherwise Django Ninja
        will interpret these fields as optional.

        """
        self.test_user.first_name = ""

        with self.assertRaises(ValidationError):
            self.test_user.full_clean()

    def test_validation_error_on_blank_last_name(self):
        """
        tests that the model throws an validation error when

        user.last_name == ""

        Note: This test is to ensure that no one changes the user model. We
        really do need these values to not be blank otherwise Django Ninja
        will interpret these fields as optional.

        """

        self.test_user.last_name = ""

        with self.assertRaises(ValidationError):
            self.test_user.full_clean()

    def test_signup_ok(self):
        """Test User signup method runs successfully and returns a User
        instance."""

        new_user_data = SignupInput(
            username="test2",
            password="test_password",
            first_name="first",
            last_name="last",
        )

        new_user = User.signup(new_user_data)
        self.assertIsInstance(new_user, User)

        # check user instance has hashed password:
        self.assertTrue(new_user.check_password(new_user_data.password))

    def test_signup_fail_duplicate_username(self):
        """Test User signup method throws Integrity error when adding duplicate
        username."""

        bad_user_data = SignupInput(
            username=self.test_user.username,
            password="test_password",
            first_name="first",
            last_name="last",
        )

        with self.assertRaises(IntegrityError):
            User.signup(bad_user_data)

    def test_login_ok(self):
        """Test User login method runs successfuly and returns a User instance
        """

        login_data = LoginInput(
            username=self.test_user.username,
            password="password",
        )

        logged_in_user = User.login(login_data)

        self.assertIsInstance(logged_in_user, User)
        self.assertEqual(self.test_user.username, logged_in_user.username)

    def test_login_fail_incorrect_password(self):
        """Test login method raises AuthenticationError on incorrect
        password."""

        bad_login_data = LoginInput(
            username=self.test_user.username,
            password="bad_password",
        )

        with self.assertRaises(AuthenticationError):
            User.login(bad_login_data)

    def test_login_fail_nonexistent_username(self):
        """Test login method raises ObjectDoesNotExist on nonexistent
        username."""

        bad_login_data = LoginInput(
            username="nonexistent_user",
            password="password",
        )

        with self.assertRaises(ObjectDoesNotExist):
            User.login(bad_login_data)
