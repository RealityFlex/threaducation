from pydantic import BaseModel
from typing import Optional

class UserRequestDto(BaseModel):
    login: str
    password: str
    full_name: str

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
    role: str
    full_name: str
    
    class Config:
        orm_mode = True