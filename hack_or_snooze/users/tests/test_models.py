from django.test import TestCase
# from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from users.models import User
from users.factories import UserFactory
from users.schemas import SignupInput
# from stories.factories import StoryFactory

# TODO: remove any unnecessary setup and imports


class UserModelTest(TestCase):
    def setUp(self):
        self.test_user = UserFactory()
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
        """Test User signup method runs successfully and returns a user
        instance."""

        new_user_data = SignupInput(
            username="test2",
            password="test_password",
            first_name="first",
            last_name="last",
        )

        new_user = User.signup(new_user_data)
        self.assertIsInstance(new_user, User)
        print("new_user is:", new_user)

        for field in new_user_data:
            self.assertEqual(new_user_data[field], new_user[field])



    # TEST: signup
        # can signup successfully (returns an instance)
        # duplicate username raises IntegrityError

    # TEST: login
        # can login successfully (returns an instance)
        # incorrect password raises AuthenticationError
        # nonexistent nonexistent username raises ObjectDoesNotExist
