from django.test import TestCase
# from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from users.factories import UserFactory
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

    # investigate full_clean
    # TEST: SIS: test_model
    # isInstance

    # TEST: first_name, last_name fields
        # test that fields are not allowed to be blank

    # TEST: signup
        # can signup successfully
        # duplicate username raises IntegrityError

    # TEST: login
        # can login successfully
        # incorrect password raises AuthenticationError
        # nonexistent nonexistent username raises ObjectDoesNotExist
