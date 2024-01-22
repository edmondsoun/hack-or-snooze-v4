from ninja import NinjaAPI

from stories.api import router as stories_router
from users.api import router as users_router

from users.exceptions import (
    InvalidUsernameException,
    EmptyPatchRequestException,
)

api = NinjaAPI()


api.add_router("/users/", users_router)
api.add_router("/stories/", stories_router)


@api.exception_handler(InvalidUsernameException)
def on_invalid_username(request, exc):
    return api.create_response(
        request,
        {"detail": exc.message},
        status=401
    )


@api.exception_handler(EmptyPatchRequestException)
def on_empty_patch_request(request, exc):
    return api.create_response(
        request,
        {"detail": exc.message},
        status=400
    )
