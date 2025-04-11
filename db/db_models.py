from sqlalchemy.orm import relationship
from db.db_connect import Base
from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP, func


class Palette(Base):
    __tablename__ = "palettes"

    id = Column(Integer, primary_key=True)
    predominant = Column(Text, nullable=False)
    dark = Column(Text, nullable=False)
    light = Column(Text, nullable=False)
    median_brightness = Column(Text, nullable=False)
    most_saturated = Column(Text, nullable=False)
    least_saturated = Column(Text, nullable=False)
    coolest = Column(Text, nullable=False)
    warmest = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f"<Palette(id={self.id}, predominant={self.predominant}, "
            f"dark={self.dark}, light={self.light})>"
        )


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    poster = Column(Text)  # Poster image URL or path

    # Use a foreign key and relationship named with "pallet"
    poster_pallet_id = Column(Integer, ForeignKey("palettes.id", ondelete="SET NULL"), nullable=True)
    poster_pallet = relationship("Palette", foreign_keys=[poster_pallet_id])

    created_at = Column(TIMESTAMP, server_default=func.now())

    # One-to-many relationship to StoryChapter
    chapters = relationship("StoryChapter", back_populates="story", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Story(id={self.id}, title={self.title})>"


class StoryChapter(Base):
    __tablename__ = "story_chapters"

    id = Column(Integer, primary_key=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"))
    chapter_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    image = Column(Text)  # Image URL or path

    # Use a foreign key and relationship named "image_pallet"
    image_pallet_id = Column(Integer, ForeignKey("palettes.id", ondelete="SET NULL"), nullable=True)
    image_pallet = relationship("Palette", foreign_keys=[image_pallet_id])

    # Back-reference to Story
    story = relationship("Story", back_populates="chapters")

    def __repr__(self):
        return f"<StoryChapter(id={self.id}, chapter_index={self.chapter_index})>"
