from db.db_models import ShortVideo
from sqlalchemy.future import select
from sqlalchemy import func

from engine.utils import generate_random_ids


class ShortVideoManager:


    @staticmethod
    async def get_short_video(offset, limit, session):
        try:  
            result = await session.execute(
            select(func.min(ShortVideo.id), func.max(ShortVideo.id))
            )  
            min_id, max_id = result.first()
            random_ids = generate_random_ids(min_id, max_id, limit)
            query = select(ShortVideo).where(ShortVideo.id.in_(random_ids))
            short_video_data = await session.execute(query)
            return short_video_data.scalars().all()
        except Exception as e:
            session.rollback()
