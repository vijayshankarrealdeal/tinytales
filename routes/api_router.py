from fastapi import APIRouter
from routes.story_route import story_router

router = APIRouter()
router.include_router(story_router, prefix="/story", tags=["story"])

