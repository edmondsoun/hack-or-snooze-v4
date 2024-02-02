from django.db import models
from django.contrib.auth.models import AbstractUser

from ninja.errors import AuthenticationError

from stories.models import Story


class User(AbstractUser):
    """User model."""

    username = models.CharField(
        primary_key=True,
        max_length=150,
    )

    favorites = models.ManyToManyField(
        Story,
        related_name="favorited_by",
        blank=True,
    )

    def update(self, patch_data):
        """Update user record and return updated user instance."""

        for field, value in patch_data.items():
            if (field == 'password'):
                self.set_password(raw_password=patch_data['password'])
            else:
                setattr(self, field, value)

        self.save()

        return self
