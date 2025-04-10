from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.models import User
from schemas.user import UserCreate, UserUpdate
from crud.profile_type import get_profile_type_by_id


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get a user by ID"""
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_login(db: Session, login: str) -> Optional[User]:
    """Get a user by login"""
    return db.query(User).filter(User.login == login).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get a list of users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    # Check if user with login already exists
    existing = get_user_by_login(db, user.login)
    if existing:
        raise HTTPException(status_code=400, detail="Login already registered")
    
    # Check if profile type exists
    profile_type = get_profile_type_by_id(db, user.type_id)
    if not profile_type:
        raise HTTPException(status_code=400, detail="Invalid profile type")
    
    # In a real application, you would hash the password here
    # For example: user.password = hash_password(user.password)
    
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
    """Update a user"""
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the user fields if provided
    update_data = user.dict(exclude_unset=True)
    
    # If type_id is being updated, check if it exists
    if "type_id" in update_data:
        profile_type = get_profile_type_by_id(db, update_data["type_id"])
        if not profile_type:
            raise HTTPException(status_code=400, detail="Invalid profile type")
    
    # In a real application, you would hash the password here if it's being updated
    # if "password" in update_data:
    #     update_data["password"] = hash_password(update_data["password"])
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    """Delete a user"""
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()