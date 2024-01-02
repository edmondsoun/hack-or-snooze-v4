from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from ninja.errors import AuthenticationError


class User(AbstractUser):
    """User model. Currently draws from AbstractUser with no additional
    columns."""

    # TODO: model should include DB constraints on username pattern to mirror
    # schema validation?

    username = models.CharField(
        primary_key=True,
        max_length=150,
    )

    @classmethod
    def signup(cls, user_data):
        """Sign up a new user with provided credentials.

        Returns user instance or raises IntegrityError on duplicate username."""

        user = cls.objects.create(
            username=user_data.username,
        )

        user.set_password(raw_password=user_data.password)
        user.save()

        return user

    @classmethod
    def login(cls, user_data):
        """Log in an existing user with provided credentials.

        Returns user instance or raises error if credentials are incorrect."""

        user = cls.objects.get(username=user_data.username)

        if user.check_password(user_data.password):
            return user
        else:
            raise AuthenticationError("Unauthorized")



class Favorite(models.Model):
    """Favorite model.

    A favorite is a many-to-many relationship between users and stories.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='favorites',
    )

    story = models.ForeignKey(
        'stories.Story',
        on_delete=models.RESTRICT,
    )

    class Meta:
        unique_together = ['user_id', 'story_id']
