from typing import List
from fastapi import APIRouter, Query, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_connect import get_db
from engine.short_video import ShortVideoManager
from models.short_video_model import ShortVideoOutput
from engine.auth_managers import oauth2_scheme


short_video_router = APIRouter(tags=["short_video"])

@short_video_router.get(
    "/get_videos",
    status_code=status.HTTP_200_OK,
    response_model=List[ShortVideoOutput],
    dependencies=[Depends(oauth2_scheme)],
)
async def get_short_video(
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    session: AsyncSession = Depends(get_db),
):
    videos = await ShortVideoManager.get_short_video(offset, limit, session)
    return videos


@short_video_router.post(
    "/like_unlike_videos",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(oauth2_scheme)],
)
async def like_unlike_video(
    user_id: int,
    video_id: int,
    session: AsyncSession = Depends(get_db),
):
    await ShortVideoManager.like_video(user_id, video_id, session)
    return {"message": "Like/unlike updated successfully"}


@short_video_router.post(
    "/save_videos",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(oauth2_scheme)],
)
async def save_video(
    user_id: int,
    video_id: int,
    session: AsyncSession = Depends(get_db),
):
    await ShortVideoManager.save_video(user_id, video_id, session)
    return {"message": "Save/unsave updated successfully"}


@short_video_router.post(
    "/view_videos",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(oauth2_scheme)],
)
async def view_video(
    user_id: int,
    video_id: int,
    session: AsyncSession = Depends(get_db),
):
    await ShortVideoManager.view_video(user_id, video_id, session)
    return {"message": "View recorded successfully"}
