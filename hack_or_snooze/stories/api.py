from typing import List
from pydantic import UUID4

from django.shortcuts import get_object_or_404

from ninja import Router, Schema, ModelSchema

from .models import Story
# from users.api import Unauthorized
# from users.models import User

from users.auth_utils import token_header

# TODO: Find a more general config area for this, so we dont dupe
FORBID_EXTRA_FIELDS_KEYWORD = "forbid"


router = Router()


class StorySchema(ModelSchema):
    class Meta:
        model = Story
        # NOTE: current frontend expects 'id' as 'storyId' in response JSON:
        fields = ['id', 'username', 'title',
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


class Unauthorized(Schema):
    error: str


@router.post(
    '/',
    response=StoryPostOutput,
    summary="PLACEHOLDER",
    auth=token_header
)
def create_story(request, data: StoryPostInput):
    """Create a story.

    Returns newly created story:
        {
            "story": {
                "id": "725ff2f9-2cc4-4e29-abab-95b9921f5a6b",
                "username": "test",
                "title": "testtitle",
                "author": "testauthor",
                "url": "test.com",
                "created": "2000-01-01T00:00:00Z",
                "modified": "2000-01-01T00:00:00Z"
            }
        }

    Authentication: token
    Authorization: all users
    """

    username = request.auth
    story_data = data.dict()

    story = Story.objects.create(username=username, **story_data)

    return {"story": story}


@router.get(
    '/',
    response=StoryGetAllOutput
)
def get_stories(request):
    """Get all stories.

    Returns list of stories:
        {
            "stories": [Story, Story...]
        }

    Where "Story" is:
        {
                "id": "725ff2f9-2cc4-4e29-abab-95b9921f5a6b",
                "username": "test",
                "title": "testtitle",
                "author": "testauthor",
                "url": "test.com",
                "created": "2000-01-01T00:00:00Z",
                "modified": "2000-01-01T00:00:00Z"
        }

    Authentication: none
    """

    stories = Story.objects.all()

    return {"stories": stories}


# 3 possible errors:
# 1: You did not give me a UUID
# 2: You gave me something that appears to be a UUID but it's not formatted correctly
# 3: You gave me a proper UUID, but there is no such id in the DB

@router.get(
    '/{story_id}',
    response=StoryGetOutput
)
def get_story(request, story_id: UUID4):
    """Get story by ID.

    Returns story data:
        {
            "story": {
                "id": "725ff2f9-2cc4-4e29-abab-95b9921f5a6b",
                "username": "test",
                "title": "testtitle",
                "author": "testauthor",
                "url": "test.com",
                "created": "2000-01-01T00:00:00Z",
                "modified": "2000-01-01T00:00:00Z"
            }
        }


    Authentication: none
    """

    story = get_object_or_404(Story, id=story_id)

    return {"story": story}


@router.delete(
    '/{story_id}',
    response={200: StoryDeleteOutput, 401: Unauthorized},
    auth=token_header,
)
def delete_story(request, story_id: UUID4):
    """Delete story by ID.

    Returns confirmation with ID of deleted story:
        {
            "deleted": true,
            "id": "725ff2f9-2cc4-4e29-abab-95b9921f5a6b"
        }

    Authentication: token
    Authorization: same user or admin
    """

    curr_user = request.auth

    story = get_object_or_404(Story, id=story_id)

    if story.username != curr_user.username and curr_user.is_staff is not True:
        return 401, {"error": "Unauthorized."}

    story.delete()

    return {
        "deleted": True,
        "id": story_id
    }


# STAFFNOTE: Further study includes prompt to allow users to edit stories. Do we
# actually want this?
