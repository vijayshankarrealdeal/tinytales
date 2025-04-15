import datetime
from sqlalchemy import case, func, desc, select
from db.db_models import User, ShortVideo, Story, UserView, UserLike, UserSave
from sqlalchemy.ext.asyncio import AsyncSession


class AnalyticsManager:

    @staticmethod
    def _age_weight_case(field, age_field):
        return case(
            (age_field <= 5, field * 1.5),
            (age_field <= 12, field * 1.2),
            else_=field
        )

    @staticmethod
    async def get_age_weighted_top_videos_this_week(session: AsyncSession, limit=10):
        now = datetime.datetime.now()
        start_of_week = now - datetime.timedelta(days=7)

        user_age = User.age

        view_subq = (
            select(
                UserView.short_video_id,
                func.sum(case((user_age <= 5, 1.5), (user_age <= 12, 1.2), else_=1.0)).label("view_score")
            )
            .join(User, User.id == UserView.user_id)
            .where(UserView.created_at >= start_of_week)
            .group_by(UserView.short_video_id)
            .subquery()
        )

        like_subq = (
            select(
                UserLike.short_video_id,
                func.sum(case((user_age <= 5, 3.0), (user_age <= 12, 2.5), else_=2.0)).label("like_score")
            )
            .join(User, User.id == UserLike.user_id)
            .where(UserLike.created_at >= start_of_week)
            .group_by(UserLike.short_video_id)
            .subquery()
        )

        save_subq = (
            select(
                UserSave.short_video_id,
                func.sum(case((user_age <= 5, 6.0), (user_age <= 12, 5.0), else_=4.0)).label("save_score")
            )
            .join(User, User.id == UserSave.user_id)
            .where(UserSave.created_at >= start_of_week)
            .group_by(UserSave.short_video_id)
            .subquery()
        )

        result = await session.execute(
            select(
                ShortVideo,
                func.coalesce(view_subq.c.view_score, 0).label("views"),
                func.coalesce(like_subq.c.like_score, 0).label("likes"),
                func.coalesce(save_subq.c.save_score, 0).label("saves"),
                (
                    func.coalesce(view_subq.c.view_score, 0) +
                    func.coalesce(like_subq.c.like_score, 0) +
                    func.coalesce(save_subq.c.save_score, 0)
                ).label("score")
            )
            .outerjoin(view_subq, ShortVideo.id == view_subq.c.short_video_id)
            .outerjoin(like_subq, ShortVideo.id == like_subq.c.short_video_id)
            .outerjoin(save_subq, ShortVideo.id == save_subq.c.short_video_id)
            .order_by(desc("score"))
            .limit(limit)
        )

        return result.scalars().all()

    @staticmethod
    async def recommend_videos_for_user(user_id: int, session: AsyncSession, limit=10):
        user = await session.get(User, user_id)
        if not user or user.age is None:
            raise ValueError("User or age not found")

        now = datetime.datetime.now()
        last_week = now - datetime.timedelta(days=7)

        user_group = 'A' if user.age <= 5 else 'B' if user.age <= 12 else 'C'
        user_age_group_case = case(
            (User.age <= 5, 'A'),
            (User.age <= 12, 'B'),
            else_='C'
        )

        # Get IDs already interacted with
        liked_ids = await session.execute(select(UserLike.short_video_id).where(UserLike.user_id == user_id))
        saved_ids = await session.execute(select(UserSave.short_video_id).where(UserSave.user_id == user_id))
        viewed_ids = await session.execute(select(UserView.short_video_id).where(UserView.user_id == user_id))

        excluded_ids = {
            *{r[0] for r in liked_ids.fetchall()},
            *{r[0] for r in saved_ids.fetchall()},
            *{r[0] for r in viewed_ids.fetchall()}
        }

        view_subq = (
            select(
                UserView.short_video_id,
                func.count(UserView.id).label("view_score")
            )
            .join(User, User.id == UserView.user_id)
            .where(UserView.created_at >= last_week, user_age_group_case == user_group)
            .group_by(UserView.short_video_id)
            .subquery()
        )

        like_subq = (
            select(
                UserLike.short_video_id,
                func.count(UserLike.id).label("like_score")
            )
            .join(User, User.id == UserLike.user_id)
            .where(UserLike.created_at >= last_week, user_age_group_case == user_group)
            .group_by(UserLike.short_video_id)
            .subquery()
        )

        save_subq = (
            select(
                UserSave.short_video_id,
                func.count(UserSave.id).label("save_score")
            )
            .join(User, User.id == UserSave.user_id)
            .where(UserSave.created_at >= last_week, user_age_group_case == user_group)
            .group_by(UserSave.short_video_id)
            .subquery()
        )

        result = await session.execute(
            select(
                ShortVideo,
                func.coalesce(view_subq.c.view_score, 0),
                func.coalesce(like_subq.c.like_score, 0),
                func.coalesce(save_subq.c.save_score, 0),
                (
                    func.coalesce(view_subq.c.view_score, 0) +
                    func.coalesce(like_subq.c.like_score, 0) * 2 +
                    func.coalesce(save_subq.c.save_score, 0) * 3
                ).label("score")
            )
            .outerjoin(view_subq, ShortVideo.id == view_subq.c.short_video_id)
            .outerjoin(like_subq, ShortVideo.id == like_subq.c.short_video_id)
            .outerjoin(save_subq, ShortVideo.id == save_subq.c.short_video_id)
            .where(ShortVideo.id.not_in(excluded_ids))
            .order_by(desc("score"))
            .limit(limit)
        )

        return result.all()

    @staticmethod
    async def recommend_stories_for_user(user_id: int, session: AsyncSession, limit=10):
        user = await session.get(User, user_id)
        if not user or user.age is None:
            raise ValueError("User or age not found")

        now = datetime.datetime.now()
        last_week = now - datetime.timedelta(days=7)

        user_group = 'A' if user.age <= 5 else 'B' if user.age <= 12 else 'C'
        user_age_group_case = case(
            (User.age <= 5, 'A'),
            (User.age <= 12, 'B'),
            else_='C'
        )

        # Get IDs already interacted with
        liked_ids = await session.execute(select(UserLike.story_id).where(UserLike.user_id == user_id))
        saved_ids = await session.execute(select(UserSave.story_id).where(UserSave.user_id == user_id))
        viewed_ids = await session.execute(select(UserView.story_id).where(UserView.user_id == user_id))

        excluded_ids = {
            *{r[0] for r in liked_ids.fetchall()},
            *{r[0] for r in saved_ids.fetchall()},
            *{r[0] for r in viewed_ids.fetchall()}
        }

        view_subq = (
            select(
                UserView.story_id,
                func.count(UserView.id).label("view_score")
            )
            .join(User, User.id == UserView.user_id)
            .where(UserView.created_at >= last_week, user_age_group_case == user_group)
            .group_by(UserView.story_id)
            .subquery()
        )

        like_subq = (
            select(
                UserLike.story_id,
                func.count(UserLike.id).label("like_score")
            )
            .join(User, User.id == UserLike.user_id)
            .where(UserLike.created_at >= last_week, user_age_group_case == user_group)
            .group_by(UserLike.story_id)
            .subquery()
        )

        save_subq = (
            select(
                UserSave.story_id,
                func.count(UserSave.id).label("save_score")
            )
            .join(User, User.id == UserSave.user_id)
            .where(UserSave.created_at >= last_week, user_age_group_case == user_group)
            .group_by(UserSave.story_id)
            .subquery()
        )

        result = await session.execute(
            select(
                Story,
                func.coalesce(view_subq.c.view_score, 0),
                func.coalesce(like_subq.c.like_score, 0),
                func.coalesce(save_subq.c.save_score, 0),
                (
                    func.coalesce(view_subq.c.view_score, 0) +
                    func.coalesce(like_subq.c.like_score, 0) * 2 +
                    func.coalesce(save_subq.c.save_score, 0) * 3
                ).label("score")
            )
            .outerjoin(view_subq, Story.id == view_subq.c.story_id)
            .outerjoin(like_subq, Story.id == like_subq.c.story_id)
            .outerjoin(save_subq, Story.id == save_subq.c.story_id)
            .where(Story.id.not_in(excluded_ids))
            .order_by(desc("score"))
            .limit(limit)
        )

        return result.all()
