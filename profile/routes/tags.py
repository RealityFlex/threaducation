# app/routes/tags.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.tag import Tag, TagCreate, TagForUser, TagForUserCreate, TagForUserDetail
from services import tag_service
from utils.auth import get_current_user, is_institution, TokenData

router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)

@router.get("/", response_model=List[Tag])
def read_tags(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = tag_service.get_tags(db, skip=skip, limit=limit)
    return tags

@router.get("/type/{tag_type_id}", response_model=List[Tag])
def read_tags_by_type(tag_type_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = tag_service.get_tags_by_type(db, tag_type_id=tag_type_id, skip=skip, limit=limit)
    return tags

@router.post("/", response_model=Tag)
def create_tag(tag: TagCreate, db: Session = Depends(get_db), token_data: TokenData = Depends(is_institution)):
    # Only institutions can create tags
    return tag_service.create_tag(db=db, tag=tag)

@router.get("/user/{user_id}", response_model=List[TagForUserDetail])
def read_user_tags(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = tag_service.get_tags_for_user(db, user_id=user_id, skip=skip, limit=limit)
    return tags

@router.post("/user/", response_model=TagForUser)
def assign_tag_to_user(tag_for_user: TagForUserCreate, db: Session = Depends(get_db), token_data: TokenData = Depends(is_institution)):
    # Check if the user requesting this is the institution that owns the tag or has permission
    return tag_service.assign_tag_to_user(db=db, tag_for_user=tag_for_user)

@router.delete("/user/{tag_id}/{user_id}")
def remove_tag_from_user(tag_id: int, user_id: int, db: Session = Depends(get_db), token_data: TokenData = Depends(is_institution)):
    tag_for_user = tag_service.remove_tag_from_user(db, tag_id=tag_id, user_id=user_id)
    if tag_for_user is None:
        raise HTTPException(status_code=404, detail="Tag not found for user")
    return {"detail": "Tag successfully removed from user"}