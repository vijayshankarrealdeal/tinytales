import datetime

from sqlalchemy import desc, func
from sqlalchemy.future import select

from db.db_models import ShortVideo, Story, UserView


class ViewAnalyticsManager:

    @staticmethod
    async def get_top_viewed_videos_this_week(session, limit=10):
        try:
            start_of_week = datetime.utcnow() - datetime.timedelta(days=7)

            result = await session.execute(
                select(ShortVideo, func.count(UserView.id).label("view_count"))
                .join(UserView, UserView.short_video_id == ShortVideo.id)
                .where(UserView.created_at >= start_of_week)
                .group_by(ShortVideo.id)
                .order_by(desc("view_count"))
                .limit(limit)
            )
            return result.all()
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def get_top_viewed_stories_this_week(session, limit=10):
        try:
            start_of_week = datetime.utcnow() - timedelta(days=7)

            result = await session.execute(
                select(Story, func.count(UserView.id).label("view_count"))
                .join(UserView, UserView.story_id == Story.id)
                .where(UserView.created_at >= start_of_week)
                .group_by(Story.id)
                .order_by(desc("view_count"))
                .limit(limit)
            )
            return result.all()
        except Exception as e:
            await session.rollback()
            raise e
