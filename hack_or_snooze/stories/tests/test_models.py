from django.test import TestCase

from stories.factories import StoryFactory


class StoryModelTestCase(TestCase):
    def setUp(self):
        self.test_story = StoryFactory()

    def test_story_id_is_string(self):
        """Test that the id on stories is a str"""

        self.assertIsInstance(self.test_story.id, str)

    def test_dunder_str(self):
        self.test_story = StoryFactory()

        self.assertEqual(str(self.test_story), self.test_story.title)
