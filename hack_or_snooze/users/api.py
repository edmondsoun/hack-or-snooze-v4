from typing import List

from ninja import ModelSchema, Router
from ninja.security import APIKeyHeader

from .models import User
from .utils import generate_token, check_token

router = Router()

class ApiKey(APIKeyHeader):
    """Class to provide authentication via token in header."""

    param_name = "token"

    def authenticate(self, request, key):
        """
        Parse token of submission and check validity.

        Tokens are formatted like:
            "<username>:<hash>"

        On success, returns username.

        On failure, returns None. Error message JSON is automatically generated:
            {"detail": "Unauthorized"}
        """
        print("in authenticate")

        try:
            username, token = key.split(":")
        except ValueError:
            return None

        if check_token(username, token):
            return username


token_header = ApiKey()

######## SCHEMA ################################################################

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['username']


######## AUTH ##################################################################

@router.post('/signup')
def signup(request):
    """
    Handle user signup. User must send:
        # TODO:

    On success, return auth token:

    On failure, return error JSON.

    Authentication: none
    """

    # TODO: user.set_password


@router.post('/login')
def login(request):
    """
    Handle user signup. User must send:
        # TODO:

    On success, return auth token and user information:
        # TODO: describe shape of JSON

    On failure, return error JSON.

    Authentication: none
    """

    # TODO: user.check_password



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