from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status, Depends
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_connect import get_db
from db.db_models import Story, StoryChapter, Palette
from models.payload_base import PayloadBaseIn, PayloadBaseOut
from engine.auth_managers import oauth2_scheme


story_router = APIRouter()


@story_router.post(
    "/add_story",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(oauth2_scheme)],
)
async def add_story(story: PayloadBaseIn, session: AsyncSession = Depends(get_db)):
    try:
        story_payload = await PayloadBaseOut.create(story)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Payload creation error: {e}")
    try:
        poster_palette_obj = Palette(**story_payload.poster_pallet.model_dump())
        session.add(poster_palette_obj)
        await session.flush()
    except Exception as e:
        print(f"Poster palette insert error: {e}")
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
            await session.flush()  # flush so palette gets an ID

            chapter = StoryChapter(
                chapter_index=idx,
                content=chapter_data.content,
                image=chapter_data.image,
                image_pallet=chapter_palette_obj,
            )
            new_story.chapters.append(chapter)  # use the 'chapters' relationship
        except Exception as e:
            print(f"Chapter creation error at chapter {idx}: {e}")
            raise HTTPException(
                status_code=400, detail=f"Chapter creation error at chapter {idx}: {e}"
            )

    session.add(new_story)
    try:
        await session.commit()
        await session.refresh(new_story)
    except IntegrityError as e:
        await session.rollback()
        print(f"Integrity error during commit: {e.orig}")
        raise HTTPException(
            status_code=400, detail=f"Integrity error during commit: {e.orig}"
        )
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Database error during commit: {e}")
        raise HTTPException(
            status_code=400, detail=f"Database error during commit: {e}"
        )
    except Exception as e:
        await session.rollback()
        print(f"Unexpected error during commit: {e}")
        raise HTTPException(
            status_code=400, detail=f"Unexpected error during commit: {e}"
        )

    return story_payload


@story_router.get(
    "/fetch_story",
    status_code=status.HTTP_200_OK,
    response_model=List[PayloadBaseOut],
    dependencies=[Depends(oauth2_scheme)],
)
async def get_story(
    story_id: Optional[int] = None,
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of records to return"
    ),
    session: AsyncSession = Depends(get_db),
):
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
            raise HTTPException(
                status_code=404, detail="No story found for the given id"
            )
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

    return stories
