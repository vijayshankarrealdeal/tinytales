from typing import Optional
from pydantic import BaseModel


class ShortVideoOutput(BaseModel):
    """
    Short video output model.
    """

    id: int
    title: str
    url: str
    views: int
    likes: int
    #saves: int
    is_liked: Optional[bool] = False
    is_saved: Optional[bool] = False
    is_viewed: Optional[bool] = False

    class Config:
        orm_mode = True