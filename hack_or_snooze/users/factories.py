
import factory

from factory import LazyAttribute


class UserFactory(factory.django.DjangoModelFactory):
    """Factory Class for Users"""

    class Meta:
        model = 'users.User'
        django_get_or_create = ('username', )

    username = "test"
    password = factory.PostGenerationMethodCall(
        'set_password', 'password'
    )
    first_name = "keys"
    last_name = "soun"
