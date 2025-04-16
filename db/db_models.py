from sqlalchemy.orm import relationship
from db.db_connect import Base
from sqlalchemy import ARRAY, Column, Boolean, Integer, Text, ForeignKey, TIMESTAMP, func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    fullname = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    is_new_user = Column(Boolean, default=False)
    gender = Column(Text, nullable=True)
    dob = Column(Text, nullable=True)
    age = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


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
        return f"<Palette(id={self.id}, predominant={self.predominant})>"


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    poster = Column(Text)
    poster_pallet_id = Column(Integer, ForeignKey("palettes.id", ondelete="SET NULL"), nullable=True)
    poster_pallet = relationship("Palette", foreign_keys=[poster_pallet_id])
    created_at = Column(TIMESTAMP, server_default=func.now())
    chapters = relationship("StoryChapter", back_populates="story", cascade="all, delete-orphan")
    views = Column(Integer, default=0, nullable=False)
    likes = Column(Integer, default=0, nullable=False)
    saves = Column(Integer, default=0, nullable=False)
    tags = Column(ARRAY(Text), nullable=True)

    def __repr__(self):
        return f"<Story(id={self.id}, title={self.title})>"


class StoryChapter(Base):
    __tablename__ = "story_chapters"

    id = Column(Integer, primary_key=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    chapter_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    image = Column(Text, nullable=True)
    image_pallet_id = Column(Integer, ForeignKey("palettes.id", ondelete="SET NULL"), nullable=True)

    image_pallet = relationship("Palette", foreign_keys=[image_pallet_id])
    story = relationship("Story", back_populates="chapters")

    def __repr__(self):
        return f"<StoryChapter(id={self.id}, chapter_index={self.chapter_index})>"


class ShortVideo(Base):
    __tablename__ = "short_videos"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    views = Column(Integer, default=0, nullable=False)
    likes = Column(Integer, default=0, nullable=False)
    saves = Column(Integer, default=0, nullable=False)
    filename = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    tags = Column(ARRAY(Text), nullable=True)

    def __repr__(self):
        return f"<ShortVideo(id={self.id}, title={self.title})>"


class UserLike(Base):
    __tablename__ = "user_likes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    short_video_id = Column(Integer, ForeignKey("short_videos.id", ondelete="CASCADE"), nullable=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User")
    short_video = relationship("ShortVideo")
    story = relationship("Story")

    def __repr__(self):
        return f"<UserLike(user_id={self.user_id}, video_id={self.short_video_id}, story_id={self.story_id})>"


class UserSave(Base):
    __tablename__ = "user_saves"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    short_video_id = Column(Integer, ForeignKey("short_videos.id", ondelete="CASCADE"), nullable=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User")
    short_video = relationship("ShortVideo")
    story = relationship("Story")

    def __repr__(self):
        return f"<UserSave(user_id={self.user_id}, video_id={self.short_video_id}, story_id={self.story_id})>"


class UserView(Base):
    __tablename__ = "user_views"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    short_video_id = Column(Integer, ForeignKey("short_videos.id", ondelete="CASCADE"), nullable=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User")
    short_video = relationship("ShortVideo")
    story = relationship("Story")

    def __repr__(self):
        return f"<UserView(user_id={self.user_id}, short_video_id={self.short_video_id}, story_id={self.story_id})>"