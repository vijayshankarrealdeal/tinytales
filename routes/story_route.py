from fastapi import APIRouter, Depends, Query, Request, status
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
    "/fetch_story_by_id",
    status_code=status.HTTP_200_OK,
    response_model=List[PayloadBaseOut],
    dependencies=[Depends(oauth2_scheme)],
)
async def get_story_by_id(
    story_id: Optional[int] = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
):
    return await StoryManager.fetch_story(session, story_id, offset, limit)

@story_router.get(
    "/fetch_story",
    status_code=status.HTTP_200_OK,
    response_model=List[PayloadBaseOut],
    dependencies=[Depends(oauth2_scheme)],
)
async def get_story(
    request: Request,
    limit: int = Query(2, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
):
    user_id = request.state.user.id
    return await StoryManager.get_recommended_stories(user_id, session, limit)



@story_router.post(
    "/like_unlike_story",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(oauth2_scheme)],
)
async def like_unlike_stories(
    request: Request,
    story_id: int,
    session: AsyncSession = Depends(get_db),
):
    user_id = request.state.user.id
    await StoryManager.like_story(user_id, story_id, session)
    return {"message": "Like/unlike updated successfully"}


@story_router.post(
    "/save_story",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(oauth2_scheme)],
)
async def save_stories(
    request: Request,
    story_id: int,
    session: AsyncSession = Depends(get_db),
):
    user_id = request.state.user.id
    await StoryManager.save_story(user_id, story_id, session)
    return {"message": "Save/unsave updated successfully"}


@story_router.post(
    "/view_story",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(oauth2_scheme)],
)
async def view_stories(
    request: Request,
    story_id: int,
    session: AsyncSession = Depends(get_db),
):
    user_id = request.state.user.id
    await StoryManager.view_story(user_id, story_id, session)
    return {"message": "View recorded successfully"}
