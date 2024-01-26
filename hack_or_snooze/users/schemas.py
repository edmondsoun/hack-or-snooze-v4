import re
from typing import List

from pydantic import validator, model_validator

from ninja import ModelSchema, Schema, Field

from hack_or_snooze.exceptions import InvalidUsernameException
from hack_or_snooze.settings import FORBID_EXTRA_FIELDS_KEYWORD
from stories.schemas import StorySchema

from .models import User

SLUGIFIED_STRING_PATTERN = re.compile('^[0-9a-zA-Z-_]*$')


### USERS SCHEMAS ###

class UserSchema(ModelSchema):
    """User Schema"""

    stories: List[StorySchema]
    favorites: List[StorySchema]

    class Meta:
        model = User
        # for adding a field, it must literally exist on the model, it can't
        # just be a relationship
        fields = ['username', 'first_name', 'last_name', 'date_joined']


class UserOutput(Schema):
    """Schema for user output."""

    user: UserSchema


class UserPatchInput(ModelSchema):
    """Schema for PATCH /users/{username} response body"""

    class Meta:
        model = User
        fields = ['password', 'first_name', 'last_name']
        fields_optional = ['password', 'first_name', 'last_name']

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD

    # NOTE: Leaving these here for reference while we refactor.
    # We are intentionally opting-in to less validation so that 
    # students can get some experience with apis that will literally
    # do what you ask them to.

    # We need check_fields=False because we are accessing these fields through
    # its model:
    # @validator('first_name', pre=True, check_fields=False)
    # def check_first_name(cls, value):
    #     """If first_name is sent as an empty string, set it to None.
    #     Otherwise, return original value."""
    #     if value == "":
    #         return None
    #     return value

    # @validator('last_name', pre=True, check_fields=False)
    # def check_last_name(cls, value):
    #     """If last_name is sent as an empty string, set it to None.
    #     Otherwise, return original value."""
    #     if value == "":
    #         return None
    #     return value

    # @validator('password', pre=True, check_fields=False)
    # def check_password(cls, value):
    #     """If password is sent as an empty string, set it to None.
    #     Otherwise, return original value."""
    #     if value == "":
    #         return None
    #     return value

    # @model_validator(mode="after")
    # def check_missing_or_empty_data(self):
    #     """Check that request body contains some data to patch.

    #     Returns self or raises EmptyPatchRequestException.
    #     """

    #     patch_data = self.dict(exclude_none=True)

    #     if len(patch_data) == 0:
    #         raise EmptyPatchRequestException(
    #             "Patch body empty. Must send at least one non-empty field."
    #         )

    #     return self


### FAVORITES SCHEMAS ###

class FavoritePostInput(Schema):
    """Schema for POST /users/{username}/favorites response body"""

    story_id: str


class FavoriteDeleteInput(Schema):
    """Schema for DELETE /users/{username}/favorites response body"""

    story_id: str


### AUTH SCHEMAS ###

class SignupInput(ModelSchema):
    """Schema for POST /signup request body"""

    username: str = Field(..., min_length=2)
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    password: str = Field(..., min_length=5)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD

    # NOTE: There is no validator to ensure that user passwords meet a 
    # minimum length. Consequently, this means that a signup with a "" password
    # is valid.
    
    @validator('username', pre=True, check_fields=False)
    def check_username(cls, value):
        """Check username against regex pattern for slugified string.

        Returns original value or raises InvalidUsernameException."""

        if not SLUGIFIED_STRING_PATTERN.match(value):
            raise InvalidUsernameException(
                "Username must contain only numbers, letters, underscores or hyphens.")
        return value


class LoginInput(ModelSchema):
    """Schema for POST /login request body"""

    class Meta:
        model = User
        fields = ['username', 'password']

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD


class AuthOutput(Schema):
    """Schema for auth routes response."""
    token: str
    user: UserSchema
