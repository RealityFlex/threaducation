from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import requests

from database.database import get_db
from models.models import User
from schemas.schemas import UserRequestDto, TokensDto
from utils.security import password_encode
from config import settings

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
async def register_user(user: UserRequestDto, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.login == user.login).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this login already exists"
        )
    
    # Create new user
    hashed_password = password_encode(user.password)
    postgres_user = User(
        login=user.login,
        password=hashed_password,
        role="customer",
        external_id="-1",
        full_name=user.full_name,
        additional_info=""
    )
    
    db.add(postgres_user)
    db.commit()
    db.refresh(postgres_user)
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User registered successfully"}
    )