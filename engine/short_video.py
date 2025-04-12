from db.db_models import ShortVideo
from sqlalchemy.future import select

class ShortVideoManager:

    @staticmethod
    async def get_short_video(offset, limit, session):
        try:
            query = select(ShortVideo).offset(offset).limit(limit)
            short_video_data = await session.execute(query)
            return short_video_data.scalars().all()
        except Exception as e:
            session.rollback()