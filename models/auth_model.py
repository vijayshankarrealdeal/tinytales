from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    

class UserRegister(UserBase):
    email: str
    password: str = Field(..., min_length=6, max_length=50)
    confirm_password: str = Field(..., min_length=6, max_length=50)

    class Config:
        orm_mode = True

class UserLogin(UserBase):
    password: str = Field(..., min_length=6, max_length=50)

    class Config:
        orm_mode = True