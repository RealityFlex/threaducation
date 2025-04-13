# app/schemas/tag.py
from typing import Optional, List
from pydantic import BaseModel

class TagBase(BaseModel):
    name: str
    tag_type_id: int

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    tag_id: int

    class Config:
        orm_mode = True

class TagForUserBase(BaseModel):
    user_id: int
    tag_id: int

class TagForUserCreate(TagForUserBase):
    pass

class TagForUser(TagForUserBase):
    id: int

    class Config:
        orm_mode = True

class TagForUserDetail(TagForUser):
    tag: Tag

    class Config:
        orm_mode = True