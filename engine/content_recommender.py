from itertools import zip_longest
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from db.db_models import UserLike, UserSave, UserView, Story, StoryChapter, ShortVideo
from engine.utils import generate_random_ids


class ContentRecommender:

    @staticmethod
    async def get_interleaved_video_recommendations(user_id: int, session, recommend_fn, limit: int = 10):
        # Step 1: Exclude already interacted video IDs
        liked_ids = await session.execute(select(UserLike.short_video_id).where(UserLike.user_id == user_id))
        saved_ids = await session.execute(select(UserSave.short_video_id).where(UserSave.user_id == user_id))
        viewed_ids = await session.execute(select(UserView.short_video_id).where(UserView.user_id == user_id))

        exclude_ids = {
            *{r[0] for r in liked_ids.fetchall() if r[0]},
            *{r[0] for r in saved_ids.fetchall() if r[0]},
            *{r[0] for r in viewed_ids.fetchall() if r[0]},
        }

        all_recommendations = await recommend_fn(user_id, session, limit * 2)
        recommended = [
            content for content, *_ in all_recommendations if content.id not in exclude_ids
        ][:limit]

        minmax = await session.execute(select(func.min(ShortVideo.id), func.max(ShortVideo.id)))
        min_id, max_id = minmax.first()
        random_ids = set(generate_random_ids(min_id, max_id, limit * 2))
        random_ids -= exclude_ids | {r.id for r in recommended}

        random_items = []
        if random_ids:
            result = await session.execute(
                select(ShortVideo).where(ShortVideo.id.in_(list(random_ids)[:limit]))
            )
            random_items = result.scalars().all()

        interleaved = []
        for a, b in zip_longest(recommended, random_items):
            if a:
                interleaved.append(a)
            if b:
                interleaved.append(b)

        return interleaved[:limit]

    @staticmethod
    async def get_interleaved_story_recommendations(user_id: int, session, recommend_fn, limit: int = 10):
        # Step 1: Exclude already interacted story IDs
        liked_ids = await session.execute(select(UserLike.story_id).where(UserLike.user_id == user_id))
        saved_ids = await session.execute(select(UserSave.story_id).where(UserSave.user_id == user_id))
        viewed_ids = await session.execute(select(UserView.story_id).where(UserView.user_id == user_id))

        exclude_ids = {
            *{r[0] for r in liked_ids.fetchall() if r[0]},
            *{r[0] for r in saved_ids.fetchall() if r[0]},
            *{r[0] for r in viewed_ids.fetchall() if r[0]},
        }

        all_recommendations = await recommend_fn(user_id, session, limit * 2)
        recommended = [
            content for content, *_ in all_recommendations if content.id not in exclude_ids
        ][:limit]

        minmax = await session.execute(select(func.min(Story.id), func.max(Story.id)))
        min_id, max_id = minmax.first()
        random_ids = set(generate_random_ids(min_id, max_id, limit * 2))
        random_ids -= exclude_ids | {r.id for r in recommended}

        random_items = []
        if random_ids:
            result = await session.execute(
                select(Story)
                .where(Story.id.in_(list(random_ids)[:limit]))
                .options(
                    selectinload(Story.chapters).selectinload(StoryChapter.image_pallet),
                    selectinload(Story.poster_pallet),
                )
            )
            random_items = result.scalars().all()

        interleaved = []
        for a, b in zip_longest(recommended, random_items):
            if a:
                interleaved.append(a)
            if b:
                interleaved.append(b)

        return interleaved[:limit]
