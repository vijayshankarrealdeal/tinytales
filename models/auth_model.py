from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str
    

class UserRegister(UserBase):
    fullname: str
    password: str 
    #= Field(..., min_length=6, max_length=50)

    class Config:
        orm_mode = True

class UserLogin(UserBase):
    password: str 
    #= Field(..., min_length=6, max_length=50)

    class Config:
        orm_mode = True