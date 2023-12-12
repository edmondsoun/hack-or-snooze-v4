# from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils.models import TimeStampedModel

class User(AbstractUser, TimeStampedModel):
    """User model."""

    # username = models.TextField(primary_key=True, max_length=50)
    # name = models.TextField(max_length=100)

    pass