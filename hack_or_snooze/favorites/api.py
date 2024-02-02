from django.core.exceptions import ObjectDoesNotExist

from ninja import Router

from hack_or_snooze.error_schemas import (
    BadRequest,
    Unauthorized,
    ObjectNotFound,
)
from stories.models import Story
from users.models import User
from users.auth_utils import token_header

from users.schemas import (
    UserOutput,
)

router = Router()


@router.post(
    '/{str:username}/{str:story_id}/favorite',
    response={
        200: UserOutput,
        400: BadRequest,
        401: Unauthorized,
        404: ObjectNotFound
    },
    auth=token_header
)
def add_favorite(request, username: str, story_id: str):
    """
    Add a story to a user's favorites.

    On success, returns user data with target story added to user.favorites:

        {
            "user": {
                "stories": [Story, Story...],
                "favorites": [Story, Story...],
                "username": "test",
                "first_name": "First",
                "last_name": "Last",
                "date_joined": "2000-01-01T00:00:00Z"
            }
        }

    **Authentication: token**

    **Authorization: same user or admin**
    """
    curr_user = request.auth

    if username != curr_user.username and curr_user.is_staff is not True:
        return 401, {"detail": "Unauthorized"}

    # this covers the case where the curr_user is staff, but the target user
    # does not exist:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return 404, {"detail": "User not found."}

    try:
        story = Story.objects.get(id=story_id)
    except ObjectDoesNotExist:
        return 404, {"detail": "Story not found."}

    if story in user.stories.all():
        return 400, {"detail": "Cannot add own user stories to favorites"}

    isFavorited = User.favorites.through.objects.filter(
        user_id=username, story_id=story_id).exists()

    if isFavorited:
        return 400, {"detail": "Story already favorited."}

    user.favorites.add(story)

    return {"user": user}


@router.post(
    '/{str:username}/{str:story_id}/unfavorite',
    response={
        200: UserOutput,
        400: BadRequest,
        401: Unauthorized,
        404: ObjectNotFound
    },
    auth=token_header
)
def remove_favorite(request, username: str, story_id: str):
    """
    Remove a story from a user's favorites.

    On success, returns user data with target story removed from the user's
    favorites:

        {
            "user": {
                "stories": [Story, Story...],
                "favorites": [Story, Story...],
                "username": "test",
                "first_name": "First",
                "last_name": "Last",
                "date_joined": "2000-01-01T00:00:00Z"
            }
        }

    **Authentication: token**

    **Authorization: same user or admin**
    """
    curr_user = request.auth

    if username != curr_user.username and curr_user.is_staff is not True:
        return 401, {"detail": "Unauthorized"}

    isFavorited = User.favorites.through.objects.filter(
        user_id=username, story_id=story_id).exists()

    if not isFavorited:
        return 404, {"detail": "Favorite not found."}

    story = Story.objects.get(id=story_id)
    user = User.objects.get(username=username)

    user.favorites.remove(story)

    return {"user": user}
