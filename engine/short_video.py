from db.db_models import ShortVideo
from sqlalchemy.future import select
from sqlalchemy import func

from engine.utils import generate_random_ids


from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from models import ShortVideo, UserLike, UserSave
from utils import generate_random_ids  # your helper


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
        except Exception:
            await session.rollback()
            raise

    @staticmethod
    async def like_video(user_id: int, video_id: int, session):
        try:
            # Check if already liked
            exists = await session.execute(
                select(UserLike).where(
                    UserLike.user_id == user_id,
                    UserLike.short_video_id == video_id
                )
            )
            like = exists.scalar_one_or_none()

            if like:
                # Unlike: remove record, decrement counter
                await session.execute(
                    delete(UserLike).where(UserLike.id == like.id)
                )
                await session.execute(
                    ShortVideo.__table__.update()
                    .where(ShortVideo.id == video_id)
                    .values(likes=ShortVideo.likes - 1)
                )
            else:
                # Like: add record, increment counter
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
    async def save_video(user_id: int, video_id: int, session):
        try:
            exists = await session.execute(
                select(UserSave).where(
                    UserSave.user_id == user_id,
                    UserSave.short_video_id == video_id
                )
            )
            save = exists.scalar_one_or_none()

            if save:
                # Unsave
                await session.execute(
                    delete(UserSave).where(UserSave.id == save.id)
                )
                await session.execute(
                    ShortVideo.__table__.update()
                    .where(ShortVideo.id == video_id)
                    .values(saves=ShortVideo.saves - 1)
                )
            else:
                # Save
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



