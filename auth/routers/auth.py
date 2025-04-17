from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import requests

from database.database import get_db
from models.models import User, Tag, TagType, TagsForUser
from schemas.schemas import UserRegistrationDto, TokensDto
from utils.security import password_encode
from config import settings
from utils.id_generator import generate_id

router = APIRouter(tags=["authentication"])

@router.get("/refresh", response_model=TokensDto)
async def update(refresh_token: str):
    """Refresh access token using refresh token"""
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "refresh_token": refresh_token,
        "client_id": settings.CLIENT_ID,
        "grant_type": "refresh_token",
        "client_secret": settings.CLIENT_SECRET
    }
    
    response = requests.post(settings.KEYCLOAK_URL, headers=headers, data=data)
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, 
            detail="Token refresh failed"
        )
    
    response_data = response.json()
    return TokensDto(
        access_token=response_data.get("access_token", ""),
        refresh_token=response_data.get("refresh_token", "")
    )

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegistrationDto, db: Session = Depends(get_db)):
    """Register a new user with educational details and tags"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.login == user_data.login).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this login already exists"
        )
    
    # Get profile type ID for student (assuming it exists)
    profile_type_id = 2  # Assuming 1 is for students
    
    # Create new user
    user_id = generate_id()
    hashed_password = password_encode(user_data.password)
    
    # Create description from educational details
    description = f"University: {user_data.university}, Faculty: {user_data.faculty}, " \
                 f"Department: {user_data.department}, Course: {user_data.course}"
    
    new_user = User(
        user_id=user_id,
        login=user_data.login,
        password=hashed_password,
        type_id=profile_type_id,
        name=user_data.fullName,
        image_link="",  # Default empty image link
        description=description,
        rating=0.0  # Default rating
    )
    
    db.add(new_user)
    db.flush()  # Flush to get the user ID
    
    # Process interests and activities (tags of type 2)
    tag_type_id = 2  # Assuming 2 is for interests/activities type
    
    # Process interests
    await add_tags_for_user(db, user_id, user_data.interests, tag_type_id, "interest")
    
    # Process activities
    await add_tags_for_user(db, user_id, user_data.activities, tag_type_id, "activity")
    
    # Commit all changes to the database
    db.commit()
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "User registered successfully",
            "user_id": user_id
        }
    )

async def add_tags_for_user(db: Session, user_id: int, tags: List[str], tag_type_id: int, prefix: str):
    """Helper function to add tags for a user"""
    for tag_name in tags:
        # Check if tag already exists
        tag = db.query(Tag).filter(Tag.name == tag_name, Tag.tag_type_id == tag_type_id).first()
        
        if not tag:
            # Create new tag
            tag_id = generate_id()
            tag = Tag(
                tag_id=tag_id,
                name=tag_name,
                tag_type_id=tag_type_id
            )
            db.add(tag)
            db.flush()
        
        # Link tag to user
        tag_for_user_id = generate_id()
        tag_for_user = TagsForUser(
            id=tag_for_user_id,
            user_id=user_id,
            tag_id=tag.tag_id
        )
        db.add(tag_for_user)