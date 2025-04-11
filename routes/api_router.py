from fastapi import APIRouter
from routes.story_route import story_router
from routes.auth_router import user_router

router = APIRouter()
router.include_router(story_router, prefix="/story", tags=["story"])
router.include_router(user_router, prefix="/user", tags=["user"])
