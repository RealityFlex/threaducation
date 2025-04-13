# app/schemas/user.py
from typing import Optional, List
from pydantic import BaseModel

class ProfileTypeBase(BaseModel):
    name: str

class ProfileTypeCreate(ProfileTypeBase):
    pass

class ProfileType(ProfileTypeBase):
    type_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    login: str
    name: str
    type_id: int
    image_link: Optional[str] = None
    description: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    login: str
    password: str

class User(UserBase):
    user_id: int
    rating: float

    class Config:
        orm_mode = True

class UserDetail(User):
    profile_type: ProfileType

    class Config:
        orm_mode = True