from django.test import TestCase


from stories.factories import StoryFactory


class StoryModelTest(TestCase):
    def setUp(self):
        self.test_story = StoryFactory()

    def test_story_id_is_string(self):
        """Test that the id on stories is a str"""

        self.assertIsInstance(self.test_story.id, str)
