from typing import List

from ninja import ModelSchema, Router
from ninja.security import APIKeyHeader

from .models import User

router = Router()

class ApiKey(APIKeyHeader):

    param_name = "token"

    def authenticate(self, request, key):
        """TODO:"""
        if key == "supersecret":
            return key

        # Step 1: split username and hash
        # Step 2: rehash username and check against existing hash
        # Step 3: if they match, return, else, Unauthorized

header_key = ApiKey()


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

    # FIXME:
    pass


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
    pass


######## USERS #################################################################
# Initial test route:
@router.get('/', response=List[UserSchema], summary="PLACEHOLDER", auth=header_key)
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