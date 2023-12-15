# from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils.models import TimeStampedModel

class User(AbstractUser, TimeStampedModel):
    """User model.

    Draws from AbstractUser and TimeStampedModel to produce the following schema:
    #TODO:

    """

    pass