from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_connect import get_db
from engine.short_video import ShortVideoManager


short_video_router = APIRouter(tags=["short_video"])



@short_video_router.post("/get_videos",status_code=status.HTTP_201_CREATED)
async def get_short_video(session: AsyncSession = Depends(get_db)):
    token = await ShortVideoManager().get_short_video(session)
    return token
