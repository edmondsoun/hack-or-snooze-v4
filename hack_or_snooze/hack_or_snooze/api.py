from ninja import NinjaAPI

from stories.api import router as stories_router
from users.api import router as users_router

from hack_or_snooze.exceptions import InvalidUsernameException


api = NinjaAPI()


api.add_router("/users/", users_router)
api.add_router("/stories/", stories_router)


# Handle exceptions raised in the validators themselves:
@api.exception_handler(InvalidUsernameException)
def on_invalid_username(request, exc):
    """Custom exception handler for failed username validation."""
    return api.create_response(
        request,
        {"detail": exc.message},
        status=400
    )
