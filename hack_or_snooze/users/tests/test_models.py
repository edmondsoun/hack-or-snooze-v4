from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from users.models import User
from users.factories import UserFactory
from users.schemas import SignupInput, LoginInput
# from stories.factories import StoryFactory

# TODO: remove any unnecessary setup and imports


class UserModelTest(TestCase):
    def setUp(self):
        self.test_user = UserFactory()
        # self.test_user.save()
        self.new_user_data = SignupInput(
            username="test2",
            password="test_password",
            first_name="first",
            last_name="last",
        )
        self.login_data = LoginInput(
            username=self.test_user.username,
            password="password",
        )
        # self.edmond_user = UserFactory(username="edmond")

        # self.test_story = StoryFactory()
        # self.edmond_story = StoryFactory(user=self.edmond_user)

        # self.test_user.favorites.add(self.edmond_story)

    # def test_details(self):
    #     self.assertEqual(self.test_user.username, "test")

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

        new_user = User.signup(self.new_user_data)
        self.assertIsInstance(new_user, User)

        # change the password field since the user one will have the hashed
        # password
        # TODO: Check out __dict__ before we solidify this test as done
        self.new_user_data.password = new_user.password
        new_data_dict = dict(self.new_user_data)
        # new_user_dict = new_user.__dict__

        for field in new_data_dict:
            self.assertEqual(new_data_dict[field], new_user[field])

    def test_signup_duplicate_username(self):
        """Test User signup method throws Integrity error when adding duplicate
        username"""

        with self.assertRaises(IntegrityError):
            User.signup(**self.new_user_data, username=self.test_user)

    def test_login_ok(self):
        """Test User login method runs successfuly and returns a User instance
        """
        logged_in_user = User.login(self.login_data)

        self.assertIsInstance(logged_in_user, User)
        self.assertEqual(self.test_user.username, logged_in_user.username)

    def test_login_raises_authentication_error(self):
        pass

    # TEST: signup
        # can signup successfully (returns an instance)✅
        # duplicate username raises IntegrityError✅

    # TEST: login
        # can login successfully (returns an instance)✅
        # incorrect password raises AuthenticationError
        # nonexistent nonexistent username raises ObjectDoesNotExist
