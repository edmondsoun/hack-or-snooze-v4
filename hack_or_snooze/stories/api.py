from typing import List

from ninja import Router, Schema, ModelSchema
from .models import Story
from users.models import User

from users.auth_utils import ApiKey

# FIXME: maybe figure out a different way of handling this rather than 
token_header = ApiKey()


router = Router()


class StorySchema(ModelSchema):
    class Meta:
        model = Story
        # NOTE: current frontend expects 'id' as 'storyId' in response JSON:
        fields = ['id', 'username', 'title',
                  'author', 'url', 'created', 'modified']


class StoryPostIn(Schema):
    author: str
    title: str
    url: str

    class Config:
        extra = "forbid"


@router.post('/', response=StorySchema, summary="PLACEHOLDER", auth=token_header)
def create_story(request, payload: StoryPostIn):
    """Create a story.

    Returns newly created story:
        { id, username, title, author, url, created, modified }

    Authentication: token
    Authorization: all users
    """

    username = request.auth
    story_data = payload.dict()

    story = Story.objects.create(username=username, **story_data)
    return story


@router.get('/', response=List[StorySchema])
def get_stories(request):
    """Get all stories.

    Returns list of story objects as JSON.

    Authentication: token
    Authorization: all users
    """

    stories = Story.objects.all()

    return stories

# STAFFNOTE: The type of id on the story object is UUID, you can
# inspect this in pdb with StorySchema.model_fields, and look at the
# corresponding fields and their type annotations


@router.get('/{str:story_id}')
def get_story(request, story_id: str):
    """Get individual story by ID.

    Returns individual story data as JSON.

    Authentication: token
    Authorization: all users
    """
    pass

# TODO: update
# TODO: delete
