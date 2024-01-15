from typing import List
from pydantic import constr

from ninja import ModelSchema, Schema

from .models import User
from stories.schemas import StorySchema

FORBID_EXTRA_FIELDS_KEYWORD = "forbid"
ALPHANUMERIC_STRING_PATTERN = r'^[0-9a-zA-Z]*$'

### USERS SCHEMAS###


class UserSchema(ModelSchema):
    stories: List[StorySchema]
    favorites: List[StorySchema]

    class Meta:
        model = User
        # for adding a field, it must literally exist on the model, it can't
        # just be a relationship
        fields = ['username', 'first_name', 'last_name', 'date_joined']


class UserOutput(Schema):
    user: UserSchema


class UserPatchInput(ModelSchema):
    # NICETOHAVE: re-enter password for authentication?

    class Meta:
        model = User
        fields = ['password', 'first_name', 'last_name']
        fields_optional = ['password', 'first_name', 'last_name']

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD
## FAVORITES SCHEMAS###


class FavoritePostInput(Schema):
    story_id: str


class FavoriteDeleteInput(Schema):
    story_id: str


### AUTH SCHEMAS###


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
