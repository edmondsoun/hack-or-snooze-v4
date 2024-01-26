from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth import authenticate

from ninja import Router

from hack_or_snooze.error_schemas import (
    BadRequest,
    Unauthorized,
    ObjectNotFound,
)
from stories.models import Story

from .schemas import (
    UserOutput,
    UserPatchInput,
    FavoritePostInput,
    FavoriteDeleteInput,
    SignupInput,
    LoginInput,
    AuthOutput,
)
from .models import User
from .auth_utils import AUTH_KEY, token_header, generate_token

router = Router()


######## AUTH #################################################################

@router.post(
    '/signup',
    response={201: AuthOutput, 400: BadRequest}
)
def signup(request, data: SignupInput):
    """
    Handles user signup. User must send:

        {
            "username": "test",
            "password": "password",
            "first_name": "First",
            "last_name": "Last"
        }

    On success, creates new user and returns auth token and user info:

        {
            "token": "test:098f6bcd4621",
            "user": {
                "stories": [Story, Story...],
                "favorites": [Story, Story...],
                "username": "test",
                "first_name": "First",
                "last_name": "Last",
                "date_joined": "2000-01-01T00:00:00Z"
            }
        }

    On failure for repeat username, returns error JSON:

        {
            "detail": "Username already exists."
        }

    **Authentication: none**
    """
    if User.objects.filter(username=data.username).exists():
        return 400, {"detail": "Username already exists."}

    with transaction.atomic():
        user = User.objects.create_user(
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            password=data.password
        )

    token = generate_token(user.username)

    return 201, {
        AUTH_KEY: token,
        "user": user
    }


@router.post(
    '/login',
    response={200: AuthOutput, 401: Unauthorized}
)
def login(request, data: LoginInput):
    """
    Handles user login. User must send:

        {
            "username":"test",
            "password":"password"
        }

    On success, returns auth token and user info:

        {
            "token": "test:098f6bcd4621",
            "user": {
                "stories": [Story, Story...],
                "favorites": [Story, Story...],
                "username": "test",
                "first_name": "First",
                "last_name": "Last",
                "date_joined": "2000-01-01T00:00:00Z"
            }
        }

    On failure with bad credentials, returns error JSON:

        {
            "detail": "Invalid credentials."
        }

    **Authentication: none**
    """

    user = authenticate(username=data.username, password=data.password)

    if user is None:
        return 401, {"detail": "Invalid credentials."}

    token = generate_token(user.username)

    return {
        AUTH_KEY: token,
        "user": user
    }


######## USERS ################################################################

@router.get(
    '/{str:username}',
    response={200: UserOutput, 401: Unauthorized},
    auth=token_header
)
def get_user(request, username: str):
    """
    Get information about a single user.

    On success, returns user info:

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

    user = get_object_or_404(User, username=username)

    return {"user": user}


@router.patch(
    '/{str:username}',
    response={200: UserOutput, 400: BadRequest, 401: Unauthorized},
    auth=token_header
)
def update_user(request, username: str, data: UserPatchInput):
    """
    Update a single user.

    On success, returns user info:

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

    # exclude_none removes any value set to None. A value may be set to None
    # automatically by Django Ninja because the field was not provided, or by
    # one of our additional validators:
    patch_data = data.dict(exclude_none=True)

    user = get_object_or_404(User, username=username)

    updated_user = user.update(patch_data)

    return {"user": updated_user}


######## FAVORITES ############################################################

@router.post(
    '/{str:username}/favorites',
    response={
        200: UserOutput,
        400: BadRequest,
        401: Unauthorized,
        404: ObjectNotFound
    },
    auth=token_header
)
def add_favorite(request, username: str, data: FavoritePostInput):
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

    story_id = data.story_id

    try:
        story = Story.objects.get(id=story_id)
    except ObjectDoesNotExist:
        return 404, {"detail": "Story not found."}

    if story in user.stories.all():
        return 400, {"detail": "Cannot add own user stories to favorites"}

    # user.favorites is a many-to-many relationship. In Django, a many-to-many
    # field by default is constrained to only allow one instance of a
    # relationship between the two objects
    # calling this again, will NOT duplicate the relationship if it already
    # exists

    user.favorites.add(story)

    return {"user": user}


@router.delete(
    '/{str:username}/favorites',
    response={
        200: UserOutput,
        400: BadRequest,
        401: Unauthorized,
        404: ObjectNotFound
    },
    auth=token_header
)
def delete_favorite(request, username: str, data: FavoriteDeleteInput):
    """
    Delete a story from a user's favorites.

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

    favorite_table = User.favorites.through
    favorite = favorite_table.objects.filter(
        user_id=username,
        story_id=data.story_id
    )

    if not favorite.exists():
        return 404, {"detail": "Favorite not found."}

    story = Story.objects.get(id=data.story_id)
    user = User.objects.get(username=username)

    user.favorites.remove(story)

    return {"user": user}
