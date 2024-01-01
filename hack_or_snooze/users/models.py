from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from ninja.errors import AuthenticationError

# From: https://stackoverflow.com/questions/17165147/how-can-i-make-a-django-form-field-contain-only-alphanumeric-characters
# FIXME: this doesn't work right now, circle back to fix
alphanumeric = RegexValidator(
    regex=r'^[0-9a-zA-Z]*$',
    message='Only alphanumeric characters are allowed.'
)


class User(AbstractUser):
    """User model. Currently draws from AbstractUser with no additional
    columns."""

    username = models.CharField(
        primary_key=True,
        max_length=150,
        validators=[alphanumeric],
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
        """Sign up a new user with provided credentials.

        Returns user instance or TODO:"""

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
    )

    story = models.ForeignKey(
        'stories.Story',
        on_delete=models.RESTRICT,
    )

    class Meta:
        unique_together = ['user_id', 'story_id']
