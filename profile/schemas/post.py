from typing import List, Optional
from pydantic import BaseModel
from datetime import date

class PostBase(BaseModel):
    content: str
    child_id: Optional[int] = None
    media_link: Optional[str] = None
    post_type_id: int
    user_id: int
    creation_date: Optional[date] = None
    views_count: int


# Response models that match your DTOs
class PostDto(BaseModel):
    content: str
    childId: Optional[int] = None
    mediaLink: Optional[str] = None
    postTypeId: int
    postId: int
    userId: int
    creationDate: Optional[str] = None
    viewsCount: int
    isLiked: bool = False
    likesCount: int = 0
    commentsCount: int = 0
    
    class Config:
        orm_mode = True

    # Complete models for DB operations
class Post(PostBase):
    post_id: int
    
    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass