import uuid
import factory

from factory import LazyFunction

from users.factories import UserFactory


class StoryFactory(factory.django.DjangoModelFactory):
    """Factory Class for Users"""

    class Meta:
        model = 'stories.Story'
        django_get_or_create = ('user',)

    id = LazyFunction(lambda: str(uuid.uuid4()))
    user = factory.SubFactory(UserFactory)
    author = "test_author"
    title = "test_title"
    url = "http://test.com"
