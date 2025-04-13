# app/schemas/change_request.py
from typing import Optional
from pydantic import BaseModel

class ChangeRequestBase(BaseModel):
    description: str
    program_id: int

class ChangeRequestCreate(ChangeRequestBase):
    pass

class ChangeRequest(ChangeRequestBase):
    change_request_id: int
    from_id: int

    class Config:
        orm_mode = True