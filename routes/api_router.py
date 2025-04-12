from fastapi import APIRouter
from routes.story_route import story_router
from routes.auth_router import user_router
from routes.short_video_router import short_video_router

router = APIRouter()
router.include_router(story_router, prefix="/story", tags=["story"])
router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(short_video_router, prefix="/short_video", tags=["short_video"])