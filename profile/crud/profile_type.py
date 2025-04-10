from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.models import ProfileType
from schemas.profile_type import ProfileTypeCreate


def get_profile_types(db: Session) -> List[ProfileType]:
    """Get all profile types"""
    return db.query(ProfileType).all()


def get_profile_type_by_id(db: Session, type_id: int) -> ProfileType:
    """Get a profile type by ID"""
    profile_type = db.query(ProfileType).filter(ProfileType.type_id == type_id).first()
    if not profile_type:
        return None
    return profile_type


def get_profile_type_by_name(db: Session, name: str) -> ProfileType:
    """Get a profile type by name"""
    return db.query(ProfileType).filter(ProfileType.name == name).first()


def create_profile_type(db: Session, profile_type: ProfileTypeCreate) -> ProfileType:
    """Create a new profile type"""
    # Check if profile type already exists
    existing = get_profile_type_by_name(db, profile_type.name)
    if existing:
        raise HTTPException(status_code=400, detail="Profile type already exists")
        
    db_profile_type = ProfileType(**profile_type.dict())
    db.add(db_profile_type)
    db.commit()
    db.refresh(db_profile_type)
    return db_profile_type