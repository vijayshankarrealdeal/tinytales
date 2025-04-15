from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from db.db_connect import get_db
from engine.auth_managers import oauth2_scheme
from engine.story_manager import StoryManager
from models.payload_base import PayloadBaseIn, PayloadBaseOut

story_router = APIRouter(tags=["story"])


@story_router.post(
    "/add_story",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(oauth2_scheme)],
)
async def add_story(story: PayloadBaseIn, session: AsyncSession = Depends(get_db)):
    return await StoryManager.add_story(story, session)


@story_router.get(
    "/fetch_story",
    status_code=status.HTTP_200_OK,
    response_model=List[PayloadBaseOut],
    dependencies=[Depends(oauth2_scheme)],
)
async def get_story(
    story_id: Optional[int] = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
):
    return await StoryManager.fetch_story(session, story_id, offset, limit)
