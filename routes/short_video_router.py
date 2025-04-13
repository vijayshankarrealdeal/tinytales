import logging
from typing import List
import aiohttp
from fastapi import APIRouter, HTTPException, Query, Request, status, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_connect import get_db
from db.db_models import ShortVideo
from engine.short_video import ShortVideoManager
from models.short_video_model import ShortVideoOutput
from engine.auth_managers import oauth2_scheme

short_video_router = APIRouter(tags=["short_video"])

from fastapi import APIRouter, Request, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_connect import get_db
from db.db_models import ShortVideo
import aiohttp
import logging

short_video_router = APIRouter(tags=["short_video"])


@short_video_router.get(
    "/get_videos",
    status_code=status.HTTP_201_CREATED,
    response_model=List[ShortVideoOutput],
    dependencies=[Depends(oauth2_scheme)],
)
async def get_short_video(
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of records to return"
    ),
    session: AsyncSession = Depends(get_db)):
    videos = await ShortVideoManager().get_short_video(offset, limit, session)
    return videos