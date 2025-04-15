from pydantic import BaseModel
from typing import Optional, List

class UserRequestDto(BaseModel):
    login: str
    password: str
    full_name: str

class UserRegistrationDto(BaseModel):
    fullName: str
    login: str
    password: str
    university: str
    faculty: str
    department: str
    course: str
    interests: List[str]
    activities: List[str]

class TokensDto(BaseModel):
    access_token: str
    refresh_token: str

class TokensResponseDto(BaseModel):
    accessToken: Optional[str] = None
    refreshToken: Optional[str] = None
    
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    login: str
    name: str
    description: Optional[str]
    rating: float
    
    class Config:
        orm_mode = True