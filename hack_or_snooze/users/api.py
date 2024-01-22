from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from ninja import Router
from ninja.errors import AuthenticationError

from .schemas import (UserOutput,
                      UserPatchInput,
                      FavoritePostInput,
                      FavoriteDeleteInput,
                      SignupInput,
                      LoginInput,
                      AuthOutput,
                      DuplicateUser)
from hack_or_snooze.error_schemas import (Unauthorized, BadRequest)


from .models import User
from stories.models import Story
from .auth_utils import AUTH_KEY, token_header, generate_token


router = Router()


######## AUTH ##################################################################


@router.post(
    '/signup',
    response={201: AuthOutput, 422: DuplicateUser},
    description="DESC_PLACEHOLDER",
    summary="SUMMARY_PLACEHOLDER"
)
def signup(request, data: SignupInput):
    """
    Handle user signup. User must send:
        {
            "username": "test",
            "password": "password",
            "first_name": "First",
            "last_name": "Last"
        }

    On success, creates new user and return auth token and user info:
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

    On failure for repeat username, return error JSON:
        {
            "error": "Username already exists."
        }

    Authentication: none
    """

    try:
        user = User.signup(user_data=data)
    except IntegrityError:
        return 422, {"error": "Username already exists."}

    token = generate_token(user.username)

    return 201, {
        AUTH_KEY: token,
        "user": user
    }


@router.post(
    '/login',
    response={200: AuthOutput, 401: Unauthorized},
    description="DESC_PLACEHOLDER",
    summary="SUMMARY_PLACEHOLDER"
)
def login(request, data: LoginInput):
    """
    Handle user login. User must send:
        {
            "username":"test",
            "password":"password"
        }

    On success, return auth token and user info:
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

    On failure with bad credentials, return error JSON:
        {
            "error": "Invalid credentials."
        }

    Authentication: none
    """

    try:
        user = User.login(user_data=data)
    except (ObjectDoesNotExist, AuthenticationError):
        return 401, {"error": "Invalid credentials."}

    token = generate_token(user.username)

    return {
        AUTH_KEY: token,
        "user": user
    }


######## USERS #################################################################


@router.get(
    '/{str:username}',
    response={200: UserOutput, 401: Unauthorized},
    summary="PLACEHOLDER",
    auth=token_header
)
def get_user(request, username: str):
    """Get information about a single user.

    On success, return user info:
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

    Authentication: token
    Authorization: same user or admin
    """
    curr_user = request.auth

    if username != curr_user.username and curr_user.is_staff is not True:
        return 401, {"error": "Unauthorized"}

    user = get_object_or_404(User, username=username)

    return {"user": user}


@router.patch(
    '/{str:username}',
    response={200: UserOutput, 400: BadRequest, 401: Unauthorized},
    summary="PLACEHOLDER",
    auth=token_header
)
def update_user(request, username: str, data: UserPatchInput):
    """Update a single user.

    On success, return user info:
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

    Authentication: token
    Authorization: same user or admin
    """
    curr_user = request.auth

    if username != curr_user.username and curr_user.is_staff is not True:
        return 401, {"error": "Unauthorized"}

    # exclude_unset allows us to extract only values provided by user, ignoring
    # keys auto-generated by schema that are set to None.

    # exclude_none more forcefully removes any value set to None. This catches
    # cases where the validator on the schema sets a value to None, even if it
    # was provided by the user:
    patch_data = data.dict(exclude_unset=True, exclude_none=True)

    user = get_object_or_404(User, username=username)

    updated_user = user.update(patch_data)

    return {"user": updated_user}


######## FAVORITES ############################################################

# FIXME: find a better name for username
@router.post(
    '/{str:username}/favorites',
    response={200: UserOutput, 400: BadRequest, 401: Unauthorized},
    summary="PLACEHOLDER",
    auth=token_header
)
def add_favorite(request, username: str, data: FavoritePostInput):
    """Add a story to a user's favorites.

    On success, returns user data with favorite on user.favorites.

    Authentication: token
    Authorization: same user or admin
    """
    curr_user = request.auth

    if username != curr_user.username and curr_user.is_staff is not True:
        return 401, {"error": "Unauthorized"}

    # this covers the case where the curr_user is staff, but the target user
    # does not exist
    user = get_object_or_404(User, username=username)

    story_id = data.story_id

    story = get_object_or_404(Story, id=story_id)

    if story in user.stories.all():
        return 400, {"error": "Cannot add own user stories to favorites"}

    # user.favorites is a many-to-many relationship. In Django, a many-to-many
    # field by default is constrained to only allow one instance of a
    # relationship between the two objects
    # calling this again, will NOT duplicate the relationship if it already
    # exists
    user.favorites.add(story)

    return {"user": user}


@router.delete(
    '/{str:username}/favorites',
    response={200: UserOutput, 400: BadRequest, 401: Unauthorized},
    summary="PLACEHOLDER",
    auth=token_header
)
def delete_favorite(request, username: str, data: FavoriteDeleteInput):
    """Delete a story from a user's favorites.

    On success, returns user data.

    Authentication: token
    Authorization: same user or admin
    """
    curr_user = request.auth

    if username != curr_user.username and curr_user.is_staff is not True:
        return 401, {"error": "Unauthorized"}

    # this covers the case where the curr_user is staff, but the target user
    # does not exist
    user = get_object_or_404(User, username=username)

    story_id = data.story_id

    story = get_object_or_404(Story, id=story_id)

    # STAFFNOTE: if you try to remove a story that isn't in your favorites,
    # there is no negative consequence currently.
    user.favorites.remove(story)

    return {"user": user}
