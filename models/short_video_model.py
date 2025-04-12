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

    class Config:
        orm_mode = True
