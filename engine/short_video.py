from sqlalchemy import func, select, insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from itertools import zip_longest
from db.db_models import ShortVideo, UserLike, UserSave, UserView
from engine.analytics_manager import AnalyticsManager
from engine.utils import generate_random_ids



class ShortVideoManager:

    @staticmethod
    async def get_short_video(offset, limit, session: AsyncSession):
        try:
            top_week_videos = await AnalyticsManager.get_age_weighted_top_videos_this_week(session, limit)
            print("Top videos this week:", top_week_videos)
            result = await session.execute(
                select(func.min(ShortVideo.id), func.max(ShortVideo.id))
            )
            min_id, max_id = result.first()
            random_ids = set(generate_random_ids(min_id, max_id, limit + len(top_week_videos)))
            random_ids = random_ids - {video.id for video in top_week_videos}
            random_ids = list(random_ids)
            query = select(ShortVideo).where(ShortVideo.id.in_(random_ids))
            short_video_data = await session.execute(query)
            random_data = short_video_data.scalars().all()
            data = []
            for a, b in zip_longest(top_week_videos, random_data):
                if a is not None:
                    data.append(a)
                if b is not None:
                    data.append(b)
            return data
            
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def like_video(user_id: int, video_id: int, session: AsyncSession):
        try:
            exists = await session.execute(
                select(UserLike).where(
                    UserLike.user_id == user_id,
                    UserLike.short_video_id == video_id
                )
            )
            like = exists.scalar_one_or_none()

            if like:
                await session.execute(
                    delete(UserLike).where(UserLike.id == like.id)
                )
                await session.execute(
                    ShortVideo.__table__.update()
                    .where(ShortVideo.id == video_id)
                    .values(likes=ShortVideo.likes - 1)
                )
            else:
                await session.execute(
                    insert(UserLike).values(user_id=user_id, short_video_id=video_id)
                )
                await session.execute(
                    ShortVideo.__table__.update()
                    .where(ShortVideo.id == video_id)
                    .values(likes=ShortVideo.likes + 1)
                )

            await session.commit()

        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def save_video(user_id: int, video_id: int, session: AsyncSession):
        try:
            exists = await session.execute(
                select(UserSave).where(
                    UserSave.user_id == user_id,
                    UserSave.short_video_id == video_id
                )
            )
            save = exists.scalar_one_or_none()

            if save:
                await session.execute(
                    delete(UserSave).where(UserSave.id == save.id)
                )
                await session.execute(
                    ShortVideo.__table__.update()
                    .where(ShortVideo.id == video_id)
                    .values(saves=ShortVideo.saves - 1)
                )
            else:
                await session.execute(
                    insert(UserSave).values(user_id=user_id, short_video_id=video_id)
                )
                await session.execute(
                    ShortVideo.__table__.update()
                    .where(ShortVideo.id == video_id)
                    .values(saves=ShortVideo.saves + 1)
                )

            await session.commit()

        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def view_video(user_id: int, video_id: int, session: AsyncSession):
        try:
            await session.execute(
                insert(UserView).values(user_id=user_id, short_video_id=video_id)
            )
            await session.execute(
                ShortVideo.__table__.update()
                .where(ShortVideo.id == video_id)
                .values(views=ShortVideo.views + 1)
            )
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
