from typing import List
from pydantic import UUID4

from django.shortcuts import get_object_or_404

from ninja import Router, Schema, ModelSchema

from .models import Story
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


class StoryPostInput(ModelSchema):
    """Schema for POST /stories request body"""
    class Meta:
        model = Story
        fields = ["author", "title", "url"]

    class Config:
        extra = FORBID_EXTRA_FIELDS_KEYWORD


@router.post(
    '/',
    response=StoryPostOutput,
    summary="PLACEHOLDER",
    auth=token_header
)
def create_story(request, payload: StoryPostInput):
    """Create a story.

    Returns newly created story:
        { id, username, title, author, url, created, modified }

    Authentication: token
    Authorization: all users
    """

    username = request.auth
    story_data = payload.dict()

    story = Story.objects.create(username=username, **story_data)
    return {"story": story}


@router.get('/', response=StoryGetAllOutput)
def get_stories(request):
    """Get all stories.

    Returns list of story objects as JSON.

    Authentication: none
    """

    stories = Story.objects.all()

    return {"stories": stories}

# STAFFNOTE: The type of id on the story object is UUID, you can
# inspect this in pdb with StorySchema.model_fields, and look at the
# corresponding fields and their type annotations

# 3 possible errors:
# 1: You did not give me a UUID
# 2: You gave me something that appears to be a UUID but it's not formatted correctly
# 3: You gave me a proper UUID, but there is no such id in the DB

@router.get('/{story_id}', response=StoryGetOutput)
def get_story(request, story_id: UUID4):
    """Get individual story by ID.

    Returns individual story data as JSON.

    Authentication: none
    """

    story = get_object_or_404(Story, id=story_id)

    return {"story": story}

# TODO: update
# TODO: delete
