
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.deps import get_db
import crud
from schemas.profile_type import ProfileTypeCreate, ProfileTypeResponse

router = APIRouter(prefix="/profile-types", tags=["Profile Types"])


@router.get("/", response_model=List[ProfileTypeResponse])
def get_profile_types(db: Session = Depends(get_db)):
    """Get all profile types"""
    return crud.get_profile_types(db)


@router.post("/", response_model=ProfileTypeResponse, status_code=status.HTTP_201_CREATED)
def create_profile_type(profile_type: ProfileTypeCreate, db: Session = Depends(get_db)):
    """Create a new profile type"""
    return crud.create_profile_type(db, profile_type)