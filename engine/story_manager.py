from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
from db.db_models import Story, StoryChapter, Palette
from engine.analytics_manager import AnalyticsManager
from engine.content_recommender import ContentRecommender
from models.payload_base import PayloadBaseIn, PayloadBaseOut


class StoryManager:

    @staticmethod
    async def add_story(story: PayloadBaseIn, session: AsyncSession):
        try:
            story_payload = await PayloadBaseOut.create(story)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Payload creation error: {e}")

        try:
            poster_palette_obj = Palette(**story_payload.poster_pallet.model_dump())
            session.add(poster_palette_obj)
            await session.flush()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Poster palette insert error: {e}")

        new_story = Story(
            title=story_payload.title,
            poster=story_payload.poster,
            poster_pallet=poster_palette_obj,
        )

        for idx, chapter_data in enumerate(story_payload.chapters):
            try:
                chapter_palette_obj = Palette(**chapter_data.image_pallet.model_dump())
                session.add(chapter_palette_obj)
                await session.flush()

                chapter = StoryChapter(
                    chapter_index=idx,
                    content=chapter_data.content,
                    image=chapter_data.image,
                    image_pallet=chapter_palette_obj,
                )
                new_story.chapters.append(chapter)
            except Exception as e:
                raise HTTPException(
                    status_code=400, detail=f"Chapter creation error at chapter {idx}: {e}"
                )

        session.add(new_story)
        try:
            await session.commit()
            await session.refresh(new_story)
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Integrity error during commit: {e.orig}"
            )
        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Database error during commit: {e}"
            )
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Unexpected error during commit: {e}"
            )

        return story_payload

    @staticmethod
    async def fetch_story(session: AsyncSession, story_id: int = None, offset: int = 0, limit: int = 10):
        if story_id:
            query = (
                select(Story)
                .where(Story.id == story_id)
                .options(
                    joinedload(Story.poster_pallet),
                    joinedload(Story.chapters).joinedload(StoryChapter.image_pallet),
                )
            )
            result = await session.execute(query)
            stories = result.scalars().unique().all()
            if not stories:
                raise HTTPException(status_code=404, detail="No story found for the given id")
        else:
            query = (
                select(Story)
                .options(
                    joinedload(Story.poster_pallet),
                    joinedload(Story.chapters).joinedload(StoryChapter.image_pallet),
                )
                .offset(offset)
                .limit(limit)
            )
            result = await session.execute(query)
            stories = result.scalars().unique().all()
            for story in stories:
                story.chapters = sorted(story.chapters, key=lambda x: x.id)

        return stories
    
    @staticmethod
    async def get_recommended_stories(user_id, session, limit=10):
        return await ContentRecommender.get_interleaved_story_recommendations(
            user_id=user_id,
            session=session,
            # content_model=Story,
            recommend_fn=AnalyticsManager.recommend_stories_for_user,
            # id_field_name="story_id",
            limit=limit
        )
