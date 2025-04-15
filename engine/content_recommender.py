
# engine/content_recommender.py

from itertools import zip_longest
from sqlalchemy import select, func
from db.db_models import UserLike, UserSave, UserView
from engine.utils import generate_random_ids



class ContentRecommender:

    @staticmethod
    async def get_interleaved_recommendations(
        user_id: int,
        session,
        content_model,
        recommend_fn,  # function like AnalyticsManager.recommend_videos_for_user
        id_field_name: str,
        limit: int = 10
    ):
        # Step 1: Fetch IDs already liked, saved, viewed
        liked_ids = await session.execute(
            select(getattr(UserLike, id_field_name)).where(UserLike.user_id == user_id)
        )
        saved_ids = await session.execute(
            select(getattr(UserSave, id_field_name)).where(UserSave.user_id == user_id)
        )
        viewed_ids = await session.execute(
            select(getattr(UserView, id_field_name)).where(UserView.user_id == user_id)
        )

        exclude_ids = {
            *{r[0] for r in liked_ids.fetchall()},
            *{r[0] for r in saved_ids.fetchall()},
            *{r[0] for r in viewed_ids.fetchall()},
        }

        # Step 2: Fetch personalized recommendations
        all_recommendations = await recommend_fn(user_id, session, limit * 2)
        recommended = [
            content for content, *_ in all_recommendations if content.id not in exclude_ids
        ][:limit]

        # Step 3: Fetch random unseen content
        minmax = await session.execute(select(func.min(content_model.id), func.max(content_model.id)))
        min_id, max_id = minmax.first()
        random_ids = set(generate_random_ids(min_id, max_id, limit * 2))
        random_ids -= exclude_ids | {r.id for r in recommended}

        random_items = []
        if random_ids:
            result = await session.execute(
                select(content_model).where(content_model.id.in_(list(random_ids)[:limit]))
            )
            random_items = result.scalars().all()

        # Step 4: Interleave
        interleaved = []
        for a, b in zip_longest(recommended, random_items):
            if a:
                interleaved.append(a)
            if b:
                interleaved.append(b)

        return interleaved[:limit]
