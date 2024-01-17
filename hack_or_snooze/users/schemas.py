import re
from typing import List
from typing_extensions import Annotated
from pydantic import validator, StringConstraints

from ninja import ModelSchema, Schema

from .models import User
from stories.schemas import StorySchema

from users.exceptions import InvalidUsernameException

FORBID_EXTRA_FIELDS_KEYWORD = "forbid"
ALPHANUMERIC_STRING_PATTERN = re.compile('^[0-9a-zA-Z]*$')

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

    # We need check_fields=False to allow these because we are inhereting
    # these fields from a parent model:
    @validator('first_name', pre=True, check_fields=False)
    def check_first_name(cls, value):
        """If first_name is sent as an empty string, set it to None."""
        if value == "":
            return None
        return value

    @validator('last_name', pre=True, check_fields=False)
    def check_last_name(cls, value):
        """If last_name is sent as an empty string, set it to None."""
        if value == "":
            return None
        return value

    @validator('password', pre=True, check_fields=False)
    def check_password(cls, value):
        """If password is sent as an empty string, set it to None."""
        if value == "":
            return None
        return value


## FAVORITES SCHEMAS###

class FavoritePostInput(Schema):
    story_id: str


class FavoriteDeleteInput(Schema):
    story_id: str


### AUTH SCHEMAS###


class SignupInput(ModelSchema):
    # TODO: Change how this is displayed in the docs OR see if we can default to
    # "Schema" display instead of "Example Value":
    # username: Annotated[
    #     str,
    #     StringConstraints(pattern=ALPHANUMERIC_STRING_PATTERN)
    # ]

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD

    @validator('username', pre=True, check_fields=False)
    def check_username(cls, value):
        """If username does not conform to ALPHANUMERIC String"""
        # test that incoming value meets regex constraint
        if not ALPHANUMERIC_STRING_PATTERN.match(value):
            raise InvalidUsernameException("testing custom exception validator")
        return value
        # if it doesnot throw error
        # if it does, return value


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
