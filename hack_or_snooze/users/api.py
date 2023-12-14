from typing import List

from ninja import ModelSchema, Router
from .models import User

router = Router()

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['username']

# @router.get('/', response=List[UserSchema], summary="PLACEHOLDER")
# def get_users(request):
#     users = User.objects.all()
#     return users

# TODO: ENDPOINT STUBS:

@router.get('/{int:user_id}')
def get_user(request, user_id: int):
    pass

@router.get('/{int:user_id}')
def update_user(request, user_id: int):
    pass
    # FIXME: better patch/put?