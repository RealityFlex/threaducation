# app/routes/subjects.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from database import get_db
from schemas.subject import Subject, SubjectCreate
from services import subject_service
from utils.auth import get_current_user, is_institution, TokenData

router = APIRouter(
    prefix="/subjects",
    tags=["subjects"]
)

@router.get("/", response_model=List[Subject])
def read_subjects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subjects = subject_service.get_subjects(db, skip=skip, limit=limit)
    return subjects

@router.post("/", response_model=Subject)
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(is_institution)
):
    return subject_service.create_subject(db=db, subject=subject)

@router.get("/{subject_id}", response_model=Subject)
def read_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = subject_service.get_subject(db, subject_id=subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.put("/{subject_id}", response_model=Subject)
def update_subject(
    subject_id: int,
    subject_data: Dict[str, Any],
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(is_institution)
):
    subject = subject_service.get_subject(db, subject_id=subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    updated_subject = subject_service.update_subject(db, subject_id=subject_id, subject_data=subject_data)
    return updated_subject

@router.delete("/{subject_id}")
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(is_institution)
):
    subject = subject_service.get_subject(db, subject_id=subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    subject_service.delete_subject(db, subject_id=subject_id)
    return {"detail": "Subject successfully deleted"}