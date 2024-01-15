from django.test import TestCase
from users.factories import UserFactory
from stories.factories import StoryFactory


class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.test_story = StoryFactory()
        # print(f"test_story id: {self.test_story.id}")
        self.edmond_user = UserFactory(username="edmond")
        self.edmond_story = StoryFactory(user=self.edmond_user)
        # print(f"edmond_story id: {self.edmond_story.id}")
        # self.test_user = UserFactory.create(favorites=(self.edmond_story))
        self.test_user = UserFactory()
        self.test_user.favorites.add(self.edmond_story)

    def test_details(self):
        self.assertEqual(self.test_user.username, "test")

    #TEST: SIS: test_model
    # isInstance

    #TEST: signup
        # can signup successfully
        # duplicate username raises IntegrityError

    #TEST: login
        # can login successfully
        # incorrect password raises AuthenticationError
        # nonexistent username raises ObjectDoesNotExist
