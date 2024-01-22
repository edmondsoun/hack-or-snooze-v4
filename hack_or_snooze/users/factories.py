import factory
import datetime

FACTORY_USER_DEFAULT_PASSWORD = "password"


class UserFactory(factory.django.DjangoModelFactory):
    """Factory Class for Users"""

    class Meta:
        model = 'users.User'
        django_get_or_create = ('username', )

    # need to camel case because "_" is prohibited in usernames by our schema
    username = "user"
    password = factory.PostGenerationMethodCall(
        'set_password', FACTORY_USER_DEFAULT_PASSWORD
    )
    first_name = "userFirst"
    last_name = "userLast"
    date_joined = datetime.datetime(
        2020,1,1,0,0,0,0,
        tzinfo=datetime.timezone.utc
    )
    # We will need this if we want to generate a user with pre-generated
    # favorites
    # favorites = factory.SubFactory(StoryFactory)

    # @factory.post_generation
    # def add_stories(self, create, extracted, **kwargs):
    #     if not create or not extracted:
    #         return

    #     self.stories.add(*extracted)

    # factory boy does not support ways to construct many to many relationships
    # so instead it will perform this operation AFTER generating the model
    # Just invoke the intended factory and pass in as a tuple the items you want
    # to add:
    # UserFactory.create(stories=(story1, story2, story3))