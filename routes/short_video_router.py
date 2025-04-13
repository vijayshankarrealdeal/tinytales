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


@short_video_router.get("/stream_video_by_id")
async def stream_video_by_id(
    video_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    try:
        # Fetch video record
        video_record = await session.get(ShortVideo, video_id)
        if not video_record or not video_record.url:
            raise HTTPException(status_code=404, detail="Video not found")

        # Clean up any trailing '?'
        video_url = video_record.url.rstrip("?")
        headers = {}

        if range_header := request.headers.get("range"):
            headers["Range"] = range_header

        timeout = aiohttp.ClientTimeout(total=30)  # Optional: timeout control
        print(f"🔌 Streaming video (video_id={video_id}, url={video_url})")
        async with aiohttp.ClientSession(timeout=timeout) as http_session:
            async with http_session.get(video_url, headers=headers) as resp:
                if resp.status not in (200, 206):
                    raise HTTPException(status_code=resp.status, detail="Failed to fetch video from Supabase")

                stream_headers = dict(resp.headers)
                status_code = 206 if "Content-Range" in stream_headers else 200

                # Stream safely with error handling
                async def safe_stream():
                    try:
                        async for chunk in resp.content.iter_chunked(1024 * 512):
                            yield chunk
                    except aiohttp.ClientConnectionError as e:
                        logging.warning(f"🔌 Client connection closed unexpectedly during streaming (video_id={video_id}) {e}")
                    except Exception as e:
                        logging.error(f"❌ Unexpected streaming error (video_id={video_id}): {e}")

                return StreamingResponse(
                    safe_stream(),
                    status_code=status_code,
                    headers={
                        "Content-Type": stream_headers.get("Content-Type", "video/mp4"),
                       
                        "Content-Range": stream_headers.get("Content-Range", ""),
                        "Accept-Ranges": "bytes",
                    },
                )
    except Exception as e:
        logging.exception("Unhandled error in stream_video_by_id")
        raise HTTPException(status_code=500, detail="Internal server error during video streaming")
