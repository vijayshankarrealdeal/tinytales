from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    is_new_user: bool = Field(default=False)
    email: str 
    
class UserRegister(UserBase):
    fullname: str
    password: str = Field(..., min_length=6, max_length=50)

    class Config:
        orm_mode = True

class UserLogin(UserBase):
    password: str = Field(..., min_length=6, max_length=50)

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    fullname: str
    email: str
    is_new_user: bool
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    password: Optional[str] = None
    is_new_user: Optional[bool] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[str] = None
    class Config:
        orm_mode = True