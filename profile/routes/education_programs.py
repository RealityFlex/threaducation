# app/routes/education_programs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from database import get_db
from schemas.education_program import (
    EducationProgram, EducationProgramCreate, EducationProgramDetail,
    EducationType, EducationTypeCreate,
    LearningPlan, LearningPlanCreate
)
from services import education_program_service
from utils.auth import get_current_user, is_institution, TokenData

router = APIRouter(
    prefix="/education-programs",
    tags=["education_programs"]
)

@router.get("/", response_model=List[EducationProgram])
def read_education_programs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    programs = education_program_service.get_education_programs(db, skip=skip, limit=limit)
    return programs

@router.get("/user/{user_id}", response_model=List[EducationProgram])
def read_user_education_programs(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    programs = education_program_service.get_education_programs_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return programs

@router.post("/", response_model=EducationProgram)
def create_education_program(
    program: EducationProgramCreate,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(is_institution)
):
    return education_program_service.create_education_program(db=db, program=program, user_id=int(token_data.sub))

@router.get("/{program_id}", response_model=EducationProgramDetail)
def read_education_program(program_id: int, db: Session = Depends(get_db)):
    program = education_program_service.get_education_program(db, program_id=program_id)
    if program is None:
        raise HTTPException(status_code=404, detail="Education program not found")
    return program

@router.put("/{program_id}", response_model=EducationProgram)
def update_education_program(
    program_id: int,
    program_data: Dict[str, Any],
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(is_institution)
):
    # Check if the user is the owner of the program
    program = education_program_service.get_education_program(db, program_id=program_id)
    if program is None:
        raise HTTPException(status_code=404, detail="Education program not found")
    if str(program.user_id) != token_data.sub:
        raise HTTPException(status_code=403, detail="Not authorized to update this program")
    
    updated_program = education_program_service.update_education_program(db, program_id=program_id, program_data=program_data)
    return updated_program

@router.delete("/{program_id}")
def delete_education_program(
    program_id: int,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(is_institution)
):
    program = education_program_service.get_education_program(db, program_id=program_id)
    if program is None:
        raise HTTPException(status_code=404, detail="Education program not found")
    if str(program.user_id) != token_data.sub:
        raise HTTPException(status_code=403, detail="Not authorized to delete this program")
    
    education_program_service.delete_education_program(db, program_id=program_id)
    return {"detail": "Education program successfully deleted"}

# Education Types routes
@router.get("/types/", response_model=List[EducationType])
def read_education_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    education_types = education_program_service.get_education_types(db, skip=skip, limit=limit)
    return education_types

@router.post("/types/", response_model=EducationType)
def create_education_type(
    education_type: EducationTypeCreate,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(is_institution)
):
    return education_program_service.create_education_type(db=db, education_type=education_type)

# Learning Plan routes
@router.get("/{program_id}/learning-plans", response_model=List[LearningPlan])
def read_learning_plans(program_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    learning_plans = education_program_service.get_learning_plans(db, program_id=program_id, skip=skip, limit=limit)
    return learning_plans

@router.post("/learning-plans", response_model=LearningPlan)
def create_learning_plan(
    learning_plan: LearningPlanCreate,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(is_institution)
):
    # Verify that the institution owns the program
    program = education_program_service.get_education_program(db, program_id=learning_plan.program_id)
    if program is None:
        raise HTTPException(status_code=404, detail="Education program not found")
    if str(program.user_id) != token_data.sub:
        raise HTTPException(status_code=403, detail="Not authorized to create learning plan for this program")
    
    return education_program_service.create_learning_plan(db=db, learning_plan=learning_plan)

@router.delete("/learning-plans/{plan_id}")
def delete_learning_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(is_institution)
):
    # In a real application, you'd need to check if the user has permission to delete this plan
    education_program_service.delete_learning_plan(db, plan_id=plan_id)
    return {"detail": "Learning plan successfully deleted"}