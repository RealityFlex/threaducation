# app/schemas/education_program.py
from typing import Optional, List
from pydantic import BaseModel

class EducationTypeBase(BaseModel):
    name: str

class EducationTypeCreate(EducationTypeBase):
    pass

class EducationType(EducationTypeBase):
    education_type_id: int

    class Config:
        orm_mode = True

class EducationProgramBase(BaseModel):
    code: int
    name: int  # This might need to be a string based on your actual data model
    time: int
    education_type_id: int
    description: str
    quota: int

class EducationProgramCreate(EducationProgramBase):
    pass

class EducationProgram(EducationProgramBase):
    program_id: int
    user_id: int

    class Config:
        orm_mode = True

class EducationProgramDetail(EducationProgram):
    education_type: EducationType

    class Config:
        orm_mode = True

class LearningPlanBase(BaseModel):
    program_id: int
    subject_id: int
    hours: int
    semester: int

class LearningPlanCreate(LearningPlanBase):
    pass

class LearningPlan(LearningPlanBase):
    id: int

    class Config:
        orm_mode = True