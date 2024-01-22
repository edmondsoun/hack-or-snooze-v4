import re
from typing import List
from pydantic import validator, model_validator

from ninja import ModelSchema, Schema

from .models import User
from stories.schemas import StorySchema

from users.exceptions import (
    InvalidUsernameException,
    EmptyPatchRequestException,
)

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

    class Meta:
        model = User
        fields = ['password', 'first_name', 'last_name']
        fields_optional = ['password', 'first_name', 'last_name']

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD

    # We need check_fields=False to allow these because we are accessing
    # these fields through its model:
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

    @model_validator(mode="after")
    def check_missing_or_empty_data(self):
        """Check that request body contains some data to patch.

        Returns self or raise EmptyPatchRequestException.
        """

        patch_data = self.dict(exclude_none=True)

        if len(patch_data) == 0:
            raise EmptyPatchRequestException(
                "Patch body empty. Must send at least one non-empty field."
            )

        return self


## FAVORITES SCHEMAS###

class FavoritePostInput(Schema):
    story_id: str


class FavoriteDeleteInput(Schema):
    story_id: str


### AUTH SCHEMAS###


class SignupInput(ModelSchema):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD

    @validator('username', pre=True, check_fields=False)
    def check_username(cls, value):
        """Check username against regex pattern for alphanumeric string."""
        if not ALPHANUMERIC_STRING_PATTERN.match(value):
            raise InvalidUsernameException("Username must be alphanumeric.")
        return value


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
