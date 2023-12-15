# from typing import List

from ninja import ModelSchema, Router
from .models import User

router = Router()

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['username']



# Initial test route:
# @router.get('/', response=List[UserSchema], summary="PLACEHOLDER")
# def get_users(request):
#     users = User.objects.all()
#     return users

# STUBS:

@router.get('/{str:username}')
def get_user(request, username: str):
    pass

@router.post('/{str:username}')
def update_user(request, username: str):
    pass
    # FIXME: check API for patch/put and swap


#### Favorites Endpoints ####
@router.post('/{str:username}/favorites/{int:favorite_id}')
def add_favorite(request, username: str, favorite_id: int):
    pass

