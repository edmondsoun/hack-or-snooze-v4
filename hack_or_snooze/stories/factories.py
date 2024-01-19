import uuid
import datetime

import factory

from factory import Sequence

from users.factories import UserFactory

# FIXME: we're finding that multiple instances of StoryFactory get generated
# with the same UUID. Need to debug this for testing.


class StoryFactory(factory.django.DjangoModelFactory):
    """Factory Class for Users"""

    class Meta:
        model = 'stories.Story'
        django_get_or_create = ('user',)

    # id = LazyFunction(lambda: str(uuid.uuid4()))
    # no matter what we use, the str(uuid) piece is always evaluated when the class
    # is defined, therefore the uuid will always be the same.

    # since it's not important that the id in the factory is a uuid, (or even for the model)
    # we could use sequence here to generate a incrementing id so that the id is always unique
    # everytime we generate a story instance during tests.
    id = Sequence(lambda count: str(uuid.uuid4()))
    user = factory.SubFactory(UserFactory)
    author = "test_author"
    title = "test_title"
    url = "http://test.com"
    created = datetime.datetime(
        2020, 1, 1, 0, 0, 0, 0,
        tzinfo=datetime.timezone.utc
    )
    modified = datetime.datetime(
        2020, 1, 1, 0, 0, 0, 0,
        tzinfo=datetime.timezone.utc
    )
