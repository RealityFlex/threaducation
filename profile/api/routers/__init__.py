from api.routers.profile_type import router as profile_type_router
from api.routers.user import router as user_router

# Make routers available from the module
__all__ = ["profile_type_router", "user_router"]