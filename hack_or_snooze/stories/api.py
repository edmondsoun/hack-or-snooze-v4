from django.shortcuts import get_object_or_404

from ninja import Router

from hack_or_snooze.error_schemas import Unauthorized

from users.auth_utils import token_header

from .models import Story
from .schemas import (
    StoryPostInput,
    StoryPostOutput,
    StoryGetAllOutput,
    StoryGetOutput,
    StoryDeleteOutput,
)

router = Router()


@router.post(
    '/',
    response=StoryPostOutput,
    auth=token_header
)
def create_story(request, data: StoryPostInput):
    """
    Create a story.

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

    **Authentication: token**
    **Authorization: all users**
    """

    curr_user = request.auth
    story_data = data.dict()

    story = Story.objects.create(user=curr_user, **story_data)

    return {"story": story}


@router.get(
    '/',
    response=StoryGetAllOutput,
    description="DESC_PLACEHOLDER"
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


@router.get(
    '/{str:story_id}',
    response=StoryGetOutput,
    description="DESC_PLACEHOLDER"
)
def get_story(request, story_id: str):
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
    '/{str:story_id}',
    response={200: StoryDeleteOutput, 401: Unauthorized},
    description="DESC_PLACEHOLDER",
    auth=token_header
)
def delete_story(request, story_id: str):
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

    if story.user.username != curr_user.username and curr_user.is_staff is not True:
        return 401, {"detail": "Unauthorized."}

    story.delete()

    return {
        "deleted": True,
        "id": story_id
    }
