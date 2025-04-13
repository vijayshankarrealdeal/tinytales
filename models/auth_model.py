from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, validator
from pydantic_core import PydanticCustomError


class UserBase(BaseModel):
    is_new_user: bool = Field(default=False)
    email: EmailStr

    @field_validator("email")
    def custom_email_error(cls, value: str):
        try:
            return EmailStr.validate(value)
        except ValueError:
            raise PydanticCustomError(
                "value_error.email", "Please provide a valid email address."
            )


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
    email: EmailStr
    is_new_user: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    password: Optional[str] = None
    is_new_user: Optional[bool] = None
    email: Optional[EmailStr] = None
    gender: Optional[str] = None
    dob: Optional[str] = None

    class Config:
        orm_mode = True
