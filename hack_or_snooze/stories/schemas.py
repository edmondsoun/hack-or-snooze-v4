from typing import List

from ninja import Schema, ModelSchema, Field

from .models import Story

FORBID_EXTRA_FIELDS_KEYWORD = "forbid"


class StorySchema(ModelSchema):
    """Story Schema"""

    # NOTE: PYDANTIC MAGIC
    username: str = Field(..., alias="user.username")

    class Meta:
        model = Story
        # FIXME: current frontend expects 'id' as 'storyId' in response JSON
        # (this will need a fix on the *frontend*):
        fields = ['id', 'title',
                  'author', 'url', 'created', 'modified']


class StoryGetOutput(Schema):
    """Schema for GET /stories/{id} response body"""

    story: StorySchema


class StoryPostOutput(Schema):
    """Schema for GET /stories/{id} response body"""

    story: StorySchema


class StoryGetAllOutput(Schema):
    """Schema for GET /stories response body"""

    stories: List[StorySchema]


class StoryDeleteOutput(ModelSchema):
    """Schema for DELETE /stories/{id} response body"""
    deleted: bool

    class Meta:
        model = Story
        fields = ["id"]

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD


class StoryPostInput(ModelSchema):
    """Schema for POST /stories request body"""
    class Meta:
        model = Story
        fields = ["author", "title", "url"]

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD
