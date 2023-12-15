# from django.db import models
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User model. Currently draws from AbstractUser with no additional
    columns."""


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