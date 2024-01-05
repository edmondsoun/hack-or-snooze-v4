from typing import List
from pydantic import constr

from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from ninja import ModelSchema, Schema, Router
from ninja.errors import AuthenticationError

from .models import User
from .auth_utils import AUTH_KEY, token_header, generate_token

from stories.api import StorySchema

FORBID_EXTRA_FIELDS_KEYWORD = "forbid"
ALPHANUMERIC_STRING_PATTERN = r'^[0-9a-zA-Z]*$'

router = Router()


######## SCHEMA ################################################################


class UserSchema(ModelSchema):
    stories: List[StorySchema]
    favorites: List[StorySchema]

    class Meta:
        model = User
        # for adding a field, it must literally exist on the model, it can't
        # just be a relationship
        fields = ['username', 'first_name', 'last_name', 'date_joined']


class UserGetOutput(Schema):
    user: UserSchema


class UserPatchInput(ModelSchema):
    # NICETOHAVE: re-enter password for authentication?

    class Meta:
        model = User
        fields = ['password', 'first_name', 'last_name']
        fields_optional = ['password', 'first_name', 'last_name']

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD


class SignupInput(ModelSchema):
    username: constr(pattern=ALPHANUMERIC_STRING_PATTERN)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD


class LoginInput(ModelSchema):
    class Meta:
        model = User
        fields = ['username', 'password']

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD


class AuthOutput(Schema):
    token: str
    user: UserSchema


class DuplicateUser(Schema):
    error: str


class Unauthorized(Schema):
    error: str


class BadRequest(Schema):
    error: str


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
    response={200: UserGetOutput, 401: Unauthorized},
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
        return 401, {"error": "Unauthorized."}

    user = User.objects.get(username=username)

    return {"user": user}


@router.patch(
    '/{str:username}',
    response={200: UserGetOutput, 400: BadRequest, 401: Unauthorized},
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
        return 401, {"error": "Unauthorized."}

    # exclude_unset allows us to extract only values provided by user, ignoring
    # keys auto-generated by schema that are set to None:
    patch_data = data.dict(exclude_unset=True)

    # if user sent empty request body, provide helpful feedback:
    if len(patch_data) == 0:
        return 400, {"error": "No data provided to patch."}

    user = get_object_or_404(User, username=curr_user)

    for attr, value in patch_data.items():
        setattr(user, attr, value)

    user.save()

    return {"user": user}


######## FAVORITES ############################################################

@router.post('/{str:username}/favorites/{int:favorite_id}')
def add_favorite(request, username: str, favorite_id: int):
    """Add a story to a user's favorites.

    On success, returns confirmation message and story data.

    Authentication: token
    Authorization: same user or admin
    """
    # TODO:


@router.delete('/{str:username}/favorites/{int:favorite_id}')
def delete_favorite(request, username: str, favorite_id: int):
    """Delete a story from a user's favorites.

    On success, returns confirmation message and story data.

    Authentication: token
    Authorization: same user or admin
    """
    # TODO:
