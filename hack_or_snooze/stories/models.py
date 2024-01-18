import uuid

from django.db import models
from django.conf import settings

from model_utils.models import TimeStampedModel


def generate_uuid():
    """Generate a dynamic UUID to use for story IDs."""
    return str(uuid.uuid4())

class Story(TimeStampedModel, models.Model):
    """Story model."""

    class Meta:
        verbose_name_plural = 'Stories'

    # The goal of using CharField instead of UUIDField here is to ensure that
    # the students *can* encounter a 404 without a lot of jumping through hoops
    id = models.CharField(
        default=generate_uuid,
        primary_key=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="stories",
        verbose_name="User who posted",
    )

    author = models.CharField(
        max_length=50,
    )

    title = models.CharField(
        max_length=200
    )

    url = models.URLField()

    def __str__(self):
        return self.title
