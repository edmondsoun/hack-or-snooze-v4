from ninja import NinjaAPI

from stories.api import router as stories_router
from users.api import router as users_router

from hack_or_snooze.exceptions import InvalidUsernameException

description = """
How to Use This API
-------------------

First, start by registering a new user using the **/api/users/signup** route
sending the following information:

    {
        "username": "string",
        "first_name": "string",
        "last_name": "string",
        "password": "string"
    }

Upon a successful request to that endpoint, you will receive a JSON payload that
includes your user details as well as a token. Like so:

    {
        "token": "your_username:token_data"
        "user": ...
    }

With your new token, you can now use all of the endpoints that require auth
(the endpoints marked with a lock). You will need to send this token in the 
HEADERS of your request like so:

    HEADER: token: your_token

You can also supply this token to the **AUTHORIZE** button located at the top of this
documentation for usage in these interactive endpoints.

"""


api = NinjaAPI(
    title="Hack Or Snooze API",
    description=description
    
)


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
