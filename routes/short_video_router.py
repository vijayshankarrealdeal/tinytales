from typing import List
from fastapi import APIRouter, Query, Request, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_connect import get_db
from engine.short_video_manager import ShortVideoManager
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
    request: Request,
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    session: AsyncSession = Depends(get_db)
):
    user_id = request.state.user.id
    videos = await ShortVideoManager.get_short_video(user_id, offset, limit, session)
    return videos


@short_video_router.post(
    "/like_unlike_videos",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(oauth2_scheme)],
)
async def like_unlike_video(
    request: Request,
    video_id: int,
    session: AsyncSession = Depends(get_db),
):
    user_id = request.state.user.id
    await ShortVideoManager.like_video(user_id, video_id, session)
    return {"message": "Like/unlike updated successfully"}


@short_video_router.post(
    "/save_videos",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(oauth2_scheme)],
)
async def save_video(
    request: Request,
    video_id: int,
    session: AsyncSession = Depends(get_db),
):
    user_id = request.state.user.id
    await ShortVideoManager.save_video(user_id, video_id, session)
    return {"message": "Save/unsave updated successfully"}


@short_video_router.post(
    "/view_videos",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(oauth2_scheme)],
)
async def view_video(
    request: Request,
    video_id: int,
    session: AsyncSession = Depends(get_db),
):
    user_id = request.state.user.id
    await ShortVideoManager.view_video(user_id, video_id, session)
    return {"message": "View recorded successfully"}

@short_video_router.get("/saved_videos", status_code=status.HTTP_200_OK, dependencies=[Depends(oauth2_scheme)])
async def get_saved_videos(
    request: Request,
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    session: AsyncSession = Depends(get_db),
):
    user_id = request.state.user.id
    videos = await ShortVideoManager.get_saved_videos(user_id, offset, limit, session)
    return videos 