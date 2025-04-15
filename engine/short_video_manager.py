from sqlalchemy import func, select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_models import ShortVideo, UserLike, UserSave, UserView
from engine.analytics_manager import AnalyticsManager
from engine.content_recommender import ContentRecommender



class ShortVideoManager:

    @staticmethod
    async def get_short_video(user_id, offset, limit, session):
        return await ContentRecommender.get_interleaved_video_recommendations(
            user_id=user_id,
            session=session,
            #content_model=ShortVideo,
            recommend_fn=AnalyticsManager.recommend_videos_for_user,
            #id_field_name="short_video_id",
            limit=limit
        )


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
