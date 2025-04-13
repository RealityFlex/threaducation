from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from typing import Optional

security = HTTPBearer()

class TokenData(BaseModel):
    sub: str
    roles: list
    preferred_username: str

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    This function doesn't actually validate the token as KrakenD is handling
    the JWT validation. We just extract user info from token for convenience.
    In a real-world scenario, you would validate this token.
    """
    try:
        # Just decode the token without verification since KrakenD handles this
        # This is just to extract information from the token
        token = credentials.credentials
        payload = jwt.decode(token, options={"verify_signature": False})
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        
        token_data = TokenData(
            sub=payload.get("sub"),
            roles=payload.get("threaducation_types", {}).get("roles", []),
            preferred_username=payload.get("preferred_username", "")
        )
        return token_data
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

def is_institution(token_data: TokenData = Depends(get_current_user)):
    if "Institution" not in token_data.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation requires institution privileges"
        )
    return token_data

def is_student(token_data: TokenData = Depends(get_current_user)):
    if "Student" not in token_data.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation requires student privileges"
        )
    return token_data