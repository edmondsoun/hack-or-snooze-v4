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

    # Need to set blank=False, otherwise the ModelSchema from DjangoNinja will
    # interpret these fields as optional in the schema and coerce
    # their value to None if not included on the request:
    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )

    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
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
