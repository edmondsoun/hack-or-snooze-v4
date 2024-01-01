from typing import List
from pydantic import constr

from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from ninja import ModelSchema, Schema, Router
from ninja.security import APIKeyHeader
from ninja.errors import AuthenticationError

from .models import User
from .utils import generate_token, check_token

FORBID_EXTRA_FIELDS_KEYWORD = "forbid"
ALPHANUMERIC_STRING = r'^[0-9a-zA-Z]*$'

router = Router()


class ApiKey(APIKeyHeader):
    """Class to provide authentication via token in header."""

    param_name = "token"

    def authenticate(self, request, token):
        """
        Parse token of submission and check validity.

        Tokens are formatted like:
            "<username>:<hash>"

        On success, returns username.

        On failure, returns None. Error message JSON is automatically generated:
            {"detail": "Unauthorized"}
        """
        print("in authenticate")

        if check_token(token):
            username = token.split(":")[0]
            return username


token_header = ApiKey()

######## SCHEMA ################################################################

# TODO: this is a placeholder schema for prototyping and will likely be removed


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['username']


class LoginIn(ModelSchema):
    class Meta:
        model = User
        fields = ['username', 'password']

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD


class SignupIn(ModelSchema):
    username: constr(pattern=ALPHANUMERIC_STRING)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD


class DuplicateUser(Schema):
    error: str


class Unauthorized(Schema):
    error: str


class AuthTokenOut(Schema):
    token: str


######## AUTH ##################################################################


@router.post('/signup', response={200: AuthTokenOut, 422: DuplicateUser})
def signup(request, data: SignupIn):
    """
    Handle user signup. User must send:
        {
            "username": "test",
            "password": "password"
        }

    On success, return auth token:
        {
            "token": "test:098f6bcd4621"
        }

    On failure, return error JSON:

    Authentication: none
    """

    try:
        user = User.signup(user_data=data)
    except IntegrityError:
        return 422, {"error": "Username already exists."}

    token = generate_token(user.username)

    return {"token": token}


@router.post('/login', response={200: AuthTokenOut, 401: Unauthorized})
def login(request, data: LoginIn):
    """
    Handle user login. User must send:
        {
            "username":"test",
            "password":"password"
        }

    On success, return auth token and user information:
        {
            "token": "test:098f6bcd4621"
        }

    On failure, return error JSON:
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

    return {"token": token}

    # if user:
    #     return user
    # else:
    #     return 401, {"error": "unauthorized"}


######## USERS #################################################################
# Initial test route:
@router.get('/', response=List[UserSchema], summary="PLACEHOLDER", auth=token_header)
def get_users(request):
    print("TESTING", request.auth)

    users = User.objects.all()
    return users


@router.get('/{str:username}')
def get_user(request, username: str):
    """Get information about a single user.

    Authentication: token
    Authorization: same user or admin
    """
    # TODO:


@router.post('/{str:username}')
def update_user(request, username: str):
    """Update a single user.

    Authentication: token
    Authorization: same user or admin
    """
    # TODO:
    # FIXME: check API for patch/put and swap


######## FAVORIRTES ############################################################

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
