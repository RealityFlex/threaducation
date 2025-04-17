# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.user import User, UserCreate, UserDetail, UserLogin, ProfileType, ProfileTypeCreate, UserMeDto
from services import user_service
from utils.auth import get_current_user, TokenData

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/me", response_model=UserMeDto)
def read_users_me(x_user: str = Header(..., alias="x-user"), db: Session = Depends(get_db)):
    user_id = int(x_user.split(":")[-1])
    user_with_posts = user_service.get_user_with_posts(db, user_id)
    if user_with_posts is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_with_posts

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserDetail)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/profile-types/", response_model=List[ProfileType])
def read_profile_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    profile_types = user_service.get_profile_types(db, skip=skip, limit=limit)
    return profile_types

@router.post("/profile-types/", response_model=ProfileType)
def create_profile_type(profile_type: ProfileTypeCreate, db: Session = Depends(get_db)):
    return user_service.create_profile_type(db, name=profile_type.name)