import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from django.conf import settings


# Create your models here.

class Story(TimeStampedModel, models.Model):
    """Story model."""

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.RESTRICT)
    author = models.TextField()
    title = models.TextField()
    url = models.URLField()


    # Because it's a foreign key, we end up with a DB column named "user_id_id".
    # Leaving the below in case we need to swap names around/alias something:

    # @property
    # def user_id(self):
    #     return self.user_id