# app/schemas/subject.py
from typing import Optional, List
from pydantic import BaseModel

class SubjectBase(BaseModel):
    name: str
    description: int  # This might need to be a string based on your actual data model

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    subject_id: int

    class Config:
        orm_mode = True