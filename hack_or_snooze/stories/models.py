import uuid

from django.db import models
from django.conf import settings

from model_utils.models import TimeStampedModel


class Story(TimeStampedModel, models.Model):
    """Story model."""

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
    )

    # related_name gives us ability to do things like: User.stories.all()
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="stories_old",
        verbose_name="User who posted",
    )

    author = models.CharField(
        max_length=50,
    )

    title = models.CharField(
        max_length=200
    )

    url = models.URLField()