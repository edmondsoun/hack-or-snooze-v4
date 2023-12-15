# from django.db import models
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# From: https://stackoverflow.com/questions/17165147/how-can-i-make-a-django-form-field-contain-only-alphanumeric-characters
alphanumeric = RegexValidator(
    r'^[0-9a-zA-Z]*$',
    'Only alphanumeric characters are allowed.'
)

class User(AbstractUser):
    """User model. Currently draws from AbstractUser with no additional
    columns."""

    username = models.CharField(
        primary_key=True,
        max_length=150,
        validators=[alphanumeric],
    )


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