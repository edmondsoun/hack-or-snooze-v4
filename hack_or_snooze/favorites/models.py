from django.db import models
from django.conf import settings


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