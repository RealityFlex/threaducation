from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    login: str
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)


class UserCreate(UserBase):
    password: str
    type_id: int


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    type_id: Optional[int] = None


class UserResponse(UserBase):
    user_id: int
    type_id: int
    
    class Config:
        orm_mode = True