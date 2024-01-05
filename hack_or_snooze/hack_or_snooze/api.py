from ninja import NinjaAPI

from stories.api import router as stories_router
from users.api import router as users_router

api = NinjaAPI()

# STAFFNOTE: it's possible to add middleware-style auth to all operations 
# declared below! investigate this further down the line:

api.add_router("/users/", users_router)
api.add_router("/stories/", stories_router)


