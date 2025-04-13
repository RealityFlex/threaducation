# app/services/subject_service.py
from sqlalchemy.orm import Session
from models.subject import Subject
from schemas.subject import SubjectCreate

def get_subject(db: Session, subject_id: int):
    return db.query(Subject).filter(Subject.subject_id == subject_id).first()

def get_subjects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Subject).offset(skip).limit(limit).all()

def create_subject(db: Session, subject: SubjectCreate):
    db_subject = Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def update_subject(db: Session, subject_id: int, subject_data: dict):
    db_subject = get_subject(db, subject_id)
    if db_subject:
        for key, value in subject_data.items():
            setattr(db_subject, key, value)
        db.commit()
        db.refresh(db_subject)
    return db_subject

def delete_subject(db: Session, subject_id: int):
    db_subject = get_subject(db, subject_id)
    if db_subject:
        db.delete(db_subject)
        db.commit()
    return db_subject