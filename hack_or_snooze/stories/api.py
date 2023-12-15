from ninja import Router, ModelSchema
from .models import Story

router = Router()

class StorySchema(ModelSchema):
    class Meta:
        model = Story
        fields =  ['id', 'user_id', 'author', 'created', 'modified']


@router.post('/')
def create_story(request):
    pass

@router.get('/')
def get_stories(request, user_id: int):
    """Get all stories.

    Returns list of story objects as JSON.

    Authentication: token
    Authorization: all users
    """
    pass

# TODO: is there a UUID type for the id?
@router.get('/{str:story_id}')
def get_story(request, story_id: str):
    """Get individual story by ID.

    Returns individual story data as JSON.

    Authentication: token
    Authorization: all users
    """
    pass